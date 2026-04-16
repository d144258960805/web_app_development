# 路由設計文件：線上算命系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 | GET | / | templates/index.html | 顯示首頁、功能入口 |
| 註冊頁面 | GET | /auth/register | templates/auth/register.html | 顯示註冊表單 |
| 註冊處理 | POST | /auth/register | — | 接收註冊資料、存入DB並重導向登入頁 |
| 登入頁面 | GET | /auth/login | templates/auth/login.html | 顯示登入表單 |
| 登入處理 | POST | /auth/login | — | 接收登入資訊、設定Session並重導向首頁 |
| 登出處理 | GET | /auth/logout | — | 清除Session並重導向首頁 |
| 抽籤頁面 | GET | /fortune/draw | templates/fortune/draw.html | 顯示搖籤筒頁面 |
| 抽籤處理 | POST | /fortune/draw | — | 隨機抽籤，紀錄存入DB，重導向至結果頁 |
| 塔羅占卜頁面 | GET | /fortune/tarot | templates/fortune/tarot.html | 顯示塔羅牌陣選牌頁面 |
| 塔羅處理 | POST | /fortune/tarot | — | 隨機抽塔羅牌，紀錄存入DB，重導向至結果頁 |
| 算命詳細結果 | GET | /fortune/result/<id> | templates/fortune/result.html | 顯示該次算命的詳細結果 |
| 歷史紀錄列表 | GET | /history/ | templates/history/list.html | 列表顯示使用者所有算命紀錄 |
| 歷史紀錄詳情 | GET | /history/<id> | templates/fortune/result.html | 顯示單筆歷史紀錄結果 |
| 捐獻頁面 | GET | /donation/donate | templates/donation/donate.html | 顯示捐香油錢頁面 |
| 捐獻處理 | POST | /donation/donate | — | 接收捐獻表單，建立訂單並重導向成功提示或首頁 |
| 分享結果 | GET | /share/<id> | templates/fortune/result.html 或自訂分享區 | 產生可分享的公開算命結果頁面 |

## 2. 每個路由的詳細說明

### 2.1 首頁 (Main)
- **URL**: `GET /`
- **處理邏輯**: 決定使用者呈現每日運勢或進入首頁動畫。
- **輸出**: 渲染 `index.html`。
- **錯誤處理**: 遇到伺服器錯誤顯示通用 500 頁面。

### 2.2 會員模組 (Auth)
- **註冊 (GET /auth/register)**
  - 輸出: 渲染 `register.html`。
- **註冊處理 (POST /auth/register)**
  - 輸入: `username`, `password`, `confirm_password`。
  - 邏輯: 呼叫 User.create 建立帳號；若帳號已存在或密碼不符，返回錯誤訊息。
  - 輸出: 重導向到 `/auth/login`。
- **登入 (GET /auth/login)**
  - 輸出: 渲染 `login.html`。
- **登入處理 (POST /auth/login)**
  - 輸入: `username`, `password`。
  - 邏輯: 查詢 User 驗證密碼；成功則登入使用者。
  - 輸出: 成功重導向至首頁 `/`；失敗留在登入頁顯示錯誤。
- **登出 (GET /auth/logout)**
  - 邏輯: 使用 Flask-Login 登出使用者。
  - 輸出: 重導向至首頁 `/`。

### 2.3 算命模組 (Fortune)
- **線上抽籤 (GET /fortune/draw)**
  - 邏輯: 處理授權檢查（需登入）。
  - 輸出: 渲染 `draw.html` 搭載動畫庫。
- **線上抽籤 (POST /fortune/draw)**
  - 邏輯: 從 backend 讀取 json 進行抽籤亂數，接著使用 `FortuneRecord.create` 存擋。
  - 輸出: 導向至 `/fortune/result/<id>`。
- **塔羅占卜 (GET /fortune/tarot)**
  - 邏輯: 處理授權檢查（需登入）。
  - 輸出: 渲染 `tarot.html` 搭載選牌 UI。
- **塔羅占卜 (POST /fortune/tarot)**
  - 輸入: 所選擇的牌位或牌陣資料。
  - 邏輯: 對應塔羅牌邏輯，產生正逆位與結果，使用 `FortuneRecord.create` 存擋。
  - 輸出: 導向至 `/fortune/result/<id>`。
- **結果 (GET /fortune/result/<id>)**
  - 邏輯: 透過 `FortuneRecord.get_by_id` 找回資料並回傳。若 ID 查無資料則回報 404。
  - 輸出: 渲染 `result.html`。

### 2.4 歷史紀錄模組 (History)
- **歷史首頁 (GET /history/)**
  - 邏輯: 根據使用者 ID 調用 `FortuneRecord.get_all_by_user` 列出其過往的算命履歷。
  - 輸出: 渲染 `list.html`。
- **歷史紀錄詳情 (GET /history/<id>)**
  - 邏輯: 根據 record_id 以及當前的 user_id 校驗讀取，預防越權。
  - 輸出: 渲染 `result.html` 或重導往。

### 2.5 捐獻模組 (Donation)
- **捐獻表單 (GET /donation/donate)**
  - 邏輯: 確認登入態，提供捐款選擇數字。
  - 輸出: 渲染 `donate.html`。
- **捐獻建立 (POST /donation/donate)**
  - 輸入: `amount` (金額)。
  - 邏輯: 調用 `Donation.create` 建立訂單，並更新訂單狀態。
  - 輸出: 成功後重導向 `/` 或特定的捐獻成果頁（初期可先用Flash提示）。

### 2.6 分享模組 (Share)
- **分享閱覽 (GET /share/<id>)**
  - 邏輯: 此頁面**允許非會員**檢視特定算命結果（唯讀），調用 `FortuneRecord.get_by_id`。
  - 輸出: 渲染公眾的結果畫面。

## 3. Jinja2 模板清單

所有的視圖模板都會繼承於 `base.html`：
- `templates/base.html`: 核心框架、導覽列、頁尾與基礎 CSS / JS 引入。
- `templates/index.html`: 首頁內容。
- `templates/auth/login.html`: 登入表單。
- `templates/auth/register.html`: 註冊表單。
- `templates/fortune/draw.html`: 抽籤畫面，搭載動態展示。
- `templates/fortune/tarot.html`: 塔羅選牌陣與動畫的展示。
- `templates/fortune/result.html`: 展示一次抽籤或翻牌的詳細文案。
- `templates/history/list.html`: 高階歷史紀錄統整呈現頁。
- `templates/donation/donate.html`: 香油錢奉獻操作介面。
