import os
import sys
import argparse
from pdf_processor import convert_pdf_to_images
from claude_processor import process_images_with_claude, get_input_images
from extract_html import process_claude_responses

def read_prompt(prompt_file="prompt.txt"):
    """Read prompt from file"""
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading prompt file: {str(e)}")
        return None

def check_config():
    """Check if config.py exists and has API key"""
    try:
        import config
        if not hasattr(config, 'ANTHROPIC_API_KEY') or not config.ANTHROPIC_API_KEY:
            print("\nError: ANTHROPIC_API_KEY not found in config.py")
            print("Please copy config.example.py to config.py and add your API key")
            return None
        return config.ANTHROPIC_API_KEY
    except ImportError:
        print("\nError: config.py not found")
        print("Please copy config.example.py to config.py and add your API key")
        return None

def process_pdf_directory(pdf_dir="PDF", output_dir="output_images"):
    """Process all PDFs in the specified directory"""
    if not os.path.exists(pdf_dir):
        print(f"\nError: '{pdf_dir}' directory not found")
        print(f"Please create a '{pdf_dir}' directory and place your PDF files in it")
        return False
    
    pdfs = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    if not pdfs:
        print(f"\nNo PDF files found in '{pdf_dir}' directory")
        return False
    
    for pdf in pdfs:
        pdf_path = os.path.join(pdf_dir, pdf)
        print(f"\nProcessing {pdf}...")
        images_data = convert_pdf_to_images(pdf_path, output_dir)
        if not images_data:
            print(f"Failed to process {pdf}")
            continue
        print(f"PDF pages have been converted to images in '{output_dir}' directory")
    return True

def handle_pdf(args):
    """Handle PDF conversion command"""
    # Convert PDF to images
    images_data = convert_pdf_to_images(args.pdf_path, args.output_dir)
    
    if not images_data:
        print("No images were generated. Exiting.")
        sys.exit(1)
    
    print(f"\nPDF pages have been converted to images in '{args.output_dir}' directory.")

def handle_claude(args):
    """Handle Claude processing command"""
    # Check API key
    api_key = check_config()
    if not api_key:
        sys.exit(1)
    
    # Read prompt
    prompt = read_prompt()
    if not prompt:
        print("Error: No prompt found in prompt.txt")
        sys.exit(1)
    
    # Get images from output directory
    images_data = get_input_images(args.output_dir)
    if not images_data:
        print(f"No valid images found in {args.output_dir} directory. Exiting.")
        sys.exit(1)
    
    # Process with Claude
    print("\nProcessing images with Claude...")
    process_images_with_claude(images_data, prompt, api_key, args.output_dir)

def handle_html(args):
    """Handle HTML extraction command"""
    print("\nExtracting HTML from Claude responses...")
    if not process_claude_responses():
        print("Failed to extract HTML from Claude responses.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='PDF and Image Processing Tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # PDF command
    pdf_parser = subparsers.add_parser('pdf', help='Convert PDF to images')
    pdf_parser.add_argument('pdf_path', help='Path to the PDF file')
    pdf_parser.add_argument('--output-dir', default='output_images',
                           help='Output directory for images (default: output_images)')
    
    # Claude command
    claude_parser = subparsers.add_parser('claude', 
                                        help='Process images from output_images directory with Claude')
    claude_parser.add_argument('--output-dir', default='output_images',
                             help='Output directory for images and Claude responses (default: output_images)')
    
    # HTML command
    html_parser = subparsers.add_parser('html',
                                      help='Extract HTML from Claude responses')
    
    args = parser.parse_args()
    
    # If no command provided, process PDFs from PDF directory
    if not args.command:
        if process_pdf_directory():
            # If PDFs were processed successfully, continue with Claude processing
            api_key = check_config()
            if not api_key:
                sys.exit(1)
            
            prompt = read_prompt()
            if not prompt:
                print("Error: No prompt found in prompt.txt")
                sys.exit(1)
            
            images_data = get_input_images("output_images")
            if images_data:
                print("\nProcessing images with Claude...")
                process_images_with_claude(images_data, prompt, api_key, "output_images")
                print("\nExtracting HTML from Claude responses...")
                if not process_claude_responses():
                    print("Failed to extract HTML from Claude responses.")
                    sys.exit(1)
            else:
                print("No valid images found in output_images directory. Exiting.")
                sys.exit(1)
    elif args.command == 'pdf':
        handle_pdf(args)
    elif args.command == 'claude':
        handle_claude(args)
    elif args.command == 'html':
        handle_html(args)
    else:
        parser.print_help()
        print("\nNote: To use Claude integration:")
        print("1. Copy config.example.py to config.py")
        print("2. Add your Anthropic API key to config.py")
        print("3. Modify prompt.txt with your desired prompt")
        print("4. Ensure your images are in the output_images directory")
        sys.exit(1)

if __name__ == "__main__":
    main()