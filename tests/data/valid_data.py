VALID_CONTEXT = {
    "tz": {"type": "timezone"},
    "presence": {"type": "enum"},
    "lightIntensity": {"type": "continuous"},
    "lightbulbColor": {"type": "enum"},
}
VALID_OUTPUT = ["lightbulbColor"]
VALID_MODEL_TYPE = "boosting"
VALID_TREE_MAX_DEPTH = 5
VALID_TQ = 100
VALID_TREE_MAX_OPERATIONS = 50000
VALID_LEARNING_PERIOD = 6000000
VALID_CONFIGURATION = {
    "context": VALID_CONTEXT,
    "output": VALID_OUTPUT,
    "time_quantum": VALID_TQ,
}
VALID_NUM_ROUND = 100
VALID_LEARNING_RATE = 0.1
VALID_BOOSTING_CONFIGURATION = {
    "model_type": VALID_MODEL_TYPE,
    "context": VALID_CONTEXT,
    "output": VALID_OUTPUT,
    "num_iterations": VALID_NUM_ROUND,
    "learning_rate": VALID_LEARNING_RATE,
    "tree_max_depth": VALID_TREE_MAX_DEPTH,
    "tree_max_operations": VALID_TREE_MAX_OPERATIONS,
    "operations_as_events": True,
}

VALID_GENERATOR_CONFIGURATION = {
    "context": VALID_CONTEXT,
    "output": VALID_OUTPUT,
    "time_quantum": VALID_TQ,
    "operations_as_events": True,
    "learning_period": VALID_LEARNING_PERIOD,
    "tree_max_operations": VALID_TREE_MAX_OPERATIONS,
    "filter": ["test_filter"],
}

VALID_GENERATOR_BOOSTING_CONFIGURATION = {
    "model_type": VALID_MODEL_TYPE,
    "context": VALID_CONTEXT,
    "output": VALID_OUTPUT,
    "num_iterations": VALID_NUM_ROUND,
    "learning_rate": VALID_LEARNING_RATE,
    "tree_max_operations": VALID_TREE_MAX_OPERATIONS,
    "operations_as_events": True,
    "filter": ["test_filter"],
}

VALID_LARGE_CONFIGURATION = {
    "context": {
        "e1": {"type": "enum"},
        "e2": {"type": "enum"},
        "e3": {"type": "enum"},
        "e4": {"type": "enum"},
        "c1": {"type": "continuous"},
        "c2": {"type": "continuous"},
        "c3": {"type": "continuous"},
        "c4": {"type": "continuous"},
        "time": {"type": "time_of_day", "is_generated": True},
        "day_of_week": {"type": "time_of_day", "is_generated": True},
        "tz": {"type": "timezone"},
    },
    "output": ["c4"],
    "time_quantum": 100,
    "learning_period": 3600 * 24 * 7,
}

VALID_TIMESTAMP = 1458741230
VALID_LAST_TIMESTAMP = 1458741735
VALID_OPERATIONS_SET = [
    {
        "timestamp": VALID_TIMESTAMP,
        "context": {
            "tz": "+02:00",
            "presence": "occupant",
            "lightIntensity": 1,
            "lightbulbColor": "#ffffff",
        },
    },
    {
        "timestamp": 1458741331,
        "context": {"presence": "player", "lightIntensity": 0.5},
    },
    {"timestamp": 1458741432, "context": {"presence": "none", "lightIntensity": 0}},
    {"timestamp": 1458741533, "context": {"presence": "occupant+player"}},
    {
        "timestamp": 1458741634,
        "context": {
            "tz": "+01:00",
            "presence": "occupant",
            "lightIntensity": 0.8,
            "lightbulbColor": "#f56fff",
        },
    },
    {
        "timestamp": VALID_LAST_TIMESTAMP,
        "context": {
            "presence": "player",
            "lightIntensity": 0.5,
            "lightbulbColor": "#fff596",
        },
    },
]

VALID_OPERATIONS_SET_COMPLETE_1 = [
    {
        "timestamp": 1462464800,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.4,
            "lightbulbColor": "green",
        },
    },
    {
        "timestamp": 1462464900,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.4,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465000,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.8,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465100,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.8,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465200,
        "context": {
            "tz": "+02:00",
            "presence": "giselle",
            "lightIntensity": 0.8,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465300,
        "context": {
            "tz": "+02:00",
            "presence": "giselle",
            "lightIntensity": 0.8,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465400,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.4,
            "lightbulbColor": "green",
        },
    },
    {
        "timestamp": 1462465500,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.4,
            "lightbulbColor": "green",
        },
    },
    {
        "timestamp": 1462465600,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.4,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465700,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.6,
            "lightbulbColor": "green",
        },
    },
    {
        "timestamp": 1462465800,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.4,
            "lightbulbColor": "green",
        },
    },
]

VALID_OPERATIONS_SET_COMPLETE_2 = [
    {
        "timestamp": 1462465510,
        "context": {
            "tz": "+02:00",
            "presence": "giselle",
            "lightIntensity": 1,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465620,
        "context": {
            "tz": "+02:00",
            "presence": "giselle",
            "lightIntensity": 1,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465730,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.6,
            "lightbulbColor": "pink",
        },
    },
    {
        "timestamp": 1462465840,
        "context": {
            "tz": "+02:00",
            "presence": "giselle",
            "lightIntensity": 0.8,
            "lightbulbColor": "green",
        },
    },
    {
        "timestamp": 1462465950,
        "context": {
            "tz": "+02:00",
            "presence": "robert",
            "lightIntensity": 0.4,
            "lightbulbColor": "green",
        },
    },
    {
        "timestamp": 1462466060,
        "context": {
            "tz": "+02:00",
            "presence": "giselle",
            "lightIntensity": 1,
            "lightbulbColor": "green",
        },
    },
]
