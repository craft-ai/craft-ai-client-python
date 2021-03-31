import unittest

from craft_ai.pandas import CRAFTAI_PANDAS_ENABLED

if CRAFTAI_PANDAS_ENABLED:
    import copy
    import pandas as pd

    import craft_ai.pandas

    from .data import pandas_valid_data, valid_data
    from .utils import generate_entity_id
    from . import settings

    AGENT_ID_1_BASE = "test_pandas_1"
    AGENT_ID_2_BASE = "test_pandas_2"
    GENERATOR_ID_BASE = "test_pandas_generator"

    SIMPLE_AGENT_CONFIGURATION = pandas_valid_data.SIMPLE_AGENT_CONFIGURATION
    SIMPLE_AGENT_DATA = pandas_valid_data.SIMPLE_AGENT_DATA
    COMPLEX_AGENT_CONFIGURATION = pandas_valid_data.COMPLEX_AGENT_CONFIGURATION
    COMPLEX_AGENT_CONFIGURATION_2 = pandas_valid_data.COMPLEX_AGENT_CONFIGURATION_2
    COMPLEX_AGENT_DATA = pandas_valid_data.COMPLEX_AGENT_DATA
    COMPLEX_AGENT_DATA_2 = pandas_valid_data.COMPLEX_AGENT_DATA_2

    CLIENT = craft_ai.pandas.Client(settings.CRAFT_CFG)


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasSimpleGeneratorWithOpperations(unittest.TestCase):
    def setUp(self):
        self.agent_1_id = generate_entity_id(AGENT_ID_1_BASE + "GeneratorWithOp")
        self.agent_2_id = generate_entity_id(AGENT_ID_2_BASE + "GeneratorWithOp")
        self.generator_id = generate_entity_id(GENERATOR_ID_BASE + "GeneratorWithOp")

        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_agent(self.agent_2_id)
        CLIENT.delete_generator(self.generator_id)
        CLIENT.create_agent(valid_data.VALID_CONFIGURATION, self.agent_1_id)
        CLIENT.create_agent(valid_data.VALID_CONFIGURATION, self.agent_2_id)
        CLIENT.add_agent_operations(self.agent_1_id, valid_data.VALID_OPERATIONS_SET)
        CLIENT.add_agent_operations(self.agent_2_id, valid_data.VALID_OPERATIONS_SET)
        generator_configuration = copy.deepcopy(
            valid_data.VALID_GENERATOR_CONFIGURATION
        )
        generator_configuration["filter"] = [self.agent_1_id, self.agent_2_id]
        CLIENT.create_generator(generator_configuration, self.generator_id)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_agent(self.agent_2_id)
        CLIENT.delete_generator(self.generator_id)

    def test_simple_pd_get_generator_operations(self):
        df = CLIENT.get_generator_operations(self.generator_id, None, None)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 12)
        self.assertEqual(len(df.dtypes), 6)
        self.assertEqual(
            df.first_valid_index(), pd.Timestamp("2016-03-23 13:53:50+0000", tz="UTC"),
        )
        self.assertEqual(
            df.last_valid_index(), pd.Timestamp("2016-03-23 14:02:15+0000", tz="UTC"),
        )

    def test_get_generator_operations_with_pdtimestamp(self):
        ops_df = CLIENT.get_generator_operations(
            self.generator_id,
            pd.Timestamp(valid_data.VALID_TIMESTAMP, unit="s", tz="UTC"),
            pd.Timestamp(valid_data.VALID_LAST_TIMESTAMP, unit="s", tz="UTC"),
        )

        ground_truth_ops_df = CLIENT.get_generator_operations(
            self.generator_id,
            valid_data.VALID_TIMESTAMP,
            valid_data.VALID_LAST_TIMESTAMP,
        )

        self.assertIsInstance(ops_df, pd.DataFrame)
        self.assertNotEqual(ops_df.get("agent_id").any(), None)
        self.assertNotEqual(ops_df.columns.any(), None)
        self.assertTrue(ops_df.equals(ground_truth_ops_df))


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasComplexGeneratorWithOpperations(unittest.TestCase):
    def setUp(self):
        self.agent_1_id = generate_entity_id(AGENT_ID_1_BASE + "GeneratorWithOp")
        self.agent_2_id = generate_entity_id(AGENT_ID_2_BASE + "GeneratorWithOp")
        self.generator_id = generate_entity_id(GENERATOR_ID_BASE + "GeneratorWithOp")

        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_agent(self.agent_2_id)
        CLIENT.delete_generator(self.generator_id)
        CLIENT.create_agent(valid_data.VALID_CONFIGURATION, self.agent_1_id)
        CLIENT.create_agent(valid_data.VALID_CONFIGURATION, self.agent_2_id)
        CLIENT.add_agent_operations(
            self.agent_1_id, valid_data.VALID_OPERATIONS_SET_COMPLETE_1
        )
        CLIENT.add_agent_operations(
            self.agent_2_id, valid_data.VALID_OPERATIONS_SET_COMPLETE_2
        )
        generator_configuration = copy.deepcopy(
            valid_data.VALID_GENERATOR_CONFIGURATION
        )
        generator_configuration["filter"] = [self.agent_1_id, self.agent_2_id]
        CLIENT.create_generator(generator_configuration, self.generator_id)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_agent(self.agent_2_id)
        CLIENT.delete_generator(self.generator_id)

    def test_complex_pd_get_generator_operations(self):
        df = CLIENT.get_generator_operations(self.generator_id, None, None)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 17)
        self.assertEqual(len(df.dtypes), 6)
        self.assertEqual(
            df.first_valid_index(), pd.Timestamp("2016-05-05 16:13:20+0000", tz="UTC"),
        )
        self.assertEqual(
            df.last_valid_index(), pd.Timestamp("2016-05-05 16:34:20+0000", tz="UTC"),
        )
