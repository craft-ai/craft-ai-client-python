import unittest
import copy

from craft_ai import Client, errors as craft_err

from . import settings
from .data import valid_data, invalid_data
from .utils import generate_entity_id

NB_OPERATIONS_TO_ADD = 1000
NB_AGENTS_TO_ADD_OPERATIONS = 5

AGENT_BASE = "test_add_agents_op_bulk"


class TestAddOperationsBulkSuccess(unittest.TestCase):
    """Checks that the client succeeds when adding operations to
    multiple agent(s) with OK input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)

    def setUp(self):
        self.agent_id1 = generate_entity_id(AGENT_BASE + "BulkSucc")
        self.agent_id2 = generate_entity_id(AGENT_BASE + "BulkSucc")
        self.client.delete_agent(self.agent_id1)
        self.client.delete_agent(self.agent_id2)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id1)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id2)

    def tearDown(self):
        # This ensures that agents are properly deleted every time
        self.client.delete_agent(self.agent_id1)
        self.client.delete_agent(self.agent_id2)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_add_agents_operations_bulk_with_correct_input(self):
        """add_agents_operations_bulk should succeed when given correct input data.

    It should give a proper JSON response with a list containing dicts with
    'id' fields being the same as the one in parameters, 'message' fields
    being a string, 'status' fields being 201 and no 'error' field.
    """
        payload = [
            {"id": self.agent_id1, "operations": valid_data.VALID_OPERATIONS_SET},
            {"id": self.agent_id2, "operations": valid_data.VALID_OPERATIONS_SET},
        ]
        resp = self.client.add_agents_operations_bulk(payload)

        self.assertIsInstance(resp, list)
        self.assertEqual(resp[0].get("id"), self.agent_id1)
        self.assertEqual(resp[1].get("id"), self.agent_id2)
        self.assertEqual(resp[0].get("status"), 201)
        self.assertEqual(resp[1].get("status"), 201)
        self.assertTrue("message" in resp[0].keys())
        self.assertTrue("message" in resp[1].keys())

        self.addCleanup(self.clean_up_agents, [self.agent_id1, self.agent_id2])

    def test_add_agents_operations_bulk_with_many_operations(self):
        """add_agents_operations_bulk should succeed when given a lot of operations to
    add.

    It should give a proper JSON response with a list containing dicts with
    'id' fields being the same as the one in parameters, 'message' fields
    being a string, 'status' fields being 201 and no 'error' field.
    """
        # Creating a large operation set
        operations = copy.deepcopy(valid_data.VALID_OPERATIONS_SET[:])
        operation = operations[-1]
        timestamp = operation["timestamp"]
        num_operation = 0
        while num_operation < NB_OPERATIONS_TO_ADD:
            operation["timestamp"] = timestamp + num_operation
            operations.append(operation.copy())
            num_operation += 1
        operations = sorted(operations, key=lambda operation: operation["timestamp"])

        # Add the operations to multiple agents
        payload = [
            {"id": self.agent_id1, "operations": operations},
            {"id": self.agent_id2, "operations": operations},
        ]
        resp = self.client.add_agents_operations_bulk(payload)

        self.assertIsInstance(resp, list)
        self.assertEqual(resp[0].get("id"), self.agent_id1)
        self.assertEqual(resp[1].get("id"), self.agent_id2)
        self.assertEqual(resp[0].get("status"), 201)
        self.assertEqual(resp[1].get("status"), 201)
        self.assertTrue("message" in resp[0].keys())
        self.assertTrue("message" in resp[1].keys())

        self.addCleanup(self.clean_up_agents, [self.agent_id1, self.agent_id2])


class TestAddOperationsGroupAgentsBulkSuccess(unittest.TestCase):
    """Checks that the client succeeds when adding operations to a lot
    of agents with OK input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agents = [
            generate_entity_id("test_add_agents_operations_bulk")
            for i in range(NB_AGENTS_TO_ADD_OPERATIONS)
        ]

    def setUp(self):
        # Makes sure that no agent with the same ID already exists
        for agent_id in self.agents:
            self.client.delete_agent(agent_id)
            self.client.create_agent(valid_data.VALID_CONFIGURATION, agent_id)

    def tearDown(self):
        # This ensures that agents are properly deleted every time
        for agent_id in self.agents:
            self.client.delete_agent(agent_id)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_add_agents_operations_bulk_group_agents(self):
        """add_agents_operations_bulk should succeed when given a lot of agents to add
        operations to.

        It should give a proper JSON response with a list containing dicts with
        'id' fields being the same as the one in parameters, 'message' fields
        being a string, 'status' fields being 201 and no 'error' field.
        """
        payload = []
        for agent_id in self.agents:
            payload.append(
                {"id": agent_id, "operations": valid_data.VALID_OPERATIONS_SET}
            )

        response = self.client.add_agents_operations_bulk(payload)

        for i, resp in enumerate(response):
            self.assertEqual(resp.get("id"), self.agents[i])
            self.assertEqual(resp.get("status"), 201)
            self.assertTrue("message" in resp.keys())
            self.assertEqual(
                resp["added_operations_count"], len(valid_data.VALID_OPERATIONS_SET)
            )

        self.addCleanup(self.clean_up_agents, self.agents)


