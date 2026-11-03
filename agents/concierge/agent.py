
import os
import sys
import logging

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import google_search

from oishii.logging import OishiiLogger

MODEL = 'gemini-3.5-flash'
PROMPT_TEMPLATE = """
You are a menu concierge. The user message contains a location and a request.
ALWAYS call the `check_location` tool first, with the location from the user's message.
- If it returns status='error', return an empty menu.
- If it returns status='success', recommend up to 5 menus that matches the request for that location.

You will refine the menu according to the feedbacks received by the nutritionist.
"""

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'TRUE'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'elite-caster-125113'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'asia-northeast1'

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

logger = OishiiLogger(name='menu_concierge')
logging.getLogger("google_adk").setLevel(logging.DEBUG)

def check_location(location: str) -> dict[str, str]:
    """
    Returns a dictionary with the status and report of the location check.

    :param str location: The location to check.
    :return: A dictionary with the status and report. If the location is not valid, the status is 'error' and the report is the error message. If the location is valid, the status is 'success' and the report is 'Location is valid.'.
    """
    logger.logger.info(f"Received location: {location}")

    if location != "":
        return {
            'status': 'success',
            'report': 'Location is valid.'
        }
    else:
        return {
            'status': 'error',
            'error_message': f"Location is not valid. {location}"
        }

root_agent = LlmAgent(
    model=MODEL,
    name='menu_concierge',
    description='A helpful concierge that recommends a menu based on the location and the request.',
    instruction=PROMPT_TEMPLATE,
    tools=[check_location],
)

logger.logger.info(f"Agent loaded: {root_agent.name}")

a2a_app = to_a2a(root_agent, port=8001)
