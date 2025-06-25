from PIL import Image
import sys
import os
# Add the root directory to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_path)
from config import IMAGE_PATHS, PDF_PATH


def save_images_to_pdf(image_paths, pdf_path):
    # Load and convert all images
    pages = [Image.open(p).convert("RGB") for p in image_paths]

    if pages:
        # Overwrite the PDF with new images
        pages[0].save(
            pdf_path,
            save_all=True,
            append_images=pages[1:]
        )
        print(f"PDF saved successfully to {pdf_path}.")
    else:
        print("No images to save.")

if __name__ == "__main__":
    # Run the function
    save_images_to_pdf(IMAGE_PATHS, PDF_PATH)
