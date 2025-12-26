import typer
from pathlib import Path
from typing import Optional
from .core import convert_pdf_to_images

app = typer.Typer()

@app.command()
def convert(
    path: Path = typer.Argument(..., help="Path to the PDF file or directory containing PDFs"),
    output_dir: Path = typer.Option(..., "--output", "-o", help="Directory to save images"),
    fmt: str = typer.Option("png", "--format", "-f", help="Output image format (png, jpeg, etc.)"),
    dpi: int = typer.Option(200, "--dpi", "-d", help="DPI for conversion"),
    pages: Optional[str] = typer.Option(None, "--pages", "-p", help="Specific pages to convert (e.g., '1,3,5-7')")
):
    """
    Convert a PDF file or all PDFs in a directory to images.
    """
    if not path.exists():
        typer.echo(f"Error: Path {path} not found.", err=True)
        raise typer.Exit(code=1)

    pdf_files = []
    if path.is_file():
        if path.suffix.lower() == ".pdf":
            pdf_files.append(path)
        else:
            typer.echo(f"Error: {path} is not a PDF file.", err=True)
            raise typer.Exit(code=1)
    elif path.is_dir():
        pdf_files = list(path.glob("*.pdf"))
        if not pdf_files:
            typer.echo(f"No PDF files found in {path}.")
            return

    for pdf_path in pdf_files:
        # Create a subfolder for each PDF within the output directory
        current_output = output_dir / pdf_path.stem
        current_output.mkdir(parents=True, exist_ok=True)

        try:
            saved_files = convert_pdf_to_images(pdf_path, current_output, fmt, dpi, pages)
            typer.echo(f"Successfully converted {pdf_path.name} to {len(saved_files)} images in {current_output}")
        except Exception as e:
            typer.echo(f"Error converting {pdf_path.name}: {e}", err=True)
            if len(pdf_files) == 1:
                raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

