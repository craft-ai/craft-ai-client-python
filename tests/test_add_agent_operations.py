import unittest

import copy
import craft_ai
import pandas as pd

from . import settings
from .utils import generate_entity_id
from .data import valid_data, invalid_data


class TestAddOperationsSuccess(unittest.TestCase):
    """Checks that the client succeeds when getting an agent with OK input"""

    @classmethod
    def setUpClass(cls):
        cls.client = craft_ai.Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_add_agent_operations")

    def setUp(self):
        self.client.delete_agent(self.agent_id)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)

    def tearDown(self):
        self.client.delete_agent(self.agent_id)

    def test_add_agent_operations_with_correct_input(self):
        """add_agent_operations should succeed when given correct input data

        It should give a proper JSON response with a `message` fields being a
        string.
        """
        resp = self.client.add_agent_operations(
            self.agent_id, valid_data.VALID_OPERATIONS_SET
        )

        self.assertIsInstance(resp, dict)
        resp_keys = resp.keys()
        self.assertTrue("message" in resp_keys)
        self.assertEqual(
            resp["added_operations_count"], len(valid_data.VALID_OPERATIONS_SET)
        )

    def test_add_agent_operations_with_many_operations(self):
        """add_agent_operations should succeed when given lots of operations

        It should give a proper JSON response with a `message` fields being a
        string.
        """
        operations = copy.deepcopy(valid_data.VALID_OPERATIONS_SET[:])

        while len(operations) < 2000:
            new_operation = operations[-1].copy()
            new_operation["timestamp"] += 10
            operations.append(new_operation)

        resp = self.client.add_agent_operations(
            self.agent_id,
            sorted(operations, key=lambda operation: operation["timestamp"]),
        )

        self.assertIsInstance(resp, dict)
        resp_keys = resp.keys()
        self.assertTrue("message" in resp_keys)
        self.assertEqual(resp["added_operations_count"], len(operations))

    def test_add_agent_operations_with_some_duplicates(self):
        """add_agent_operations should succeed and lmerge duplicate timestamps
        """
        operations = copy.deepcopy(valid_data.VALID_OPERATIONS_SET[:])

        while len(operations) < 500:
            new_operation = operations[-1].copy()
            new_operation["timestamp"] += 10
            operations.append(new_operation)

        # Creating two duplicates
        operations[100]["timestamp"] = operations[101]["timestamp"]
        operations[300]["timestamp"] = operations[301]["timestamp"]

        resp = self.client.add_agent_operations(
            self.agent_id,
            sorted(operations, key=lambda operation: operation["timestamp"]),
        )

        self.assertIsInstance(resp, dict)
        resp_keys = resp.keys()
        self.assertTrue("message" in resp_keys)
        self.assertEqual(resp["added_operations_count"], len(operations) - 2)


class TestAddOperationsFailure(unittest.TestCase):
    """Checks that the client fails properly when getting an agent with bad
    input"""

    @classmethod
    def setUpClass(cls):
        cls.client = craft_ai.Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_add_agent_operations")

    def setUp(self):
        self.client.delete_agent(self.agent_id)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)

    def tearDown(self):
        self.client.delete_agent(self.agent_id)

    def test_add_agent_operations_with_invalid_agent_id(self):
        """add_agent_operations should fail when given a non-string/empty string ID

        It should raise an error upon request for operations posting
        for an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for empty_id in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_ai.errors.CraftAiBadRequestError,
                self.client.add_agent_operations,
                invalid_data.UNDEFINED_KEY[empty_id],
                valid_data.VALID_OPERATIONS_SET,
            )

    def test_add_agent_operations_with_empty_operations_set(self):
        """add_agent_operations should fail when given an empty set of operations

        It should raise an error upon request for posting an empty set of
        operations to an agent's configuration.
        """
        for ops_set in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_ai.errors.CraftAiBadRequestError,
                self.client.add_agent_operations,
                self.agent_id,
                invalid_data.UNDEFINED_KEY[ops_set],
            )

    def test_add_agent_operations_with_invalid_operation_set(self):
        """add_agent_operations should fail when given an invalid set of operations

        It should raise an error upon request for posting an invalid set of
        operations to an agent's configuration.
        """
        for ops_set in invalid_data.INVALID_OPS_SET:
            self.assertRaises(
                craft_ai.errors.CraftAiBadRequestError,
                self.client.add_agent_operations,
                self.agent_id,
                invalid_data.INVALID_OPS_SET[ops_set],
            )

    def test_add_agent_operations_with_a_dataframe_should_fail(self):
        """add_agent_operations should fail when given an invalid set of operations

        It should raise an error upon request for posting an invalid set of
        operations to an agent's configuration.
        """
        dataframeOperations = pd.DataFrame()
        self.assertRaises(
            craft_ai.errors.CraftAiBadRequestError,
            self.client.add_agent_operations,
            self.agent_id,
            dataframeOperations,
        )
