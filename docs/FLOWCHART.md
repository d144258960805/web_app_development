# 流程圖文件：線上算命系統

## 1. 使用者流程圖（User Flow）

以下流程圖描述使用者從進入網站開始，到完成各項功能的完整操作路徑。

```mermaid
flowchart LR
    A(["🌐 使用者開啟網站"]) --> B["首頁"]
    B --> C{"已登入？"}

    %% 未登入：導向會員系統
    C -->|否| D["登入頁面"]
    D --> E{"有帳號？"}
    E -->|否| F["註冊頁面"]
    F --> G["填寫帳號密碼"]
    G --> H["註冊成功"]
    H --> D
    E -->|是| I["輸入帳號密碼"]
    I --> J{"驗證通過？"}
    J -->|否| D
    J -->|是| B

    %% 已登入：選擇功能
    C -->|是| K{"選擇功能"}

    %% 功能 1：線上抽籤
    K -->|抽籤| L["抽籤頁面"]
    L --> M["搖籤筒動畫"]
    M --> N["顯示籤詩結果"]
    N --> O{"下一步？"}
    O -->|儲存| P["儲存至歷史紀錄"]
    O -->|分享| Q["分享至社群媒體"]
    O -->|再抽一次| L
    O -->|回首頁| B

    %% 功能 2：塔羅占卜
    K -->|塔羅占卜| R["塔羅占卜頁面"]
    R --> S["選擇牌陣 / 翻牌"]
    S --> T["顯示塔羅結果"]
    T --> O

    %% 功能 3：查看歷史紀錄
    K -->|歷史紀錄| U["歷史紀錄列表"]
    U --> V["查看單筆詳細結果"]
    V --> O

    %% 功能 4：捐香油錢
    K -->|捐香油錢| W["捐獻頁面"]
    W --> X["選擇金額"]
    X --> Y["確認付款"]
    Y --> Z["捐獻成功提示"]
    Z --> B

    %% 登出
    K -->|登出| AA["登出"]
    AA --> B
```

### 流程說明

- **進入網站**：使用者開啟網站後會進入首頁，系統判斷是否已登入。
- **未登入**：需先註冊或登入，才能使用算命功能與歷史紀錄。
- **已登入**：可自由選擇抽籤、塔羅占卜、查看歷史紀錄、捐香油錢等功能。
- **算命結果**：每次算命完成後，使用者可選擇儲存、分享、再試一次或返回首頁。

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 會員註冊流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as User Model
    participant DB as SQLite

    User->>Browser: 點擊「註冊」
    Browser->>Flask: GET /auth/register
    Flask-->>Browser: 渲染 register.html

    User->>Browser: 填寫帳號密碼並送出
    Browser->>Flask: POST /auth/register
    Flask->>Flask: 驗證表單資料
    Flask->>Flask: 密碼加密（Werkzeug hash）
    Flask->>Model: 建立 User 物件
    Model->>DB: INSERT INTO users
    DB-->>Model: 成功
    Model-->>Flask: 回傳 User 物件
    Flask-->>Browser: 重導向至登入頁
    Browser-->>User: 顯示「註冊成功，請登入」
```

### 2.2 會員登入流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as User Model
    participant DB as SQLite

    User->>Browser: 點擊「登入」
    Browser->>Flask: GET /auth/login
    Flask-->>Browser: 渲染 login.html

    User->>Browser: 輸入帳號密碼並送出
    Browser->>Flask: POST /auth/login
    Flask->>Model: 查詢使用者帳號
    Model->>DB: SELECT FROM users WHERE username=?
    DB-->>Model: 回傳使用者資料
    Model-->>Flask: 回傳 User 物件

    alt 密碼驗證成功
        Flask->>Flask: Flask-Login 建立 Session
        Flask-->>Browser: 重導向至首頁
        Browser-->>User: 顯示已登入首頁
    else 密碼驗證失敗
        Flask-->>Browser: 重新渲染 login.html
        Browser-->>User: 顯示「帳號或密碼錯誤」
    end
```

### 2.3 線上抽籤流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant JSON as fortune_sticks.json
    participant Model as Fortune Model
    participant DB as SQLite

    User->>Browser: 點擊「線上抽籤」
    Browser->>Flask: GET /fortune/draw
    Flask-->>Browser: 渲染 draw.html（含搖籤筒動畫）

    User->>Browser: 點擊「搖籤筒」按鈕
    Browser->>Flask: POST /fortune/draw
    Flask->>JSON: 隨機抽取一支籤
    JSON-->>Flask: 回傳籤詩資料（編號、籤詩、解籤）
    Flask->>Model: 建立 FortuneRecord 物件
    Model->>DB: INSERT INTO fortune_records
    DB-->>Model: 成功
    Model-->>Flask: 回傳紀錄物件
    Flask-->>Browser: 渲染 result.html（籤詩結果）
    Browser-->>User: 顯示籤詩與解籤內容
