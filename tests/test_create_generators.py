import copy
import unittest

from craft_ai import Client, errors as craft_err

from . import settings
from .utils import generate_entity_id
from .data import valid_data, invalid_data


class TestCreateGeneratorSuccess(unittest.TestCase):
    """Checks that the client succeeds when creating a generator with OK input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_create_gen_agent_SUCC")
        cls.generator_id = generate_entity_id("test_create_gen_gen_SUCC")
        cls.filter = [cls.agent_id]

    def setUp(self):
        self.client.delete_agent(self.agent_id)
        self.client.delete_generator(self.generator_id)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)

    def tearDown(self):
        try:
            self.client.delete_generator(self.generator_id)
            self.client.delete_agent(self.agent_id)
        except craft_err.CraftAiError:
            return

    def clean_up_generator(self, generator_id):
        # Makes sure that no generator with the standard ID remains
        try:
            self.client.delete_generator(generator_id)
        except craft_err.CraftAiError:
            return

    def test_create_generator_given_generator_id(self):
        """create_generator should succeed when given a string ID

    It should give a proper JSON response with `id` and
    `configuration` fields being strings and `id` being the same as the one
    given as a parameter.
    """
        generator_configuration = valid_data.VALID_GENERATOR_CONFIGURATION.copy()
        generator_configuration["filter"] = self.filter
        resp = self.client.create_generator(generator_configuration, self.generator_id)
        self.assertEqual(resp.get("id"), self.generator_id)


class TestCreateGeneratorFailure(unittest.TestCase):
    """Checks that the client fails when creating an generator with bad input"""

    @classmethod
    def setUpClass(cls):
        cls.client = Client(settings.CRAFT_CFG)
        cls.agent_id = generate_entity_id("test_create_gen_agent_FAIL")
        cls.generator_id = generate_entity_id("test_create_gen_gen_FAIL")
        cls.filter = [cls.agent_id]

    def setUp(self):
        # Makes sure that no agent with the same ID already exists
        self.client.delete_agent(self.agent_id)
        self.client.delete_generator(self.generator_id)
        self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)

    def tearDown(self):
        try:
            self.client.delete_generator(self.generator_id)
            self.client.delete_agent(self.agent_id)
        except craft_err.CraftAiError:
            return

    def clean_up_generator(self, generator_id):
        # Makes sure that no generator with the standard ID remains
        self.client.delete_generator(generator_id)

    def test_create_generator_with_existing_generator_id(self):
        """create_generator should fail when given an ID that already exists

    It should raise an error upon request for creation of
    an generator with an ID that already exists, since generator IDs
    should always be unique.
    """
        # Calling create_generator a first time
        generator_configuration = valid_data.VALID_GENERATOR_CONFIGURATION.copy()
        generator_configuration["filter"] = self.filter
        self.client.create_generator(generator_configuration, self.generator_id)
        # Asserting that an error is risen the second time
        self.assertRaises(
            craft_err.CraftAiBadRequestError,
            self.client.create_generator,
            generator_configuration,
            self.generator_id,
        )

    def test_create_generator_with_invalid_generator_id(self):
        """create_generator should fail whith an invalid generator id

    It should raise an error upon request for creation of
    an generator with an invalid id.
    """
        # Asserting that an error is risen the second time
        generator_configuration = valid_data.VALID_GENERATOR_CONFIGURATION.copy()
        generator_configuration["filter"] = self.filter
        self.assertRaises(
            craft_err.CraftAiBadRequestError,
            self.client.create_generator,
            generator_configuration,
            "toto/tutu",
        )

    def test_create_generator_with_invalid_context(self):
        """create_generator should fail when given an invalid or no context

    It should raise an error upon request for creation of
    an generator with no context or a context that is invalid.
    """
        for inv_context in invalid_data.INVALID_CONTEXTS:
            configuration = {
                "context": invalid_data.INVALID_CONTEXTS[inv_context],
                "output": ["lightbulbColor"],
                "time_quantum": 100,
                "filter": self.filter,
            }
            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.create_generator,
                configuration,
                self.generator_id,
            )

    def test_create_generator_with_undefined_configuration(self):
        """create_generator should fail when given no configuration key in the request body

    It should raise an error upon request for creation of an generator with
    no configuration key in the request body, since it is a mandatory field to
    create an generator.
    """
        # Testing all non dict configuration cases
        for empty_configuration in invalid_data.UNDEFINED_KEY:
            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.create_generator,
                invalid_data.UNDEFINED_KEY[empty_configuration],
                self.generator_id,
            )

    def test_create_generator_with_invalid_time_quantum(self):
        """create_generator should fail when given an invalid time quantum

    It should raise an error upon request for creation of an generator with
    an incorrect time quantum in the configuration, since it is essential to
    perform any action with craft ai.
    """
        for inv_tq in invalid_data.INVALID_TIME_QUANTA:
            configuration = {
                "context": valid_data.VALID_CONTEXT,
                "output": valid_data.VALID_OUTPUT,
                "time_quantum": invalid_data.INVALID_TIME_QUANTA[inv_tq],
                "filter": self.filter,
            }
            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.create_generator,
                configuration,
                self.generator_id,
            )

    def test_create_generator_with_invalid_agent_name_in_filter(self):
        """create_generator should fail when given an invalid filter

    It should raise an error upon request for creation of an generator with
    incorrect filter, since it is essential to
    the creation of generator.
    """
        for inv_filter in invalid_data.INVALID_FILTER:
            configuration_invalid_filter = copy.deepcopy(
                valid_data.VALID_GENERATOR_CONFIGURATION
            )
            configuration_invalid_filter["filter"] = invalid_data.INVALID_FILTER[
                inv_filter
            ]
            self.assertRaises(
                craft_err.CraftAiBadRequestError,
                self.client.create_generator,
                configuration_invalid_filter,
                self.generator_id,
            )
