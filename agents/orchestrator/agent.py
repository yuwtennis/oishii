import json
import sys
from typing import AsyncGenerator

from google.adk import Event
from google.adk.agents import BaseAgent, InvocationContext, LoopAgent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.events import EventActions

from oishii.entities import UserDemographic, NutritionistFeedback
from oishii.logging import OishiiLogger
from oishii.values import AgentType, MenuStatus

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

logger = OishiiLogger(name='menu_concierge')

def create_save_output_callback(key: AgentType):
    """Creates a callback to save the agent's final response to session state."""
    def callback(ctx: CallbackContext):
        for event in reversed(ctx.session.events):
            if event.author == ctx.agent_name and event.content and event.content.parts:
                if key == AgentType.NUTRITIONIST:
                    try:
                        ctx.state[key.value] = json.loads(event.content.parts[0].text)
                    except json.JSONDecodeError:
                        ctx.state[key.value] = event.content.parts[0].text
                else:
                    ctx.state[key.value] = event.content.parts[0].text
                print(f"Agent {ctx.agent_name} Saving {key.value} output to state. ")
                return
    return callback


class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(
            self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        logger.logger.info(f"Checking status and escalating if needed. State: {ctx.session.state}")
        status: NutritionistFeedback = NutritionistFeedback.model_validate(ctx.session.state[AgentType.NUTRITIONIST.value])

        # This will be future use
        # If any of the feedbacks includes HEALTHY then continue otherwise
        should_stop = (
                len([s.status for s in status.feedbacks if s.status == MenuStatus.HEALTHY.value]) == 0
        )

        yield Event(
            author=self.name,
            actions=EventActions(escalate=should_stop)
        )


concierge_agent = RemoteA2aAgent(
    name='concierge',
    agent_card=(
        f'http://localhost:8001/{AGENT_CARD_WELL_KNOWN_PATH}'
    ),
    after_agent_callback=create_save_output_callback(AgentType.CONCIERGE),
)

nutrition_agent = RemoteA2aAgent(
    name='nutritionist',
    agent_card=(
        f'http://localhost:8002/{AGENT_CARD_WELL_KNOWN_PATH}'
    ),
    after_agent_callback=create_save_output_callback(AgentType.NUTRITIONIST),
    input_schema=UserDemographic,
)

root_agent = LoopAgent(
    name='refinement_loop',
    description='Refines the agent output',
    max_iterations=1,
    sub_agents=[
        concierge_agent,
        nutrition_agent,
        CheckStatusAndEscalate(
            name='check_status_and_escalate',
        )],
)
