from app.policies.policy_engine import PolicyEngine

catalogue={"ok":{"id":"ok","name":"Available","stock":3},"out":{"id":"out","name":"Sold out","stock":0}}
def test_rejects_discount_over_limit(): assert not PolicyEngine().validate_order([{"id":"ok"}],25,True,catalogue).approved
def test_requires_confirmation(): assert not PolicyEngine().validate_order([{"id":"ok"}],0,False,catalogue).approved
def test_rejects_invalid_product(): assert not PolicyEngine().validate_order([{"id":"bad"}],0,True,catalogue).approved
def test_rejects_out_of_stock(): assert not PolicyEngine().validate_order([{"id":"out"}],0,True,catalogue).approved
def test_approves_valid_confirmed_order(): assert PolicyEngine().validate_order([{"id":"ok"}],10,True,catalogue).approved
