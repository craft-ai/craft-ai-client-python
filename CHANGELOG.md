# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/craft-ai/craft-ai-client-python/compare/v2.1.1...HEAD) ##

## [2.1.1](https://github.com/craft-ai/craft-ai-client-python/compare/v2.1.0...v2.1.1) - 2021-02-25 ##

### Changed

- Move CI to github action
### Fixed

- Empty dataframe on add_agent_context_operation and decide will advise you to use the pandas client.
- Empty payload now throw a proper error.
- Fix bug on timezone when operations are added with bulk API
- Fix bug on missing values when operations are added with bulk API
- Fix test using bad formated configuration
- Add catch around cleanups in tests
- Fix return value of add_agents_operations_bulk when valid and invalid agent's id given.
- Fix reference to travis in docs.

## [2.1.0](https://github.com/craft-ai/craft-ai-client-python/compare/v2.0.0...v2.1.0) - 2020-10-26 ##

### Added

- Add a test in the pandas client to check the error message when deciding based on a tree from no samples.
- Add support for generators bulk in the `client`: `create_generators_bulk`, `delete_generators_bulk`, `get_generators_decision_trees_bulk`.

### Fixed

- Boolean outputs are properly supported.
- A specific error is now raised for a tree based on no context operations.
- Re-enable the creation of agent with configuration test.
- Print the error when one of the linter failed.
- Remove .pylintrc file
- Fix the `add_agent_operations` message to display the number of added operations.
- Delete `is_optional` because it is now deployed everywhere.
- Fix the `semver` deprecated syntax.
- Fix tests that could let dangling agents in test projects.
- Fix deployment script.

### Changed

- Remove the dependency on the `IPython` library from the pandas client.

## [2.0.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.16.0...v2.0.0) - 2020-03-18 ##

