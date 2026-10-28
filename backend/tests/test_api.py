from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test_health():
    assert client.get('/api/health').json()['status'] == 'healthy'
def test_valuation():
    r=client.post('/api/valuation',json={'structure':'Residential','area_sqft':1000,'city_tier':'Tier 2','completion_percent':50,'finish_level':'Standard','market_multiplier':1.25})
    assert r.status_code == 200 and r.json()['total_budget_inr'] > 0
def test_advisory():
    r=client.post('/api/advisory',json={'condition':'Heavy Rain'})
    assert r.status_code == 200 and len(r.json()['actions']) > 0
def test_chat_empty_rejected():
    assert client.post('/api/chat',json={'question':''}).status_code == 422
