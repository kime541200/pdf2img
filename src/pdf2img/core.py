import os
from pathlib import Path
from typing import List, Union
from pdf2image import convert_from_path, convert_from_bytes

def convert_pdf_to_images(
    pdf_path_or_bytes: Union[str, Path, bytes],
    output_folder: Union[str, Path] = None,
    fmt: str = "png",
    dpi: int = 200
) -> List[str]:
    """
    Convert a PDF file to a list of images.
    
    Args:
        pdf_path_or_bytes: Path to the PDF file or bytes of the PDF.
        output_folder: Folder to save the images. If None, images are not saved to disk but returned as PIL objects (not fully supported in this simplified return type signature, logic below handles saving).
        fmt: Image format (e.g., 'png', 'jpeg').
        dpi: DPI for the conversion.
        
    Returns:
        List of file paths to the saved images.
    """
    
    if isinstance(pdf_path_or_bytes, (str, Path)):
        images = convert_from_path(str(pdf_path_or_bytes), dpi=dpi)
    else:
        images = convert_from_bytes(pdf_path_or_bytes, dpi=dpi)
        
    saved_files = []
    
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        base_name = "page"
        if isinstance(pdf_path_or_bytes, (str, Path)):
             base_name = Path(pdf_path_or_bytes).stem
             
        for i, image in enumerate(images):
            image_path = output_path / f"{base_name}_{i + 1}.{fmt}"
            image.save(str(image_path), fmt.upper())
            saved_files.append(str(image_path))
            
    return saved_files

async def a_convert_pdf_to_images(
    pdf_path_or_bytes: Union[str, Path, bytes],
    output_folder: Union[str, Path] = None,
    fmt: str = "png",
    dpi: int = 200
) -> List[str]:
    """
    Asynchronous wrapper for convert_pdf_to_images.
    """
    import asyncio
    from functools import partial
    
    loop = asyncio.get_event_loop()
    func = partial(convert_pdf_to_images, pdf_path_or_bytes, output_folder, fmt, dpi)
    return await loop.run_in_executor(None, func)

