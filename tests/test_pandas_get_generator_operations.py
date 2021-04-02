import unittest

from craft_ai.pandas import CRAFTAI_PANDAS_ENABLED

if CRAFTAI_PANDAS_ENABLED:
    import copy
    import pandas as pd

    import craft_ai.pandas

    from .data import pandas_valid_data
    from .utils import generate_entity_id
    from . import settings

    AGENT_ID_1_BASE = "test_1_df_pd"
    AGENT_ID_2_BASE = "test_2_df_pd"
    GENERATOR_ID_BASE = "test_pandas_gen_df_pd"

    SIMPLE_AGENT_CONFIGURATION = pandas_valid_data.SIMPLE_AGENT_CONFIGURATION
    SIMPLE_AGENT_DATA = pandas_valid_data.SIMPLE_AGENT_DATA
    COMPLEX_AGENT_CONFIGURATION = pandas_valid_data.COMPLEX_AGENT_CONFIGURATION
    COMPLEX_AGENT_CONFIGURATION_2 = pandas_valid_data.COMPLEX_AGENT_CONFIGURATION_2
    COMPLEX_AGENT_DATA = pandas_valid_data.COMPLEX_AGENT_DATA
    COMPLEX_AGENT_DATA_2 = pandas_valid_data.COMPLEX_AGENT_DATA_2
    VALID_GENERATOR_CONFIGURATION = pandas_valid_data.VALID_GENERATOR_CONFIGURATION
    VALID_COMPLEX_GENERATOR_CONFIGURATION = (
        pandas_valid_data.VALID_COMPLEX_GENERATOR_CONFIGURATION
    )
    VALID_TIMESTAMP = pandas_valid_data.VALID_TIMESTAMP
    VALID_LAST_TIMESTAMP = pandas_valid_data.VALID_LAST_TIMESTAMP

    CLIENT = craft_ai.pandas.Client(settings.CRAFT_CFG)


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasSimpleGeneratorWithOpperations(unittest.TestCase):
    def setUp(self):
        self.agent_1_id = generate_entity_id(AGENT_ID_1_BASE + "GeneratorWithOp")
        self.generator_id = generate_entity_id(GENERATOR_ID_BASE + "GeneratorWithOp")

        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_generator(self.generator_id)
        CLIENT.create_agent(SIMPLE_AGENT_CONFIGURATION, self.agent_1_id)

        CLIENT.add_agent_operations(self.agent_1_id, SIMPLE_AGENT_DATA)

        generator_configuration = copy.deepcopy(VALID_GENERATOR_CONFIGURATION)
        generator_configuration["filter"] = [self.agent_1_id]
        CLIENT.create_generator(generator_configuration, self.generator_id)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_generator(self.generator_id)

    def test_simple_pd_get_generator_operations(self):
        df = CLIENT.get_generator_operations(self.generator_id, None, None)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 300)
        self.assertEqual(len(df.dtypes), 7)
        self.assertEqual(
            df.timestamp.min(),
            pd.Timestamp("2019-12-31 23:00:00+0000", tz="UTC").value / 1e9,
        )
        self.assertEqual(
            df.timestamp.max(),
            pd.Timestamp("2020-01-01 03:59:00+0000", tz="UTC").value / 1e9,
        )

    def test_get_generator_operations_with_pdtimestamp(self):

        ops_df = CLIENT.get_generator_operations(
            self.generator_id,
            pd.Timestamp(VALID_TIMESTAMP, unit="s", tz="UTC"),
            pd.Timestamp(VALID_LAST_TIMESTAMP, unit="s", tz="UTC"),
        )

        ground_truth_ops_df = CLIENT.get_generator_operations(
            self.generator_id, VALID_TIMESTAMP, VALID_LAST_TIMESTAMP,
        )

        self.assertIsInstance(ops_df, pd.DataFrame)
        self.assertFalse(ops_df.empty)
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
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION, self.agent_1_id)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION_2, self.agent_2_id)
        CLIENT.add_agent_operations(self.agent_1_id, COMPLEX_AGENT_DATA)
        CLIENT.add_agent_operations(self.agent_2_id, COMPLEX_AGENT_DATA_2)
        generator_configuration = copy.deepcopy(VALID_COMPLEX_GENERATOR_CONFIGURATION)
        generator_configuration["filter"] = [self.agent_1_id, self.agent_2_id]

        CLIENT.create_generator(generator_configuration, self.generator_id)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_agent(self.agent_2_id)
        CLIENT.delete_generator(self.generator_id)

    def test_complex_pd_get_generator_operations(self):
        df = CLIENT.get_generator_operations(self.generator_id, None, None)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 20)
        self.assertEqual(len(df.dtypes), 5)
        self.assertEqual(
            df.timestamp.min(),
            pd.Timestamp("2019-12-31 23:00:00+0000", tz="UTC").value / 1e9,
        )
        self.assertEqual(
            df.timestamp.max(),
            pd.Timestamp("2020-01-09 23:00:00+0000", tz="UTC").value / 1e9,
        )
