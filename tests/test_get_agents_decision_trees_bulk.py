import unittest
import semver

from craft_ai import Client, errors as craft_err
from craft_ai.constants import DEFAULT_DECISION_TREE_VERSION

from . import settings
from .utils import generate_entity_id
from .data import valid_data, invalid_data

NB_DECISION_TREES_TO_GET = 3
AGENT_ID_1_BASE = "get_dt_bulk_1"
AGENT_ID_2_BASE = "get_dt_bulk_2"


class TestGetDecisionTreesBulkSuccess(unittest.TestCase):
    """Checks that the client succeeds when getting
    an/multiple decision tree(s) with OK input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id1 = generate_entity_id(AGENT_ID_1_BASE + "Success")
        cls.agent_id2 = generate_entity_id(AGENT_ID_2_BASE + "Success")

    @classmethod
    def tearDown(cls):
        cls.client.delete_agent(cls.agent_id1)
        cls.client.delete_agent(cls.agent_id2)

    def setUp(self):
        self.client.delete_agent(self.agent_id1)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id1)
        self.client.add_agent_operations(
            self.agent_id1, valid_data.VALID_OPERATIONS_SET
        )

        self.client.delete_agent(self.agent_id2)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id2)
        self.client.add_agent_operations(
            self.agent_id2, valid_data.VALID_OPERATIONS_SET
        )

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_get_one_decision_tree_with_correct_input(self):
        """get_agents_decision_trees_bulk should succeed when given a correct input.

        It should give a proper JSON response with a list containing a dict
        with `id` field being string and 'tree' field being a dict. As we don't
        specify the version the field 'tree''_version' should be the one by default.
        """
        payload = [{"id": self.agent_id1, "timestamp": valid_data.VALID_LAST_TIMESTAMP}]

        decision_trees = self.client.get_agents_decision_trees_bulk(payload)

        self.assertIsInstance(decision_trees, list)
        self.assertIsInstance(decision_trees[0], dict)
        self.assertIsInstance(decision_trees[0].get("tree"), dict)
        self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
        tree_version = semver.VersionInfo.parse(
            decision_trees[0].get("tree").get("_version")
        ).to_dict()
        self.assertEqual(tree_version["major"], int(DEFAULT_DECISION_TREE_VERSION))
        self.assertNotEqual(decision_trees[0].get("tree").get("configuration"), None)
        self.assertNotEqual(decision_trees[0].get("tree").get("trees"), None)

        self.addCleanup(self.clean_up_agents, [self.agent_id1, self.agent_id2])

    def test_get_all_decision_trees_with_correct_input(self):
        """get_agents_decision_trees_bulk should succeed when given an correct input.

        It should give a proper JSON response with a list containing dicts
        with `id` field being string and 'tree' field being a dict. As we don't
        specify the version the field 'tree''_version' should be the one by default.
        """
        payload = [
            {"id": self.agent_id1, "timestamp": valid_data.VALID_LAST_TIMESTAMP},
            {"id": self.agent_id2, "timestamp": valid_data.VALID_LAST_TIMESTAMP},
        ]

        decision_trees = self.client.get_agents_decision_trees_bulk(payload)

        self.assertIsInstance(decision_trees, list)

        self.assertIsInstance(decision_trees[0], dict)
        self.assertEqual(decision_trees[0].get("id"), self.agent_id1)
        self.assertIsInstance(decision_trees[0].get("tree"), dict)
        self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
        tree_version = semver.VersionInfo.parse(
            decision_trees[0].get("tree").get("_version")
        ).to_dict()
        self.assertEqual(tree_version["major"], int(DEFAULT_DECISION_TREE_VERSION))
        self.assertNotEqual(decision_trees[0].get("tree").get("configuration"), None)
        self.assertNotEqual(decision_trees[0].get("tree").get("trees"), None)

        self.assertIsInstance(decision_trees[1], dict)
        self.assertEqual(decision_trees[1].get("id"), self.agent_id2)
        self.assertIsInstance(decision_trees[1].get("tree"), dict)
        self.assertNotEqual(decision_trees[1].get("tree").get("_version"), None)
        tree_version = semver.VersionInfo.parse(
            decision_trees[1].get("tree").get("_version")
        ).to_dict()
        self.assertEqual(tree_version["major"], int(DEFAULT_DECISION_TREE_VERSION))
        self.assertNotEqual(decision_trees[1].get("tree").get("configuration"), None)
        self.assertNotEqual(decision_trees[1].get("tree").get("trees"), None)

        self.addCleanup(self.clean_up_agents, [self.agent_id1, self.agent_id2])

    def test_get_decision_trees_bulk_specific_version(self):
        """get_agents_decision_trees_bulk should succeed when given a specific version.
        The version asked is the version 1.

        It should give a proper JSON response with a list containing a dict
        with `id` field being string and 'tree' field being a dict with the
        field '_version''major' being the version given as a parameter.
        """
        payload = [
            {"id": self.agent_id1, "timestamp": valid_data.VALID_LAST_TIMESTAMP},
            {"id": self.agent_id2, "timestamp": valid_data.VALID_LAST_TIMESTAMP},
        ]
        version = 1
        decision_trees = self.client.get_agents_decision_trees_bulk(payload, version)

        self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
        tree_version = semver.VersionInfo.parse(
            decision_trees[0].get("tree").get("_version")
        ).to_dict()
        self.assertEqual(tree_version["major"], version)
        self.assertNotEqual(decision_trees[1].get("tree").get("_version"), None)
        tree_version = semver.VersionInfo.parse(
            decision_trees[1].get("tree").get("_version")
        ).to_dict()
        self.assertEqual(tree_version["major"], version)

        self.addCleanup(self.clean_up_agents, [self.agent_id1, self.agent_id2])

    def test_get_decision_trees_bulk_specific_version2(self):
        """get_agents_decision_trees_bulk should succeed when given a specific version.
        The version asked is the version 2.

        It should give a proper JSON response with a list containing a dict
        with `id` field being string and 'tree' field being a dict with the
        field '_version''major' being the version given as a parameter.
        """
        payload = [
            {"id": self.agent_id1, "timestamp": valid_data.VALID_LAST_TIMESTAMP},
            {"id": self.agent_id2, "timestamp": valid_data.VALID_LAST_TIMESTAMP},
        ]
        version = 2
        decision_trees = self.client.get_agents_decision_trees_bulk(payload, version)

        self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
        tree_version = semver.VersionInfo.parse(
            decision_trees[0].get("tree").get("_version")
        ).to_dict()
        self.assertEqual(tree_version["major"], version)

        self.assertNotEqual(decision_trees[1].get("tree").get("_version"), None)
        tree_version = semver.VersionInfo.parse(
            decision_trees[1].get("tree").get("_version")
        ).to_dict()
        self.assertEqual(tree_version["major"], version)

        self.addCleanup(self.clean_up_agents, [self.agent_id1, self.agent_id2])

    def test_get_decision_trees_bulk_without_timestamp(self):
        """get_agents_decision_trees_bulk should succeed when given no timestamp.

        It should give a proper JSON response with a list containing a dict
        with `id` field being string and 'tree' field being a dict and the
        timestamp should be the same as the one of the last operation.
        """
        payload = [{"id": self.agent_id1}, {"id": self.agent_id2}]
        decision_trees = self.client.get_agents_decision_trees_bulk(payload)

        true_payload = [
            {"id": self.agent_id1, "timestamp": valid_data.VALID_LAST_TIMESTAMP},
            {"id": self.agent_id2, "timestamp": valid_data.VALID_LAST_TIMESTAMP},
        ]
        ground_truth_decision_tree = self.client.get_agents_decision_trees_bulk(
            true_payload
        )

        self.assertEqual(
            decision_trees[0].get("tree"), ground_truth_decision_tree[0].get("tree")
        )

        self.addCleanup(self.clean_up_agents, [self.agent_id1, self.agent_id2])


class TestGetGroupDecisionTreesBulkSuccess(unittest.TestCase):
    """Checks that the client succeeds when getting
    an/multiple decision tree(s) with OK input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.client = Client(settings.CRAFT_CFG)
        cls.agents = []

    @classmethod
    def tearDownClass(cls):
        for agent_id in cls.agents:
            try:
                cls.client.delete_agent(agent_id)
            except craft_err.CraftAiError:
                continue

    def setUp(self):
        for i in range(NB_DECISION_TREES_TO_GET):
            self.agents.append(generate_entity_id(AGENT_ID_1_BASE + "GroupSucc"))

        # Makes sure that no agent with the same ID already exists
        for agent_id in self.agents:
            self.client.delete_agent(agent_id)
            self.client.create_agent(valid_data.VALID_CONFIGURATION, agent_id)
            self.client.add_agent_operations(agent_id, valid_data.VALID_OPERATIONS_SET)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_get_group_decision_trees(self):
        """get_agents_decision_trees_bulk should succeed when given a lot of decision
        trees to retrieve.

        It should give a proper JSON response with a list containing dicts
        with `id` field being string and 'tree' field being a dict.
        """
        payload = []
        for agent_id in self.agents:
            payload.append(
                {"id": agent_id, "timestamp": valid_data.VALID_LAST_TIMESTAMP}
            )

        decision_trees = self.client.get_agents_decision_trees_bulk(payload)

        for decision_tree in decision_trees:
            self.assertIsInstance(decision_tree, dict)
            self.assertIsInstance(decision_tree.get("tree"), dict)
            self.assertFalse("error" in decision_tree)

        self.addCleanup(self.clean_up_agents, self.agents)


