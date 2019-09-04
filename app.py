import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

usam = db.Table("usam",
    db.Column('paciente_id', db.Integer, db.ForeignKey('PACIENTES.id')),
    db.Column('medico_id', db.Integer, db.ForeignKey('MEDICOS.id'))
) #REVISADO

possuem = db.Table("possuem",
    db.Column('paciente_id', db.Integer, db.ForeignKey('PACIENTES.id')),
    db.Column('doenca_id', db.Integer, db.ForeignKey('DOENCAS.id'))
) #REVISADO

class Pacientes(db.Model): #REVISADO
    __tablename__ = 'PACIENTES'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64))
    tipoSanguinio = db.Column(db.String(3))
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(1))
    rg = db.Column(db.String(14))
    cpf = db.Column(db.String(14), unique=True)
    profissao = db.Column(db.String(64))
    indicacao = db.Column(db.String(64))
    # endereco
    rua = db.Column(db.String(64))
    bairo = db.Column(db.String(64))
    cep = db.Column(db.String(9))
    numero = db.Column(db.String(5))
    cidade = db.Column(db.String(34))
    estado = db.Column(db.String(34))
    # fim endereco
    #urgencia
    urgenciaNome = db.Column(db.String(64))
    urgenciaTelefone = db.Column(db.String(11))
    observacao = db.Column(db.String(128))
    #fim urgencia
    #MATR convenio
    matr = db.Column(db.String(14))
    #-------------------------------
    
    contatos_id = db.Column(db.Integer, db.ForeignKey('CONTATOS.id')) #1-N REVISADO
    convenios = db.relationship('Convenios', backref='PACIENTES') #REVISADO
    
    doencas = db.relationship('Doencas', backref='PACIENTES')
    anamneses = db.relationship('Anamneses', uselist=False, backref='PACIENTES')  #REVISADO
    
    medicamentos = db.relationship('Medicamentos',
                                    secondary='usam',
                                    backref=db.backref('PACIENTES', lazy='dynamic'),
                                    lazy='dynamic') #REVISADO
    
    doencas = db.relationship('Doencas',
                                    secondary='possuem',
                                    backref=db.backref('PACIENTES', lazy='dynamic'),
                                    lazy='dynamic') #REVISADO N-N
    
    '''@staticmethod
    def inserir_tipos():
        db.session.add(Dentista(nome="Ismael"))
        db.session.add(Dentista(nome="Alves"))
        db.session.add(Dentista(nome="Lima"))
        db.session.commit()'''

        
class Convenios(db.Model): #REVISADO
    __tablename__ = 'CONVENIOS'
    id = db.Column(db.Integer, primary_key=True) #VERIFICAR
    tipoPlano = db.Column(db.String(32))
    
    paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id')) #REVISADO

class Contatos(db.Model): #REVISADO
    __tablename__ = 'CONTATOS'
    id = db.Column(db.Integer, primary_key=True) #VERIFICAR
    contato = db.Column(db.String(11))
    
    pacientes = db.relationship('Pacientes', backref='CONTATOS') #REVISADO

class Anamneses(db.Model):
    __tablename__ = 'ANAMNESES'
    id = db.Column(db.Integer, primary_key=True) #VERIFICAR
    
    bemSaude = db.Column(db.Boolean)
    sobCuidado = db.Column(db.Boolean)
    motivoCuidado = db.Column(db.String(64), default="")
    usaMedicamentos = db.Column(db.Boolean)
    hemorragia = db.Column(db.Boolean)
    fumante = db.Column(db.Boolean)
    tempoFuma = db.Column(db.Interval)
    cigarrosPorDia = db.Column(db.Integer)
    
    #--------------------RELATIONSHIPS e FKs-------------------
    
    paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id'))
    #medicamentos = db.relationship('Medicamentos', backref='ANAMNESES') #FK
    #medicoResponsavel = db.relationship('Medicos', backref='ANAMNESES') #FK

receitas = db.Table ('receitas', 
    db.Column('medicamentos_id', db.Integer, db.ForeignKey('MEDICAMENTOS.id')),
    db.Column('medicos_id', db.Integer, db.ForeignKey('MEDICOS.id'))
) #REVISADO

class Medicamentos(db.Model):
    __tablename__ = 'MEDICAMENTOS'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(32))
    
    medicos = db.relationship('Medicos', 
                            secondary=receitas,
                            backref=db.backref('MEDICAMENTOS', lazy='dynamic'),
                            lazy='dynamic') #REVISADO
    #anamneses_id = db.Column(db.Integer, db.ForeignKey('ANAMNESES.id'))

class Medicos(db.Model):
    __tablename__ = 'MEDICOS'
    id = db.Column(db.Integer, primary_key=True) #VERIFICAR
    
    #telefone = db.relationship('Contatos', backref='MEDICOS') #TELEFONE DO MEDICO

class Doencas(db.Model):
    __tablename__ = 'DOENCAS'
    id = db.Column(db.String(4), primary_key=True) #VERIFICAR
    Doencas = db.Column(db.String(20))
    
    #paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id'))

@app.route('/')
def inicio():
    return render_template("base.html")


@app.route('/clientes')
def clientes():
    return render_template('clientes/clientes.html')


@app.route('/dentista/cadastro', methods = ['POST', 'GET'])
def cadastroDentista():
    if request.method == 'POST':
        nome = request.form['nome']
        sexo = request.form['sexo']
        email = request.form['email']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        estado = request.form['estado']
    return render_template('dentistas/cadastrodentista2.html')


@app.route('/procedimentos')
def procedimentos():
    return render_template('procedimentos/procedimentos.html')


@app.route('/secretaria/cadastro')
def cadastroSecretaria():
    return render_template('secretaria/cadastroSecretaria.html')


@app.route('/relatorio')
def relatorio():
    return render_template('Relatorio.html')


'''@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Dentista=Dentista)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    upgrade()
    Dentista.inserir_tipos()'''
