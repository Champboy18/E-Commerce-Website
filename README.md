E-Commerce Website (Flask + SQLite)

This is a simple e-commerce website built with Flask, SQLite, HTML/CSS, and Jinja templates.
It includes:
- Homepage with featured products
- Category & search filtering
- Product details page
- Working cart system
- SQLite database with sample products
- Editable product images and details

HOW TO RUN THE PROJECT
1. Install Python 3.10+ (check using: py --version)
2. Open the project folder:
   cd ecommerce_option_b_fixed
3. Create & activate virtual environment:
   py -m venv .venv
   .venv\Scripts\activate  (Windows)
4. Install dependencies:
   pip install -r requirements.txt
5. Start server:
   py app.py
6. Initialize database (first time only):
   Visit http://localhost:5000/init

EDITING THE DATABASE
Use SQLiteStudio → Open database.db → Table: Products → Edit fields → Write Changes

UPDATING PRODUCT IMAGES
Use direct image URLs (ending in .jpg/.png), or store images in static/images/ and set URL:
   /static/images/myphoto.jpg

PROJECT STRUCTURE
- app.py
- database.db
- requirements.txt
- schema.sql
- sample_data.sql
- templates/
- static/
- Procfile

TECH STACK
- Python (Flask)
- SQLite
- HTML + CSS
- Jinja2 Templates
- Session-based Cart
