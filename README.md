# HRSM System for Software Development Process (A252 Group 7)

A Flask-based Human Resource Management (HRSM) System built for the Software Development Process course.

---

### 🛠️ Development Guidelines

The frontend and backend architectural components follow standard Flask structure conventions:

* **HTML Templates:** Placed inside the `templates/` directory.
* **Stylesheets:** Placed inside the `static/css/` directory.
* **JavaScript:** Placed inside the `static/js/` directory.
* **Core Backend:** Located within the `app/` directory (modules, controllers, routes, and database models).

---

### 🚀 Setup and Installation

Follow these steps sequentially to configure and run the application in your local environment.

#### 1. Clone the Repository
Pull the project repository from GitHub and navigate into the project directory:
`git clone https://github.com/RealBlank21/HRSM-G7`
`cd HRSM-G7`

#### 2. Verify Python Installation
Ensure you have Python 3.8 or higher installed on your machine. You can verify this by checking your current version:
`python --version`

#### 3. Initialize a Virtual Environment
Isolate project dependencies by generating a clean Python virtual environment:
`python -m venv venv`

Activate the virtual environment based on your current Operating System:
* **Windows (Command Prompt):** `venv\Scripts\activate.bat`
* **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
* **macOS / Linux:** `source venv/bin/activate`

#### 4. Install Dependencies
Ensure your virtual environment is active, then install all project-specific dependencies:
`pip install -r requirements.txt`

#### 5. Configure Environment Settings
Create a file named `.env` in the root folder of your project workspace to initialize essential application secrets:
```text
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```
### 6. Run the local Server
Launch the Flask development server using the main execution file:
`python app.py`

Once initialized, open your web browser and view the application live at: `http://127.0.0.1:5000/`