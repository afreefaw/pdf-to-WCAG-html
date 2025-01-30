import json
import os
import re

def extract_html_from_response(response_text):
    # Find content between ```html and ``` tags
    match = re.search(r'```html\n(.*?)```', response_text, re.DOTALL)
    if match:
        return match.group(1)
    return None

def process_claude_responses():
    # Get the directory of claude responses
    responses_dir = os.path.join('output_images', 'claude_responses')
    output_dir = 'output_images'  # Save HTML files in output_images

    # Check if responses directory exists
    if not os.path.exists(responses_dir):
        print(f"Error: Claude responses directory not found at {responses_dir}")
        return False

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Store all HTML content with their indices for combined file
    all_content = []

    # Get all JSON files and sort them numerically by page number
    files = [(int(f.split('.')[0].replace('p', '')), f) 
             for f in os.listdir(responses_dir) if f.endswith('.json')]
    files.sort(key=lambda x: x[0])  # Sort by page number

    # Process each JSON file
    for idx, filename in files:
        json_path = os.path.join(responses_dir, filename)
        
        # Read JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract HTML content
        html_content = extract_html_from_response(data['response'])
        
        if html_content:
            html_filename = f'p{idx}.html'
            html_path = os.path.join(output_dir, html_filename)
            
            # Save individual HTML content
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Created {html_path}")

            # Store content for combined file
            all_content.append((idx, html_content))
        else:
            print(f"No HTML content found in {filename}")

    # Create combined HTML file if we have content
    if all_content:
        # Sort by index
        all_content.sort(key=lambda x: x[0])
        
        # Combine all HTML content
        combined_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Combined Pages</title>
    <style>
        .page-break {
            page-break-after: always;
            margin-bottom: 30px;
            border-bottom: 1px solid #ccc;
        }
        .page-number {
            text-align: center;
            font-weight: bold;
            margin: 20px 0;
        }
    </style>
</head>
<body>
"""
        
        # Add each page's content
        for idx, content in all_content:
            combined_html += f'<div class="page-number">Page {idx}</div>\n'
            combined_html += content + '\n'
            if idx != all_content[-1][0]:  # Don't add page break after last page
                combined_html += '<div class="page-break"></div>\n'
        
        combined_html += "</body>\n</html>"
        
        # Save combined HTML file
        combined_path = os.path.join(output_dir, 'combined.html')
        with open(combined_path, 'w', encoding='utf-8') as f:
            f.write(combined_html)
        print(f"\nCreated combined HTML file: {combined_path}")
        return True
    return False

if __name__ == '__main__':
    process_claude_responses()