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

tomar = db.table('tomar',
        db.Column('paciente_id', db.Integer, db.ForeignKey('PACIENTES.id')),
        db.Column('medicamento_id', db.Integer,db.ForeignKey('MEDICAMENTOS.id'))
)
possuir = db.table('possuir',
        db.Column('paciente_id', db.Integer, db.ForeignKey('PACIENTES.id')),
        db.Column('doenca_id', db.Integer, db.ForeignKey('DOENCAS.id')),
)
receitar = db.table('receitar',
        db.Column('medicamento_id', db.Integer, db.ForeignKey('MEDICAMENTOS.id')),
        db.Column('medico_id', db.Integer, db.ForeignKey('MEDICOS.id')),
)

class Pacientes(db.Model):
    __tablename__ = 'PACIENTES'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64))
    tipoSanguinio = db.Column(db.String(3))
    idade = db.Column(db.Integer)
    sexo = db.Column(db.String(1))
    rg = db.Column(db.String(14))
    cpf = db.Column(db.String(14))
    profissao = db.Column(db.String(64))
    indicacao = db.Column(db.String(64))
    ###ENDERECO###
    rua = db.Column(db.String(64))
    bairro = db.Column(db.String(64))
    cep = db.Column(db.String(9))
    numero = db.Column(db.String(5))
    cidade = db.Column(db.String(32))
    estado = db.Column(db.String(2))
    ###URGENCIA###
    urgenciaNome = db.Column(db.String(64))
    urgenciaTelefone = db.Column(db.String(11))
    observacao = db.Column(db.String(128))
    ###MATRICULA Convenio###
    matr = db.Column(db.String(14))
    ###CHAVES ESTRANGEIRAS###
    convenio_id = db.Column(db.Integer, db.ForeignKey('CONVENIOS.id'), default=0) #PK
    ###RELACIONAMENTOS###
    anamnese = db.relationship('Anamneses', backref='PACIENTES', uselist=False)
    contatos = db.relationship('Contatos', backref='PACIENTES')
    medicamentos = db.relationship('Medicamentos',
                secondary=tomar,
                backref=db.backref('PACIENTES', lazy='dynamic'),
                lazy='dynamic')
    doencas = db.relationship('Doencas',
                secondary=possuir,
                backref=db.backref('PACIENTES', lazy='dynamic'),
                lazy='dynamic')

class Anamneses(db.Model):
    __tablename__ = 'ANAMNESES'
    id = db.Column(db.Integer, primary_key=True)
    bemSaude = db.Column(db.Boolean)
    sobCuidado = db.Column(db.Boolean)
    motivoCuidado = db.Column(db.String(64))
    usaMedicamentos = db.Column(db.Boolean)
    hemorragia = db.Column(db.Boolean)
    fumante = db.Column(db.Boolean)
    tempoFuma = db.Column(db.Interval)
    cigarrosPorDia = db.Column(db.Integer)
    ###Chaves Estrangeiras###
    paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id')) #PK

class Contatos(db.Model):
    __tablename__ = 'CONTATOS'
    id = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(11))
    paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id')) #PK

class Convenios(db.Model):
    __tablename__ = 'CONVENIOS'
    id = db.Column(db.Integer, primary_key=True)
    tipoPlano = db.Column(db.String(16))
    pacientes = db.relationship('Pacientes', backref='CONVENIOS')

class Doencas(db.Model):
    __tablename__ = 'DOENCAS'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(32))

class Medicamentos(db.Model):
    __tablename__ = 'MEDICAMENTOS'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(32))
    medicos = db.relationship('Medicos',
                secondary=receitar,
                backref=db.backref('MEDICAMENTOS', lazy='dynamic'),
                lazy='dynamic')

class Medicos(db.Model):
    __tablename__ = 'MEDICOS'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(32))

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
