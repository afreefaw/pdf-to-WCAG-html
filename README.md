# PDF to WCAG 2.0 Conversion Tool

This tool helps convert PDF documents into WCAG 2.0 compliant format. The process involves three main steps:
1. Converting PDF pages to images
2. Processing these images with Claude AI to create accessible content
3. Extracting HTML content from Claude's responses

## Setup Instructions (Windows)

### 1. Install Git Bash
1. Download Git Bash from: https://git-scm.com/download/win
2. Run the installer
3. Use all default options during installation
4. After installation, you can find "Git Bash" in your Start menu

### 2. Install Python
1. Download Python **3.10** from: https://www.python.org/downloads/windows/
2. Run the installer
3. **IMPORTANT**: Check the box that says "Add Python to PATH" during installation

### 3. Get the Project Files
1. Create a folder where you want to store the project
2. Open Git Bash (from Start menu)
3. Navigate to your folder using the `cd` command, for example:
   ```
   cd "C:/Users/YourUsername/Documents"
   ```
4. Clone the project (or download and extract if provided as a ZIP file)

### 4. Set Up the Project
1. In Git Bash, navigate to the project folder
2. Run these commands one by one:
   ```
   source scripts/env.sh
   ```
   This will create a virtual environment and install required packages
   Note this may not work if you are on a work network.

### 5. Configure Claude API
1. Copy `config.example.py` and rename to `config.py`
2. Open `config.py` in a text editor
3. Replace `your-api-key-here` with your Anthropic API key (https://console.anthropic.com/)
4. Save the file

## Using the Tool

### Automatic Processing
The simplest way to use the tool is to:
1. Create a `PDF` directory in the project folder
2. Place your PDF files in the `PDF` directory
3. In Git Bash, run:
   ```
   python main.py
   ```
This will automatically:
- Process all PDFs in the `PDF` directory
- Convert them to images
- Process the images with Claude
- Extract the HTML content

### Manual Step-by-Step Processing

If you prefer more control, you can run each step manually:

#### Step 1: Convert PDF to Images
1. Place your PDF file in the project folder
2. In Git Bash, run:
   ```
   python main.py pdf "YourPDFFile.pdf"
   ```
   Replace "YourPDFFile.pdf" with your actual PDF filename
3. The converted images will be saved in the `output_images` folder

#### Step 2: Process with Claude
1. Ensure your images are in the `output_images` folder
2. In Git Bash, run:
   ```
   python main.py claude
   ```
3. The processed results will be saved in the same `output_images` folder

#### Step 3: Extract HTML
1. After Claude has processed the images, run:
   ```
   python main.py html
   ```
2. This will create:
   - Individual HTML files for each page (p1.html, p2.html, etc.)
   - A combined.html file containing all pages with proper styling and page breaks

## Directory Structure
- `PDF/`: Place your PDF files here for automatic processing
- `output_images/`: Contains converted PDF pages, Claude's processed results, and generated HTML files
- `scripts/`: Contains setup and utility scripts