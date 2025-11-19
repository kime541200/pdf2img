import os
import sys
from pathlib import Path

# Add the src directory to the python path so we can import pdf2img if not installed
# This is just for the sake of this example running from the repo root
sys.path.append(str(Path(__file__).parent.parent / "src"))

from pdf2img.client import Pdf2ImgClient

def main():
    # 1. 設定檔案路徑
    # 假設我們在專案根目錄執行此腳本，或者直接指定絕對路徑
    base_dir = Path(__file__).parent.parent
    pdf_path = base_dir / "assets" / "example.pdf"
    output_dir = base_dir / "examples" / "output_images"

    # 檢查測試檔案是否存在
    if not pdf_path.exists():
        print(f"錯誤: 找不到測試檔案 {pdf_path}")
        print("請確保 'assets/example.pdf' 存在")
        return

    print(f"準備轉換檔案: {pdf_path}")
    print(f"輸出目錄: {output_dir}")

    # 2. 初始化 Client
    # 請確保 Server 已經啟動 (docker-compose up 或 uvicorn)
    server_url = os.getenv("PDF2IMG_SERVER_URL", "http://localhost:8000")
    client = Pdf2ImgClient(base_url=server_url)

    try:
        # 3. 呼叫轉換 API
        print("正在上傳並轉換中...")
        images = client.convert(
            pdf_path=pdf_path,
            output_dir=output_dir,
            fmt="png",
            dpi=200
        )

        # 4. 顯示結果
        print(f"\n轉換成功！共產生 {len(images)} 張圖片：")
        for img in images:
            print(f"- {img}")
            
    except Exception as e:
        print(f"\n轉換失敗: {e}")
        print("提示: 請確認 Server 是否已啟動 (http://localhost:8000)")

if __name__ == "__main__":
    main()

