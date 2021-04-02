import pandas as pd
import numpy as np
from numpy.random import randn
from craft_ai.pandas import MISSING_VALUE, OPTIONAL_VALUE
from random import random, randint

NB_OPERATIONS = 300
NB_MANY_OPERATIONS = 1000

SIMPLE_AGENT_BOOSTING_CONFIGURATION = {
    "model_type": "boosting",
    "context": {
        "a": {"type": "enum"},
        "b": {"type": "continuous"},
        "c": {"type": "continuous"},
        "d": {"type": "continuous"},
        "e": {"type": "continuous"},
    },
    "output": ["a"],
    "min_samples_per_leaf": 1,
    "operations_as_events": True,
    "tree_max_operations": 50000,
    "num_iterations": 20,
    "learning_rate": 0.5,
}

SIMPLE_AGENT_CONFIGURATION = {
    "context": {
        "a": {"type": "continuous"},
        "b": {"type": "continuous"},
        "c": {"type": "continuous"},
        "d": {"type": "continuous"},
        "e": {"type": "continuous"},
    },
    "output": ["a"],
    "time_quantum": 100,
    "min_samples_per_leaf": 1,
}

SIMPLE_AGENT_BOOSTING_DATA = pd.DataFrame(
    [
        [str(randint(1, 3)), random(), random(), random(), random()]
        for i in range(NB_OPERATIONS)
    ],
    columns=["a", "b", "c", "d", "e"],
    index=pd.date_range("20200101", periods=NB_OPERATIONS, freq="T").tz_localize(
        "Europe/Paris"
    ),
)

SIMPLE_AGENT_BOOSTING_MANY_DATA = pd.DataFrame(
    [
        [str(randint(1, 3)), random(), random(), random(), random()]
        for i in range(NB_MANY_OPERATIONS)
    ],
    columns=["a", "b", "c", "d", "e"],
    index=pd.date_range("20200101", periods=NB_MANY_OPERATIONS, freq="T").tz_localize(
        "Europe/Paris"
    ),
)

SIMPLE_AGENT_DATA = pd.DataFrame(
    randn(NB_OPERATIONS, 5),
    columns=["a", "b", "c", "d", "e"],
    index=pd.date_range("20200101", periods=NB_OPERATIONS, freq="T").tz_localize(
        "Europe/Paris"
    ),
)

SIMPLE_AGENT_MANY_DATA = pd.DataFrame(
    randn(NB_MANY_OPERATIONS, 5),
    columns=["a", "b", "c", "d", "e"],
    index=pd.date_range("20200101", periods=NB_MANY_OPERATIONS, freq="T").tz_localize(
        "Europe/Paris"
    ),
)

SIMPLE_AGENT_DATA_DICT = [
    {
        "timestamp": 1558741230,
        "context": {"a": 10, "b": 10, "c": 10, "d": 10, "e": 10},
    },
    {"timestamp": 1558741331, "context": {"a": 10, "b": 11, "c": 12, "e": 13}},
    {"timestamp": 1558741432, "context": {"a": 13, "b": 44, "c": 33, "d": 22}},
    {"timestamp": 1558741533, "context": {"a": 11, "d": 55, "e": 55}},
    {"timestamp": 1558741634, "context": {"a": 33, "c": 66, "d": 22, "e": 44}},
    {"timestamp": 1558741735, "context": {"a": 1, "b": 33, "c": 33, "d": 44}},
]

COMPLEX_AGENT_CONFIGURATION = {
    "context": {
        "a": {"type": "continuous"},
        "b": {"type": "enum"},
        "tz": {"type": "timezone"},
    },
    "output": ["b"],
    "time_quantum": 100,
    "min_samples_per_leaf": 1,
    "operations_as_events": True,
    "learning_period": 3600 * 24 * 365,
    "tree_max_operations": 50000,
}

COMPLEX_AGENT_CONFIGURATION_2 = {
    "context": {
        "a": {"type": "continuous"},
        "b": {"type": "enum"},
        "tz": {"type": "timezone"},
    },
    "output": ["a"],
    "time_quantum": 100,
    "min_samples_per_leaf": 1,
    "operations_as_events": True,
    "learning_period": 3600 * 24 * 365,
    "tree_max_operations": 50000,
}

COMPLEX_AGENT_DATA = pd.DataFrame(
    [
        [1, "Pierre", "+02:00"],
        [2, "Paul"],
        [3],
        [4],
        [5, "Jacques"],
        [6],
        [7],
        [8, np.nan, "+01:00"],
        [9],
        [10],
    ],
    columns=["a", "b", "tz"],
    index=pd.date_range("20200101", periods=10, freq="D").tz_localize("Europe/Paris"),
)

