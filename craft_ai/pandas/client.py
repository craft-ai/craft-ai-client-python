import json
import pandas as pd

from .. import Client as VanillaClient
from .. import Time
from ..constants import DEFAULT_DECISION_TREE_VERSION
from ..errors import CraftAiBadRequestError
from .interpreter import Interpreter
from .utils import format_input, is_valid_property_value, create_timezone_df


def chunker(to_be_chunked_df, chunk_size):
    return (
        to_be_chunked_df[pos : pos + chunk_size]
        for pos in range(0, len(to_be_chunked_df), chunk_size)
    )


class Client(VanillaClient):
    """Client class for craft ai's API using pandas dataframe types"""

    def add_agent_operations(self, agent_id, operations):
        if isinstance(operations, pd.DataFrame):
            if not isinstance(operations.index, pd.DatetimeIndex):
                raise CraftAiBadRequestError(
                    "Invalid dataframe given, it is not time indexed."
                )
            if operations.index.tz is None:
                raise CraftAiBadRequestError(
                    """tz-naive DatetimeIndex are not supported,
                                     it must be tz-aware."""
                )
            agent = super(Client, self).get_agent(agent_id)
            operations = operations.copy(deep=True)

            tz_col = [
                key
                for key, value in agent["configuration"]["context"].items()
                if value["type"] == "timezone"
            ]
            if tz_col:
                tz_col = tz_col[0]
                operations[tz_col] = create_timezone_df(operations, tz_col).iloc[:, 0]

            chunk_size = self.config["operationsChunksSize"]
            for chunk in chunker(operations, chunk_size):
                chunk_operations = [
                    {
                        "timestamp": row.name.value
                        // 10 ** 9,  # Timestamp.value returns nanoseconds
                        "context": {
                            col: format_input(row[col])
                            for col in chunk.columns
                            if is_valid_property_value(col, row[col])
                        },
                    }
                    for _, row in chunk.iterrows()
                ]
                super(Client, self).add_agent_operations(agent_id, chunk_operations)

            return {
                "message": 'Successfully added %i operation(s) to the agent "%s/%s/%s" context.'
                % (
                    len(operations),
                    self.config["owner"],
                    self.config["project"],
                    agent_id,
                )
            }
        else:
            return super(Client, self).add_agent_operations(agent_id, operations)

    def add_agents_operations_bulk(self, payload):
        """Add operations to a group of agents.

        :param list payload: contains the informations necessary for the action.
        It's in the form [{"id": agent_id, "operations": operations}]
        With id that is an str containing only characters in "a-zA-Z0-9_-"
        and must be between 1 and 36 characters. It must referenced an
        existing agent.
        With operations either a list of dict or a DataFrame that has
        the form given in the craft_ai documentation and the configuration of
        the agent.

        :return: list of agents containing a message about the added
        operations.
        :rtype: list of dict.

        :raises CraftAiBadRequestError: if all of the ids are invalid or
        referenced non existing agents or one of the operations is invalid.
        """
        # Check all ids, raise an error if all ids are invalid
        valid_indices, _, _ = self._check_entity_id_bulk(
            payload, check_serializable=False
        )
        valid_payload = [payload[i] for i in valid_indices]

        new_payload = []
        for agent in valid_payload:
            operations = agent["operations"]
            agent_id = agent["id"]
            if isinstance(operations, pd.DataFrame):
                if not isinstance(operations.index, pd.DatetimeIndex):
                    raise CraftAiBadRequestError(
                        "Invalid dataframe given for agent "
                        "{}, it is not time indexed.".format(agent_id)
                    )
                if operations.index.tz is None:
                    raise CraftAiBadRequestError(
                        "tz-naive DatetimeIndex are not supported for "
                        "agent {}, it must be tz-aware.".format(agent_id)
                    )

                agent = super(Client, self).get_agent(agent_id)
                tz_col = [
                    key
                    for key, value in agent["configuration"]["context"].items()
                    if value["type"] == "timezone"
                ]
                if tz_col:
                    tz_col = tz_col[0]
                    operations[tz_col] = create_timezone_df(operations, tz_col).iloc[
                        :, 0
                    ]

                new_operations = [
                    {
                        "timestamp": row.name.value
                        // 10 ** 9,  # Timestamp.value returns nanoseconds
                        "context": {
                            col: format_input(row[col])
                            for col in operations.columns
                            if is_valid_property_value(col, row[col])
                        },
                    }
                    for _, row in operations.iterrows()
                ]
                new_payload.append({"id": agent_id, "operations": new_operations})
            elif isinstance(operations, list):
                # Check if the operations are serializable
                json.dumps([agent])
                new_payload.append({"id": agent_id, "operations": operations})
            else:
                raise CraftAiBadRequestError(
                    "The operations are not put in a DataFrame or a list"
                    "of dict form for the agent {}.".format(agent_id)
                )

        return super(Client, self).add_agents_operations_bulk(new_payload)

    def get_agent_operations(self, agent_id, start=None, end=None):
        operations_list = super(Client, self).get_agent_operations(agent_id, start, end)
        return pd.DataFrame(
            [operation["context"] for operation in operations_list],
            index=pd.to_datetime(
                [operation["timestamp"] for operation in operations_list], unit="s"
            ).tz_localize("UTC"),
        )

    def get_agent_states(self, agent_id, start=None, end=None):
        states = super(Client, self).get_agent_states(agent_id, start, end)

        return pd.DataFrame(
            [state["sample"] for state in states],
            index=pd.to_datetime(
                [state["timestamp"] for state in states], unit="s"
            ).tz_localize("UTC"),
        )

    @staticmethod
    def check_decision_context_df(contexts_df):
        if isinstance(contexts_df, pd.DataFrame):
            if contexts_df.empty:
                raise CraftAiBadRequestError(
                    "Invalid dataframe given, dataframe is empty."
                )
            if not isinstance(contexts_df.index, pd.DatetimeIndex):
                raise CraftAiBadRequestError(
                    "Invalid dataframe given, it is not time indexed."
                )
            if contexts_df.index.tz is None:
                raise CraftAiBadRequestError(
                    """tz-naive DatetimeIndex are not supported,
                                     it must be tz-aware."""
                )
        else:
            raise CraftAiBadRequestError("Invalid data given, it is not a DataFrame.")

    @staticmethod
    def decide_from_contexts_df(tree, contexts_df):
        Client.check_decision_context_df(contexts_df)
        return Interpreter.decide_from_contexts_df(tree, contexts_df)

    def get_agent_decision_tree(
        self, agent_id, timestamp=None, version=DEFAULT_DECISION_TREE_VERSION
    ):
        # Convert pandas timestamp to a numerical timestamp in seconds
        if isinstance(timestamp, pd.Timestamp):
            timestamp = timestamp.value // 10 ** 9

        return super(Client, self).get_agent_decision_tree(agent_id, timestamp, version)

    def get_generator_decision_tree(
        self, generator_id, timestamp=None, version=DEFAULT_DECISION_TREE_VERSION
    ):
        # Convert pandas timestamp to a numerical timestamp in seconds
        if isinstance(timestamp, pd.Timestamp):
            timestamp = timestamp.value // 10 ** 9

        return super(Client, self).get_generator_decision_tree(
            generator_id, timestamp, version
        )

    def get_generator_operations(self, generator_id, start=None, end=None):
        # Convert pandas timestamp to a numerical timestamp in seconds
        if isinstance(start, pd.Timestamp):
            start = start.value // 10 ** 9
        if isinstance(end, pd.Timestamp):
            end = end.value // 10 ** 9

        operations_list = super(Client, self).get_generator_operations(
            generator_id, start, end
        )
        # convert List to DataFrame with a column for each context property
        df = pd.json_normalize(operations_list)

        return df

    def _generate_decision_df_and_tz_col(self, entity_id, contexts_df, configuration):
        df = contexts_df.copy(deep=True)

        tz_col = [
            key
            for key, value in configuration["context"].items()
            if value["type"] == "timezone"
        ]

        if tz_col:
            tz_col = tz_col[0]
            df[tz_col] = create_timezone_df(contexts_df, tz_col).iloc[:, 0]

        return df, tz_col

    def _generate_time_features(self, params, context):
        time = Time(
            t=params["context_ops"][0].value
            // 1000000000,  # Timestamp.value returns nanoseconds
            timezone=context[params["tz_col"]]
            if params["tz_col"]
            else params["context_ops"][0].tz,
        )

        return time

    def _generate_decision_context(self, params, context, time):
        configuration = params["configuration"]
        if configuration != {}:
            context_result = Interpreter._rebuild_context(configuration, context, time)
            context = context_result["context"]
        else:
            context = Interpreter.join_decide_args((context, time))
        # Convert timezones as integers into standard +/hh:mm format
        # This should only happen when no time generated value is required
        decide_context = Interpreter._convert_timezones_to_standard_format(
            configuration, context.copy()
        )

        return decide_context

    def _check_context_properties(self, params):
        context = {
            feature_name: format_input(value)
            for feature_name, value in zip(
                params["feature_names"], params["context_ops"][1:]
            )
            if is_valid_property_value(feature_name, value)
        }
        return context

    def _pandas_agent_boosting_decide_from_df(
        self, agent_id, from_ts, to_ts, params, df
    ):
        decisions_payload = []

        for row in df.itertuples(name=None):
            params["context_ops"] = row
            context = self._check_context_properties(params)
            time = self._generate_time_features(params, context)
            decide_context = self._generate_decision_context(params, context, time)

            decisions_payload.append(
                {
                    "entityName": agent_id,
                    "timeWindow": [from_ts, to_ts],
                    "context": decide_context,
                }
            )

        decisions = super(Client, self).get_agent_bulk_boosting_decision(
            decisions_payload
        )
        output_name = params["configuration"]["output"][0]

        return (
            {
                "{}_predicted_value".format(output_name): decision["output"][
                    "predicted_value"
                ]
            }
            for decision in decisions
        )

    def decide_boosting_from_contexts_df(self, agent_id, from_ts, to_ts, contexts_df):
        Client.check_decision_context_df(contexts_df)
        configuration = self.get_agent(agent_id)["configuration"]
        df, tz_col = self._generate_decision_df_and_tz_col(
            agent_id, contexts_df, configuration
        )

        predictions_iter = self._pandas_agent_boosting_decide_from_df(
            agent_id,
            from_ts,
            to_ts,
            {
                "configuration": configuration,
                "feature_names": df.columns.values,
                "tz_col": tz_col,
            },
            df,
        )
        return pd.DataFrame(predictions_iter, index=df.index)

    def _pandas_generator_boosting_decide_from_df(
        self, generator_id, from_ts, to_ts, params, df
    ):
        decisions_payload = []

        for row in df.itertuples(name=None):
            params["context_ops"] = row
            context = self._check_context_properties(params)
            time = self._generate_time_features(params, context)
            decide_context = self._generate_decision_context(params, context, time)

            decisions_payload.append(
                {
                    "entityName": generator_id,
                    "timeWindow": [from_ts, to_ts],
                    "context": decide_context,
                }
            )

        decisions = super(Client, self).get_generator_bulk_boosting_decision(
            decisions_payload
        )
        output_name = params["configuration"]["output"][0]

        return (
            {
                "{}_predicted_value".format(output_name): decision["output"][
                    "predicted_value"
                ]
            }
            for decision in decisions
        )

    def decide_generator_boosting_from_contexts_df(
        self, generator_id, from_ts, to_ts, contexts_df
    ):
        Client.check_decision_context_df(contexts_df)
        configuration = self.get_generator(generator_id)["configuration"]
        df, tz_col = self._generate_decision_df_and_tz_col(
            generator_id, contexts_df, configuration
        )

        predictions_iter = self._pandas_generator_boosting_decide_from_df(
            generator_id,
            from_ts,
            to_ts,
            {
                "configuration": configuration,
                "feature_names": df.columns.values,
                "tz_col": tz_col,
            },
            df,
        )
        return pd.DataFrame(predictions_iter, index=df.index)
