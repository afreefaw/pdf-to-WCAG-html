import anthropic
import base64
from io import BytesIO
import os
import json
import re
from datetime import datetime
from PIL import Image

def encode_image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_input_images(input_dir="input_images"):
    """
    Get all images from input directory
    
    Args:
        input_dir (str): Directory containing input images
        
    Returns:
        list: List of tuples (index, image_path, PIL.Image)
    """
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return []
        
    images_data = []
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    try:
        # Get all valid image files
        image_files = []
        for filename in os.listdir(input_dir):
            if os.path.splitext(filename)[1].lower() in valid_extensions:
                # Extract page number from filename (e.g., p1.png -> 1)
                match = re.search(r'p(\d+)', filename)
                if match:
                    page_num = int(match.group(1))
                    image_files.append((page_num, filename))
        
        # Sort by page number
        image_files.sort(key=lambda x: x[0])
        
        # Process sorted images
        for page_num, filename in image_files:
            image_path = os.path.join(input_dir, filename)
            try:
                with Image.open(image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    # Create a copy in memory
                    img_copy = img.copy()
                    images_data.append((page_num, image_path, img_copy))
            except Exception as e:
                print(f"Error loading image {filename}: {str(e)}")
                continue
                    
        print(f"\nFound {len(images_data)} valid images in '{input_dir}' directory.")
        return images_data
        
    except Exception as e:
        print(f"Error reading input directory: {str(e)}")
        return []

def process_images_with_claude(images_data, prompt, api_key, output_dir="output_images"):
    """
    Process images with Claude API
    
    Args:
        images_data (list): List of tuples (index, image_path, PIL.Image)
        prompt (str): Prompt to send to Claude
        api_key (str): Anthropic API key
        output_dir (str): Base directory for saving responses
    """
    if not api_key:
        print("Error: No API key provided")
        return False
        
    # Create responses directory
    responses_dir = os.path.join(output_dir, "claude_responses")
    if not os.path.exists(responses_dir):
        os.makedirs(responses_dir)
        
    try:
        # Initialize Claude client with required API version
        client = anthropic.Client(
            api_key=api_key,
        )
        
        # Process each image
        for idx, image_path, image in images_data:
            try:
                # Encode image
                base64_image = encode_image_to_base64(image)
                
                # Send to Claude
                print(f"Processing page {idx} ({os.path.basename(image_path)})...")
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": base64_image
                                    }
                                }
                            ]
                        }
                    ]
                )
                
                # Save Claude's response with simple p{idx}.json format
                response_path = os.path.join(responses_dir, f'p{idx}.json')
                with open(response_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'image': os.path.basename(image_path),
                        'prompt': prompt,
                        'response': message.content[0].text
                    }, f, indent=2)
                print(f"Saved response to: {response_path}")
                
            except Exception as e:
                print(f"Error processing page {idx}: {str(e)}")
                continue
                
        return True
        
    except Exception as e:
        print(f"Error initializing Claude client: {str(e)}")
        return False
