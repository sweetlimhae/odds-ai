from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .data_provider import get_odds
from .analyzer import analyze_all, recommend_combos

app = FastAPI(title='Odds AI PWA', version='1.0.0')

@app.get('/api/health')
def health():
    return {'ok': True}

@app.get('/api/analyze')
async def analyze(
    sport: str = Query('all', pattern='^(all|baseball|soccer)$'),
    window: int = Query(60, ge=30, le=120),
):
    raw = await get_odds(sport)
    analyzed = analyze_all(raw)
    combos = recommend_combos(analyzed)
    return {'sport': sport, 'window_minutes': window, 'picks': analyzed, 'combos': combos}

app.mount('/app', StaticFiles(directory='frontend', html=True), name='frontend')

@app.get('/')
def root():
    return FileResponse('frontend/index.html')
