import os
from pathlib import Path
from typing import List, Union, Optional
from pdf2image import convert_from_path, convert_from_bytes

def _parse_page_ranges(range_str: str) -> List[int]:
    """
    Parse a range string like "1,3,5-7" into a list of integers [1, 3, 5, 6, 7].
    """
    pages = set()
    for part in range_str.split(','):
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                pages.update(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                pages.add(int(part))
            except ValueError:
                continue
    return sorted(list(pages))

def convert_pdf_to_images(
    pdf_path_or_bytes: Union[str, Path, bytes],
    output_folder: Union[str, Path] = None,
    fmt: str = "png",
    dpi: int = 200,
    pages: Optional[str] = None
) -> List[str]:
    """
    Convert a PDF file to a list of images.
    
    Args:
        pdf_path_or_bytes: Path to the PDF file or bytes of the PDF.
        output_folder: Folder to save the images.
        fmt: Image format (e.g., 'png', 'jpeg').
        dpi: DPI for the conversion.
        pages: Page range string (e.g., "1,3,5-7").
        
    Returns:
        List of file paths to the saved images.
    """
    
    target_pages = None
    if pages:
        target_pages = _parse_page_ranges(pages)

    images = []
    if isinstance(pdf_path_or_bytes, (str, Path)):
        if target_pages:
            # pdf2image doesn't support arbitrary page lists, so we process groups of contiguous pages
            # for efficiency, or just convert each page one by one if they are sparse.
            # Here we'll convert each requested page range.
            current_range = []
            for p in target_pages:
                if not current_range or p == current_range[-1] + 1:
                    current_range.append(p)
                else:
                    images.extend(convert_from_path(str(pdf_path_or_bytes), dpi=dpi, 
                                                    first_page=current_range[0], last_page=current_range[-1]))
                    current_range = [p]
            if current_range:
                images.extend(convert_from_path(str(pdf_path_or_bytes), dpi=dpi, 
                                                first_page=current_range[0], last_page=current_range[-1]))
        else:
            images = convert_from_path(str(pdf_path_or_bytes), dpi=dpi)
    else:
        # bytes case - for simplicity, we convert all and then filter if target_pages is set
        # (pdf2image convert_from_bytes also supports first_page/last_page but arbitrary lists are hard)
        all_images = convert_from_bytes(pdf_path_or_bytes, dpi=dpi)
        if target_pages:
            for p in target_pages:
                if 1 <= p <= len(all_images):
                    images.append(all_images[p-1])
        else:
            images = all_images
        
    saved_files = []
    
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        base_name = "page"
        if isinstance(pdf_path_or_bytes, (str, Path)):
             base_name = Path(pdf_path_or_bytes).stem
             
        for i, image in enumerate(images):
            # If we selected specific pages, we might want to preserve the original page number in the filename
            page_num = i + 1
            if target_pages and len(target_pages) == len(images):
                page_num = target_pages[i]
                
            image_path = output_path / f"{base_name}_{page_num}.{fmt}"
            image.save(str(image_path), fmt.upper())
            saved_files.append(str(image_path))
            
    return saved_files

async def a_convert_pdf_to_images(
    pdf_path_or_bytes: Union[str, Path, bytes],
    output_folder: Union[str, Path] = None,
    fmt: str = "png",
    dpi: int = 200,
    pages: Optional[str] = None
) -> List[str]:
    """
    Asynchronous wrapper for convert_pdf_to_images.
    """
    import asyncio
    from functools import partial
    
    loop = asyncio.get_event_loop()
    func = partial(convert_pdf_to_images, pdf_path_or_bytes, output_folder, fmt, dpi, pages)
    return await loop.run_in_executor(None, func)

