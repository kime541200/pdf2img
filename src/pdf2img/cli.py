import typer
from pathlib import Path
from typing import Optional
from .core import convert_pdf_to_images

app = typer.Typer()

@app.command()
def convert(
    pdf_path: Path = typer.Argument(..., help="Path to the PDF file to convert"),
    output_dir: Path = typer.Option(..., "--output", "-o", help="Directory to save images"),
    fmt: str = typer.Option("png", "--format", "-f", help="Output image format (png, jpeg, etc.)"),
    dpi: int = typer.Option(200, "--dpi", "-d", help="DPI for conversion")
):
    """
    Convert a PDF file to images.
    """
    if not pdf_path.exists():
        typer.echo(f"Error: File {pdf_path} not found.", err=True)
        raise typer.Exit(code=1)

    try:
        saved_files = convert_pdf_to_images(pdf_path, output_dir, fmt, dpi)
        typer.echo(f"Successfully converted {pdf_path.name} to {len(saved_files)} images in {output_dir}")
        for f in saved_files:
            typer.echo(f"- {f}")
    except Exception as e:
        typer.echo(f"Error converting PDF: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

