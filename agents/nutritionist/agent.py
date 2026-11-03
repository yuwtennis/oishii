import logging
import os
import sys

from google.adk.agents.llm_agent import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from oishii.entities import NutritionistFeedback


MODEL = 'gemini-3.5-flash'
# TODO write prompt
PROMPT_TEMPLATE = """
Review the menu proposed by the concierge using {concierge_guide} and provide feedbacks on the nutritional values.
Assume the user is a {UserDemographic.gender} and {UserDemographic.age} years old.
You will evaluate the menu in following steps:

1. You will diagnose the menu and estimate the nutritional values included in the menu. If the menu is not an estimatable menu, return status='error'
2. You will test the nutrition and ensure it is within recommended dietary allowances (RDA) provided by Ministry of Health, 
Labour and Welfare of Japan. RDA is based on daily basis so you will divide it by three and take the average for threshold of single meal.


If the tests are passed return status='healthy', otherwise  status='unhealthy'.
In both status, make sure to set feedbacks to a brief expression of result of the test.
If multiple menus are evaluated make sure to evaluate them all.
"""

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'TRUE'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'elite-caster-125113'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'asia-northeast1'

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

logging.getLogger("google_adk").setLevel(logging.DEBUG)

root_agent = LlmAgent(
    model=MODEL,
    name='nutritionist',
    description='Safeguards the health of the dish by validating the ingredients and nutritional values',
    instruction='Answer user questions to the best of your knowledge',
    output_schema=NutritionistFeedback,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)

a2a_app = to_a2a(root_agent, port=8002)