COMPLEX_AGENT_DATA_2 = pd.DataFrame(
    [
        [1, "Pierre", "+02:00", [8, 9]],
        [2, "Paul"],
        [3],
        [4],
        [5, "Jacques"],
        [6],
        [7],
        [8, np.nan, "+01:00", [1, 2, 3]],
        [9],
        [10],
    ],
    columns=["a", "b", "tz", "arrays"],
    index=pd.date_range("20200101", periods=10, freq="D").tz_localize("Europe/Paris"),
)

DATETIME_AGENT_CONFIGURATION = {
    "context": {
        "a": {"type": "continuous"},
        "b": {"type": "enum"},
        "myTimeOfDay": {"type": "time_of_day"},
        "myCoolTimezone": {"type": "timezone"},
    },
    "output": ["b"],
    "time_quantum": 3600,
    "min_samples_per_leaf": 1,
}

DATETIME_AGENT_DATA = pd.DataFrame(
    [
        [1, "Pierre", "+02:00"],
        [2, "Paul"],
        [3, np.nan, "+04:00"],
        [4],
        [5, "Jacques", "UTC"],
        [6],
        [7, np.nan, "+08:00"],
        [8],
        [9],
        [10, np.nan, "+10:00"],
    ],
    columns=["a", "b", "myCoolTimezone"],
    index=pd.date_range("20200101 00:00:00", periods=10, freq="H").tz_localize("UTC"),
)

MISSING_AGENT_CONFIGURATION = {
    "context": {
        "a": {"type": "continuous"},
        "b": {"type": "enum"},
        "tz": {"type": "timezone"},
    },
    "output": ["a"],
    "time_quantum": 100,
    "min_samples_per_leaf": 1,
}

MISSING_AGENT_DATA = pd.DataFrame(
    [
        [1, MISSING_VALUE, "+02:00"],
        [2, "Paul"],
        [3, OPTIONAL_VALUE],
        [4],
        [5, "Jacques"],
        [6],
        [np.nan, OPTIONAL_VALUE],
        [8, None, "+01:00"],
        [9],
        [10],
    ],
    columns=["a", "b", "tz"],
    index=pd.date_range("20200101", periods=10, freq="D").tz_localize("Europe/Paris"),
)

MISSING_AGENT_DATA_DECISION = pd.DataFrame(
    [[1, MISSING_VALUE, "+02:00"], [3, OPTIONAL_VALUE]],
    columns=["a", "b", "tz"],
    index=pd.date_range("20200101", periods=2, freq="D").tz_localize("Europe/Paris"),
)

INVALID_PYTHON_IDENTIFIER_CONFIGURATION = {
    "context": {
        "a": {"type": "continuous"},
        "1_b": {"type": "enum"},
        "None": {"type": "enum"},
        "_c": {"type": "enum"},
        "tz": {"type": "timezone"},
    },
    "output": ["a"],
    "time_quantum": 100,
    "min_samples_per_leaf": 1,
}

INVALID_PYTHON_IDENTIFIER_DATA = pd.DataFrame(
    [
        [1, "Pierre", "Mignon", "Toto", "+02:00"],
        [2, "Paul"],
        [3],
        [4, "Tata", "Tutu"],
        [5, "Jacques"],
        [6],
        [7],
        [8, np.nan, np.nan, np.nan, "+01:00"],
        [9],
        [10],
    ],
    columns=["a", "1_b", "None", "_c", "tz"],
    index=pd.date_range("20200101", periods=10, freq="D").tz_localize("Europe/Paris"),
)

INVALID_PYTHON_IDENTIFIER_DECISION = pd.DataFrame(
    [
        [1, "Pierre", "Mignon", "Toto", "+02:00"],
        [2, "Paul", "Mignon", "Toto", "+02:00"],
        [3, "Tata", "Tutu", "Toto", "+02:00"],
    ],
    columns=["a", "1_b", "None", "_c", "tz"],
    index=pd.date_range("20200101", periods=3, freq="D").tz_localize("Europe/Paris"),
)

EMPTY_TREE = {
    "_version": "2.0.0",
    "configuration": {
        "context": {
            "a": {"type": "continuous"},
            "b": {"type": "enum"},
            "tz": {"type": "timezone"},
        },
        "output": ["b"],
        "time_quantum": 100,
        "min_samples_per_leaf": 1,
    },
    "trees": {
        "b": {"output_values": [], "prediction": {"confidence": 0, "nb_samples": 0}}
    },
}
