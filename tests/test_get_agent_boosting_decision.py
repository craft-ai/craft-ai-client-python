import unittest

from craft_ai import Client, errors as craft_err

from . import settings
from .utils import generate_entity_id
from .data import valid_data, invalid_data


class TestGetAgentBoostingDecisionSuccess(unittest.TestCase):
    """Checks that the client fails properly when getting a boosting decision with
    invalid parameters for a generator"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_get_agent_boosting_decision")

    def setUp(self):
        self.client.delete_agent(self.agent_id)
        self.client.create_agent(valid_data.VALID_BOOSTING_CONFIGURATION, self.agent_id)
        self.client.add_agent_operations(
            self.agent_id, valid_data.VALID_OPERATIONS_SET_COMPLETE_1
        )

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def test_get_decision_boosting_with_correct_input(self):
        first_timestamp = valid_data.VALID_OPERATIONS_SET_COMPLETE_1[0]["timestamp"]
        last_timestamp = valid_data.VALID_OPERATIONS_SET_COMPLETE_1[-1]["timestamp"]
        context = {"tz": "+02:00", "presence": "occupant", "lightIntensity": 1}
        decision = self.client.get_agent_boosting_decision(
            self.agent_id, first_timestamp, last_timestamp, context,
        )
        self.assertEqual(decision["output"]["predicted_value"], "pink")
        self.addCleanup(self.clean_up_agent, self.agent_id)


class TestGetAgentBoostingDecisionFailure(unittest.TestCase):
    """Checks that the client fails properly when getting a boosting decision with
    invalid parameters for a generator"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_get_agent_boosting_decision")

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def test_get_decision_boosting_with_invalid_agent_id(self):
        """get_agent_boosting_decision should fail when given a non-string/empty string ID

        It should raise an error upon request for retrieval of
        an agent with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        for empty_id in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.get_agent_boosting_decision,
                invalid_data.UNDEFINED_KEY[empty_id],
                valid_data.VALID_TIMESTAMP,
                valid_data.VALID_LAST_TIMESTAMP,
                valid_data.VALID_OPERATIONS_SET[0],
            )

    def test_get_decision_boosting_with_invalid_from_timestamp(self):
        """get_agent_boosting_decision should fail when given an invalid timestamp

        It should raise an error upon request when invalid timestamps are given
        """
        for invalid_ts in invalid_data.INVALID_TIMESTAMPS:
            self.client.delete_agent(self.agent_id)
            self.client.create_agent(
                valid_data.VALID_BOOSTING_CONFIGURATION, self.agent_id
            )
            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.get_agent_boosting_decision,
                self.agent_id,
                invalid_data.INVALID_TIMESTAMPS[invalid_ts],
                valid_data.VALID_LAST_TIMESTAMP,
                valid_data.VALID_OPERATIONS_SET[0],
            )
            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.get_agent_boosting_decision,
                self.agent_id,
                valid_data.VALID_LAST_TIMESTAMP,
                invalid_data.INVALID_TIMESTAMPS[invalid_ts],
                valid_data.VALID_OPERATIONS_SET[0],
            )
        self.addCleanup(self.clean_up_agent, self.agent_id)

    def test_get_boosting_decision_with_invalid_operations(self):
        """get_agent_boosting_decision should fail when invalid operations are given.

        It should raise an error upon request for decision making
        with invalid operations set.
        """
        for i, invalid_operation_set in enumerate(invalid_data.INVALID_OPS_SET):
            self.client.delete_agent(self.agent_id)
            self.client.create_agent(
                valid_data.VALID_BOOSTING_CONFIGURATION, self.agent_id
            )

            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.get_agent_boosting_decision,
                self.agent_id,
                valid_data.VALID_TIMESTAMP,
                valid_data.VALID_LAST_TIMESTAMP,
                invalid_operation_set,
            )

        self.addCleanup(self.clean_up_agent, self.agent_id)
