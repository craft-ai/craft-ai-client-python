import unittest

from craft_ai import Client, errors as craft_err

from . import settings
from .utils import generate_entity_id
from .data import valid_data, invalid_data


class TestGetAgentBulkBoostingDecisionSuccess(unittest.TestCase):
    """Checks that the client works properly when getting a boosting decision with
    two valid agents"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id_1 = generate_entity_id("test_get_agent_bulk_boosting_decision")
        cls.agent_id_2 = generate_entity_id("test_get_agent_bulk_boosting_decision")

    def setUp(self):
        self.client.delete_agent(self.agent_id_1)
        self.client.create_agent(valid_data.VALID_BOOSTING_CONFIGURATION, self.agent_id_1)
        self.client.add_agent_operations(
            self.agent_id_1, valid_data.VALID_OPERATIONS_SET_COMPLETE_1
        )
        self.client.delete_agent(self.agent_id_2)
        self.client.create_agent(valid_data.VALID_BOOSTING_CONFIGURATION, self.agent_id_2)
        self.client.add_agent_operations(
            self.agent_id_2, valid_data.VALID_OPERATIONS_SET_COMPLETE_1
        )

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def test_get_bulk_decision_boosting_with_correct_input(self):
        first_timestamp = valid_data.VALID_OPERATIONS_SET_COMPLETE_1[0]["timestamp"]
        last_timestamp = valid_data.VALID_OPERATIONS_SET_COMPLETE_1[-1]["timestamp"]
        timeWindow = [first_timestamp, last_timestamp]
        context = {"tz": "+02:00", "presence": "occupant", "lightIntensity": 1}
        payload = [{
            "entityName": self.agent_id_1,
            "timeWindow": timeWindow,
            "context": context
        },{
            "entityName": self.agent_id_2,
            "timeWindow": timeWindow,
            "context": context
        }]
        decisions = self.client.get_agent_bulk_boosting_decision(payload)
        self.assertEqual(decisions[0]["_version"], "1.0.0")
        self.assertEqual(decisions[0]["entityName"], self.agent_id_1)
        self.assertEqual(decisions[0]["context"], context)
        self.assertEqual(decisions[0]["timeWindow"], timeWindow)
        self.assertEqual(decisions[0]["output"]["predicted_value"], "pink")
        self.assertEqual(decisions[1]["_version"], "1.0.0")
        self.assertEqual(decisions[1]["entityName"], self.agent_id_2)
        self.assertEqual(decisions[1]["context"], context)
        self.assertEqual(decisions[1]["timeWindow"], timeWindow)
        self.assertEqual(decisions[1]["output"]["predicted_value"], "pink")
        self.addCleanup(self.clean_up_agent, self.agent_id_1)
        self.addCleanup(self.clean_up_agent, self.agent_id_2)


class TestGetAgentBoostingDecisionFailure(unittest.TestCase):
    """Checks that the client fails properly when getting bulk boosting decisions
    with invalid parameters for agents"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id_1 = generate_entity_id("test_get_agent_bulk_boosting_decision")
        cls.agent_id_2 = generate_entity_id("test_get_agent_bulk_boosting_decision")

    def setUp(self):
        self.client.delete_agent(self.agent_id_1)
        self.client.create_agent(valid_data.VALID_BOOSTING_CONFIGURATION, self.agent_id_1)
        self.client.add_agent_operations(
            self.agent_id_1, valid_data.VALID_OPERATIONS_SET_COMPLETE_1
        )
        self.client.delete_agent(self.agent_id_2)
        self.client.create_agent(valid_data.VALID_BOOSTING_CONFIGURATION, self.agent_id_2)
        self.client.add_agent_operations(
            self.agent_id_2, valid_data.VALID_OPERATIONS_SET_COMPLETE_1
        )

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def test_get_bulk_decision_boosting_with_non_existant_agent_id(self):
        """get_agent_bulk_boosting_decision should handle valid and non existant
        agents"""
        first_timestamp = valid_data.VALID_OPERATIONS_SET_COMPLETE_1[0]["timestamp"]
        last_timestamp = valid_data.VALID_OPERATIONS_SET_COMPLETE_1[-1]["timestamp"]
        timeWindow = [first_timestamp, last_timestamp]
        context = {"tz": "+02:00", "presence": "occupant", "lightIntensity": 1}
        payload = [{
            "entityName": self.agent_id_1,
            "timeWindow": timeWindow,
            "context": context
        },{
            "entityName": self.agent_id_2,
            "timeWindow": timeWindow,
            "context": context
        },{
            "entityName": "test_test",
            "timeWindow": timeWindow,
            "context": context
        }]
        decisions = self.client.get_agent_bulk_boosting_decision(payload)
        self.assertEqual(decisions[0]["_version"], "1.0.0")
        self.assertEqual(decisions[0]["entityName"], self.agent_id_1)
        self.assertEqual(decisions[0]["context"], context)
        self.assertEqual(decisions[0]["timeWindow"], timeWindow)
        self.assertEqual(decisions[0]["output"]["predicted_value"], "pink")
        self.assertEqual(decisions[1]["_version"], "1.0.0")
        self.assertEqual(decisions[1]["entityName"], self.agent_id_2)
        self.assertEqual(decisions[1]["context"], context)
        self.assertEqual(decisions[1]["timeWindow"], timeWindow)
        self.assertEqual(decisions[1]["output"]["predicted_value"], "pink")
        self.assertIsInstance(decisions[2]["error"], craft_err.CraftAiNotFoundError)
        self.addCleanup(self.clean_up_agent, self.agent_id_1)
        self.addCleanup(self.clean_up_agent, self.agent_id_2)

    def test_get_bulk_decision_boosting_with_empty_array(self):
        """get_agent_bulk_boosting_decision fail properly when emty array given"""
        self.assertRaises(
            craft_err.CraftAiBadRequestError,
            self.client.get_agent_bulk_boosting_decision,
            []
        )
