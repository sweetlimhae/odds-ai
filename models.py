from pydantic import BaseModel
from typing import Literal, Optional, List

Sport = Literal['baseball', 'soccer']
Market = Literal['moneyline', 'spread', 'total', '1x2', 'handicap', 'over_under']
Side = Literal['home', 'away', 'draw', 'over', 'under']
Risk = Literal['cautious', 'balanced', 'aggressive']

class OddsPick(BaseModel):
    match_id: str
    sport: Sport
    league: str
    kickoff_ts: str
    home_team: str
    away_team: str
    market: Market
    side: Side
    bookmaker: str
    opening_odds: float
    current_odds: float
    previous_odds: Optional[float] = None
    sharp_book_odds: Optional[float] = None
    market_avg_odds: Optional[float] = None
    domestic_odds: Optional[float] = None

class AnalyzedPick(OddsPick):
    score: int
    risk_score: int
    odds_drop_pct: float
    value_gap_pct: float
    reasons: List[str]

class Combo(BaseModel):
    type: Risk
    title: str
    picks: List[AnalyzedPick]
    combined_odds: float
    avg_score: float
    risk_label: str
    summary: str
