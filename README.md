# PDF to WCAG 2.0 Conversion Tool

This tool helps convert PDF documents into WCAG 2.0 compliant format. The process involves two main steps:
1. Converting PDF pages to images
2. Processing these images with Claude AI to create accessible content

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

### Step 1: Convert PDF to Images
1. Place your PDF file in the project folder
2. In Git Bash, run:
   ```
   python main.py pdf "YourPDFFile.pdf"
   ```
   Replace "YourPDFFile.pdf" with your actual PDF filename
3. The converted images will be saved in the `output_images` folder

### Step 2: Process with Claude
1. Ensure your images are in the `output_images` folder
2. Check that `prompt.txt` contains your desired instructions for Claude
3. In Git Bash, run:
   ```
   python main.py claude
   ```
4. The processed results will be saved in the same `output_images` folder

## Directory Structure
- `output_images/`: Contains both converted PDF pages and Claude's processed results
- `scripts/`: Contains setup and utility scripts