# README_LICENSE

## 繁體中文
### 概要
本專案支援離線簽章驗證授權：`license.json`。

### 放置位置
- PyInstaller exe：放在 exe 同資料夾
- 原始碼執行：放在專案根目錄（和 `main.py` 同層）

### 設定頁解鎖
- 可拖曳 `license.json` 到授權輸入框
- 或按選檔按鈕手動選擇

### 驗證必要欄位
- `v = 1`
- `product = "ElementGacha"`
- `features = {"paid": true}`
- `sig`（base64 Ed25519 簽章）

### canonical JSON
- 移除 `sig`
- `json.dumps(..., sort_keys=True, separators=(",", ":"))`
- 轉 UTF-8 bytes 後驗證簽章

### 驗證結果
- 成功：`paid_unlocked=True`（+1/1s，cap 36000）
- 失敗/無檔：`paid_unlocked=False`（+1/60s，cap 600）

抽卡機率不變。

### 常見 reason
- `license_not_found`
- `license_parse_error`
- `missing_field:<name>`
- `version_mismatch`
- `product_mismatch`
- `paid_feature_missing`
- `sig_base64_invalid`
- `bad_signature`
- `public_key_invalid`

### 安全提醒
- 遊戲內只放公鑰（`PUBLIC_KEY_B64`）
- 私鑰只留在你自己的簽章環境，不能放進遊戲

---------------------------------------------------------------

## English
### Overview
This project supports offline paid unlock via signed `license.json`.

### Location
- PyInstaller exe: same folder as exe
- Source run: project root (same level as `main.py`)

### In-app unlock
- Drag `license.json` onto the input box
- Or choose file manually

### Required fields
- `v = 1`
- `product = "ElementGacha"`
- `features = {"paid": true}`
- `sig` (base64 Ed25519 signature)

### Canonical JSON
- remove `sig`
- `json.dumps(..., sort_keys=True, separators=(",", ":"))`
- verify on UTF-8 bytes

### Result
- Valid: `paid_unlocked=True` (+1/1s, cap 36000)
- Invalid/missing: `paid_unlocked=False` (+1/60s, cap 600)

Gacha rates are unchanged.

### Common reasons
- `license_not_found`
- `license_parse_error`
- `missing_field:<name>`
- `version_mismatch`
- `product_mismatch`
- `paid_feature_missing`
- `sig_base64_invalid`
- `bad_signature`
- `public_key_invalid`

### Security
- Keep only public key (`PUBLIC_KEY_B64`) in app
- Never ship private key with the game

---------------------------------------------------------------

## 日本語
### 概要
署名済み `license.json` によるオフライン有料解放に対応しています。

### 配置場所
- PyInstaller exe：exe と同じフォルダ
- ソース実行：`main.py` と同階層

### 設定画面での解放
- `license.json` を入力欄へドラッグ
- または手動でファイル選択

### 必須項目
- `v = 1`
- `product = "ElementGacha"`
- `features = {"paid": true}`
- `sig`（base64 Ed25519 署名）

### canonical JSON
- `sig` を除外
- `json.dumps(..., sort_keys=True, separators=(",", ":"))`
- UTF-8 bytes で署名検証

### 結果
- 成功：`paid_unlocked=True`（+1/1s、上限36000）
- 失敗/未配置：`paid_unlocked=False`（+1/60s、上限600）

ガチャ排出率は変わりません。

### 主な reason
- `license_not_found`
- `license_parse_error`
- `missing_field:<name>`
- `version_mismatch`
- `product_mismatch`
- `paid_feature_missing`
- `sig_base64_invalid`
- `bad_signature`
- `public_key_invalid`

### セキュリティ
- アプリには公開鍵（`PUBLIC_KEY_B64`）のみ
- 秘密鍵は絶対に同梱しない

---------------------------------------------------------------

## 한국어
### 개요
서명된 `license.json` 기반 오프라인 유료 해금을 지원합니다.

### 위치
- PyInstaller exe: exe와 같은 폴더
- 소스 실행: `main.py` 와 같은 위치

### 설정 화면 해금
- `license.json`을 입력칸으로 드래그
- 또는 수동 파일 선택

### 필수 필드
- `v = 1`
- `product = "ElementGacha"`
- `features = {"paid": true}`
- `sig` (base64 Ed25519 서명)

### canonical JSON
- `sig` 제거
- `json.dumps(..., sort_keys=True, separators=(",", ":"))`
- UTF-8 bytes 기준 서명 검증

### 결과
- 성공: `paid_unlocked=True` (+1/1s, 최대 36000)
- 실패/없음: `paid_unlocked=False` (+1/60s, 최대 600)

가챠 확률은 변경되지 않습니다.

### 주요 reason
- `license_not_found`
- `license_parse_error`
- `missing_field:<name>`
- `version_mismatch`
- `product_mismatch`
- `paid_feature_missing`
- `sig_base64_invalid`
- `bad_signature`
- `public_key_invalid`

### 보안
- 앱에는 공개키(`PUBLIC_KEY_B64`)만 포함
- 개인키는 절대 게임에 포함하지 않기