class TestGetDecisionTreesBulkFailure(unittest.TestCase):
    """Checks that the client fails when when getting
    an/multiple decision tree(s) with bad input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)

    def setUp(self):
        self.agent_name = generate_entity_id(AGENT_ID_1_BASE + "Failure")

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_get_all_decision_trees_with_invalid_id(self):
        """get_agents_decision_trees_bulk should fail when given non-string/empty string ID
        or unknown ID.

        It should raise an error upon request for retrieval of multiple agents's
        decision tree with an ID that is not of type string, since agent IDs
        should always be strings.
        """
        # Add an unknown id and a dictionary without an id field
        payload = [
            {
                "id": invalid_data.UNKNOWN_ID,
                "timestamp": valid_data.VALID_LAST_TIMESTAMP,
            },
            {"timestamp": valid_data.VALID_TIMESTAMP},
        ]
        # Add all the invalid id to check
        for empty_id in invalid_data.UNDEFINED_KEY:
            payload.append(
                {
                    "id": invalid_data.UNDEFINED_KEY[empty_id],
                    "timestamp": valid_data.VALID_LAST_TIMESTAMP,
                }
            )

        self.assertRaises(
            craft_err.CraftAiBadRequestError,
            self.client.get_agents_decision_trees_bulk,
            payload,
        )

    def test_get_all_decision_trees_invalid_timestamp(self):
        """get_agents_decision_trees_bulk should fail when given invalid timestamps

        It should raise an error upon request for retrieval of multiple agents's
        decision tree with an invalid timestamp, since timestamp should always be
        a positive integer.
        """
        payload = []
        agents_lst = []
        # Add all the invalid timestamp to check
        for i, timestamp in enumerate(invalid_data.INVALID_TIMESTAMPS):
            new_agent_id = generate_entity_id(
                "test_get_all_decision_trees_invalid_timestamp"
            )

            self.client.delete_agent(new_agent_id)
            self.client.create_agent(valid_data.VALID_CONFIGURATION, new_agent_id)
            self.client.add_agent_operations(
                new_agent_id, valid_data.VALID_OPERATIONS_SET
            )

            payload.append(
                {
                    "id": new_agent_id,
                    "timestamp": invalid_data.INVALID_TIMESTAMPS[timestamp],
                }
            )
            agents_lst.append(new_agent_id)

        self.assertRaises(
            craft_err.CraftAiBadRequestError,
            self.client.get_agents_decision_trees_bulk,
            payload,
        )
        self.addCleanup(self.clean_up_agents, agents_lst)


class TestGetDecisionTreesBulkSomeFailure(unittest.TestCase):
    """Checks that the client succeed when getting an/multiple agent(s)
    with bad input and an/multiple agent(s) with valid input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id(AGENT_ID_1_BASE + "SomeFailure")

    @classmethod
    def tearDownClass(cls):
        try:
            cls.client.delete_agent(cls.agent_id)
        except craft_err.CraftAiError:
            return

    def setUp(self):
        # Makes sure that no agent with the same ID already exists
        self.client.delete_agent(self.agent_id)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)
        self.client.add_agent_operations(self.agent_id, valid_data.VALID_OPERATIONS_SET)

    def clean_up_agent(self, aid):
        # Makes sure that no agent with the standard ID remains
        self.client.delete_agent(aid)

    def clean_up_agents(self, aids):
        # Makes sure that no agent with the standard ID remains
        for aid in aids:
            self.clean_up_agent(aid)

    def test_get_some_decision_trees_with_invalid_id(self):
        """get_agents_decision_trees_bulk should succeed when given some non-string/empty string IDs
        and some valid IDs.

        It should give a proper JSON response with a list containing dicts.
        The ones having invalid ids have the `error` field being a CraftAiBadRequestError.
        The ones having valid ids have the `id` field being string and 'tree' field being a dict.
        """
        # Add valid id and timestamp
        payload = [{"id": self.agent_id, "timestamp": valid_data.VALID_LAST_TIMESTAMP}]
        # Add an unknown id and a dictionary without an id field
        payload.append(
            [
                {
                    "id": invalid_data.UNKNOWN_ID,
                    "timestamp": valid_data.VALID_LAST_TIMESTAMP,
                },
                {"timestamp": valid_data.VALID_TIMESTAMP},
            ]
        )
        # Add all the invalid id to check
        for empty_id in invalid_data.UNDEFINED_KEY:
            payload.append(
                {
                    "id": invalid_data.UNDEFINED_KEY[empty_id],
                    "timestamp": valid_data.VALID_LAST_TIMESTAMP,
                }
            )

        decision_trees = self.client.get_agents_decision_trees_bulk(payload)

        self.assertEqual(decision_trees[0].get("id"), self.agent_id)
        self.assertIsInstance(decision_trees[0].get("tree"), dict)
        self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
        self.assertNotEqual(decision_trees[0].get("tree").get("configuration"), None)
        self.assertNotEqual(decision_trees[0].get("tree").get("trees"), None)

        for i in range(1, len(decision_trees)):
            self.assertTrue("error" in decision_trees[i])

        self.addCleanup(self.clean_up_agents, [self.agent_id])

    def test_get_all_decision_trees_invalid_timestamp(self):
        """get_agents_decision_trees_bulk should succeed when given some invalid timestamps
        and some valid ones.

        It should give a proper JSON response with a list containing dicts.
        The ones having invalid timestamp have the `error` field being a CraftAiBadRequestError.
        The ones having valid timestamp have the `id` field being string and 'tree' field being
        a dict.
        """
        # Add valid id and timestamp
        payload = [{"id": self.agent_id, "timestamp": valid_data.VALID_LAST_TIMESTAMP}]
        agents_lst = [self.agent_id]
        # Add all the invalid timestamp to check
        for i, timestamp in enumerate(invalid_data.INVALID_TIMESTAMPS):
            new_agent_id = generate_entity_id(
                "test_get_all_decision_trees_invalid_timestamp"
            )

            self.client.delete_agent(new_agent_id)
            self.client.create_agent(valid_data.VALID_CONFIGURATION, new_agent_id)
            self.client.add_agent_operations(
                new_agent_id, valid_data.VALID_OPERATIONS_SET
            )

            payload.append(
                {
                    "id": new_agent_id,
                    "timestamp": invalid_data.INVALID_TIMESTAMPS[timestamp],
                }
            )
            agents_lst.append(new_agent_id)

        decision_trees = self.client.get_agents_decision_trees_bulk(payload)

        self.assertEqual(decision_trees[0].get("id"), self.agent_id)
        self.assertIsInstance(decision_trees[0].get("tree"), dict)
        self.assertNotEqual(decision_trees[0].get("tree").get("_version"), None)
        self.assertNotEqual(decision_trees[0].get("tree").get("configuration"), None)
        self.assertNotEqual(decision_trees[0].get("tree").get("trees"), None)

        for i in range(1, len(decision_trees)):
            self.assertEqual(decision_trees[i].get("id"), agents_lst[i])
            self.assertIsInstance(
                decision_trees[i].get("error"), craft_err.CraftAiBadRequestError
            )

        self.addCleanup(self.clean_up_agents, agents_lst)
