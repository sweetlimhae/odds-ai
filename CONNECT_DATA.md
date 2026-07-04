# 데이터 연결 방법

## 1. 공식 API가 있는 경우

가장 좋은 방법입니다.

Render 환경변수에 다음을 입력합니다.

```env
DATA_MODE=api
BMBETS_API_URL=발급받은_API_URL
BMBETS_API_KEY=발급받은_API_KEY
PINNACLE_API_URL=발급받은_API_URL
PINNACLE_API_KEY=발급받은_API_KEY
```

## 2. 별도 데이터 공급 서버가 있는 경우

직접 만든 수집 서버가 아래 JSON 형식으로 내려주면 됩니다.

```json
{
  "odds": []
}
```

각 odds 항목은 README의 스키마와 같아야 합니다.

## 3. CSV/수동 데이터로 운영하는 경우

현재 버전은 API 모드 중심입니다. CSV 업로드를 다시 넣으려면 frontend에 파일 업로드 UI와 backend에 CSV 파서 엔드포인트를 추가하면 됩니다.

## 하지 않는 것

- 실제 자동베팅 실행
- 로그인 우회
- 캡차 우회
- 차단 회피용 크롤링
- 사이트 약관 위반 가능성이 큰 수집