class TestAddOperationsBulkFailure(unittest.TestCase):
    """Checks that the client fail when adding operations to
    multiple agent(s) with incorrect input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_add_agents_operations_bulk_invalid_agent_id(self):
        """add_agents_operations_bulk should fail when given non-string/empty ID.

        It should raise an error upon request for operations posting
        for all agents with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        payload = []
        for empty_id in invalid_data.UNDEFINED_KEY:
            payload.append(
                {
                    "id": invalid_data.UNDEFINED_KEY[empty_id],
                    "operations": valid_data.VALID_OPERATIONS_SET,
                }
            )

        self.assertRaises(
            craft_err.CraftAiBadRequestError,
            self.client.add_agents_operations_bulk,
            payload,
        )

    def test_add_agents_operations_bulk_undefined_operations(self):
        """add_agents_operations_bulk should fail when given some undefined operations set.

        It should raise an error upon request for operations posting for all agents
        with invalid operations set.
        """
        payload = []
        agents_lst = []
        for i, invalid_operation_set in enumerate(invalid_data.UNDEFINED_KEY):
            new_agent_id = generate_entity_id(
                "test_add_agents_operations_bulk_undefined_operations"
            )
            self.client.delete_agent(new_agent_id)
            self.client.create_agent(valid_data.VALID_CONFIGURATION, new_agent_id)
            agents_lst.append(new_agent_id)
            payload.append({"id": new_agent_id, "operations": invalid_operation_set})

        self.assertRaises(
            craft_err.CraftAiBadRequestError,
            self.client.add_agents_operations_bulk,
            payload,
        )

        self.addCleanup(self.clean_up_agents, agents_lst)

    def test_add_agents_operations_bulk_invalid_operations(self):
        """add_agents_operations_bulk should fail when given some invalid operations set.

        It should raise an error upon request for operations posting
        for all agents with invalid operations set.
        """
        payload = []
        agents_lst = []
        for i, invalid_operation_set in enumerate(invalid_data.INVALID_OPS_SET):
            new_agent_id = generate_entity_id(
                "test_add_agents_operations_bulk_invalid_operations"
            )
            self.client.delete_agent(new_agent_id)
            self.client.create_agent(valid_data.VALID_CONFIGURATION, new_agent_id)
            agents_lst.append(new_agent_id)
            payload.append({"id": new_agent_id, "operations": invalid_operation_set})

        self.assertRaises(
            craft_err.CraftAiBadRequestError,
            self.client.add_agents_operations_bulk,
            payload,
        )

        self.addCleanup(self.clean_up_agents, agents_lst)


class TestAddOperationsBulkSomeFailure(unittest.TestCase):
    """Checks that the client succeed when adding operations to
  an/multiple agent(s) with bad input and an/multiple agent(s)
  with valid input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_add_agents_operations_bulk")

    def setUp(self):
        self.client.delete_agent(self.agent_id)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def test_add_agents_operations_bulk_some_invalid_agent_id(self):
        """add_agents_operations_bulk should succeed when given some non-string/empty ID
        and some valid ID.

        It should give a proper JSON response with a list containing dicts.
        The ones having valid ids have the `id` field being the same as the one given
        as a parameter and message field being a string.
        The ones having valid ids doesn't have a dict associated.
        """
        payload = [{"id": self.agent_id, "operations": valid_data.VALID_OPERATIONS_SET}]
        for empty_id in invalid_data.UNDEFINED_KEY:
            payload.append(
                {
                    "id": invalid_data.UNDEFINED_KEY[empty_id],
                    "operations": valid_data.VALID_OPERATIONS_SET,
                }
            )

        resp = self.client.add_agents_operations_bulk(payload)

        self.assertIsInstance(resp, list)
        self.assertEqual(resp[0].get("id"), self.agent_id)
        self.assertTrue("message" in resp[0].keys())
        self.assertFalse("error" in resp[0].keys())
        self.assertTrue(len(resp) == len(payload))

        self.addCleanup(self.clean_up_agent, self.agent_id)
