from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest
from google.adk.evaluation.eval_config import EvalConfig
from google.adk.evaluation.eval_set import EvalSet


@pytest.mark.asyncio
async def test_concierge_trajectory(concierge_eval_set):
    """ Test the concierge agent's trajectory."""
    config = EvalConfig(criteria={
            "tool_trajectory_avg_score": 1.0,
            "response_match_score": 0.5,
        })

    eval_set = EvalSet(**concierge_eval_set)

    await AgentEvaluator.evaluate_eval_set(
        agent_module='agents.concierge',
        eval_config=config,
        eval_set=eval_set,
    )
