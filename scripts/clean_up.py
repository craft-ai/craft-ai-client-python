import craft_ai
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
CRAFT_CFG = {"token": os.environ.get("CRAFT_TOKEN")}
JOB_ID = os.environ.get("JOB_ID", "loc")

print("Cleaning dangling agents and generators from test session.")
craft_client = craft_ai.Client(CRAFT_CFG)
agents_list = craft_client.list_agents()
agents_to_delete = [
    agent_id for agent_id in agents_list if agent_id[-3:] == JOB_ID[-3:]
]
for agent_id in agents_to_delete:
    craft_client.delete_agent(agent_id)
generators_list = craft_client.list_generators()
generators_to_delete = [
    generator_id for generator_id in generators_list if generator_id[-3:] == JOB_ID[-3:]
]
for generator_id in generators_to_delete:
    craft_client.delete_generator(generator_id)
