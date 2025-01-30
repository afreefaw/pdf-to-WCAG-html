import anthropic
import base64
from io import BytesIO
import os
import json
from datetime import datetime
from PIL import Image

def encode_image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_input_images(input_dir="output_images"):
    """
    Get all images from specified directory
    
    Args:
        input_dir (str): Directory containing images to process
        
    Returns:
        list: List of tuples (index, image_path, PIL.Image)
    """
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' not found.")
        return []
        
    images_data = []
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    try:
        for idx, filename in enumerate(sorted(os.listdir(input_dir)), 1):
            if os.path.splitext(filename)[1].lower() in valid_extensions:
                image_path = os.path.join(input_dir, filename)
                try:
                    with Image.open(image_path) as img:
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        # Create a copy in memory
                        img_copy = img.copy()
                        images_data.append((idx, image_path, img_copy))
                except Exception as e:
                    print(f"Error loading image {filename}: {str(e)}")
                    continue
                    
        print(f"\nFound {len(images_data)} valid images in '{input_dir}' directory.")
        return images_data
        
    except Exception as e:
        print(f"Error reading directory: {str(e)}")
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
        # Initialize Claude client with API version header
        client = anthropic.Client(api_key=api_key)
        
        # Process each image
        for idx, image_path, image in images_data:
            try:
                # Encode image
                base64_image = encode_image_to_base64(image)
                
                # Send to Claude
                print(f"Sending image {idx} ({os.path.basename(image_path)}) to Claude...")
                message = client.messages.create(
                    max_tokens=4096,
                    model="claude-3-5-sonnet-20241022",
                    messages=[{
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64_image
                                }
                            }
                        ]
                    }]
                )
                
                # Save Claude's response
                response_path = os.path.join(responses_dir, f'p{idx}.json')
                with open(response_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'image': os.path.basename(image_path),
                        'prompt': prompt,
                        'response': message.content[0].text
                    }, f, indent=2)
                print(f"Saved Claude's response to: {response_path}")
                
            except Exception as e:
                print(f"Error processing image {idx} with Claude: {str(e)}")
                continue
                
        return True
        
    except Exception as e:
        print(f"Error initializing Claude client: {str(e)}")
        return False