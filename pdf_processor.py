import fitz  # PyMuPDF
import os
from typing import List, Tuple
from PIL import Image
import io

def convert_pdf_to_images(pdf_path: str, output_dir: str = "output_images") -> List[Tuple[int, str, Image.Image]]:
    """
    Convert each page of a PDF to images using PyMuPDF
    
    Args:
        pdf_path (str): Path to the PDF file
        output_dir (str): Directory to save the output images
    Returns:
        list: List of tuples containing (page_number, image_path, PIL.Image)
    """
    # Validate PDF file exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        return []
        
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    try:
        # Open PDF file
        print(f"Converting PDF: {pdf_path}")
        pdf_document = fitz.open(pdf_path)
        results = []
        
        # Process each page
        for page_num in range(len(pdf_document)):
            # Get the page
            page = pdf_document[page_num]
            
            # Convert page to image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Save image
            image_path = os.path.join(output_dir, f'p{page_num + 1}.png')
            img.save(image_path, 'PNG')
            print(f"Saved: {image_path}")
            
            results.append((page_num + 1, image_path, img))
            
        pdf_document.close()
        print(f"\nSuccessfully converted {len(results)} pages to images in '{output_dir}' directory.")
        return results
        
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")
        return []