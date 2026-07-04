# Odds AI Analyzer PWA

아이폰 Safari에서 사용할 수 있는 배당 분석 PWA입니다.

## 기능

- 야구 / 축구 분석
- 경기 30분 전 / 1시간 전 / 2시간 전 필터 UI
- BMBets + Pinnacle API 연결 구조
- 배당 하락률, 샤프북 괴리, 시장 평균 괴리 점수화
- 신중형 / 균형형 / 공격형 2폴더 추천
- 실제 자동베팅 실행 없음

## 로컬 실행

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

브라우저에서 http://127.0.0.1:8000 접속

## Render 배포

1. GitHub에 이 폴더 전체 업로드
2. Render 접속
3. New + → Web Service
4. GitHub 저장소 연결
5. Build Command

```bash
pip install -r requirements.txt
```

6. Start Command

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

7. 배포 완료 후 아이폰 Safari에서 주소 접속
8. 공유 버튼 → 홈 화면에 추가

## 실제 데이터 연결

기본값은 demo 데이터입니다.

Render Environment Variables에서 아래 값을 설정합니다.

```env
DATA_MODE=api
BMBETS_API_URL=https://your-bmbets-data-endpoint.example/odds
BMBETS_API_KEY=your_key
PINNACLE_API_URL=https://your-pinnacle-data-endpoint.example/odds
PINNACLE_API_KEY=your_key
```

API 응답은 아래 형식이어야 합니다.

```json
{
  "odds": [
    {
      "match_id": "SOC-001",
      "sport": "soccer",
      "league": "EPL",
      "kickoff_ts": "2026-07-05T22:00:00+09:00",
      "home_team": "Arsenal",
      "away_team": "Chelsea",
      "market": "1x2",
      "side": "home",
      "bookmaker": "BMBets",
      "opening_odds": 1.88,
      "previous_odds": 1.82,
      "current_odds": 1.74,
      "sharp_book_odds": 1.71,
      "market_avg_odds": 1.78,
      "domestic_odds": 1.79
    }
  ]
}
```

## 주의

BMBets/Pinnacle의 공식 API나 합법적으로 접근 가능한 데이터 제공 URL이 필요합니다. 사이트 약관을 위반하는 자동 수집, 로그인 우회, 봇 차단 우회 기능은 포함하지 않았습니다.