```

### 2.4 塔羅占卜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant JSON as tarot_cards.json
    participant Model as Fortune Model
    participant DB as SQLite

    User->>Browser: 點擊「塔羅占卜」
    Browser->>Flask: GET /fortune/tarot
    Flask-->>Browser: 渲染 tarot.html（牌陣頁面）

    User->>Browser: 選擇牌陣並翻牌
    Browser->>Flask: POST /fortune/tarot
    Flask->>JSON: 隨機抽取塔羅牌（含正逆位）
    JSON-->>Flask: 回傳塔羅牌資料（牌名、解釋）
    Flask->>Model: 建立 FortuneRecord 物件
    Model->>DB: INSERT INTO fortune_records
    DB-->>Model: 成功
    Model-->>Flask: 回傳紀錄物件
    Flask-->>Browser: 渲染 result.html（塔羅結果）
    Browser-->>User: 顯示塔羅牌面與解讀
```

### 2.5 捐香油錢流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Donation Model
    participant DB as SQLite

    User->>Browser: 點擊「捐香油錢」
    Browser->>Flask: GET /donation/donate
    Flask-->>Browser: 渲染 donate.html

    User->>Browser: 選擇金額並確認捐獻
    Browser->>Flask: POST /donation/donate
    Flask->>Flask: 驗證金額合法性
    Flask->>Model: 建立 Donation 物件（狀態：模擬成功）
    Model->>DB: INSERT INTO donations
    DB-->>Model: 成功
    Model-->>Flask: 回傳捐獻紀錄
    Flask-->>Browser: 渲染成功頁面
    Browser-->>User: 顯示「捐獻成功，功德無量」
```

### 2.6 查看歷史紀錄流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Fortune Model
    participant DB as SQLite

    User->>Browser: 點擊「歷史紀錄」
    Browser->>Flask: GET /history/
    Flask->>Model: 查詢該使用者所有紀錄
    Model->>DB: SELECT FROM fortune_records WHERE user_id=?
    DB-->>Model: 回傳紀錄列表
    Model-->>Flask: 回傳紀錄物件列表
    Flask-->>Browser: 渲染 list.html（紀錄列表）
    Browser-->>User: 顯示歷史算命紀錄

    User->>Browser: 點擊某筆紀錄
    Browser->>Flask: GET /history/<record_id>
    Flask->>Model: 查詢單筆紀錄
    Model->>DB: SELECT FROM fortune_records WHERE id=?
    DB-->>Model: 回傳紀錄資料
    Model-->>Flask: 回傳紀錄物件
    Flask-->>Browser: 渲染 result.html（詳細結果）
    Browser-->>User: 顯示該次算命詳細內容
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 首頁 | `/` | GET | 顯示首頁，含功能入口與每日運勢 |
| 註冊頁面 | `/auth/register` | GET | 顯示註冊表單 |
| 註冊處理 | `/auth/register` | POST | 處理註冊資料，建立帳號 |
| 登入頁面 | `/auth/login` | GET | 顯示登入表單 |
| 登入處理 | `/auth/login` | POST | 驗證帳密，建立登入 Session |
| 登出 | `/auth/logout` | GET | 清除 Session，登出使用者 |
| 抽籤頁面 | `/fortune/draw` | GET | 顯示搖籤筒頁面 |
| 抽籤處理 | `/fortune/draw` | POST | 隨機抽籤，儲存結果並顯示 |
| 塔羅占卜頁面 | `/fortune/tarot` | GET | 顯示塔羅牌陣頁面 |
| 塔羅占卜處理 | `/fortune/tarot` | POST | 隨機抽牌，儲存結果並顯示 |
| 算命結果頁面 | `/fortune/result/<id>` | GET | 顯示單次算命的詳細結果 |
| 歷史紀錄列表 | `/history/` | GET | 顯示使用者所有算命紀錄 |
| 歷史紀錄詳情 | `/history/<id>` | GET | 顯示單筆歷史紀錄詳細內容 |
| 捐獻頁面 | `/donation/donate` | GET | 顯示捐香油錢頁面 |
| 捐獻處理 | `/donation/donate` | POST | 處理捐獻，寫入紀錄 |
| 分享結果 | `/share/<id>` | GET | 產生可分享的算命結果頁面 / 連結 |
