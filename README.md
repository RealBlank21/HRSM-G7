# HRSM System for Software Development Process A252 Group 7

A Flask-based Human Resource Management (HRSM) System.

---

### Dev Note
* .html -> templates directory
* .css -> static/css
* .js -> static/js
* backend code -> app directory

---

### How to run

1. Download Python
Ensure Python 3.x is installed on your system.

2. Set up a Virtual Environment
Run the following command to create a virtual environment:
python -m venv venv

Activate it based on your OS:
- Windows (CMD): venv\Scripts\activate.bat
- Windows (PowerShell): .\venv\Scripts\Activate.ps1

3. Install Dependencies
Run the install command inside your activated virtual environment:
`pip install -r requirements.txt`

4. Configure Environment Variables
Put the .env in the root directory.

5. Run the Application
Execute the main script:
`python app.py`

Access the local server at: http://127.0.0.1:5000/