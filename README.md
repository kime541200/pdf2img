# PDF to Image Converter (pdf2img)

這是一個基於 Python 的工具，用於將 PDF 文件逐頁轉換為圖片。支援 CLI 介面操作、Docker Server 部署，以及 Client 端函式庫調用。現在也支援透過 Web UI 進行操作。

## 功能

*   **轉換核心**: 將 PDF 每一頁轉換為圖片 (支援 PNG, JPEG 等格式)
*   **CLI 工具**: 方便的命令列操作
*   **REST API Server**: 基於 FastAPI 的遠端轉換服務
*   **Client 函式庫**: 方便整合至 Python 專案
*   **Web UI**: 基於 Streamlit 的圖形化操作介面

## 系統需求

本工具依賴 `poppler`。

*   **macOS**: `brew install poppler`
*   **Linux (Debian/Ubuntu)**: `sudo apt-get install poppler-utils`
*   **Windows**: 請下載 poppler 二進位檔案並加入 PATH。

## 安裝

### 本地開發安裝

建議先建立虛擬環境：

```bash
# 建立 venv
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows
```

您可以根據需求選擇安裝部分套件：

```bash
# 安裝完整功能 (CLI, Server, Client, UI)
pip install -e ".[all]"

# 僅安裝 Client 函式庫 (適用於只需要呼叫遠端 API 的專案)
pip install -e ".[client]"

# 僅安裝 Server
pip install -e ".[server]"

# 僅安裝 UI
pip install -e ".[ui]"

# 僅安裝基本 CLI 功能
pip install -e .
```

## 使用方法

### 1. CLI 介面

安裝後，可以直接使用 `pdf2img` 指令：

```bash
# 基本用法
pdf2img path/to/file.pdf --output ./output_images

# 指定格式與 DPI
pdf2img path/to/file.pdf --output ./output_images --format jpeg --dpi 300
```

### 2. Web UI (圖形介面)

如果您安裝了 `.[ui]` 或 `.[all]`，可以使用圖形介面來操作：

**本地啟動 UI:**

```bash
# 確保已啟動 Server (如果需要轉換功能)
# 另開終端機執行: uvicorn pdf2img.server:app --reload

# 啟動 UI
pdf2img-ui
```

瀏覽器將自動開啟 `http://localhost:8501`。

### 3. Docker 部署 (Server + UI)

使用 Docker Compose 快速啟動完整的伺服器與 UI 環境：

```bash
docker-compose up --build
```

*   **Web UI**: `http://localhost:8501`
*   **API Server**: `http://localhost:8000` (文件: `/docs`)

### 4. Client 函式庫

如果您希望在自己的 Python 程式中呼叫遠端的轉換服務：

```python
from pdf2img.client import Pdf2ImgClient

client = Pdf2ImgClient(base_url="http://localhost:8000")

# 上傳 PDF 並取得轉換後的圖片
images = client.convert(
    pdf_path="path/to/document.pdf", 
    output_dir="./remote_results",
    fmt="png",
    dpi=200
)

print(f"轉換完成: {images}")
```

### 5. 快速範例 (Quick Start)

專案中包含了一個範例腳本與測試檔案，您可以直接執行以體驗功能：

**前提**：請確保 Server 已啟動 (透過 Docker 或 uvicorn)。

```bash
# 執行範例腳本 (會將 assets/example.pdf 轉換並存至 examples/output_images)
python examples/usage_demo.py
```

或者使用 CLI 測試：

```bash
pdf2img assets/example.pdf --output examples/output_images
```

### 6. 關於 DPI 設定

DPI (Dots Per Inch) 決定了轉換後圖片的解析度與清晰度。

*   **72 - 96 DPI**: 適用於螢幕瀏覽，檔案較小，轉換速度快。
*   **150 - 200 DPI** (預設): 適用於一般用途，在品質與檔案大小間取得平衡。
*   **300+ DPI**: 適用於列印或後續需要進行 OCR (文字辨識) 的場景，檔案較大，轉換時間較長。

您可以透過 CLI 的 `--dpi` 參數、UI 的滑桿或是 Client 函式庫的參數來調整此數值。

## 專案結構

```
.
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
└── src
    └── pdf2img
        ├── __init__.py
        ├── cli.py      # CLI 進入點
        ├── client.py   # Client 函式庫
        ├── core.py     # 核心轉換邏輯
        ├── launcher.py # UI 啟動腳本
        ├── server.py   # FastAPI Server
        └── ui.py       # Streamlit UI 應用程式
```

## License

本專案採用 [MIT License](LICENSE) 授權。
