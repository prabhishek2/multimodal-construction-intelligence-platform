from datetime import datetime, timezone
from typing import Literal
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title='Multimodal Construction Intelligence API', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173','http://127.0.0.1:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

class ValuationRequest(BaseModel):
    structure: Literal['Residential','Commercial','Industrial','Institutional'] = 'Residential'
    area_sqft: int = Field(2000, ge=100, le=2000000)
    city_tier: Literal['Tier 1','Tier 2','Tier 3'] = 'Tier 2'
    completion_percent: int = Field(35, ge=0, le=100)
    finish_level: Literal['Economy','Standard','Premium'] = 'Standard'
    market_multiplier: float = Field(1.25, ge=0.8, le=2.5)
class AdvisoryRequest(BaseModel):
    condition: Literal['Normal','High Wind','Heavy Rain','Extreme Heat'] = 'Normal'
class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    condition: str = 'Normal'

@app.get('/')
def root(): return {'name':'Multimodal Construction Intelligence Platform','status':'ok','mode':'demo','docs':'/docs'}
@app.get('/api/health')
def health(): return {'status':'healthy','timestamp':datetime.now(timezone.utc).isoformat()}
@app.get('/api/features')
def features(): return {'features':[{'id':'safety','title':'Site Safety & PPE Audit','status':'manual-review-demo'},{'id':'cracks','title':'Crack Diagnostics','status':'manual-review-demo'},{'id':'valuation','title':'Planning & Valuation','status':'demo-logic'},{'id':'advisory','title':'Weather-Aware Site Assistant','status':'rule-based-demo'}]}

@app.post('/api/safety')
async def safety(image: UploadFile | None = File(default=None)):
    if image:
        if image.content_type not in {'image/jpeg','image/png','image/webp'}: raise HTTPException(415,'Upload JPG, PNG, or WEBP.')
        data = await image.read()
        if len(data)>10*1024*1024: raise HTTPException(413,'Image must be 10 MB or smaller.')
    return {'mode':'manual_review_demo','image_name':image.filename if image else None,'overall_status':'Manual review required','checks':['Hard hat / helmet','High-visibility vest','Safety footwear','Fall protection where required'],'hazards_to_review':['Edge protection','Excavations','Electrical hazards','Housekeeping and access routes'],'disclaimer':'No computer-vision model is connected; this endpoint does not detect PPE in pixels.'}

@app.post('/api/cracks')
async def cracks(image: UploadFile | None = File(default=None), context: str = Form(default='')):
    if image:
        if image.content_type not in {'image/jpeg','image/png','image/webp'}: raise HTTPException(415,'Upload JPG, PNG, or WEBP.')
        data = await image.read()
        if len(data)>10*1024*1024: raise HTTPException(413,'Image must be 10 MB or smaller.')
    return {'mode':'manual_review_demo','image_name':image.filename if image else None,'context':context,'defect_type':'Unclassified — engineer review needed','width':'Not measured','severity':'Not assessed','recommended_actions':['Photograph with a scale and record location','Monitor and document changes or water ingress','Ask a qualified structural engineer to assess'],'disclaimer':'Not a structural diagnosis; no crack-detection model is connected.'}

@app.post('/api/valuation')
def valuation(r: ValuationRequest):
    city={'Tier 1':1.25,'Tier 2':1.0,'Tier 3':0.85}[r.city_tier]; structure={'Residential':1.0,'Commercial':1.25,'Industrial':1.15,'Institutional':1.1}[r.structure]; finish={'Economy':1500,'Standard':2000,'Premium':2800}[r.finish_level]
    rate=finish*city*structure; budget=r.area_sqft*rate
    return {'structure_type':r.structure,'built_up_area_sqft':r.area_sqft,'city_tier':r.city_tier,'finish_level':r.finish_level,'assumed_rate_inr_per_sqft':round(rate,2),'total_budget_inr':round(budget,2),'completion_percent':r.completion_percent,'incurred_capex_inr':round(budget*r.completion_percent/100,2),'market_valuation_inr':round(budget*r.market_multiplier,2),'cement_bags_estimate':round(r.area_sqft*.4),'steel_kg_estimate':round(r.area_sqft*4),'assumptions':'Illustrative rates only; replace with local quotes and engineer-approved bill of quantities.'}

@app.post('/api/advisory')
def advisory(r: AdvisoryRequest):
    actions={'Normal':['Conduct toolbox talk and routine PPE checks.','Inspect access routes, lifting gear, scaffolds and housekeeping.'],'High Wind':['Check measured wind against equipment and lift-plan limits.','Secure loose materials; suspend unsafe lifting or work at height.'],'Heavy Rain':['Review excavation stability and drainage before entry.','Protect electrical equipment and reassess access and lifting risks.'],'Extreme Heat':['Provide water, shade, acclimatization and work-rest cycles.','Train supervisors to recognize heat illness and follow emergency procedures.']}[r.condition]
    return {'condition':r.condition,'headline':f'{r.condition}: review site-specific risks before work.','actions':actions,'disclaimer':'Follow local regulations, the approved site safety plan and responsible engineer instructions.'}

@app.post('/api/chat')
def chat(r: ChatRequest):
    q=r.question.lower()
    if any(k in q for k in ['concrete','pour','curing']): a='Check approved mix design, formwork, reinforcement cover, PPE, weather, placement sequence, compaction and curing plan.'
    elif any(k in q for k in ['crane','wind','lifting']): a='Check lift plan, measured wind speed, equipment limits, load chart, exclusion zone and competent operator guidance.'
    elif any(k in q for k in ['ppe','helmet','safety','hazard']): a='Verify task-specific PPE, fall protection, barriers, housekeeping, electrical safety and toolbox-talk records. Escalate imminent hazards.'
    else: a='Consult the approved method statement and site safety plan, confirm conditions with the responsible engineer, and document hazards before work.'
    return {'answer':a+f' Selected weather condition: {r.condition}.','mode':'rule_based_demo'}
