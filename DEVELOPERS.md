# Developers instructions #

## Running the tests locally ##

1. Make sure you have the following installed:
  - [Python](https://www.python.org) (any version >3.5 should work),
  - [Poetry](https://python-poetry.org),
  - bash and sed (needed for the build scripts).
2. Create a test **craft ai** project and retrieve its **write token**.
3. At the root of your local clone, create a file named `.env` with the following content.

  ```
  CRAFT_TOKEN=<retrieved_token>
  ```

4. Init the git submodules (needed for the interpreter tests)
  ```console
  $ git submodule init
  $ git submodule update
  ```

5. Install the dependencies. For the following steps, you may want use in a Python virtual environment.

  ```console
  $ poetry install -E pandas
  ```

6. Run the coding style checks.

  ```console
  $ poetry run task lint
  ```

6. Run the tests!

  ```console
  $ poetry run task test
  ```

## Releasing a new version (needs administrator rights) ##

1. Make sure the build of the master branch is passing

  [![Build Status](https://github.com/craft-ai/craft-ai-client-python/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/craft-ai/craft-ai-client-python/actions)

2. Checkout the master branch locally.

  ```console
  $ git fetch
  $ git checkout master
  $ git reset --hard origin/master
  ```

3. Update `README.md` from **craft ai** documentation found
   at <https://beta.craft.ai/doc/python>.


  ```console
  $ ./scripts/update_readme.sh
  ```

  > This will create a git commit.


4. Increment the version in `craft_ai/__init__.py` and move _Unreleased_ section
   of `CHANGELOG.md` to a newly created section for this version.

  ```console
  $ ./scripts/update_version.sh patch
  ```

  `./scripts/update_version.sh minor` and `./scripts/update_version.sh major` are
  also available - see [semver](http://semver.org) for a guideline on when to
  use which.

  > This will create a git commit and a git tag.

5. Push everything!

  ```console
  $ git push origin master --tags
  ```

  > This will trigger the publishing of this new version to
  > [PyPI](https://pypi.python.org/pypi/craft-ai) by
  > [Github actions](https://github.com/craft-ai/craft-ai-client-python/actions)
