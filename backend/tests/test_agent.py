from app.agents.growth_agent import GrowthAgent
def test_agent_returns_safe_empty_for_unknown_query():
    r=GrowthAgent().respond("unfindable quantum banana", {"preferences":[]}, [])
    assert r["recommendations"] == []
