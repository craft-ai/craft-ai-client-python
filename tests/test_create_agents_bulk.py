import unittest

from craft_ai import Client, errors as craft_err

from . import settings
from .utils import generate_entity_id
from .data import valid_data, invalid_data

NB_AGENTS_TO_CREATE = 5


class TestCreateAgentsBulkSuccess(unittest.TestCase):
    """Checks that the client succeeds when creating
    an/multiple agent(s) with OK input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id1 = generate_entity_id("test_create_agents_bulk")
        cls.agent_id2 = generate_entity_id("test_create_agents_bulk")
        cls.agent_name = generate_entity_id("test_create_agents_bulk")

    @classmethod
    def tearDownClass(cls):
        for agent_id in cls.client.list_agents():
            try:
                cls.client.delete_agent(agent_id)
            except craft_err.CraftAiError:
                continue

    def setUp(self):
        # Makes sure that no agent with the same ID already exists
        resp1 = self.client.delete_agent(self.agent_id1)
        resp2 = self.client.delete_agent(self.agent_id2)

        self.assertIsInstance(resp1, dict)
        self.assertIsInstance(resp2, dict)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        try:
            self.client.delete_agent(aid)
        except craft_err.CraftAiError:
            return

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_create_one_agent_generated_agent_id(self):
        """create_agents_bulk should succeed when given an empty `id` field.

        It should give a proper JSON response with a list containing a dict with `id` and
        `configuration` fields being strings.
        """
        payload = [{"configuration": valid_data.VALID_CONFIGURATION}]
        resp = self.client.create_agents_bulk(payload)

        self.assertIsInstance(resp[0].get("id"), str)

        self.addCleanup(self.clean_up_agent, resp[0].get("id"))

    def test_create_multiple_agents_generated_agent_id(self):
        """create_agents_bulk should succeed when given agents to create with empty `id` field.

        It should give a proper JSON response with a list containing dicts  with `id` and
        `configuration` fields being strings.
        """
        payload = [
            {"configuration": valid_data.VALID_CONFIGURATION},
            {"configuration": valid_data.VALID_CONFIGURATION},
        ]
        resp = self.client.create_agents_bulk(payload)

        self.assertIsInstance(resp[0].get("id"), str)
        self.assertIsInstance(resp[1].get("id"), str)
        self.addCleanup(self.clean_up_agents, [resp[0].get("id"), resp[1].get("id")])

    def test_create_one_agent_given_agent_id(self):
        """create_agents_bulk should succeed when given a valid string in the `id` field.

        It should give a proper JSON response with a list containing a dict with `id` and
        `configuration` fields being strings and `id` being the same as the one given as
        a parameter.
        """
        payload = [
            {"id": self.agent_id1, "configuration": valid_data.VALID_CONFIGURATION}
        ]
        resp = self.client.create_agents_bulk(payload)

        self.assertEqual(resp[0].get("id"), self.agent_id1)
        self.addCleanup(self.clean_up_agent, self.agent_id1)

    def test_create_multiple_agents_given_agent_id(self):
        """create_agents_bulk should succeed when given valid strings in the `id` field.

        It should give a proper JSON response with a list containing dicts with `id` and
        `configuration` fields being strings and the `id`s being the same as the ones given
        as parameters.
        """
        payload = [
            {"id": self.agent_id1, "configuration": valid_data.VALID_CONFIGURATION},
            {"id": self.agent_id2, "configuration": valid_data.VALID_CONFIGURATION},
        ]
        resp = self.client.create_agents_bulk(payload)

        self.assertEqual(resp[0].get("id"), self.agent_id1)
        self.assertEqual(resp[1].get("id"), self.agent_id2)
        self.addCleanup(self.clean_up_agents, [resp[0].get("id"), resp[1].get("id")])

    def test_create_agents_bulk_id_given_and_generated(self):
        """create_agents_bulk should succeed when given some agents with string `id` and some
        with empty `id` field.

        It should give a proper JSON response with a list containing dicts with `id` and
        `configuration` fields being strings and if the `id` was given as a parameter, `id`
        should be the same as the one given as a parameter.
        """
        payload = [
            {"id": self.agent_id1, "configuration": valid_data.VALID_CONFIGURATION},
            {"configuration": valid_data.VALID_CONFIGURATION},
        ]
        resp = self.client.create_agents_bulk(payload)

        self.assertEqual(resp[0].get("id"), self.agent_id1)
        self.assertIsInstance(resp[1].get("id"), str)
        self.addCleanup(self.clean_up_agents, [resp[0].get("id"), resp[1].get("id")])

    def test_create_lot_of_agents_bulk(self):
        """create_agents_bulk should succeed when given a lot of agents to create.

        It should give a proper JSON response with a list containing dicts
        with `id` and `configuration` fields being strings and the first `id` being the
        same as the one given as a parameter.
        """
        payload = []
        agents_lst = []
        for i in range(NB_AGENTS_TO_CREATE):
            new_agent_id = generate_entity_id("test_create_lot_of_agents_bulk")
            self.client.delete_agent(new_agent_id)
            payload.append(
                {"id": new_agent_id, "configuration": valid_data.VALID_CONFIGURATION}
            )
            agents_lst.append(new_agent_id)

        response = self.client.create_agents_bulk(payload)

        for i, resp in enumerate(response):
            self.assertEqual(resp.get("id"), agents_lst[i])
            self.assertFalse("error" in resp)

        self.addCleanup(self.clean_up_agents, agents_lst)


class TestCreateAgentsBulkFailure(unittest.TestCase):
    """Checks that the client fails when creating
    an/multiple agent(s) with bad input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)

    def setUp(self):
        self.agent_id1 = generate_entity_id("test_create_agents_bulk_failure")
        self.agent_id2 = generate_entity_id("test_create_agents_bulk_failure")
        self.agent_name = generate_entity_id("test_create_agents_bulk_failure")
        # Makes sure that no agent with the same ID already exists
        resp1 = self.client.delete_agent(self.agent_id1)
        resp2 = self.client.delete_agent(self.agent_id2)

        self.assertIsInstance(resp1, dict)
        self.assertIsInstance(resp2, dict)

    def tearDown(self):
        # This ensures that agents are properly deleted every time
        self.client.delete_agent(self.agent_id1)
        self.client.delete_agent(self.agent_id2)
        self.client.delete_agent(self.agent_name)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_create_agents_bulk_with_existing_agent_id(self):
        """create_agents_bulk should fail when given only IDs that already exist.

        It should raise an error upon request for creation of a bulk of agents with IDs
        that already exist, since agent IDs should always be unique.
        """
        # Calling create_agents_bulk a first time
        payload = [
            {"id": self.agent_id1, "configuration": valid_data.VALID_CONFIGURATION},
            {"id": self.agent_id2, "configuration": valid_data.VALID_CONFIGURATION},
        ]
        self.client.create_agents_bulk(payload)

        self.assertRaises(
            craft_err.CraftAiBadRequestError, self.client.create_agents_bulk, payload
        )
        self.addCleanup(self.clean_up_agents, [self.agent_id1, self.agent_id2])

    def test_create_agents_bulk_with_invalid_agent_id(self):
        """create_agents_bulk should fail when all agent IDs are invalid.

        It should raise an error upon request for creation of all agents with invalid id.
        """
        payload = [
            {"id": "toto/tutu", "configuration": valid_data.VALID_CONFIGURATION},
            {"id": "toto@tutu", "configuration": valid_data.VALID_CONFIGURATION},
        ]
        self.assertRaises(
            craft_err.CraftAiBadRequestError, self.client.create_agents_bulk, payload
        )

    def test_create_agents_with_an_empty_payload(self):
        """create_agents_bulk should fail when given payload is empty.

        It should raise an error of invalid given payload.
        """
        payload = []

        self.assertRaises(
            craft_err.CraftAiBadRequestError, self.client.create_agents_bulk, payload
        )

    def test_create_agents_bulk_with_invalid_context(self):
        """create_agents_bulk should fail when all agent contexts are invalid or the `context`
        field doesn't exist.

        It should raise an error upon request for creation of all agents with invalid context.
        """
        payload = []
        agents_lst = []
        # Add all the invalid context to check
        for i, invalid_context in enumerate(invalid_data.INVALID_CONTEXTS):
            new_agent_id = generate_entity_id(
                "test_create_agents_bulk_with_invalid_context" + str(i)
            )
            invalid_configuration = {
                "context": invalid_data.INVALID_CONTEXTS[invalid_context],
                "output": ["lightbulbColor"],
                "time_quantum": 100,
            }
            self.client.delete_agent(new_agent_id)
            payload.append({"id": new_agent_id, "configuration": invalid_configuration})
            agents_lst.append(new_agent_id)

        # Add an agent with no context field
        new_agent_id = self.agent_name.format(len(agents_lst))
        self.client.delete_agent(new_agent_id)
        invalid_configuration = {"output": ["lightbulbColor"], "time_quantum": 100}
        payload.append({"id": new_agent_id, "configuration": invalid_configuration})
        agents_lst.append(new_agent_id)

        self.assertRaises(
            craft_err.CraftAiBadRequestError, self.client.create_agents_bulk, payload
        )

        self.addCleanup(self.clean_up_agents, agents_lst)

    def test_create_agents_bulk_undefined_config(self):
        """create_agents_bulk should fail when the configuration is undefined or the
        `configuration` field doesn't exist.

        It should raise an error upon request for creation of all agents with no
        configuration key in the request body, since it is a mandatory field to
        create an agent.
        """
        payload = []
        agents_lst = []
        # Add all the invalid context to check
        for i, empty_configuration in enumerate(invalid_data.UNDEFINED_KEY):
            new_agent_id = generate_entity_id(
                "test_create_agents_bulk_undef_conf_" + str(i)
            )
            self.client.delete_agent(new_agent_id)
            payload.append(
                {
                    "id": new_agent_id,
                    "configuration": invalid_data.UNDEFINED_KEY[empty_configuration],
                }
            )
            agents_lst.append(new_agent_id)

        # Add agent with no configuration
        new_agent_id = self.agent_name.format(len(agents_lst))
        self.client.delete_agent(new_agent_id)
        payload.append({"id": new_agent_id})
        agents_lst.append(new_agent_id)

        self.assertRaises(
            craft_err.CraftAiBadRequestError, self.client.create_agents_bulk, payload
        )

        self.addCleanup(self.clean_up_agents, agents_lst)

    def test_create_agents_bulk_invalid_time_quantum(self):
        """create_agents_bulk should fail when given invalid time quantums.

        It should raise an error upon request for creation of all agent with incorrect time
        quantum in the configuration, since it is essential to perform any action with craft
        ai.
        """
        payload = []
        agents_lst = []
        # Add all the invalid time quantum to check
        for i, inv_tq in enumerate(invalid_data.INVALID_TIME_QUANTA):
            new_agent_id = generate_entity_id(
                "test_create_agents_bulk_invalid_time_quantum"
            )
            invalid_configuration = {
                "context": valid_data.VALID_CONTEXT,
                "output": valid_data.VALID_OUTPUT,
                "time_quantum": invalid_data.INVALID_TIME_QUANTA[inv_tq],
            }
            self.client.delete_agent(new_agent_id)
            payload.append({"id": new_agent_id, "configuration": invalid_configuration})
            agents_lst.append(new_agent_id)

        self.assertRaises(
            craft_err.CraftAiBadRequestError, self.client.create_agents_bulk, payload
        )

        self.addCleanup(self.clean_up_agents, agents_lst)


