import json
import pytest


@pytest.fixture
def concierge_eval_set():
    with open('tests/integration/fixtures/concierge/test_case.evalset.json') as f:
        yield json.load(f)