> :warning: craft-ai-client-python v2.0.0 drop support for python v2.
>
> If you are still using python v2, consider migrating to v3 as python v2 is [no longer supported since January 2020](https://www.python.org/doc/sunset-python-2/).
> You can still use craft-ai-client-python v1.X for the time being.

### Changed

- Root package renamed `craft_ai` (previously `craftai`) to follow python naming conventions.
- `craft_ai.pandas` now requires `pandas` v1.0.1 or compatible versions.
- Rename several functions to make them more unique and well defined:
  - `craft_ai.add_operations` becomes `craft_ai.add_agent_operations`,
  - `craft_ai.add_operations_bulk` becomes `craft_ai.add_agents_operations_bulk`,
  - `craft_ai.get_operations_list` becomes `craft_ai.get_agent_operations`,
  - `craft_ai.get_generator_operations_list` becomes `craft_ai.get_generator_operations`,
  - `craft_ai.get_state_history` becomes `craft_ai.get_agent_states`,
  - `craft_ai.get_decision_tree` becomes `craft_ai.get_agent_decision_tree`,
  - `craft_ai.get_decision_trees_bulk` becomes `craft_ai.get_agents_decision_trees_bulk`.
- Tree traversal utils have been reorganized:
  - Introducing `craft_ai.extract_output_tree` able to extract output decision tree, was previously a private function called `craft_ai.pandas._extract_tree`,
  - Renaming `craft_ai.pandas.get_paths` to `craft_ai.extract_decision_paths_from_tree`,
  - Renaming `craft_ai.pandas.get_neighbours` to `craft_ai.extract_decision_path_neighbors`.
- Operations addition functions now also returns the number of added operations as `"added_operations_count"`.

### Removed

- Remove support for python v2, now supporting v3.6.1 and later.
- Remove support for `CraftAIClient` import.

### Fixed

- Messages returned when adding operations now correctly reflects the operations merging that can occur server-side.

## [1.16.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.8...v1.16.0) - 2020-02-21 ##

### Added

- Add support for generators with the new `client` methods `create_generator`, `get_generator`, `list_generators`, `delete_generator`, `get_generator_decision_tree` and `get_generator_operations_list`.
- Support for Python version 3.7

### Fixed

- `craftai.pandas.client.decide_from_contexts_df` can use every possible feature name.
- Rollback `craftai.client` to raise errors for responses with `202` status code.

## [1.15.8](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.7...v1.15.8) - 2019-11-19 ##

### Changed

- Delete `deactivate_missing_values` flag in the configuration.

## [1.15.7](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.6...v1.15.7) - 2019-10-29 ##

### Fixed

- `craftai.decide` properly returns result information when the `standard_deviation` is `0`.

### Changed

- `client.decide` now always computes the distributed decision when no matching nodes are found.

## [1.15.6](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.5...v1.15.6) - 2019-09-19 ##

### Added

- `craftai.pandas.utils.get_paths` to list all paths of a craftai tree.
- `craftai.pandas.utils.get_neighbours` to list all neighbours paths of a given decision path.

## [1.15.5](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.4...v1.15.5) - 2019-09-05 ##

### Added

- `craftai.pandas.utils.display_tree` supports `edge_type` property that can take `constant`, `relative` or `absolute` values.

## [1.15.4](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.3...v1.15.4) - 2019-09-02 ##

### Added

- `craftai.pandas.utils.display_tree` has new inputs: `decision_path` to select a specific node via its path and `folded_nodes` to fold multiple nodes using their paths.

### Fixed

- `craftai.pandas.utils.display_tree` can be called multiple times in the same cell.

## [1.15.3](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.2...v1.15.3) - 2019-08-14 ##

### Added

- `client.decide` now returns the path to the reached node.

### Changed

- Improve `craftai.pandas.client.decide_from_contexts_df` performances.
- `craftai.pandas.client.add_operations` has now the same behavior than `craftai.pandas.client.decide_from_contexts_df`. If there is no timezone column, the function use the timezone of the index (`pandas.DateTimeIndex`).
- The client retrieves V2 trees by default.
- `craftai.get_decision_tree` accepts pd.Timestamp and datetime.datetime now

### Fixed

- `craftai.pandas.utils.display_tree` now works on Firefox.

## [1.15.2](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.1...v1.15.2) - 2019-07-03

## [1.15.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.15.0...v1.15.1) - 2019-07-03

### Added

- Predictions now return min and max information for continuous output values.
- For continuous output values, it is now possible to get the mean and standard deviation values from any node in a tree.
- `craftai.pandas` can now fully use missing values and optional values features.

### Fixed

- `craftai.pandas.decide_from_contexts_df` can take decisions on contexts with the same timestamp.

## [1.15.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.14.1...v1.15.0) - 2019-02-25

### Added

- Support timezones as UTC offset in minutes.
- Ready for the upcoming decision trees v2, including the following.
  - **Missing values**: it is now possible to handle missing values by adding `deactivate_missing_values: false` in the agent configuration. Missing values correspond to a `null` value in a given context.
  - **Optional values**: it is now possible to handle optional values by adding `is_optional: true` for a property in the agent configuration. Optional values are defined by `{}`, the empty Object, in a given context.
  - **Multi-enum operator** `in`.
  - **Boolean** property type.
  - Predictions now return the number of samples in the leaf and its distribution if it is a classification problem.

### Changed

- Relaxing the constraints on the libraries dependencies.

## [1.14.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.14.0...v1.14.1) - 2018-11-28

### Changed

- Getting rid of the `.rst` readme.

## [1.14.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.13.0...v1.14.0) - 2018-11-27

### Added

- The parameter `timestamp` is now optional in the method `client.get_decision_tree`. The default behaviour is to return the decision tree from the latest timestamp in the context operations

- Add a function to plot a decision tree in a Jupyter cell (available through `from craftai.pandas.utils import display_tree`) which returns a function to launch in order to display the tree and its corresponding html.

## [1.13.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.12.0...v1.13.0) - 2018-08-09

### Added

- It is now possible to provide a `datetime` object as timestamp with a timezone to create a `Time`: `Time(t=datetime(2011, 1, 1, 0, 0), timezone="+02:00")`.
- It is now possible to provide an ISO string date as timestamp with a timezone to create a `Time`: `Time(t="2017-01-01 03:00:00", timezone="+02:00")`.

### Fixed

- Fix unreachable server error.

## [1.12.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.11.0...v1.12.0) - 2018-04-25

### Added

- Introducing `reduce_decision_rules` (available through `from craftai import reduce_decision_rules`) a function that reduces a list of decision rules to a single rule per property.
- Introducing `format_property`, `format_decision_rules` (available through `from craftai import format_property, format_decision_rule, format_decision_rules`) respectively able to nicely format a property value, or several decision rules into a human readable string.
- It is now possible to add proxy settings in the client configuration.

## [1.11.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.10.0...v1.11.0) - 2018-04-13

### Changed

- It is no longer possible to compute a tree at a future timestamp, tests have been adapted to reflect that.
- tz-naive DatetimeIndex are no longer supported, from now it must be tz-aware.
- For learning (add_operations), you must provide a timezone column is order to generate features (time_of_day, ...).
- For decisions, you can provide a timezone column (multiple timezones supported). Otherwise, craft will use the datetimeindex tz.

### Fixed

- Fix an error occurring in the pandas client when the provided DataFrame included non-scalar values.
- The decoding of the craft ai JWT token is now resilient to spaces around the token string.
- Timezone are now used to generate features and to compute decisions.
- Fix a bug when the decisions_df was empty.

## [1.10.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.9.0...v1.10.0) - 2018-02-14

### Fixed

- `client.decide` now properly handles _advanced_ property types such as `periodic`.

## [1.9.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.8.0...v1.9.0) - 2017-11-06

### Added

- `client.get_decision_tree` now transparently retries computation up to the given `cfg.decisionTreeRetrievalTimeout`.

### Fixed

- `client.get_decision_tree` now properly returns timeout sent by the API as `errors.CraftAiLongRequestTimeOutError`.

## [1.8.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.7.1...v1.8.0) - 2017-10-24

### Added

- Support new format for timezone offsets: +/-hhmm, +/-hh and some abbreviations(CEST, PST, ...). Check the [documentation](https://beta.craft.ai/doc/http#context-properties-types) for the complete list.

## [1.7.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.7.0...v1.7.1) - 2017-10-13

### Added

- Add new function `client.get_state_history` retrieving a agent's state history. Take a look a the [documentation](https://beta.craft.ai/doc/python#retrieve-state-history) for further informations. This function is also available in the _pandas_ version.

### Fixed

- Fix the interpreter error messages to fit the [test suite](https://github.com/craft-ai/craft-ai-interpreter-test-suite) expectations.

## [1.7.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.6.0...v1.7.0) - 2017-10-13

## [1.6.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.5.0...v1.6.0) - 2017-08-22

### Added

- `client.get_operations_list` takes two new optional parameters defining time bounds for the desired operations.

### Changed

- `client.get_operations_list` handles the pagination automatically, making as many requests as necessary to the API.

## [1.5.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.4.1...v1.5.0) - 2017-08-02

### Added

- Finally adding a changelog file (yes this one).
- Adding a helper script to maintain the changelog.
- Checking agent name at the agent creation to prevent erroneous behavior with the api route.

## [1.4.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.4.0...v1.4.1) - 2017-07-19

### Changed

- The _pandas_ version of the decision operation no longer raises `CraftAiNullDecisionError`, it instead returns such errors in a specific column of the returned `DataFrame`.
- Now enforcing the usage of double-quotes in the code.

## [1.4.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.3.1...v1.4.0) - 2017-07-13

### Added

- The decision operation now raises a specific error, `CraftAiNullDecisionError`, when a tree can't predict any value for a given context.

## [1.3.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.3.0...v1.3.1) - 2017-07-10

### Fixed

- The distributed package now actually includes `craftai.pandas`.

## [1.3.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.2.3...v1.3.0) - 2017-07-09

### Added

- New specialized version of the library that understands [Pandas](https://pandas.pydata.org) `DataFrame`, this specialized version of the client can be imported as such: `import Client from craftai.pandas`.

### Changed

- Simplifying the import scheme, it is now possible to import the client class with `import Client from craftai`; the previous behavior still works.

## [1.2.3](https://github.com/craft-ai/craft-ai-client-python/compare/v1.2.2...v1.2.3) - 2017-06-06

### Fixed

- Deactivating some tests on agent creation failure to overcome a temporary regression on the API side.

## [1.2.2](https://github.com/craft-ai/craft-ai-client-python/compare/v1.2.1...v1.2.2) - 2017-06-06

### Fixed

- `client.add_operations` now returns a proper count of the added operations in every cases.

## [1.2.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.2.0...v1.2.1) - 2017-04-13

### Fixed

- The decision now properly takes into account that `day_of_week` belongs to [0,6] and not [1,7].

## [1.2.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.1.0...v1.2.0) - 2017-04-13

### Added

- Automated linting of the code using [pylint](https://www.pylint.org).
- Introducing a script to automatically update the version from `craftai/__init__.py`.
- Simplifying the build scripts using `make`.

## [1.1.0](https://github.com/craft-ai/craft-ai-client-python/compare/v1.0.1...v1.1.0) - 2017-04-04

### Added

- Client creation now extracts the right API url, the `owner` and the `project` from the given `token`.

### Changed

- Improve the `README.rst` generation to have a beautiful :lipstick: page on PyPI.
- Unifying the case of the error classes.

## [1.0.1](https://github.com/craft-ai/craft-ai-client-python/compare/v1.0.1...v1.0.0) - 2017-03-23

_no changes_

## 1.0.0 - 2017-03-22

- Initial **final** version of the Python client.
