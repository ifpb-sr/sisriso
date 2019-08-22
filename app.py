import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.environ.get('DYNO'):
    # Produção no heroku
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SECRET_KEY'] = 'hard to guess string'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

  
class Dentista(db.Model):
    __tablename__ = 'dentistas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128))
    
    
    @staticmethod
    def inserir_tipos():
        db.session.add(Dentista(nome="Ismael"))
        db.session.add(Dentista(nome="Alves"))
        db.session.add(Dentista(nome="Lima"))
        db.session.commit()
    

@app.route('/dentistas', methods=['GET'])
def dentistas():
    dentistas = Dentista.query.all()
    return render_template('dentistas/dentistas.html', dentistas=dentistas)

@app.route('/home', methods=['GET'])
def index():
    return render_template('base.html', dentistas=dentistas)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Dentista=Dentista)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    upgrade()
    Dentista.inserir_tipos()
