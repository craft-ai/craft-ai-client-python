import json
import os

import unittest
import pandas as pd

from craft_ai import Client, Interpreter, Time, errors as craft_err

from . import settings

HERE = os.path.abspath(os.path.dirname(__file__))

# Assuming we are the test folder and the folder hierarchy is correctly
# constructed
EXPECS_DIR = os.path.join(HERE, "data", "interpreter", "decide", "expectations")
TREES_DIR = os.path.join(HERE, "data", "interpreter", "decide", "trees")

CLIENT = Client(settings.CRAFT_CFG)


class TestInterpreter(unittest.TestCase):
    def check_expectation(self, tree, expectation):
        exp_context = expectation["context"]
        timestamp = None
        exp_time = expectation.get("time")
        time = Time(exp_time["t"], exp_time["tz"]) if exp_time else {}
        configuration = expectation.get("configuration")
        if configuration:
            tree["configuration"].update(configuration)

        if expectation.get("error"):
            with self.assertRaises(craft_err.CraftAiDecisionError) as context_manager:
                CLIENT.decide(tree, exp_context, timestamp)

            exception = context_manager.exception
            expected_message = ""
            if isinstance(expectation["error"]["message"], str):
                expected_message = expectation["error"]["message"]
            else:
                expected_message = expectation["error"]["message"].encode("utf8")
            self.assertEqual(exception.message, expected_message)
            self.assertEqual(
                exception.metadata, expectation["error"].get("metadata", None)
            )
        else:
            expected_decision = expectation["output"]
            decision = CLIENT.decide(tree, exp_context, time)
            self.assertEqual(decision, expected_decision)

    def test_interpreter(self):
        versions = os.listdir(TREES_DIR)
        for version in versions:
            tree_files = os.listdir(os.path.join(TREES_DIR, version))
            for tree_file in tree_files:
                if os.path.splitext(tree_file)[1] == ".json":
                    # Loading the json tree
                    with open(os.path.join(TREES_DIR, version, tree_file)) as f:
                        tree = json.load(f)
                    # Loading the expectations for this tree
                    with open(os.path.join(EXPECS_DIR, version, tree_file)) as f:
                        expectations = json.load(f)

                    for expectation in expectations:
                        with self.subTest():
                            self.check_expectation(tree, expectation)

    def test_rebuild_context(self):
        configuration = {
            "context": {
                "car": {"type": "enum"},
                "speed": {"type": "continuous"},
                "day_of_week": {"type": "day_of_week", "is_generated": False},
                "month_of_year": {"type": "month_of_year"},
                "timezone": {"type": "timezone"},
            },
            "output": ["speed"],
            "time_quantum": 500,
        }

        # pylint: disable=W0212

        # Case 2:
        # - provide none of the properties that should be generated
        state = {"car": "Renault", "day_of_week": 2, "timezone": "+01:00"}
        time = Time(1489998174, "+01:00")
        rebuilt_context = Interpreter._rebuild_context(configuration, state, time)[
            "context"
        ]
        expected_context = {
            "car": "Renault",
            "day_of_week": 2,
            "month_of_year": 3,
            "timezone": "+01:00",
        }

        # pylint: enable=W0212

        for output in expected_context:
            self.assertEqual(rebuilt_context[output], expected_context[output])

    def test_make_a_decision_on_dataframe_should_fail(self):
        """add_agent_operations should fail when given an invalid set of operations

        It should raise an error upon request for posting an invalid set of
        operations to an agent's configuration.
        """
        dataframeOperations = pd.DataFrame()
        version = "v1"
        tree_file = "oneColor.json"
        with open(os.path.join(TREES_DIR, version, tree_file)) as f:
            tree = json.load(f)
        self.assertRaises(
            craft_err.CraftAiBadRequestError, CLIENT.decide, tree, dataframeOperations
        )
