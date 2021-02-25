# **craft ai** API python client #

[![PyPI](https://img.shields.io/pypi/v/craft-ai.svg?style=flat-square)](https://pypi.python.org/pypi?:action=display&name=craft-ai) [![Build Status](https://img.shields.io/travis/craft-ai/craft-ai-client-python/master.svg?style=flat-square)](https://travis-ci.org/craft-ai/craft-ai-client-python) [![License](https://img.shields.io/badge/license-BSD--3--Clause-42358A.svg?style=flat-square)](LICENSE) [![python](https://img.shields.io/pypi/pyversions/craft-ai.svg?style=flat-square)](https://pypi.python.org/pypi?:action=display&name=craft-ai)

[**craft ai**'s Explainable AI API](http://craft.ai) enables product & operational teams to quickly deploy and run explainable AIs. craft ai decodes your data streams to deliver self-learning services.

## Get Started!

### 0 - Signup

If you're reading this you are probably already registered with **craft ai**, if not, head to [`https://beta.craft.ai/signup`](https://beta.craft.ai/signup).

### 1 - Create a project

Once your account is setup, let's create your first **project**! Go in the 'Projects' tab in the **craft ai** control center at [`https://beta.craft.ai/inspector`](https://beta.craft.ai/inspector), and press **Create a project**.

Once it's done, you can click on your newly created project to retrieve its tokens. There are two types of tokens: **read** and **write**. You'll need the **write** token to create, update and delete your agent.

### 2 - Setup

#### Install ####

#### [PIP](https://pypi.python.org/pypi/pip/) / [PyPI](https://pypi.python.org/pypi) ####

Let's first install the package from pip.

```sh
pip install --upgrade craft-ai
```
_Depending on your setup you may need to use `pip3` or `pipenv` instead of `pip`._

Then import it in your code

```python
import craft_ai
```
> This client also provides helpers to use it in conjuction with [pandas](#pandas-support)

#### Initialize ####

```python
client = craft_ai.Client({
  "token": "{token}"
})
```

### 3 - Create an agent

**craft ai** is based on the concept of **agents**. In most use cases, one agent is created per user or per device.

An agent is an independent module that stores the history of the **context** of its user or device's context, and learns which **decision** to make based on the evolution of this context in the form of a **decision tree**.

In this example, we will create an agent that learns the **decision model** of a light bulb based on the time of the day and the number of people in the room. This dataset is treated as continuous context updates. If your data is more like events, please refer to the [Advanced Configuration section](#advanced-configuration) to know how to configure your agent. Here, the agent's context has 4 properties:

- `peopleCount` which is a `continuous` property,
- `timeOfDay` which is a `time_of_day` property,
- `timezone`, a property of type `timezone` needed to generate proper values for `timeOfDay` (cf. the [context properties type section](#context-properties-types) for further information),
- and finally `lightbulbState` which is an `enum` property that is also the output.

> :information_source: `timeOfDay` is auto-generated, you will find more information below.

```python
agent_id = "my_first_agent"
configuration = {
  "context": {
    "peopleCount": {
      "type": "continuous"
    },
    "timeOfDay": {
      "type": "time_of_day"
    },
    "timezone": {
      "type": "timezone"
    },
    "lightbulbState": {
      "type": "enum"
    }
  },
  "output": ["lightbulbState"]
}

agent = client.create_agent(configuration, agent_id)
print("Agent", agent["id"], "has successfully been created")
```

Pretty straightforward to test! Open [`https://beta.craft.ai/inspector`](https://beta.craft.ai/inspector), select you project and your agent is now listed.

Now, if you run that a second time, you'll get an error: the agent `'my_first_agent'` is already existing. Let's see how we can delete it before recreating it.

```python
agent_id = "my_first_agent"
client.delete_agent(agent_id)
print("Agent", agent_id, "no longer exists")

configuration = ...
agent = client.create_agent(configuration, agent_id)
print("Agent", agent["id"], "has successfully been created")
```

_For further information, check the ['create agent' reference documentation](#create)._

### 4 - Add context operations

We have now created our first agent but it is not able to do much, yet. To learn a model it needs to be provided with data, in **craft ai** these are called context operations.

In the following we add 8 operations:

1. The initial one sets the initial state of the agent, on July 25 2016 at 5:30, in Paris, nobody is there and the light is off;
2. At 7:02, someone enters the room the light is turned on;
3. At 7:15, someone else enters the room;
4. At 7:31, the light is turned off;
5. At 8:12, everyone leaves the room;
6. At 19:23, 2 persons enter the room;
7. At 22:35, the light is turned on;
8. At 23:06, everyone leaves the room and the light is turned off.


```python
agent_id = "my_first_agent"
client.delete_agent(agent_id)
print("Agent", agent_id, "no longer exists")

configuration = ...
agent = client.create_agent(configuration, agent_id)
print("Agent", agent["id"], "has successfully been created")

context_list = [
  {
    "timestamp": 1469410200,
    "context": {
      "timezone": "+02:00",
      "peopleCount": 0,
      "lightbulbState": "OFF"
    }
  },
  {
    "timestamp": 1469415720,
    "context": {
      "timezone": "+02:00",
      "peopleCount": 1,
      "lightbulbState": "ON"
    }
  },
  {
    "timestamp": 1469416500,
    "context": {
      "timezone": "+02:00",
      "peopleCount": 2,
      "lightbulbState": "ON"
    }
  },
  {
    "timestamp": 1469417460,
    "context": {
      "timezone": "+02:00",
      "peopleCount": 2,
      "lightbulbState": "OFF"
    }
  },
  {
    "timestamp": 1469419920,
    "context": {
      "timezone": "+02:00",
      "peopleCount": 0,
      "lightbulbState": "OFF"
    }
  },
  {
    "timestamp": 1469460180,
    "context": {
      "timezone": "+02:00",
      "peopleCount": 2,
      "lightbulbState": "OFF"
    }
  },
  {
    "timestamp": 1469471700,
    "context": {
      "timezone": "+02:00",
      "peopleCount": 2,
      "lightbulbState": "ON"
    }
  },
  {
    "timestamp": 1469473560,
    "context": {
      "timezone": "+02:00",
      "peopleCount": 0,
      "lightbulbState": "ON"
    }
  }
]
client.add_agent_operations(agent_id, context_list)
print("Successfully added initial operations to agent", agent_id, "!")
```

In real-world applications you will probably do the same kind of thing when the agent is created, and then regularly throughout the lifetime of the agent with newer data.

_For further information, check the ['add context operations' reference documentation](#add-operations)._

### 5 - Compute the decision tree

The agent has acquired a context history, we can now compute a decision tree from it! A decision tree models the output, allowing us to estimate what the output would be in a given context.

The decision tree is computed at a given timestamp, which means it will consider the context history from the creation of this agent up to this moment. Let's first try to compute the decision tree at midnight on July 26, 2016.

```python
agent_id = "my_first_agent"

client.delete_agent(agent_id)
print("Agent", agent_id, "no longer exists")

configuration = ...
agent = client.create_agent(configuration, agent_id)
print("Agent", agent["id"], "has successfully been created")

context_list = ...
client.add_agent_operations(agent_id, context_list)
print("Successfully added initial operations to agent", agent_id, "!")

dt_timestamp = 1469476800
decision_tree = client.get_agent_decision_tree(agent_id, dt_timestamp)
print("The full decision tree at timestamp", dt_timestamp, "is the following:")
import json
print(json.dumps(decision_tree,indent=2))
""" Outputted tree is the following
  {
    "_version":"2.0.0",
    "trees":{
      "lightbulbState":{
        "output_values" : ["OFF", "ON"],
        "children":[
          {
            "children":[
              {
                "prediction":{
                  "confidence":0.6774609088897705,
                  "distribution":[0.8, 0.2],
                  "value":"OFF",
                  "nb_samples": 5
                },
                "decision_rule":{
                  "operand":0.5,
                  "operator":"<",
                  "property":"peopleCount"
                }
              },
              {
                "prediction":{
                  "confidence":0.8630361557006836,
                  "distribution":[0.1, 0.9],
                  "value":"ON",
                  "nb_samples": 10
                },
                "decision_rule":{
                  "operand":0.5,
                  "operator":">=",
                  "property":"peopleCount"
                }
              }
            ],
            "decision_rule":{
              "operand":[
                5,
                5.6666665
              ],
              "operator":"[in[",
              "property":"timeOfDay"
            }
          },
          {
            "children":[
              {
                "prediction":{
                  "confidence":0.9947378635406494,
                  "distribution":[1.0, 0.0],
                  "value":"ON",
                  "nb_samples": 10
                },
                "decision_rule":{
                  "operand":[
                    5.6666665,
                    20.666666
                  ],
                  "operator":"[in[",
                  "property":"timeOfDay"
                }
              },
              {
                "children":[
                  {
                    "prediction":{
                      "confidence":0.969236433506012,
                      "distribution":[0.95, 0.05],
                      "value":"OFF",
                      "nb_samples": 10
                    },
                    "decision_rule":{
                      "operand":1,
                      "operator":"<",
                      "property":"peopleCount"
                    }
                  },
                  {
                    "prediction":{
                      "confidence":0.8630361557006836,
                      "distribution":[0.2, 0.8],
                      "value":"ON",
                      "nb_samples": 15
                    },
                    "decision_rule":{
                      "operand":1,
                      "operator":">=",
                      "property":"peopleCount"
                    }
                  }
                ],
                "decision_rule":{
                  "operand":[
                    20.666666,
                    5
                  ],
                  "operator":"[in[",
                  "property":"timeOfDay"
                }
              }
            ],
            "decision_rule":{
              "operand":[
                5.6666665,
                5
              ],
              "operator":"[in[",
              "property":"timeOfDay"
            }
          }
        ]
      }
    },
    "configuration":{
      "time_quantum":600,
      "learning_period":9000000,
      "context":{
        "peopleCount":{
          "type":"continuous"
        },
        "timeOfDay":{
          "type":"time_of_day",
          "is_generated":True
        },
        "timezone":{
          "type":"timezone"
        },
        "lightbulbState":{
          "type":"enum"
        }
      },
      "output":[
        "lightbulbState"
      ]
    }
  }
"""
```

Try to retrieve the tree at different timestamps to see how it gradually learns from the new operations. To visualize the trees, use the [inspector](https://beta.craft.ai/inspector)!

_For further information, check the ['compute decision tree' reference documentation](#compute)._

### 6 - Make a decision

Once the decision tree is computed it can be used to make a decision. In our case it is basically answering this type of question: "What is the anticipated **state of the lightbulb** at 7:15 if there are 2 persons in the room ?".

```python
agent_id = "my_first_agent"

client.delete_agent(agent_id)
print("Agent", agent_id, "no longer exists")

configuration = ...
agent = client.create_agent(configuration, agent_id)
print("Agent", agent["id"], "has successfully been created")

context_list = ...
client.add_agent_operations(agent_id, context_list)
print("Successfully added initial operations to agent", agent_id, "!")

dt_timestamp = 1469476800
decision_tree = client.get_agent_decision_tree(agent_id, dt_timestamp)
print("The decision tree at timestamp", dt_timestamp, "is the following:")
print(decision_tree)

context = {
  "timezone": "+02:00",
  "timeOfDay": 7.25,
  "peopleCount": 2
}
resp = client.decide(decision_tree, context)
print("The anticipated lightbulb state is:", resp["output"]["lightbulbState"]["predicted_value"])
```

_For further information, check the ['make decision' reference documentation](#make-decision)._

### Python starter kit ###

If you prefer to get started from an existing code base, the official Python starter kit can get you there! Retrieve the sources locally and follow the "readme" to get a fully working **Wellness Coach** example using _real-world_ data.

> [:package: _Get the **craft ai** Python Starter Kit_](https://github.com/craft-ai/craft-ai-starterkit-python)

## API

### Project

**craft ai** agents belong to **projects**. In the current version, each identified users defines a owner and can create projects for themselves, in the future we will introduce shared projects.

### Configuration

Each agent has a configuration defining:

- the context schema, i.e. the list of property keys and their type (as defined in the following section),
- the output properties, i.e. the list of property keys on which the agent makes decisions,

> :warning: In the current version, only one output property can be provided.

- the `time_quantum`, i.e. the minimum amount of time, in seconds, that is meaningful for an agent; context updates occurring faster than this quantum won't be taken into account. As a rule of thumb, you should always choose the largest value that seems right and reduce it, if necessary, after some tests.
- the `learning_period`, i.e. the maximum amount of time, in seconds, that matters for an agent; the agent's decision model can ignore context that is older than this duration. You should generally choose the smallest value that fits this description.

> :warning: if no time_quantum is specified, the default value is 600.

> :warning: if no learning_period is specified, the default value is 15000 time quantums.

> :warning: the maximum learning_period value is 55000 \* time_quantum.

#### Context properties types

##### Base types: `enum`, `continuous` and `boolean`

`enum`, `continuous` and `boolean` are the three base **craft ai** types:

- an `enum` property is a string;
- a `continuous` property is a real number.
- a `boolean` property is a boolean value: `true` or `false`

> :warning: the absolute value of a `continuous` property must be less than 10<sup>20</sup>.

Here is a simple example of configuration :
```json
{
  "context": {
    "timezone": {
      "type": "enum"
    },
    "temperature": {
      "type": "continuous"
    },
    "lightbulbState": {
      "type": "enum"
    }
  },
  "output": ["lightbulbState"],
  "time_quantum": 100,
  "learning_period": 108000
}
```

##### Time types: `timezone`, `time_of_day`, `day_of_week`, `day_of_month` and `month_of_year`

**craft ai** defines the following types related to time:

- a `time_of_day` property is a real number belonging to **[0.0; 24.0[**, each value represents the number of hours in the day since midnight (e.g. 13.5 means 13:30),
- a `day_of_week` property is an integer belonging to **[0, 6]**, each value represents a day of the week starting from Monday (0 is Monday, 6 is Sunday).
- a `day_of_month` property is an integer belonging to **[1, 31]**, each value represents a day of the month.
- a `month_of_year` property is an integer belonging to **[1, 12]**, each value represents a month of the year.
- a `timezone` property can be:
  * a string value representing the timezone as an offset from UTC, supported formats are:

    - **±[hh]:[mm]**,
    - **±[hh][mm]**,
    - **±[hh]**,

    where `hh` represent the hour and `mm` the minutes from UTC (eg. `+01:30`)), between `-12:00` and
    `+14:00`.

  * an integer belonging to **[-720, 840]** which represents the timezone as an offset from UTC:

    - in hours if the integer belongs to **[-15, 15]**
    - in minutes otherwise

  * an abbreviation among the following:

    - **UTC** or **Z** Universal Time Coordinated,
    - **GMT** Greenwich Mean Time, as UTC,
    - **BST** British Summer Time, as UTC+1 hour,
    - **IST** Irish Summer Time, as UTC+1,
    - **WET** Western Europe Time, as UTC,
    - **WEST** Western Europe Summer Time, as UTC+1,
    - **CET** Central Europe Time, as UTC+1,
    - **CEST** Central Europe Summer Time, as UTC+2,
    - **EET** Eastern Europe Time, as UTC+2,
    - **EEST** Eastern Europe Summer Time, as UTC+3,
    - **MSK** Moscow Time, as UTC+3,
    - **MSD** Moscow Summer Time, as UTC+4,
    - **AST** Atlantic Standard Time, as UTC-4,
    - **ADT** Atlantic Daylight Time, as UTC-3,
    - **EST** Eastern Standard Time, as UTC-5,
    - **EDT** Eastern Daylight Saving Time, as UTC-4,
    - **CST** Central Standard Time, as UTC-6,
    - **CDT** Central Daylight Saving Time, as UTC-5,
    - **MST** Mountain Standard Time, as UTC-7,
    - **MDT** Mountain Daylight Saving Time, as UTC-6,
    - **PST** Pacific Standard Time, as UTC-8,
    - **PDT** Pacific Daylight Saving Time, as UTC-7,
    - **HST** Hawaiian Standard Time, as UTC-10,
    - **AKST** Alaska Standard Time, as UTC-9,
    - **AKDT** Alaska Standard Daylight Saving Time, as UTC-8,
    - **AEST** Australian Eastern Standard Time, as UTC+10,
    - **AEDT** Australian Eastern Daylight Time, as UTC+11,
    - **ACST** Australian Central Standard Time, as UTC+9.5,
    - **ACDT** Australian Central Daylight Time, as UTC+10.5,
    - **AWST** Australian Western Standard Time, as UTC+8.

> :information_source: By default, the values of the `time_of_day` and `day_of_week`
> properties are generated from the [`timestamp`](#timestamp) of an agent's
> state and the agent's current `timezone`. Therefore, whenever you use generated
> `time_of_day` and/or `day_of_week` in your configuration, you **must** provide a
> `timezone` value in the context. There can only be one `timezone` property.
>
> If you wish to provide their values manually, add `is_generated: false` to the
> time types properties in your configuration. In this case, since you provide the values, the
> `timezone` property is not required, and you must update the context whenever
> one of these time values changes in a way that is significant for your system.

##### Examples

Let's take a look at the following configuration. It is designed to model the **color** of a lightbulb (the `lightbulbColor` property, defined as an output) depending on the **outside light intensity** (the `lightIntensity` property), the **TV status** (the `TVactivated` property) the **time of the day** (the `time` property) and the **day of the week** (the `day` property).

`day` and `time` values will be generated automatically, hence the need for
`timezone`, the current Time Zone, to compute their value from given
[`timestamps`](#timestamp).

The `time_quantum` is set to 100 seconds, which means that if the lightbulb
color is changed from red to blue then from blue to purple in less that 1
minutes and 40 seconds, only the change from red to purple will be taken into
account.

The `learning_period` is set to 108 000 seconds (one month) , which means that
the state of the lightbulb from more than a month ago can be ignored when learning
the decision model.

```json
{
  "context": {
    "lightIntensity": {
      "type": "continuous"
    },
    "TVactivated": {
      "type": "boolean"
    },
    "time": {
      "type": "time_of_day"
    },
    "day": {
      "type": "day_of_week"
    },
    "timezone": {
      "type": "timezone"
    },
    "lightbulbColor": {
      "type": "enum"
    }
  },
  "output": ["lightbulbColor"],
  "time_quantum": 100,
  "learning_period": 108000
}
```

In this second example, the `time` property is not generated, no property of
type `timezone` is therefore needed. However values of `time` must be manually
provided continuously.

```json
{
  "context": {
    "time": {
      "type": "time_of_day",
      "is_generated": false
    },
    "lightIntensity": {
      "type": "continuous"
    },
      "TVactivated": {
      "type": "boolean"
    },
    "lightbulbColor": {
      "type": "enum"
    }
  },
  "output": ["lightbulbColor"],
  "time_quantum": 100,
  "learning_period": 108000
}
```

### Timestamp

**craft ai** API heavily relies on `timestamps`. A `timestamp` is an instant represented as a [Unix time](https://en.wikipedia.org/wiki/Unix_time), that is to say the amount of seconds elapsed since Thursday, 1 January 1970 at midnight UTC. Note that some programming languages use timestamps in milliseconds, but here we only refer to timestamps **in seconds**. In most programming languages this representation is easy to retrieve, you can refer to [**this page**](https://github.com/techgaun/unix-time/blob/master/README.md) to find out how.

#### `craft_ai.Time` #####

The `craft_ai.Time` class facilitates the handling of time types in **craft ai**. It is able to extract the different **craft ai** formats from various _datetime_ representations, thanks to [datetime](https://docs.python.org/3.5/library/datetime.html).

```python
# From a unix timestamp and an explicit UTC offset
t1 = craft_ai.Time(1465496929, "+10:00")

# t1 == {
#   utc: "2016-06-09T18:28:49.000Z",
#   timestamp: 1465496929,
#   day_of_week: 4,
#   time_of_day: 4.480277777777778,
#   timezone: "+10:00"
# }

# From a unix timestamp and using the local UTC offset.
t2 = craft_ai.Time(1465496929)

# Value are valid if in Paris !
# t2 == {
#   utc: "2016-06-09T18:28:49.000Z",
#   timestamp: 1465496929,
#   day_of_week: 3,
#   time_of_day: 20.480277777777776,
#   timezone: "+02:00"
# }

# From a ISO 8601 string. Note that here it should not have any ":" in the timezone part
t3 = craft_ai.Time("1977-04-22T01:00:00-0500")

# t3 == {
#   utc: "1977-04-22T06:00:00.000Z",
#   timestamp: 230536800,
#   day_of_week: 4,
#   time_of_day: 1,
#   timezone: "-05:00"
# }

# Retrieve the current time with the local UTC offset
now = craft_ai.Time()

# Retrieve the current time with the given UTC offset
nowP5 = craft_ai.Time(timezone="+05:00")
```

### Advanced configuration

The following **advanced** configuration parameters can be set in specific cases. They are **optional**. Usually you would not need them.

- **`operations_as_events`** is a boolean, either `true` or `false`. The default value is `false`. If it is set to true, all context operations are treated as events, as opposed to context updates. This is appropriate if the data for an agent is made of events that have no duration, and if many events are more significant than a few. If `operations_as_events` is `true`, `learning_period` and the advanced parameter `tree_max_operations` must be set as well. In that case, `time_quantum` is ignored because events have no duration, as opposed to the evolution of an agent's context over time.
- **`tree_max_operations`** is a positive integer. It **can and must** be set only if `operations_as_events` is `true`. It defines the maximum number of events on which a single decision tree can be based. It is complementary to `learning_period`, which limits the maximum age of events on which a decision tree is based.
- **`tree_max_depth`** is a positive integer. It defines the maximum depth of decision trees, which is the maximum distance between the root node and a leaf (terminal) node. A depth of 0 means that the tree is made of a single root node. By default, `tree_max_depth` is set to 6 if the output is categorical (e.g. `enum`), or to 4 if the output is numerical (e.g. `continuous`).
- **`min_samples_per_leaf`** is a positive integer. It defines the minimum number of samples that must be in a leaf to allow a split that creates this leaf. It is complementary to `tree_max_depth` in preventing the tree from overgrowing, hence limiting overfitting. By default, `min_samples_per_leaf` is set to 4.

These advanced configuration parameters are optional, and will appear in the agent information returned by **craft ai** only if you set them to something other than their default value. If you intend to use them in a production environment, please get in touch with us.

### Agent

#### Create

Create a new agent, and define its [configuration](#configuration).

> The agent's identifier is a case sensitive string between 1 and 36 characters long. It only accepts letters, digits, hyphen-minuses and underscores (i.e. the regular expression `/[a-zA-Z0-9_-]{1,36}/`).

```python
client.create_agent(
  { # The configuration
    "context": {
      "peopleCount": {
        "type": "continuous"
      },
      "timeOfDay": {
        "type": "time_of_day"
      },
      "timezone": {
        "type": "timezone"
      },
      "lightbulbState": {
        "type": "enum"
      }
    },
    "output": [ "lightbulbState" ],
    "time_quantum": 100,
    "learning_period": 108000
  },
  "my_new_agent" # id for the agent, if undefined a random id is generated
)
```

#### Delete

```python
client.delete_agent(
  "my_new_agent" # The agent id
)
```

#### Retrieve

```python
client.get_agent(
  "my_new_agent" # The agent id
)
```

#### List

```python
client.list_agents()
# Return a list of agents' name
# Example: [ "my_new_agent", "joyful_octopus", ... ]

```

#### Create and retrieve shared url

Create and get a shareable url to view an agent tree.
Only one url can be created at a time.

```python
client.get_shared_agent_inspector_url(
  "my_new_agent", # The agent id.
  1464600256 # optional, the timestamp for which you want to inspect the tree.
)
```

#### Delete shared url

Delete a shareable url.
The previous url cannot access the agent tree anymore.

```python
client.delete_shared_agent_inspector_url(
  'my_new_agent' # The agent id.
)
```



### Generator

The craft ai API lets you generate decision trees built on data from one or several agents by creating a generator. It is useful to:
  - test several hyper-parameters and features sets without reloading all the data for each try
  - gather data from different agents to make new models on top of them, enhancing the possible data combinations and allowing you to inspect the global behavior across your agents

We define the data stream(s) used by a generator by specifying a list of agents as a filter in its configuration. Other than the filter, the configuration of a generator is similar to an agent's configuration. It has to verify some additional properties:

- Every feature defined in the context configuration of the generator must be present in **all** the agent that match the filter, with the same context types.
- The parameters `operations_as_events` must be set to true.
- It follows that the parameters `tree_max_operations` and `learning_period` must be set with valid integers.
- The agent names provided in the list must be valid agent identifiers.

#### Create

Create a new generator, and define its [configuration](#configuration).

> The generator's identifier is a case sensitive string between 1 and 36 characters long. It only accepts letters, digits, hyphen-minuses and underscores (i.e. the regular expression `/[a-zA-Z0-9_-]{1,36}/`).

```python

GENERATOR_NAME = 'smarthome_gen'
GENERATOR_FILTER = ['smarthome']
GENERATOR_CONFIGURATION = {
  "context": {
    "light": {
      "type": "enum"
    },
    "tz": {
      "type": "timezone"
    },
    "movement": {
      "type": "continuous"
    },
    "time": {
      "type": "time_of_day",
      "is_generated": True
    }
  },
  "output": [
    "light"
  ],
  "learning_period": 1500000,
  "tree_max_operations": 15000,
  "operations_as_events": True,
  'filter': GENERATOR_FILTER
}

client.create_generator(
  GENERATOR_CONFIGURATION, # A valid configuration.
  GENERATOR_NAME # The generator id.
)
```

#### Delete

```python
GENERATOR_NAME = 'smarthome_gen'
client.delete_generator(
  GENERATOR_NAME
)
```

#### Retrieve

```python
GENERATOR_NAME = 'smarthome_gen'
client.get_generator(
  GENERATOR_NAME
)

### Ouputted info is the following
"""
{
  "_version": "2.0.0"
  "id": "smarthome_gen",
  "configuration": {
    "operations_as_events": True,
    "learning_period": 1500000,
    "tree_max_operations": 15000,
    "context": {
      "light": {
        "type": "enum"
      },
      "tz": {
        "type": "timezone"
      },
      "movement": {
        "type": "continuous"
      },
      "time": {
        "type": "time_of_day",
        "is_generated": True
      }
    },
    "output": [
      "light"
    ],
    "filter": [
      "smarthome"
    ]
  },
  "firstTimestamp": 1254836352,
  "lastTimestamp": 1272721522,
  "agents": [
    "smarthome"
  ],
}
"""
###

```

#### Retrieve generators list

```python
client.list_generators() # Return the list of generators in the project.
```

#### List operations in the generator

Retrieve the context operations of agents matching the generator's filter. Each operation also contains the identifier of the agent for which it was added, in the `agent_id` property.

```python
GENERATOR_NAME = 'smarthome_gen'
START_TIMESTAMP = 1478894153
END_TIMESTAMP = 1478895266

client.get_generator_operations(
  GENERATOR_NAME,   # The generator id
  START_TIMESTAMP,  # Optional, the **start** timestamp from which the
                    # operations are retrieved (inclusive bound)
  END_TIMESTAMP     # Optional, the **end** timestamp up to which the
                    # operations are retrieved (inclusive bound)
)
```

> This call can generate multiple requests to the craft ai API as results are paginated.

#### Get decision tree

```python
DECISION_TREE_TIMESTAMP = 1469473600
GENERATOR_NAME = 'smarthome_gen'
client.get_generator_decision_tree(
  GENERATOR_NAME, # The generator id
  DECISION_TREE_TIMESTAMP # The timestamp at which the decision tree is retrieved
)

""" Outputted tree is the following
{
  "_version": "2.0.0",
  "trees": {
    "light": {
      "children": [
        {
          "predicted_value": "OFF",
          "confidence": 0.9966583847999572,
          "decision_rule": {
            "operand": [
              7.25,
              22.65
            ],
            "operator": "[in[",
            "property": "time"
          }
        },
        {
          "children": [
            {
              "predicted_value": "ON",
              "confidence": 0.9618390202522278,
              "decision_rule": {
                "operand": [
                  22.65,
                  0.06666667
                ],
                "operator": "[in[",
                "property": "time"
              }
            },
            {
              "children": [
                {
                  "predicted_value": "OFF",
                  "confidence": 0.9797198176383972,
                  "decision_rule": {
                    "operand": [
                      0.06666667,
                      0.6
                    ],
                    "operator": "[in[",
                    "property": "time"
                  }
                },
                {
                  "children": [
                    {
                      "predicted_value": "ON",
                      "confidence": 0.9585137963294984,
                      "decision_rule": {
                        "operand": [
                          0.6,
                          2.25
                        ],
                        "operator": "[in[",
                        "property": "time"
                      }
                    },
                    {
                      "children": [
                        {
                          "predicted_value": "OFF",
                          "confidence": 0.8077218532562256,
                          "decision_rule": {
                            "operand": [
                              2.25,
                              2.4666667
                            ],
                            "operator": "[in[",
                            "property": "time"
                          }
                        }
                      ],
                      "decision_rule": {
                        "operand": [
                          2.25,
                          7.25
                        ],
                        "operator": "[in[",
                        "property": "time"
                      }
                    }
                  ],
                  "decision_rule": {
                    "operand": [
                      0.6,
                      7.25
                    ],
                    "operator": "[in[",
                    "property": "time"
                  }
                }
              ],
              "decision_rule": {
                "operand": [
                  0.06666667,
                  7.25
                ],
                "operator": "[in[",
                "property": "time"
              }
            }
          ],
          "decision_rule": {
            "operand": [
              22.65,
              7.25
            ],
            "operator": "[in[",
            "property": "time"
          }
        }
      ]
    }
  },
  "configuration": {
    "operations_as_events": True,
    "learning_period": 1500000,
    "tree_max_operations": 15000,
    "context": {
      "light": {
        "type": "enum"
      },
      "tz": {
        "type": "timezone"
      },
      "movement": {
        "type": "continuous"
      },
      "time": {
        "type": "time_of_day",
        "is_generated": True
      }
    },
    "output": [
      "light"
    ],
    "filter": [
      "smarthome"
    ]
  }
}
"""
```

#### Get decision

```python
const CONTEXT_OPS = {
  "tz": "+02:00",
  "movement": 2,
  "time": 7.5
};
const DECISION_TREE_TIMESTAMP = 1469473600;
const GENERATOR_NAME = 'smarthome_gen';

client.computeGeneratorDecision(
  GENERATOR_NAME, # The name of the generator
  DECISION_TREE_TIMESTAMP, # The timestamp at which the decision tree is retrieved
  CONTEXT_OPS # A valid context operation according to the generator configuration
)
"""
{
  "_version": "2.0.0",
  "context": {
    "tz": "+02:00",
    "movement": 2,
    "time": 7.5
  },
  "output": {
    "light": {
      "predicted_value": "OFF",
      "confidence": 0.8386044502258301,
      "decision_rules": [
        {
          "operand": [
            2.1166666,
            10.333333
          ],
          "operator": "[in[",
          "property": "time"
        },
        {
          "operand": [
            2.1166666,
            9.3
          ],
          "operator": "[in[",
          "property": "time"
        },
        {
          "operand": [
            2.1166666,
            8.883333
          ],
          "operator": "[in[",
          "property": "time"
        },
        {
          "operand": [
            3.5333333,
            8.883333
          ],
          "operator": "[in[",
          "property": "time"
        }
      ],
      "nb_samples": 442,
      "decision_path": "0-0-0-0-1",
      "distribution": [
        0.85067874,
        0.14932127
      ]
    }
  }
}
"""
```

### Context

#### Add operations

```python
client.add_agent_operations(
  "my_new_agent", # The agent id
  [ # The list of context operations
    {
      "timestamp": 1469410200,
      "context": {
        "timezone": "+02:00",
        "peopleCount": 0,
        "lightbulbState": "OFF"
      }
    },
    {
      "timestamp": 1469415720,
      "context": {
        "timezone": "+02:00",
        "peopleCount": 1,
        "lightbulbState": "ON"
      }
    },
    {
      "timestamp": 1469416500,
      "context": {
        "timezone": "+02:00",
        "peopleCount": 2,
        "lightbulbState": "ON"
      }
    },
    {
      "timestamp": 1469417460,
      "context": {
        "timezone": "+02:00",
        "peopleCount": 2,
        "lightbulbState": "OFF"
      }
    },
    {
      "timestamp": 1469419920,
      "context": {
        "timezone": "+02:00",
        "peopleCount": 0,
        "lightbulbState": "OFF"
      }
    },
    {
      "timestamp": 1469460180,
      "context": {
        "timezone": "+02:00",
        "peopleCount": 2,
        "lightbulbState": "OFF"
      }
    },
    {
      "timestamp": 1469471700,
      "context": {
        "timezone": "+02:00",
        "peopleCount": 2,
        "lightbulbState": "ON"
      }
    },
    {
      "timestamp": 1469473560,
      "context": {
        "timezone": "+02:00",
        "peopleCount": 0,
        "lightbulbState": "ON"
      }
    }
  ]
)
```

##### Missing Values

If the value of a base type property is **missing**, you can send a `null` value. **craft ai** will take into account as much information as possible from this incomplete context.

A context operation with a missing value looks like:
```json
[
  {
    "timestamp": 1469415720,
    "context": {
      "peopleCount": "OFF",
      "lightbulbState": null
    }
  },
  ...
]
```

##### Optional Values

If the value of an **optional** property is not filled at some point—as should be expected from an optional value—send the empty JSON Object `{}` to **craft ai**:

A context with an optional value looks like:
```json
[
  {
    "timestamp": 1469415720,
    "context": {
      "timezone": "+02:00",
      "temperature": {},
      "lightbulbState": "OFF"
    }
  },
  ...
]
```

#### List operations

```python
client.get_agent_operations(
  "my_new_agent", # The agent id
  1478894153, # Optional, the **start** timestamp from which the
              # operations are retrieved (inclusive bound)
  1478895266, # Optional, the **end** timestamp up to which the
              # operations are retrieved (inclusive bound)
)
```

> This call can generate multiple requests to the craft ai API as results are paginated.

#### Retrieve state

```python
client.get_context_state(
  "my_new_agent", # The agent id
  1469473600 # The timestamp at which the context state is retrieved
)
```

#### Retrieve state history

```python
client.get_agent_states(
  "my_new_agent", # The agent id
  1478894153, # Optional, the **start** timestamp from which the
              # operations are retrieved (inclusive bound)
  1478895266, # Optional, the **end** timestamp up to which the
              # operations are retrieved (inclusive bound)
)
```

### Decision tree

Decision trees are computed at specific timestamps, directly by **craft ai** which learns from the context operations [added](#add-operations) throughout time.

When you [compute](#compute) a decision tree, **craft ai** returns an object containing:

- the **API version**
- the agent's configuration as specified during the agent's [creation](#create-agent)
- the tree itself as a JSON object:

  - Internal nodes are represented by a `"decision_rule"` object and a `"children"` array. The first one, contains the `"property`, and the `"property"`'s value, to decide which child matches a context.
  - Leaves have a `"predicted_value"`, `"confidence"` and `"decision_rule"` object for this value, instead of a `"children"` array. `"predicted_value`" is an estimation of the output in the contexts matching the node. `"confidence"` is a number between 0 and 1 that indicates how confident **craft ai** is that the output is a reliable prediction. When the output is a numerical type, leaves also have a `"standard_deviation"` that indicates a margin of error around the `"predicted_value"`.
  - The root only contains a `"children"` array.

#### Compute

```python
client.get_agent_decision_tree(
  "my_new_agent", # The agent id
  1469473600 # Optional the timestamp at which we want the decision
             # tree, default behavior is to return the decision tree
             # from the latest timestamp in context operations
)
```

#### Make decision

> :information_source: To make a decision, first compute the decision tree then use the **offline interpreter**.

### Bulk

The craft ai API includes a bulk route which provides a programmatic option to perform asynchronous operations on agents. It allows the user to create, delete, add operations and compute decision trees for several agents at once.

> :warning: the bulk API is a quite advanced feature. It comes on top of the basic routes to create, delete, add context operations and compute decision tree. If messages are not self-explanatory, please refer to the basic routes that does the same operation for a single agent.



#### Bulk - Create agents

To create several agents at once, use the method `create_agents_bulk` as the following:

```python
agent_id_1 = 'my_first_agent'
agent_id_2 = 'my_second_agent'

configuration_1 = {
  "context": {
    "peopleCount": {
      "type": "continuous"
    },
    "timeOfDay": {
      "type": "time_of_day"
    },
    "timezone": {
      "type": "timezone"
    },
    "lightbulbState": {
      "type": "enum"
    }
  },
  "output": ["lightbulbState"]
}
configuration_2 = { ... }

creation_bulk_payload = [
  {'id': agent_id_1, 'configuration': configuration_1},
  {'id': agent_id_2, 'configuration': configuration_2}
]

created_agents = client.create_agents_bulk(creation_bulk_payload)
print(created_agents)
```

The variable `created_agents` is an **array of responses**. If an agent has been successfully created, the corresponding response is an object similar to the classic `create_agent()` response. When there are **mixed results**, `created_agents` should looks like:

```python
[
  {'_version': '2.0.0',                                 # creation succeeded
   'configuration': {
      'context': {
        ...
      },
      'output': ...,
      'learning_period': 1500000,
      'time_quantum': 100
   },
   'id': 'my_first_agent'},
  {'error': CraftAiBadRequestError('error-message'),    # creation failed
   'id': 'my_second_agent'
  }
]
```

#### Bulk - Delete agents

To delete several agents at once, use the method `delete_agents_bulk` as the following:

```python
agent_id_1 = 'my_first_agent'
agent_id_2 = 'my_second_agent'

deletion_bulk_payload = [
  {'id': agent_id_1},
  {'id': agent_id_2}
]

deleted_agents = client.delete_agents_bulk(creation_bulk_payload)
print(agents_deleted)
```

The variable `deleted_agents` is an **array of responses**. If an agent has been successfully deleted, the corresponding response is an object similar to the classic `delete_agent()` response. When there are **mixed results**, `deleted_agents` should looks like:

```python
[
  {'id': 'my_first_agent',                              # deletion succeeded
   'creationDate': 1557492944277,
   'lastContextUpdate': 1557492944277,
   'lastTreeUpdate': 1557492944277,
   'configuration': {
      'context': {
        ...
      },
      'output': ...,
      'learning_period': 1500000,
      'time_quantum': 100
   },
   '_version': '2.0.0'
  },
  {'error': CraftAiBadRequestError('error-message'),    # deletion failed
   'id': 'my_second_agent'
  },
  {'id': 'my_unknown_agent'}                            # deletion succeeded
]
```

#### Bulk - Add context Operations

To add operations to several agents at once, use the method `add_agents_operations_bulk` as the following:

```python
agent_id_1 = 'my_first_agent'
agent_id_2 = 'my_second_agent'

operations_agent_1 = [
  {
    'timestamp': 1469410200,
    'context': {
      'timezone': '+02:00',
      'peopleCount': 0,
      'lightbulbState': 'OFF'
    }
  },
  {
    'timestamp': 1469410200,
    'context': {
      'timezone': '+02:00',
      'peopleCount': 1,
      'lightbulbState': 'ON'
    }
  },
  {
    'timestamp': 1469410200,
    'context': {
      'timezone': '+02:00',
      'peopleCount': 2,
      'lightbulbState': 'ON'
    }
  },
  {
    'timestamp': 1469410200,
    'context': {
      'timezone': '+02:00',
      'peopleCount': 2,
      'lightbulbState': 'OFF'
    }
  }
]
operations_agent_2 = [ ... ]

addition_operations_bulk_payload = [
  {'id': agent_id_1, 'operations': operations_agent_1},
  {'id': agent_id_2, 'operations': operations_agent_2}
]

agents = client.addAgentContextOperationsBulk(addition_operations_bulk_payload)
```
The variable `agents` is an **array of responses**. If an agent has successfully received operations, the corresponding response is an object similar to the classic `add_agent_operations()` response. When there are **mixed results**, `agents` should looks like:

```python
[
  {
    'status': 201,                                # Addition of operation succeeded
    'message': 'message',
    'id': 'my_first_agent'
  }
  {
    'status': 500,                                 # Addition of operation failed
    'error': CraftAiBadRequestError('error_message'),
    'id': 'my_second_agent'
  }
]
```

#### Bulk - Compute agents' decision trees

To get the tree of several agents at once, use the method `get_agents_decision_trees_bulk` as the following:

```python
agent_id_1 = 'my_first_agent'
agent_id_2 = 'my_second_agent'

decision_tree_bulk_payload =  [
  {'id': agent_id_1},
  {'id': agent_id_2}
]

trees = client.get_agents_decision_trees_bulk(decision_tree_bulk_payload)
```
The variable `trees` is an **array of responses**. If an agent’s model has successfully been created, the corresponding response is an object similar to the classic `get_agents_decision_trees_bulk()` response. When there are **mixed results**, trees should looks like:

```python
[
  {'id': 'my_first_agent',                              # Getting of the tree succeeded
   'tree': {
     'trees': { ... }
     '_version': '1.1.0',
     'configuration': { ... }
   }
   'timestamp': 1458741735
   },
   {
   'error': CraftAiBadRequestError('error_message'),  # Getting of the tree failed
   'id': 'my_second_agent'
   }
   {
   'error': CraftAiNotFoundError('error_message'),    # Getting of the tree failed
   'id': 'my_unknown_agent'
   }
]
```

#### Bulk - Create generators



#### Bulk - Delete generators



#### Bulk - Compute generators' decision trees



### Advanced client configuration ###

The simple configuration to create the `client` is just the token. For special needs, additional advanced configuration can be provided.

#### Amount of operations sent in one chunk ####

`client.add_agent_operations` splits the provided operations into chunks in order to limit the size of the http requests to the craft ai API. In the client configuration, `operationsChunksSize` can be increased in order to limit the number of request, or decreased when large http requests cause errors.

```python
client = craft_ai.Client({
    # Mandatory, the token
    "token": "{token}",
    # Optional, default value is 200
    "operationsChunksSize": {max_number_of_operations_sent_at_once}
})
```

#### Timeout duration for decision trees retrieval ####

It is possible to increase or decrease the timeout duration of `client.get_agent_decision_tree`, for exemple to account for especially long computations.

```python
client = craft_ai.Client({
    # Mandatory, the token
    "token": "{token}",
    # Optional, default value is 600000 (10 minutes)
    "decisionTreeRetrievalTimeout": "{timeout_duration_for_decision_trees_retrieval}"
})
```

#### Proxy ####

It is possible to provide proxy configuration in the `proxy` property of the client configuration. It will be used to call the craft ai API (through HTTPS). The expected format is a host name or IP and port, optionally preceded by credentials such as `http://user:pass@10.10.1.10:1080`.

```python
client = craft_ai.Client({
    # Mandatory, the token
    "token": "{token}",
    # Optional, no default value
    "proxy": "http://{user}:{password}@{host_or_ip}:{port}"
})
```

#### Advanced network configuration ####

For more advanced network configuration, it is possible to access the [Requests Session](http://docs.python-requests.org/en/master/user/advanced/#session-objects) used by the client to send requests to the craft ai API, through `client._requests_session`.

```python
# Disable SSL certificate verification
client._requests_session.verify = False
```
## Interpreter ##

The decision tree interpreter can be used offline from decisions tree computed through the API.

### Make decision ###

Note that the python interpreter takes an array of contexts.

```python
tree = { ... } # Decision tree as retrieved through the craft ai REST API

# Compute the decision on a fully described context
decision = craft_ai.Interpreter.decide(
  tree,
  [{ # The context on which the decision is made
    "timezone": "+02:00",
    "timeOfDay": 7.5,
    "peopleCount": 3
  }]
)

# Or Compute the decision on a context created from the given one and filling the
# `day_of_week`, `time_of_day` and `timezone` properties from the given `Time`

decision = craft_ai.Interpreter.decide(
  tree,
  [{
    "timezone": "+02:00",
    "peopleCount": 3
  },
  craft_ai.Time("2010-01-01T07:30:30+0200")
  ]
)
```

A computed `decision` on an `enum` output type would look like:

```python
{
  "context": { # In which context the decision was made
    "timezone": "+02:00",
    "timeOfDay": 7.5,
    "peopleCount": 3
  },
  "output": { # The decision itself
    "lightbulbState": {
      "predicted_value": "ON"
      "confidence": 0.9937745256361138, # The confidence in the decision
      "decision_rules": [ # The ordered list of decision_rules that were validated to reach this decision
        {
          "property": "timeOfDay",
          "operator": ">=",
          "operand": 6
        },
        {
          "property": "peopleCount",
          "operator": ">=",
          "operand": 2
        }
      ],
      "nb_samples": 25,
      "distribution": [0.05, 0.95],
      "decision_path" "0-1-1"
    },
  }
}
```

A `decision` for a numerical output type would look like:

```python
  "output": {
    "lightbulbIntensity": {
      "predicted_value": 10.5,
      "standard_deviation": 1.25, # For numerical types, this field is returned in decisions.
      "min": 8.0,
      "max": 11,
      "nb_samples": 25,
      "decision_rules": [ ... ],
      "confidence": ...,
      "decision_path" ...
    }
  }
```

A `decision` for a categorical output type would look like:

```python
  "output": {
    "lightbulbState": {
      "predicted_value": "OFF",
      "nb_samples": 25,
      "distribution" : [ ... ], # Distribution of the output classes normalized by the number of samples in the reached node.
      "decision_rules": [ ... ],
      "confidence": ...,
      "decision_path" ...
    }
  }
```

A `decision` in a case where the tree cannot make a prediction:

```python
  "output": {
    "lightbulbState": {
      "predicted_value": None,
      "distribution" : [ ... ], # Distribution of the output classes normalized by the number of samples in the reached node.
      "confidence": 0, # Zero confidence if the decision is null
      "decision_rules": [ ... ],
      "decision_path" ...
    }
  }
```

### Reduce decision rules ###

From a list of decision rules, as retrieved when taking a decision, when taking a decision compute an equivalent & minimal list of rules.

```python
from craft_ai import reduce_decision_rules

# `decision` is the decision tree as retrieved from taking a decision
decision = craft_ai.Interpreter.decide( ... )

# `decision_rules` is the decision rules that led to decision for the `lightBulbState` value
decision_rules = decision["output"]["lightBulbState"]["decision_rules"]

# `minimal_decision_rules` has the mininum list of rules strictly equivalent to `decision_rules`
minimal_decision_rules = reduce_decision_rules(decisionRules)
```

### Format decision rules ###

From a list of decision rules, compute a _human readable_ version of these rules, in english.

```python
from craft_ai import format_decision_rules

# `decision` is the decision tree as retrieved from taking a decision
decision = craft_ai.Interpreter.decide( ... )

# `decision_rules` is the decision rules that led to decision for the `lightBulbState` value
decision_rules = decision["output"]["lightbulbState"]["decision_rules"]

# `decision_rules_str` is a human readable string representation of the rules.
decision_rules_str = format_decision_rules(decision_rules)
```

## Error Handling ##

When using this client, you should be careful wrapping calls to the API with `try/except` blocks, in accordance with the [EAFP](https://docs.python.org/3/glossary.html#term-eafp) principle.

The **craft ai** python client has its specific exception types, all of them inheriting from the `CraftAIError` type.

All methods which have to send an http request (all of them except `decide`) may raise either of these exceptions: `CraftAINotFoundError`, `CraftAIBadRequestError`, `CraftAICredentialsError` or `CraftAIUnknownError`.

The `decide` method only raises `CrafAIDecisionError` of `CraftAiNullDecisionError` type of exceptions. The latter is raised when no the given context is valid but no decision can be made.

## Pandas support ##

The craft ai python client optionally supports [pandas](http://pandas.pydata.org/) a very popular library used for all things data.

You'll need to install `craft-ai` with its `pandas` [extra](https://packaging.python.org/tutorials/installing-packages/#installing-setuptools-extras)

```sh
pip install --upgrade craft-ai[pandas]
```

Then, instead of importing the default module, do the following

```python
import craft_ai.pandas

# Most of the time you'll need the following
import numpy as np
import pandas as pd

# Client must then be defined using craft_ai.pandas module
client = craft_ai.pandas.Client({
  "token": "{token}"
})
```

The craft ai pandas module is derived for the _vanilla_ one, with the following methods are overriden to support pandas' [`DataFrame`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

#### `craft_ai.pandas.Client.get_agent_operations` #####

Retrieves the desired operations as a `DataFrame` where:

- each operation is a row,
- each context property is a column,
- the index is [_time based_](https://pandas.pydata.org/pandas-docs/stable/timeseries.html), [timezone-aware](https://pandas.pydata.org/pandas-docs/stable/timeseries.html#working-with-time-zones) and matching the operations timestamps,
- `np.NaN` means no value were given at this property for this timestamp.

```python
df = client.get_agent_operations("my_new_agent")

# `df` is a pd.DataFrame looking like
#
#                            peopleCount  lightbulbState   timezone
# 2013-01-01 00:00:00+00:00   0            OFF              +02:00
# 2013-01-02 00:00:00+00:00   1            ON               NaN
# 2013-01-03 00:00:00+00:00   2            NaN              NaN
# 2013-01-04 00:00:00+00:00   NaN          OFF              NaN
# 2013-01-05 00:00:00+00:00   0            NaN              NaN
```

#### `craft_ai.pandas.Client.add_agent_operations` #####

Add a `DataFrame` of operations to the desired agent. The format is the same as above.

```python
df = pd.DataFrame(
  [
    [0, "OFF", "+02:00"],
    [1, "ON", np.nan], # timezone will be "+02:00"
    [2, np.nan, np.nan],
    [np.nan, "OFF", np.nan],
    [0, np.nan, np.nan]
  ],
  columns=['peopleCount', 'lightbulbState', 'timezone'],
  index=pd.date_range('20130101', periods=5, freq='D').tz_localize("UTC")
)
client.add_agent_operations("my_new_agent", df)
```

Given an object that is not a `DataFrame` this method behave like the _vanilla_ `craft_ai.Client.add_agent_operations`.

Furthermore, missing values and optional values can be handled by the craft ai pandas client. To do so, we introduce two new types that are `craft_ai.pandas.MISSING_VALUE` for [missing values](#missing-values) and `craft_ai.pandas.OPTIONAL_VALUE` for [optional values](#optional-values).
To send your `DataFrame` with actual missing values or optional values, you must use one of these types:

```python
from craft_ai.pandas import MISSING_VALUE, OPTIONAL_VALUE

df = pd.DataFrame(
  [
    [0, "+02:00"],
    [1, MISSING_VALUE],
    [2, MISSING_VALUE],
    [1, OPTIONAL_VALUE],
    [0, np.nan]
  ],
  columns=['peopleCount', 'timezone'],
  index=pd.date_range('20130101', periods=5, freq='D').tz_localize("UTC")
)
client.add_agent_operations("my_new_agent", df)
```

To ensure that all the missing values contained in your `DataFrame` are to the right format and can be handled by the craft ai pandas client, it is suggested to preprocess this latter by replacing all `na` values by the desired one:

```python
contexts_df.fillna(MISSING_VALUE) # Or OPTIONAL_VALUE
```

#### `craft_ai.pandas.Client.get_agent_states` #####

Retrieves the desired state history as a `DataFrame` where:

- each state is a row,
- each context property is a column,
- the index is [_time based_](https://pandas.pydata.org/pandas-docs/stable/timeseries.html), [timezone-aware](https://pandas.pydata.org/pandas-docs/stable/timeseries.html#working-with-time-zones) and matching the operations timestamps.

```python
df = client.get_agent_states("my_new_agent")

# `df` is a pd.DataFrame looking like
#
#                            peopleCount  lightbulbState   timezone
# 2013-01-01 00:00:00+00:00   0            OFF              +02:00
# 2013-01-02 00:00:00+00:00   1            ON               +02:00
# 2013-01-03 00:00:00+00:00   2            ON               +02:00
# 2013-01-04 00:00:00+00:00   2            OFF              +02:00
# 2013-01-05 00:00:00+00:00   0            OFF              +02:00
```

#### `craft_ai.pandas.Client.decide_from_contexts_df` #####

Make multiple decisions on a given `DataFrame` following the same format as above.

```python
decisions_df = client.decide_from_contexts_df(tree, pd.DataFrame(
  [
    [0, "+02:00"],
    [1, "+02:00"],
    [2, "+02:00"],
    [1, "+02:00"],
    [0, "+02:00"]
  ],
  columns=['peopleCount', 'timezone'],
  index=pd.date_range('20130101', periods=5, freq='D').tz_localize("UTC")
))
# `decisions_df` is a pd.DataFrame looking like
#
#                            lightbulbState_predicted_value   lightbulbState_confidence  ...
# 2013-01-01 00:00:00+00:00   OFF                              0.999449                  ...
# 2013-01-02 00:00:00+00:00   ON                               0.970325                  ...
# 2013-01-03 00:00:00+00:00   ON                               0.970325                  ...
# 2013-01-04 00:00:00+00:00   ON                               0.970325                  ...
# 2013-01-05 00:00:00+00:00   OFF                              0.999449                  ...
```

This function also accepts craft ai missing values and optional values types, `craft_ai.pandas.MISSING_VALUE` and `craft_ai.pandas.OPTIONAL_VALUE`.

```python
from craft_ai.pandas import MISSING_VALUE, OPTIONAL_VALUE

decisions_df = client.decide_from_contexts_df(tree, pd.DataFrame(
  [
    [0, "+02:00"],
    [MISSING_VALUE, "+02:00"],
    [2, "+02:00"],
    [MISSING_VALUE, "+02:00"],
    [0, "+02:00"]
  ],
  columns=['peopleCount', 'timezone'],
  index=pd.date_range('20130101', periods=5, freq='D').tz_localize("UTC")
))
```

This function never raises `CraftAiNullDecisionError`, instead it inserts these errors in the result `Dataframe` in a specific `error` column.

#### `craft_ai.pandas.utils.create_tree_html` #####

Returns a HTML version of the given decision tree. If this latter is saved in a `.html` file, it can be opened in
a browser to be visualized.

```python

from  craft_ai.pandas.utils import create_tree_html

tree = client.get_agent_decision_tree(
  "my_agent", # The agent id
  timestamp # The timestamp at which the decision tree is retrieved
)

html = create_tree_html(
  tree, # The decision tree
  decision_path, # (Optional) The path to a node. This will plot the tree with this node already selected. Default: ""
  edge_type, # (Optional) The way the decision tree edges are plotted - ("constant", "absolute" or "relative"). Default: "constant"
  folded_nodes, # (Optional) An array of nodes path to fold when the tree is plotted. Default: None
  height # (Optional) The height in pixel of the created plot. Default: 500.
)

# ...
# ... save the html string to visualize it in a browser
# ...
```

#### `craft_ai.pandas.utils.display_tree` #####

Display a decision tree in a Jupyter Notebook.
This function can be useful for analyzing the induced decision trees.

```python

from  craft_ai.pandas.utils import display_tree

tree = client.get_agent_decision_tree(
  "my_agent", # The agent id
  timestamp # The timestamp at which the decision tree is retrieved
)

display_tree(
  tree, # The decision tree
  decision_path, # (Optional) The path to a node. This will plot the tree with this node already selected. Default: ""
  edge_type, # (Optional) The way the decision tree edges are plotted - ("constant", "absolute" or "relative"). Default: "constant"
  folded_nodes, # (Optional) An array of nodes path to fold when the tree is plotted. Default: None
  height # (Optional) The height in pixel of the created plot. Default: 500.
)
```

#### `craft_ai.pandas.client.add_agents_operations_bulk` #####

Add operations to several agents at once.
```python
agent_id_1 = 'my_first_agent'
agent_id_2 = 'my_second_agent'

operations_agent_1 = pd.DataFrame(
  [
    [0, "OFF", "+02:00"],
    [1, "ON", np.nan], # timezone will be "+02:00"
    [2, np.nan, np.nan],
    [np.nan, "OFF", np.nan],
    [0, np.nan, np.nan]
  ],
  columns=['peopleCount', 'lightbulbState', 'timezone'],
  index=pd.date_range('20130101', periods=5, freq='D').tz_localize("UTC")
)
operations_agent_2 = pd.DataFrame([...])

addition_operations_bulk_payload = [
    {'id': agent_id_1, 'operations': operations_agent_1},
    {'id': agent_id_2, 'operations': operations_agent_2}
]

client.add_agents_operations_bulk(addition_operations_bulk_payload)
```
Given an object that is not a `DataFrame` this method behave like the _vanilla_ `craft_ai.Client.add_agents_operations_bulk`.
