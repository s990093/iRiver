# backend-iRiver

後端專案基於 **Django** 框架，提供音樂管理、任務管理、評論系統、Docker 支援以及網路安全相關功能。專案結構清晰，便於擴展和維護。

## 功能列表

### 核心模組

* **Administration**：管理後台，提供用戶和系統管理功能。
* **Discover**：內容推薦與搜尋功能，支援網路安全優化。
* **Music**：音樂播放與列表管理，支援新搜尋樣式。
* **Reviews**：評論系統，結合網路安全檢查。
* **Task**：任務管理系統，包含 Docker 任務和自動化功能。
* **Token / User**：用戶身份管理，支援資料夾功能和搜尋條件優化。
* **iRiver / lib / pytube / static / templates**：專案支援模組，包含 Docker 設定、資源管理、靜態檔案與郵件模板。

### 其他功能

* **Docker 支援**：專案包含 Dockerfile，可快速建立容器化環境。
* **網路安全**：部分模組加入安全性增強（如 Discover、Task、Reviews、Static）。
* **多功能搜尋**：Token 模組提供新的搜尋條件，提高搜尋精準度。
* **資料夾管理**：用戶模組支援新增資料夾功能，便於音樂和任務管理。
* **Requirements 管理**：包含 `requirements.txt` 與 `requirements-linux.txt`，支援不同系統安裝依賴。

---

## 專案結構

```
backend-iRiver/
├─ Administration/
├─ Discover/
├─ Docker/
├─ Music/
├─ Reviews/
├─ Sandbox/
├─ Task/
├─ Token/
├─ Track/
├─ User/
├─ iRiver/
├─ lib/
├─ pytube/
├─ static/
├─ templates/
├─ manage.py
├─ requirements.txt
├─ requirements-linux.txt
├─ Dockerfile
├─ README.md
├─ LICENSE.md
└─ robots.txt
```

---

## 安裝與部署

### 1. 環境建置

使用 Python 3.10+，建議搭配虛擬環境：

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
# 若在 Linux，可用:
pip install -r requirements-linux.txt
```

### 3. 設定資料庫

專案預設使用 Django ORM，可修改 `settings.py` 配置資料庫（SQLite / MySQL / PostgreSQL）。

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 啟動專案

```bash
python manage.py runserver
```

專案將在 `http://127.0.0.1:8000` 啟動。

### 5. Docker 部署（可選）

```bash
docker build -t backend-iriver .
docker run -p 8000:8000 backend-iriver
```

---

## 更新紀錄 (簡要)

* 修正音樂播放列表問題 (`palylistSet`)
* 新增資料夾功能
* 改善搜尋功能及精準度
* Docker 支援與任務自動化
* 加強網路安全模組
* 更新依賴與 Docker 設定

---

## 開發建議

1. 建議使用 **VSCode + Python 插件** 開發，便於管理 Django 專案。
2. 新增模組時，記得在 `INSTALLED_APPS` 註冊。
3. 注意 `static` 與 `templates` 路徑設定，以確保前後端資源正確引用。

---
