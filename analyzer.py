from __future__ import annotations
from itertools import combinations
from typing import List
from .models import OddsPick, AnalyzedPick, Combo


def pct_change(old: float, new: float) -> float:
    if not old:
        return 0.0
    return round((new - old) / old * 100, 2)


def analyze_pick(p: OddsPick) -> AnalyzedPick:
    score = 40
    risk = 50
    reasons = []

    drop = pct_change(p.opening_odds, p.current_odds)
    if drop <= -6:
        score += 25; risk -= 12; reasons.append('초기배당 대비 강한 하락')
    elif drop <= -3:
        score += 16; risk -= 7; reasons.append('초기배당 대비 의미 있는 하락')
    elif drop <= -1:
        score += 7; reasons.append('초기배당 대비 소폭 하락')
    elif drop >= 4:
        score -= 12; risk += 14; reasons.append('배당 상승으로 신뢰도 하락')

    if p.previous_odds:
        recent = pct_change(p.previous_odds, p.current_odds)
        if recent <= -2:
            score += 12; risk -= 5; reasons.append('최근 구간에서도 배당 하락')
        elif recent >= 2:
            score -= 8; risk += 8; reasons.append('최근 구간 배당 반등')

    value_gap = 0.0
    if p.sharp_book_odds and p.domestic_odds:
        value_gap = pct_change(p.sharp_book_odds, p.domestic_odds)
        if value_gap >= 3:
            score += 12; reasons.append('국내/표시 배당이 샤프북 대비 높음')
        elif value_gap <= -3:
            score -= 10; risk += 10; reasons.append('국내/표시 배당 메리트 부족')

    if p.market_avg_odds:
        avg_gap = pct_change(p.market_avg_odds, p.current_odds)
        if avg_gap >= 2:
            score += 6; reasons.append('시장 평균 대비 배당 메리트')

    if p.market in ['spread', 'handicap']:
        score += 4; reasons.append('핸디캡 시장 신호 반영')
    if p.market in ['total', 'over_under'] and p.side == 'under':
        score += 3; reasons.append('언더 흐름 보조 신호 반영')
    if p.market == '1x2' and p.side == 'draw':
        risk += 22; score -= 8; reasons.append('무승부 선택은 변동성 높음')

    score = max(0, min(100, score))
    risk = max(1, min(100, risk))
    if not reasons:
        reasons.append('뚜렷한 우위 신호 없음')

    return AnalyzedPick(**p.model_dump(), score=score, risk_score=risk, odds_drop_pct=drop, value_gap_pct=value_gap, reasons=reasons)


def filter_by_time_window(picks: List[OddsPick], window_minutes: int, now_ts: str | None = None) -> List[OddsPick]:
    # 서버/브라우저 시간차 문제를 피하려고 demo에서는 프론트 필터 대신 백엔드에서 kickoff_ts 기준으로 단순 통과.
    # 실제 운영 시에는 datetime 파싱으로 now~now+window_minutes 경기만 남기면 됩니다.
    return picks


def analyze_all(picks: List[OddsPick]) -> List[AnalyzedPick]:
    return sorted([analyze_pick(p) for p in picks], key=lambda x: (x.score, -x.risk_score), reverse=True)


def make_combo(candidates: List[AnalyzedPick], combo_type: str) -> Combo | None:
    if len(candidates) < 2:
        return None

    pairs = list(combinations(candidates, 2))

    def combined(pair):
        return round(pair[0].current_odds * pair[1].current_odds, 2)

    if combo_type == 'cautious':
        valid = [p for p in pairs if p[0].score >= 75 and p[1].score >= 75 and combined(p) <= 3.2]
        chosen = sorted(valid or pairs, key=lambda p: (p[0].score + p[1].score, -combined(p)), reverse=True)[0]
        title, label = '신중형 2폴더', '낮음'
        summary = '적중 가능성을 우선한 조합입니다.'
    elif combo_type == 'balanced':
        valid = [p for p in pairs if p[0].score >= 65 and p[1].score >= 65 and 2.4 <= combined(p) <= 4.5]
        chosen = sorted(valid or pairs, key=lambda p: (abs(combined(p)-3.4), -(p[0].score+p[1].score)))[0]
        title, label = '균형형 2폴더', '중간'
        summary = '안정성과 수익성을 같이 보는 조합입니다.'
    else:
        valid = [p for p in pairs if p[0].score >= 55 and p[1].score >= 55 and combined(p) >= 3.2]
        chosen = sorted(valid or pairs, key=lambda p: (combined(p), p[0].score + p[1].score), reverse=True)[0]
        title, label = '공격형 2폴더', '높음'
        summary = '배당을 더 노리는 고위험 조합입니다.'

    return Combo(
        type=combo_type,
        title=title,
        picks=list(chosen),
        combined_odds=combined(chosen),
        avg_score=round((chosen[0].score + chosen[1].score) / 2, 1),
        risk_label=label,
        summary=summary,
    )


def recommend_combos(analyzed: List[AnalyzedPick]) -> List[Combo]:
    combos = []
    for t in ['cautious', 'balanced', 'aggressive']:
        combo = make_combo(analyzed, t)
        if combo:
            combos.append(combo)
    return combos
