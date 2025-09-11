# Password Generator & Checker (Flask)


A simple **Flask web application** that generates strong random passwords and checks their safety based on length and character variety.  
It features a **modern glassmorphism UI**, password generation, and a visual safe/unsafe indicator.


## Features

- Generate secure random passwords with adjustable length.
- Checks password strength (length, uppercase, lowercase, digits, symbols).
- Modern responsive UI with gradient & glassmorphism styling.
- Built with **Flask**, **HTML/CSS**, and Python standard libraries.

## Installation

1. **Clone or download** the repository:
```bash
git clone https://github.com/yourusername/password-app.git
cd password-app
```
2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```
3. Install Flask
`pip install flask`

## Running the App
`python app.py`
Then open your browser at
`http://127.0.0.1:5000/`

## Password Safety Rules
- A password is considered safe if:
- It meets the minimum length (default 12).
- Contains at least one lowercase letter.
- Contains at least one uppercase letter.
- Contains at least one digit.
- Contains at least one special character.

