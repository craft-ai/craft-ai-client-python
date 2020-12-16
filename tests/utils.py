from os import environ

ENTITY_MAX_LEN = 36
BASE_NAME_MAX_LEN = ENTITY_MAX_LEN - 3 - 3 - 2
JOB_ID = environ.get("JOB_ID", "loc")

counters = {}


def generate_entity_id(base_name="entity"):
    # Keep only the first characters
    base_name = base_name[:BASE_NAME_MAX_LEN]
    counter = counters[base_name] if base_name in counters else 0
    counter += 1
    counters[base_name] = counter
    return "{}_{:03}_{}".format(base_name, counter, JOB_ID[-3:])
