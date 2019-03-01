import unittest

import craftai

from . import settings
from .data import valid_data, invalid_data


# TODO : add a function that delete a lot od agents
# TODO 2 : add the case of absence of a field
NB_AGENTS_TO_DELETE = 100

class TestDeleteAgentWithValidID(unittest.TestCase):
  """Checks that the client succeeds when deleting an agent with OK input"""
  @classmethod
  def setUpClass(cls):
    cls.client = craftai.Client(settings.CRAFT_CFG)
    cls.agent_id = valid_data.VALID_ID  + "_" + settings.RUN_ID

  def setUp(self):
    # Creating an agent may raise an error if one with the same ID
    # already exists. Although it shouldn' matter for the deletion test,
    # it is necessary to catch this kind of errors.
    try:
      self.client.create_agent(valid_data.VALID_CONFIGURATION, self.agent_id)
    except craftai.errors.CraftAiBadRequestError as e:
      if "one already exists" not in e.message:
        raise e

  def test_delete_agent_with_valid_id(self):
    resp = self.client.delete_agent(self.agent_id)
    self.assertIsInstance(resp, dict)
    self.assertTrue("id" in resp.keys())

class TestDeleteAgentWithUnknownID(unittest.TestCase):
  """Checks that the client succeeds when deleting an agent which
  doesn't exist"""

  @classmethod
  def setUpClass(cls):
    cls.client = craftai.Client(settings.CRAFT_CFG)
    cls.agent_id = valid_data.VALID_ID  + "_" + settings.RUN_ID

  def test_delete_agent_with_unknown_id(self):
    """delete_agent should succeed when given a non-string/empty string ID

    It should return a json with just a message upon request for
    deletion of an agent with an ID that is not of type string,
    since agent IDs should always be strings.
    """

    # Calling delete twice to make sure the ID doesn't exist
    # Since it's the function we are testing, it wouldn't be clean
    # to do this in the setUp phase.
    self.client.delete_agent(self.agent_id)
    resp = self.client.delete_agent(self.agent_id)
    self.assertIsInstance(resp, dict)
    self.assertTrue("message" in resp.keys())


class TestDeleteAgentWithInvalidID(unittest.TestCase):
  """Checks that the client fails when trying to delete an invalid agent"""
  @classmethod
  def setUpClass(cls):
    cls.client = craftai.Client(settings.CRAFT_CFG)

  def setUp(self):
    self.client = craftai.Client(settings.CRAFT_CFG)

  def test_delete_agent_with_invalid_id(self):
    """delete_agent should fail when given a non-string/empty string ID

    It should raise an error upon request for deletion of
    an agent with an ID that is not of type string, since agent IDs
    should always be strings.
    """

    for empty_id in invalid_data.UNDEFINED_KEY:
      self.assertRaises(
        craftai.errors.CraftAiBadRequestError,
        self.client.delete_agent,
        invalid_data.UNDEFINED_KEY[empty_id])
