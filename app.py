from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Purchase
from logic import get_most_common_product
from datetime import datetime
import os

import pymysql

app = Flask(__name__)

# Configuration de la base de données pour Railway ou Local
db_url = os.environ.get('DATABASE_URL') or os.environ.get('MYSQL_URL')

if db_url:
    # Railway fournit parfois mysql://, SQLAlchemy préfère mysql+pymysql://
    if db_url.startswith('mysql://'):
        db_url = db_url.replace('mysql://', 'mysql+pymysql://', 1)
    
    # Gestion du certificat self-signed pour Railway
    # Option 1: Ajouter les paramètres SSL dans l'URL
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_url + "?ssl_mode=REQUIRED&ssl_verify_identity=false"
    
    # Option 2 (plus propre avec SQLAlchemy): Utiliser connect_args
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'ssl': {
                'ssl_mode': 'DISABLED'  # ou 'REQUIRED' avec verify_identity=False selon le besoin
            }
        }
    }
else:
    # Configuration locale
    db_user = 'famille_user'
    db_password = 'FAWAZ1*3*5*7*'
    db_host = 'localhost'
    db_name = 'family_expenses'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev_secret_key' # For flash messages

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    # U.S-3: Trié par date décroissante
    # U.S-4: Filtrage par période
    
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    query = Purchase.query
    
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            query = query.filter(Purchase.date >= start_date)
        except ValueError:
            pass # Ignore invalid date format
            
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            query = query.filter(Purchase.date <= end_date)
        except ValueError:
            pass

    purchases = query.order_by(Purchase.date.desc()).all()
    
    # U.S-5: Produit le plus utilisé
    # U.S-6: Montant total
    total_expenses = sum(p.price for p in purchases)
    
    product_names = [p.product_name for p in purchases]
    most_common_product = get_most_common_product(product_names)

    return render_template('index.html', purchases=purchases, total_expenses=total_expenses, most_common_product=most_common_product)

@app.route('/add', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        date_str = request.form.get('date')
        shopper_name = request.form.get('shopper_name')
        
        # U.S-2: Validation
        errors = []
        if not product_name:
            errors.append("Le nom du produit est requis.")
        if not price:
            errors.append("Le prix est requis.")
        else:
            try:
                price = float(price)
                if price <= 0:
                    errors.append("Le prix doit être positif.")
            except ValueError:
                errors.append("Le prix doit être un nombre valide.")
        
        date_obj = datetime.utcnow()
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                errors.append("Date invalide.")
        
        if not shopper_name:
            errors.append("Le nom de l'acheteur est requis.")
            
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add.html', 
                                   product_name=product_name, 
                                   price=price, 
                                   date=date_str, 
                                   shopper_name=shopper_name)
        
        new_purchase = Purchase(
            product_name=product_name,
            price=price,
            date=date_obj,
            shopper_name=shopper_name
        )
        db.session.add(new_purchase)
        db.session.commit()
        flash('Achat enregistré avec succès!', 'success')
        return redirect(url_for('index'))
        
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