class TestCreateAgentsBulkSomeFailure(unittest.TestCase):
    """Checks that the client succeed when creating an/multiple agent(s)
    with bad input and an/multiple agent(s) with valid input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)

    @classmethod
    def tearDownClass(cls):
        for agent_id in cls.client.list_agents():
            try:
                cls.client.delete_agent(agent_id)
            except craft_err.CraftAiError:
                continue

    def setUp(self):
        self.agent_id = generate_entity_id("test_create_agents_bulk_SomeFail")
        self.agent_name = generate_entity_id("test_create_agents_bulk_SomeFail")
        # Makes sure that no agent with the same ID already exists
        resp = self.client.delete_agent(self.agent_id)
        self.assertIsInstance(resp, dict)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            try:
                self.clean_up_agent(aid)
            except craft_err.CraftAiError:
                continue

    def test_create_some_agents_with_existing_agent_id(self):
        """create_agents_bulk should succeed when some of the ID given already exist
        and the others doesn't.

        It should give a proper JSON response with a list containing dicts.
        The ones having existing IDs have the `error` field being a CraftAiBadRequestError.
        The ones having valid IDs have `configuration` field being strings.
        In either case they should have 'id' being the same as the one given as a parameter.
        """
        payload = [
            {"id": self.agent_id, "configuration": valid_data.VALID_CONFIGURATION},
            {"configuration": valid_data.VALID_CONFIGURATION},
        ]
        resp1 = self.client.create_agents_bulk(payload)
        resp2 = self.client.create_agents_bulk(payload)

        self.assertEqual(resp2[0].get("id"), self.agent_id)
        self.assertIsInstance(resp2[0].get("error"), craft_err.CraftAiBadRequestError)
        self.assertFalse("configuration" in resp2[0])
        self.assertIsInstance(resp1[1].get("id"), str)
        self.assertTrue("configuration" in resp1[1])
        self.assertIsInstance(resp2[1].get("id"), str)
        self.assertTrue("configuration" in resp2[1])

        self.addCleanup(
            self.clean_up_agents,
            [self.agent_id, resp1[1].get("id"), resp2[1].get("id")],
        )

    def test_create_some_agents_with_invalid_agent_id(self):
        """create_agents_bulk should succeed when some of the ID given are invalid
        and the others are valid.

        It should give a proper JSON response with a list containing dicts.
        The ones having invalid IDs have the `error` field being a CraftAiBadRequestError.
        The ones having valid IDs have `configuration` field being strings.
        In either case they should have 'id' being the same as the one given as a parameter.
        """
        payload = [
            {"id": "toto/tutu", "configuration": valid_data.VALID_CONFIGURATION},
            {"id": self.agent_id, "configuration": valid_data.VALID_CONFIGURATION},
        ]
        resp = self.client.create_agents_bulk(payload)

        self.assertEqual(resp[0].get("id"), "toto/tutu")
        self.assertIsInstance(resp[0].get("error"), craft_err.CraftAiBadRequestError)
        self.assertFalse("configuration" in resp[0])
        self.assertEqual(resp[1].get("id"), self.agent_id)
        self.assertTrue("configuration" in resp[1])

        self.addCleanup(self.clean_up_agent, self.agent_id)

    def test_create_same_agents_in_bulk(self):
        """create_agents_bulk should succeed when agents in a bulk have the same ID given.

        It should give a proper JSON response with a list containing two dicts.
        The first one should have 'id' being the same as the one given as a parameter,
        and the `configuration` field being strings.
        The second one should have `id` being the same as the one given as a parameter
        'error' field being a CraftAiBadRequestError.
        """
        # Calling create_agents_bulk a first time
        payload = [
            {"id": self.agent_id, "configuration": valid_data.VALID_CONFIGURATION},
            {"id": self.agent_id, "configuration": valid_data.VALID_CONFIGURATION},
        ]
        resp = self.client.create_agents_bulk(payload)

        self.assertEqual(resp[0].get("id"), self.agent_id)
        self.assertEqual(resp[1].get("id"), self.agent_id)
        self.assertTrue("configuration" in resp[0] or "configuration" in resp[1])
        if "configuration" in resp[0]:
            self.assertIsInstance(
                resp[1].get("error"), craft_err.CraftAiBadRequestError
            )
        elif "configuration" in resp[1]:
            self.assertIsInstance(
                resp[0].get("error"), craft_err.CraftAiBadRequestError
            )

        self.addCleanup(self.clean_up_agent, self.agent_id)

    def test_create_some_agents_bulk_invalid_context(self):
        """create_agents_bulk should succeed with some agents with invalid context
        and some with valid context.

        It should give a proper JSON response with a list containing dicts.
        The ones having invalid context have the `error` field being a CraftAiBadRequestError.
        The ones having valid ids have the `id` field being string and 'configuration' field
        being a dict.
        """
        # Add valid agent with a valid configuration
        payload = [
            {"id": self.agent_id, "configuration": valid_data.VALID_CONFIGURATION}
        ]
        agents_lst = [self.agent_id]
        # Add all the invalid context to check
        for i, invalid_context in enumerate(invalid_data.INVALID_CONTEXTS):
            new_agent_id = generate_entity_id(
                "test_create_some_agents_bulk_invalid_context"
            )
            invalid_configuration = {
                "context": invalid_data.INVALID_CONTEXTS[invalid_context],
                "output": ["lightbulbColor"],
                "time_quantum": 100,
            }
            self.client.delete_agent(new_agent_id)
            payload.append({"id": new_agent_id, "configuration": invalid_configuration})
            agents_lst.append(new_agent_id)

        # Add an agent with no context field
        new_agent_id = self.agent_name.format(len(agents_lst))
        self.client.delete_agent(new_agent_id)
        invalid_configuration = {"output": ["lightbulbColor"], "time_quantum": 100}

        resp = self.client.create_agents_bulk(payload)

        self.assertEqual(resp[0].get("id"), self.agent_id)
        self.assertTrue("configuration" in resp[0])
        self.assertFalse("error" in resp[0])

        for i in range(1, len(resp)):
            self.assertEqual(resp[i].get("id"), agents_lst[i])
            self.assertTrue("error" in resp[i])
            self.assertFalse("configuration" in resp[i])

        self.addCleanup(self.clean_up_agents, agents_lst)

    def test_create_some_agents_undef_config(self):
        """create_agents_bulk should succeed with some agents with undefined configuration
        and some with valid configuration.

        It should give a proper JSON response with a list containing dicts.
        The ones having invalid configuration have the `error` field being a CraftAiBadRequestError.
        The ones having valid ids have the `id` field being string and 'configuration' field
        being a dict.
        The valid ones should have `id` and `configuration` fields being strings.
        The invalid ones should have 'id' and 'error' fields.
        """
        # Add valid agent with a valid configuration
        payload = [
            {"id": self.agent_id, "configuration": valid_data.VALID_CONFIGURATION}
        ]
        agents_lst = [self.agent_id]
        # Add all the invalid configuration to check
        for i, empty_configuration in enumerate(invalid_data.UNDEFINED_KEY):
            new_agent_id = generate_entity_id(
                "test_create_some_agents_undef_config" + str(i)
            )
            self.client.delete_agent(new_agent_id)
            payload.append(
                {
                    "id": new_agent_id,
                    "configuration": invalid_data.UNDEFINED_KEY[empty_configuration],
                }
            )
            agents_lst.append(new_agent_id)

        # Add agent with no configuration
        new_agent_id = self.agent_name.format(len(agents_lst))
        self.client.delete_agent(new_agent_id)
        payload.append({"id": new_agent_id})
        agents_lst.append(new_agent_id)

        resp = self.client.create_agents_bulk(payload)

        self.assertEqual(resp[0].get("id"), self.agent_id)
        self.assertTrue("configuration" in resp[0])
        self.assertFalse("error" in resp[0])

        for i in range(1, len(resp)):
            self.assertEqual(resp[i].get("id"), agents_lst[i])
            self.assertTrue("error" in resp[i])
            self.assertFalse("configuration" in resp[i])

        self.addCleanup(self.clean_up_agents, agents_lst)

    def test_create_some_agents_inval_time_quant(self):
        """create_agents_bulk should succeed with some agents with invalid time quantum
        in the configuration and some with valid configuration.

        It should give a proper JSON response with a list containing dicts.
        The ones having invalid time quantum have the `error` field being a CraftAiBadRequestError.
        The ones having valid ids have the `id` field being string and 'configuration' field
        being a dict.
        """
        # Add valid agent with a valid configuration
        payload = [
            {"id": self.agent_id, "configuration": valid_data.VALID_CONFIGURATION}
        ]
        agents_lst = [self.agent_id]
        # Add all the invalid time quantum to check
        for i, inv_tq in enumerate(invalid_data.INVALID_TIME_QUANTA):
            new_agent_id = generate_entity_id(
                "test_create_some_agents_inval_time_quant"
            )
            invalid_configuration = {
                "context": valid_data.VALID_CONTEXT,
                "output": valid_data.VALID_OUTPUT,
                "time_quantum": invalid_data.INVALID_TIME_QUANTA[inv_tq],
            }
            self.client.delete_agent(new_agent_id)
            payload.append({"id": new_agent_id, "configuration": invalid_configuration})
            agents_lst.append(new_agent_id)

        resp = self.client.create_agents_bulk(payload)

        self.assertEqual(resp[0].get("id"), self.agent_id)
        self.assertTrue("configuration" in resp[0])
        self.assertFalse("error" in resp[0])

        for i in range(1, len(resp)):
            self.assertEqual(resp[i].get("id"), agents_lst[i])
            self.assertTrue("error" in resp[i])
            self.assertIsInstance(
                resp[i].get("error"), craft_err.CraftAiBadRequestError
            )
            self.assertFalse("configuration" in resp[i])

        self.addCleanup(self.clean_up_agents, agents_lst)
