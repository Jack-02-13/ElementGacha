# README_GAME

## 繁體中文
### 1) 遊戲目標
- 收集全部 118 種元素。
- 重複抽到會累加持有數量。

### 2) 抽卡券與抽卡
- 抽卡券（ticket）會隨時間自動累積。
- 抽卡（draw）會消耗抽卡券。

免費玩家：
- 每 60 秒 +1 張券
- 上限 600

已解鎖玩家：
- 每 1 秒 +1 張券
- 上限 36000

> 時間只影響抽卡券生成，不影響抽卡機率。

### 3) 抽卡機率（固定）
- R1: 50%
- R2: 30%
- R3: 14.5%
- R4: 5%
- R5: 0.5%

流程：
1. 先抽稀有度
2. 再從該稀有度池等機率抽 1 個元素

### 4) 主要畫面
- 主選單：開始抽卡 / 圖鑑 / 設定 / 離開 / ?
- 抽卡頁：顯示券數、速度、統計、抽卡結果、詳細資料
- 圖鑑頁：分段圖鑑 / 週期表圖鑑，點元素看詳情
- 設定頁：授權檔、存檔管理、語言切換

### 5) 付費解鎖
- 使用 `license.json` 驗證
- 成功：套用付費券規則
- 失敗或無檔：維持免費規則

細節請看 `README_LICENSE.md`

### 6) 存檔
- 可匯出 `save.json` 備份
- 可匯入 `save.json` 還原

### 7) 常見問題
- 為什麼有存檔但未解鎖？
  - 解鎖看 `license.json` 驗證，不看存檔。
- 付費會提高機率嗎？
  - 不會，只改抽卡券生成速度與上限。

---------------------------------------------------------------

## English
### 1) Goal
- Collect all 118 elements.
- Duplicate pulls increase owned count.

### 2) Tickets and Draws
- Tickets are generated over time automatically.
- Draws consume tickets.

Free:
- +1 ticket every 60s
- Cap 600

Unlocked:
- +1 ticket every 1s
- Cap 36000

> Time affects ticket generation only, not draw rates.

### 3) Rates (fixed)
- R1: 50%
- R2: 30%
- R3: 14.5%
- R4: 5%
- R5: 0.5%

Flow:
1. Roll rarity
2. Pick one element uniformly from that rarity pool

### 4) Screens
- Main: Start / Collection / Settings / Exit / ?
- Gacha: tickets, speed, stats, results, detail panel
- Collection: segmented view / periodic table view
- Settings: license, save management, language

### 5) Paid Unlock
- Uses `license.json` verification
- Valid: paid ticket rules
- Invalid/missing: free ticket rules

See `README_LICENSE.md` for details.

### 6) Save
- Export `save.json`
- Import `save.json`

### 7) FAQ
- Why still locked with existing save?
  - Unlock is based on `license.json` verification.
- Does paid increase rarity rates?
  - No. Only ticket speed/cap changes.

---------------------------------------------------------------

## 日本語
### 1) 目標
- 118種類の元素をすべて収集します。
- 重複で所持数が増加します。

### 2) チケットとガチャ
- チケットは時間で自動増加。
- ガチャはチケットを消費。

無料：
- 60秒ごとに +1
- 上限 600

解放後：
- 1秒ごとに +1
- 上限 36000

> 時間の影響はチケット生成のみです。

### 3) 排出率（固定）
- R1: 50%
- R2: 30%
- R3: 14.5%
- R4: 5%
- R5: 0.5%

流れ：
1. レア度抽選
2. そのレア度プールから等確率で1つ抽選

### 4) 画面
- メイン：開始 / 図鑑 / 設定 / 終了 / ?
- ガチャ：チケット、速度、統計、結果、詳細
- 図鑑：分段表示 / 周期表表示
- 設定：ライセンス、セーブ管理、言語

### 5) 有料解放
- `license.json` を検証
- 成功：有料ルール適用
- 失敗・未配置：無料ルール

詳細は `README_LICENSE.md` を参照してください。

### 6) セーブ
- `save.json` 書き出し
- `save.json` 読み込み

### 7) FAQ
- セーブがあるのに未解放？
  - 解放判定は `license.json` 検証です。
- 有料で排出率は上がる？
  - 上がりません。チケット速度/上限のみ変更。

---------------------------------------------------------------

## 한국어
### 1) 목표
- 118종 원소를 모두 수집합니다.
- 중복 뽑기는 보유 수량이 증가합니다.

### 2) 티켓과 뽑기
- 티켓은 시간에 따라 자동 생성됩니다.
- 뽑기는 티켓을 소모합니다.

무료:
- 60초마다 +1
- 최대 600

해금:
- 1초마다 +1
- 최대 36000

> 시간은 티켓 생성에만 영향을 줍니다.

### 3) 확률 (고정)
- R1: 50%
- R2: 30%
- R3: 14.5%
- R4: 5%
- R5: 0.5%

절차:
1. 희귀도 추첨
2. 해당 희귀도 풀에서 균등 확률로 1개 선택

### 4) 화면
- 메인: 시작 / 도감 / 설정 / 종료 / ?
- 뽑기: 티켓, 속도, 통계, 결과, 상세 정보
- 도감: 구간 보기 / 주기율표 보기
- 설정: 라이선스, 저장 관리, 언어

### 5) 유료 해금
- `license.json` 검증 사용
- 성공: 유료 티켓 규칙 적용
- 실패/없음: 무료 규칙 유지

자세한 내용은 `README_LICENSE.md` 참고.

### 6) 저장
- `save.json` 내보내기
- `save.json` 가져오기

### 7) FAQ
- 저장이 있는데 왜 미해금인가요?
  - 해금은 `license.json` 검증 결과로 판단합니다.
- 유료면 확률이 올라가나요?
  - 아니요. 티켓 속도/상한만 바뀝니다。
