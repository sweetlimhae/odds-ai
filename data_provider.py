import os
from typing import List
import httpx
from .models import OddsPick

DEMO = [
    dict(match_id='KBO-001', sport='baseball', league='KBO', kickoff_ts='2026-07-05T18:30:00+09:00', home_team='LG', away_team='Doosan', market='moneyline', side='home', bookmaker='BMBets', opening_odds=1.78, previous_odds=1.72, current_odds=1.66, sharp_book_odds=1.64, market_avg_odds=1.70, domestic_odds=1.70),
    dict(match_id='KBO-002', sport='baseball', league='KBO', kickoff_ts='2026-07-05T18:30:00+09:00', home_team='KIA', away_team='SSG', market='moneyline', side='away', bookmaker='BMBets', opening_odds=1.92, previous_odds=1.84, current_odds=1.76, sharp_book_odds=1.73, market_avg_odds=1.80, domestic_odds=1.82),
    dict(match_id='SOC-001', sport='soccer', league='EPL', kickoff_ts='2026-07-05T22:00:00+09:00', home_team='Arsenal', away_team='Chelsea', market='1x2', side='home', bookmaker='BMBets', opening_odds=1.88, previous_odds=1.82, current_odds=1.74, sharp_book_odds=1.71, market_avg_odds=1.78, domestic_odds=1.79),
    dict(match_id='SOC-002', sport='soccer', league='LaLiga', kickoff_ts='2026-07-05T23:00:00+09:00', home_team='Real Madrid', away_team='Sevilla', market='handicap', side='home', bookmaker='BMBets', opening_odds=1.95, previous_odds=1.89, current_odds=1.82, sharp_book_odds=1.80, market_avg_odds=1.85, domestic_odds=1.86),
    dict(match_id='SOC-003', sport='soccer', league='UCL', kickoff_ts='2026-07-06T04:00:00+09:00', home_team='PSG', away_team='Inter', market='over_under', side='under', bookmaker='BMBets', opening_odds=1.91, previous_odds=1.86, current_odds=1.79, sharp_book_odds=1.77, market_avg_odds=1.82, domestic_odds=1.84),
    dict(match_id='SOC-004', sport='soccer', league='SerieA', kickoff_ts='2026-07-06T01:30:00+09:00', home_team='Milan', away_team='Roma', market='1x2', side='draw', bookmaker='BMBets', opening_odds=3.30, previous_odds=3.22, current_odds=3.08, sharp_book_odds=3.02, market_avg_odds=3.12, domestic_odds=3.15),
]


def _normalize_external(item: dict) -> OddsPick:
    return OddsPick(**item)


async def fetch_external(url: str, api_key: str | None) -> list[OddsPick]:
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
    items = data.get('odds', data if isinstance(data, list) else [])
    return [_normalize_external(x) for x in items]


async def get_odds(sport: str = 'all') -> List[OddsPick]:
    mode = os.getenv('DATA_MODE', 'demo').lower()
    picks: list[OddsPick] = []

    if mode == 'api':
        for prefix in ['BMBETS', 'PINNACLE']:
            url = os.getenv(f'{prefix}_API_URL')
            key = os.getenv(f'{prefix}_API_KEY')
            if url:
                picks.extend(await fetch_external(url, key))
    else:
        picks = [OddsPick(**x) for x in DEMO]

    if sport and sport != 'all':
        picks = [p for p in picks if p.sport == sport]
    return picks
