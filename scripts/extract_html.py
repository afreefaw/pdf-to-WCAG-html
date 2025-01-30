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
    # Get the directory of claude responses relative to the script location
    responses_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'output_images', 'claude_responses')
    output_dir = os.path.dirname(responses_dir)  # Save HTML files in output_images

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Store all HTML content with their indices for combined file
    all_content = []

    # Process each JSON file in the directory
    for filename in sorted(os.listdir(responses_dir)):  # Sort to process in order
        if filename.endswith('.json'):
            json_path = os.path.join(responses_dir, filename)
            
            # Read JSON file
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract HTML content
            html_content = extract_html_from_response(data['response'])
            
            if html_content:
                # Extract index from filename (p{idx}.json) and create HTML filename
                idx = filename.split('.')[0].replace('p', '')
                html_filename = f'p{idx}.html'
                html_path = os.path.join(output_dir, html_filename)
                
                # Save individual HTML content
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"Created {html_path}")

                # Store content for combined file
                all_content.append((int(idx), html_content))
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

if __name__ == '__main__':
    process_claude_responses()