import unittest

from craft_ai.pandas import CRAFTAI_PANDAS_ENABLED

if CRAFTAI_PANDAS_ENABLED:
    import copy
    import pandas as pd

    from numpy.random import randn

    import craft_ai.pandas

    from .data import pandas_valid_data, valid_data
    from .utils import generate_entity_id
    from . import settings

    AGENT_ID_1_BASE = "test_pandas_1"
    AGENT_ID_2_BASE = "test_pandas_2"
    GENERATOR_ID_BASE = "test_pandas_generator"

    SIMPLE_AGENT_CONFIGURATION = pandas_valid_data.SIMPLE_AGENT_CONFIGURATION
    SIMPLE_AGENT_BOOSTING_CONFIGURATION  = pandas_valid_data.SIMPLE_AGENT_BOOSTING_CONFIGURATION
    SIMPLE_AGENT_DATA = pandas_valid_data.SIMPLE_AGENT_DATA
    SIMPLE_AGENT_MANY_DATA = pandas_valid_data.SIMPLE_AGENT_MANY_DATA
    COMPLEX_AGENT_CONFIGURATION = pandas_valid_data.COMPLEX_AGENT_CONFIGURATION
    COMPLEX_AGENT_CONFIGURATION_2 = pandas_valid_data.COMPLEX_AGENT_CONFIGURATION_2
    COMPLEX_AGENT_DATA = pandas_valid_data.COMPLEX_AGENT_DATA
    COMPLEX_AGENT_DATA_2 = pandas_valid_data.COMPLEX_AGENT_DATA_2
    DATETIME_AGENT_CONFIGURATION = pandas_valid_data.DATETIME_AGENT_CONFIGURATION
    DATETIME_AGENT_DATA = pandas_valid_data.DATETIME_AGENT_DATA
    MISSING_AGENT_CONFIGURATION = pandas_valid_data.MISSING_AGENT_CONFIGURATION
    MISSING_AGENT_DATA = pandas_valid_data.MISSING_AGENT_DATA
    MISSING_AGENT_DATA_DECISION = pandas_valid_data.MISSING_AGENT_DATA_DECISION
    INVALID_PYTHON_IDENTIFIER_CONFIGURATION = (
        pandas_valid_data.INVALID_PYTHON_IDENTIFIER_CONFIGURATION
    )
    INVALID_PYTHON_IDENTIFIER_DATA = pandas_valid_data.INVALID_PYTHON_IDENTIFIER_DATA
    INVALID_PYTHON_IDENTIFIER_DECISION = (
        pandas_valid_data.INVALID_PYTHON_IDENTIFIER_DECISION
    )
    EMPTY_TREE = pandas_valid_data.EMPTY_TREE

    CLIENT = craft_ai.pandas.Client(settings.CRAFT_CFG)


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasSimpleAgent(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "SimpleAgent")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(SIMPLE_AGENT_CONFIGURATION, self.agent_id)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_add_agent_operations_df_bad_index(self):
        df = pd.DataFrame(randn(10, 5), columns=["a", "b", "c", "d", "e"])

        self.assertRaises(
            craft_ai.pandas.errors.CraftAiBadRequestError,
            CLIENT.add_agent_operations,
            self.agent_id,
            df,
        )

    def test_add_agent_operations_df(self):
        CLIENT.add_agent_operations(self.agent_id, SIMPLE_AGENT_DATA)
        agent = CLIENT.get_agent(self.agent_id)
        self.assertEqual(
            agent["firstTimestamp"],
            SIMPLE_AGENT_DATA.first_valid_index().value // 10 ** 9,
        )
        self.assertEqual(
            agent["lastTimestamp"],
            SIMPLE_AGENT_DATA.last_valid_index().value // 10 ** 9,
        )

    def test_add_agent_operations_df_unexpected_property(self):
        df = pd.DataFrame(
            randn(300, 6),
            columns=["a", "b", "c", "d", "e", "f"],
            index=pd.date_range("20200101", periods=300, freq="T").tz_localize(
                "Europe/Paris"
            ),
        )

        self.assertRaises(
            craft_ai.pandas.errors.CraftAiBadRequestError,
            CLIENT.add_agent_operations,
            self.agent_id,
            df,
        )


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasComplexAgent(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "ComplexAgent")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION, self.agent_id)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_add_agent_operations_df_complex_agent(self):
        CLIENT.add_agent_operations(self.agent_id, COMPLEX_AGENT_DATA)
        agent = CLIENT.get_agent(self.agent_id)
        self.assertEqual(
            agent["firstTimestamp"],
            COMPLEX_AGENT_DATA.first_valid_index().value // 10 ** 9,
        )
        self.assertEqual(
            agent["lastTimestamp"],
            COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9,
        )

    def test_add_agent_operations_df_without_tz(self):
        test_df = COMPLEX_AGENT_DATA.drop(columns="tz")
        CLIENT.add_agent_operations(self.agent_id, test_df)
        agent = CLIENT.get_agent(self.agent_id)
        self.assertEqual(
            agent["firstTimestamp"],
            COMPLEX_AGENT_DATA.first_valid_index().value // 10 ** 9,
        )
        self.assertEqual(
            agent["lastTimestamp"],
            COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9,
        )


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasMissingAgent(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "MissingAgent")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(MISSING_AGENT_CONFIGURATION, self.agent_id)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_add_agent_operations_df_missing_agent(self):
        CLIENT.add_agent_operations(self.agent_id, MISSING_AGENT_DATA)
        agent = CLIENT.get_agent(self.agent_id)
        self.assertEqual(
            agent["firstTimestamp"],
            MISSING_AGENT_DATA.first_valid_index().value // 10 ** 9,
        )
        self.assertEqual(
            agent["lastTimestamp"],
            MISSING_AGENT_DATA.last_valid_index().value // 10 ** 9,
        )


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasSimpleAgentWithData(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "SimpleAgentWData")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(SIMPLE_AGENT_CONFIGURATION, self.agent_id)
        CLIENT.add_agent_operations(self.agent_id, SIMPLE_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_get_agent_operations_df(self):
        df = CLIENT.get_agent_operations(self.agent_id)

        self.assertEqual(len(df), 300)
        self.assertEqual(len(df.dtypes), 5)
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2020-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2020-01-01 04:59:00", tz="Europe/Paris"),
        )

    def test_get_agent_states_df(self):
        df = CLIENT.get_agent_states(self.agent_id)

        self.assertEqual(len(df), 180)
        self.assertEqual(len(df.dtypes), 5)
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2020-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2020-01-01 04:58:20", tz="Europe/Paris"),
        )

    def test_tree_visualization(self):
        tree1 = CLIENT.get_agent_decision_tree(
            self.agent_id, DATETIME_AGENT_DATA.last_valid_index().value // 10 ** 9
        )
        craft_ai.pandas.utils.create_tree_html(tree1, "", "constant", None, 500)

    def test_display_tree_raised_error(self):
        tree1 = CLIENT.get_agent_decision_tree(
            self.agent_id, DATETIME_AGENT_DATA.last_valid_index().value // 10 ** 9
        )
        self.assertRaises(
            craft_ai.pandas.errors.CraftAiError,
            craft_ai.pandas.utils.display_tree,
            tree1,
        )


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasSimpleAgentWithOperations(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "SimpleAgentWOp")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)
        CLIENT.add_agent_operations(self.agent_id, valid_data.VALID_OPERATIONS_SET)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_get_decision_tree_with_pdtimestamp(self):
        # test if we get the same decision tree
        decision_tree = CLIENT.get_agent_decision_tree(
            self.agent_id, pd.Timestamp(valid_data.VALID_TIMESTAMP, unit="s", tz="UTC")
        )
        ground_truth_decision_tree = CLIENT.get_agent_decision_tree(
            self.agent_id, valid_data.VALID_TIMESTAMP
        )
        self.assertIsInstance(decision_tree, dict)
        self.assertNotEqual(decision_tree.get("_version"), None)
        self.assertNotEqual(decision_tree.get("configuration"), None)
        self.assertNotEqual(decision_tree.get("trees"), None)
        self.assertEqual(decision_tree, ground_truth_decision_tree)


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasComplexAgentWithData(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "ComplexAgentWData")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION, self.agent_id)
        CLIENT.add_agent_operations(self.agent_id, COMPLEX_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_get_agent_operations_df_complex_agent(self):
        df = CLIENT.get_agent_operations(self.agent_id)

        self.assertEqual(len(df), 10)
        self.assertEqual(len(df.dtypes), 3)
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2020-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2020-01-10 00:00:00", tz="Europe/Paris"),
        )

    def test_decide_from_contexts_df(self):
        tree = CLIENT.get_agent_decision_tree(
            self.agent_id, COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9
        )
        test_df = COMPLEX_AGENT_DATA
        test_df_copy = test_df.copy(deep=True)
        df = CLIENT.decide_from_contexts_df(tree, test_df)

        self.assertEqual(len(df), 10)
        self.assertEqual(len(df.dtypes), 6)
        self.assertTrue(test_df.equals(test_df_copy))
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2020-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2020-01-10 00:00:00", tz="Europe/Paris"),
        )

        # Also works as before, with a plain context
        output = CLIENT.decide(tree, {"a": 1, "tz": "+02:00"})

        self.assertEqual(output["output"]["b"]["predicted_value"], "Pierre")

    def test_decide_from_contexts_df_zero_rows(self):
        tree = CLIENT.get_agent_decision_tree(
            self.agent_id, COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9
        )
        test_df = COMPLEX_AGENT_DATA.iloc[:0, :]

        self.assertRaises(
            craft_ai.errors.CraftAiBadRequestError,
            CLIENT.decide_from_contexts_df,
            tree,
            test_df,
        )

    def test_decide_from_contexts_df_empty_df(self):
        tree = CLIENT.get_agent_decision_tree(
            self.agent_id, COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9
        )

        self.assertRaises(
            craft_ai.errors.CraftAiBadRequestError,
            CLIENT.decide_from_contexts_df,
            tree,
            pd.DataFrame(),
        )


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasComplexAgent2WithData(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "ComplexAgent2WData")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION_2, self.agent_id)
        CLIENT.add_agent_operations(self.agent_id, COMPLEX_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_decide_from_contexts_df_null_decisions(self):
        tree = CLIENT.get_agent_decision_tree(
            self.agent_id, COMPLEX_AGENT_DATA.last_valid_index().value // 10 ** 9
        )

        test_df = pd.DataFrame(
            [["Jean-Pierre", "+02:00"], ["Paul"]],
            columns=["b", "tz"],
            index=pd.date_range("20200201", periods=2, freq="D").tz_localize(
                "Europe/Paris"
            ),
        )
        test_df_copy = test_df.copy(deep=True)

        df = CLIENT.decide_from_contexts_df(tree, test_df)
        self.assertEqual(len(df), 2)
        self.assertTrue(test_df.equals(test_df_copy))

        self.assertTrue(pd.notnull(df["a_predicted_value"][0]))
        self.assertTrue(pd.notnull(df["a_predicted_value"][1]))


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasComplexAgent3WithData(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "ComplexAgent3WData")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(COMPLEX_AGENT_CONFIGURATION_2, self.agent_id)
        CLIENT.add_agent_operations(self.agent_id, COMPLEX_AGENT_DATA_2)

    def test_decide_from_contexts_df_empty_tree(self):

        test_df = pd.DataFrame(
            [[0, "Jean-Pierre", "+02:00"], [1, "Paul", "+02:00"]],
            columns=["a", "b", "tz"],
            index=pd.date_range("20200201", periods=2, freq="D").tz_localize(
                "Europe/Paris"
            ),
        )

        df = CLIENT.decide_from_contexts_df(EMPTY_TREE, test_df)

        expected_error_message = (
            "Unable to take decision: the decision tree is not "
            "based on any context operations."
        )

        self.assertEqual(len(df), 2)
        self.assertEqual(df.columns, ["error"])
        self.assertEqual(df["error"][0], expected_error_message)
        self.assertEqual(df["error"][1], expected_error_message)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_decide_from_contexts_df_with_array(self):
        tree = CLIENT.get_agent_decision_tree(
            self.agent_id, COMPLEX_AGENT_DATA_2.last_valid_index().value // 10 ** 9
        )

        test_df = pd.DataFrame(
            [["Jean-Pierre", "+02:00"], ["Paul"]],
            columns=["b", "tz"],
            index=pd.date_range("20200201", periods=2, freq="D").tz_localize(
                "Europe/Paris"
            ),
        )
        test_df_copy = test_df.copy(deep=True)

        df = CLIENT.decide_from_contexts_df(tree, test_df)
        self.assertEqual(len(df), 2)
        self.assertTrue(test_df.equals(test_df_copy))
        self.assertTrue(pd.notnull(df["a_predicted_value"][0]))
        self.assertTrue(pd.notnull(df["a_predicted_value"][1]))


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasMissingAgentWithData(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "MissingAgentWData")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(MISSING_AGENT_CONFIGURATION, self.agent_id)
        CLIENT.add_agent_operations(self.agent_id, MISSING_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_decide_from_missing_contexts_df(self):
        tree = CLIENT.get_agent_decision_tree(
            self.agent_id, MISSING_AGENT_DATA.last_valid_index().value // 10 ** 9, "2"
        )

        df = CLIENT.decide_from_contexts_df(tree, MISSING_AGENT_DATA_DECISION)

        self.assertEqual(len(df), 2)
        self.assertEqual(
            df.first_valid_index(),
            pd.Timestamp("2020-01-01 00:00:00", tz="Europe/Paris"),
        )
        self.assertEqual(
            df.last_valid_index(),
            pd.Timestamp("2020-01-02 00:00:00", tz="Europe/Paris"),
        )

        # Also works as before, with a context containing an optional value
        output = CLIENT.decide(tree, {"b": {}, "tz": "+02:00"})

        self.assertTrue(pd.notnull(output["output"]["a"]["predicted_value"]))

        # Also works as before, with a context containing a missing value
        output = CLIENT.decide(tree, {"b": None, "tz": "+02:00"})

        self.assertTrue(pd.notnull(output["output"]["a"]["predicted_value"]))


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasDatetimeAgentWithData(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "DatetimeAgentWData")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(DATETIME_AGENT_CONFIGURATION, self.agent_id)
        CLIENT.add_agent_operations(self.agent_id, DATETIME_AGENT_DATA)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_datetime_states_df(self):
        df = CLIENT.get_agent_states(self.agent_id)

        self.assertEqual(len(df), 10)
        self.assertEqual(len(df.dtypes), 4)
        self.assertEqual(df["myTimeOfDay"].tolist(), [2, 3, 6, 7, 4, 5, 14, 15, 16, 19])

    # This test is commented because of the current non-deterministic behavior of craft ai.
    # def test_datetime_decide_from_contexts_df(self):
    #   tree = CLIENT.get_agent_decision_tree(AGENT_ID,
    #                                   DATETIME_AGENT_DATA.last_valid_index().value // 10 ** 9)

    #   test_df = pd.DataFrame(
    #     [
    #       [1],
    #       [3],
    #       [7]
    #     ],
    #     columns=["a"],
    #     index=pd.date_range("20200101 00:00:00",
    #                         periods=3,
    #                         freq="H").tz_localize("Asia/Shanghai"))
    #   test_df_copy = test_df.copy(deep=True)

    #   df = CLIENT.decide_from_contexts_df(tree, test_df)
    #   self.assertEqual(len(df), 3)
    #   self.assertEqual(len(df.dtypes), 6)
    #   self.assertEqual(df["b_predicted_value"].tolist(), ["Pierre", "Paul", "Jacques"])
    #   self.assertTrue(test_df.equals(test_df_copy))


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasAgentWithInvalidIdentifier(unittest.TestCase):
    def setUp(self):
        self.agent_id = generate_entity_id(AGENT_ID_1_BASE + "InvalidIdentifier")
        CLIENT.delete_agent(self.agent_id)
        CLIENT.create_agent(INVALID_PYTHON_IDENTIFIER_CONFIGURATION, self.agent_id)
        CLIENT.add_agent_operations(self.agent_id, INVALID_PYTHON_IDENTIFIER_DATA)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_id)

    def test_decide_from_python_invalid_identifier(self):
        tree = CLIENT.get_agent_decision_tree(
            self.agent_id,
            INVALID_PYTHON_IDENTIFIER_DATA.last_valid_index().value // 10 ** 9,
            "2",
        )

        test_df = INVALID_PYTHON_IDENTIFIER_DECISION.copy(deep=True)
        df = CLIENT.decide_from_contexts_df(tree, test_df)
        self.assertEqual(len(df), 3)
        self.assertEqual(len(df.dtypes), 8)


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasGeneratorWithOperation(unittest.TestCase):
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

    def test_get_generator_decision_tree_with_pdtimestamp(self):
        # test if we get the same decision tree
        decision_tree = CLIENT.get_generator_decision_tree(
            self.generator_id,
            pd.Timestamp(valid_data.VALID_TIMESTAMP, unit="s", tz="UTC"),
        )
        ground_truth_decision_tree = CLIENT.get_generator_decision_tree(
            self.generator_id, valid_data.VALID_TIMESTAMP
        )
        self.assertIsInstance(decision_tree, dict)
        self.assertNotEqual(decision_tree.get("_version"), None)
        self.assertNotEqual(decision_tree.get("configuration"), None)
        self.assertNotEqual(decision_tree.get("trees"), None)
        self.assertEqual(decision_tree, ground_truth_decision_tree)


@unittest.skipIf(CRAFTAI_PANDAS_ENABLED is False, "pandas is not enabled")
class TestPandasBoostingGeneratorWithOperation(unittest.TestCase):

    def setUp(self):
        self.agent_1_id = generate_entity_id(AGENT_ID_1_BASE + "BoostGeneratorWithOp")
        self.agent_2_id = generate_entity_id(AGENT_ID_2_BASE + "BoostGeneratorWithOp")
        self.generator_id = generate_entity_id(GENERATOR_ID_BASE + "BoostGeneratorWithOp")

        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_agent(self.agent_2_id)
        CLIENT.delete_generator(self.generator_id)
        CLIENT.create_agent(SIMPLE_AGENT_BOOSTING_CONFIGURATION , self.agent_1_id)
        CLIENT.create_agent(SIMPLE_AGENT_BOOSTING_CONFIGURATION , self.agent_2_id)
        CLIENT.add_agent_operations(self.agent_1_id, SIMPLE_AGENT_DATA)
        CLIENT.add_agent_operations(self.agent_2_id, SIMPLE_AGENT_MANY_DATA)
        generator_configuration = copy.deepcopy(
            SIMPLE_AGENT_BOOSTING_CONFIGURATION
        )
        generator_configuration["filter"] = [self.agent_1_id, self.agent_2_id]
        CLIENT.create_generator(generator_configuration, self.generator_id)

    def tearDown(self):
        CLIENT.delete_agent(self.agent_1_id)
        CLIENT.delete_agent(self.agent_2_id)
        CLIENT.delete_generator(self.generator_id)

    def test_get_generator_boosting_with_pdtimestamp(self):
        context_df = pd.DataFrame(
            randn(4, 5),
            columns=["a", "b", "c", "d", "e"],
            index=pd.date_range("20200101", periods=4, freq="T").tz_localize(
                "Europe/Paris"
            )
        )
        decisions = CLIENT.decide_generator_boosting_from_contexts_df(
            self.generator_id,
            SIMPLE_AGENT_DATA.last_valid_index().value // 10 ** 9,
            SIMPLE_AGENT_MANY_DATA.last_valid_index().value // 10 ** 9,
            context_df
        )
        self.assertEqual(decisions.shape[0], 4)
