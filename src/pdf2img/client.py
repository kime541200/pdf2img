import httpx
from pathlib import Path
from typing import List
import zipfile
import io

class Pdf2ImgClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def convert(
        self, 
        pdf_path: Path, 
        output_dir: Path,
        fmt: str = "png",
        dpi: int = 200
    ) -> List[str]:
        """
        Convert a PDF file by sending it to the remote server.
        Downloads and extracts the resulting images to output_dir.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"File {pdf_path} not found")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        url = f"{self.base_url}/convert"
        
        files = {'file': (pdf_path.name, open(pdf_path, 'rb'), 'application/pdf')}
        params = {'fmt': fmt, 'dpi': dpi}

        try:
            with httpx.Client(timeout=None) as client: # timeout=None because conversion can take time
                response = client.post(url, files=files, params=params)
                response.raise_for_status()

                # The response is a zip file
                zip_content = io.BytesIO(response.content)
                with zipfile.ZipFile(zip_content) as zip_ref:
                    zip_ref.extractall(output_dir)
                    return [str(output_dir / name) for name in zip_ref.namelist()]
        
        except httpx.RequestError as e:
            raise RuntimeError(f"Network error occurred: {e}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Server returned error {e.response.status_code}: {e.response.text}")

