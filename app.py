import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets.html5 import NumberInput
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
# import pdb
# pdb.set_trace()

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

class Pacientes(db.Model):
    __tablename__ = 'PACIENTES'
    id_paciente = db.Column(db.Integer, primary_key=True)
    nomePacientes = db.Column(db.String(64))
    tipoSanguinio = db.Column(db.String(3))
    dataNascimentoPaciente = db.Column(db.Date)
    sexo = db.Column(db.String(1))
    rg = db.Column(db.String(14))
    cpf = db.Column(db.String(14))
    profissao = db.Column(db.String(64))
    indicacao = db.Column(db.String(64))

    tipo = db.Column(db.String(16))
    logradouro = db.Column(db.String(64))
    bairro = db.Column(db.String(64))
    cep = db.Column(db.String(9))
    numero = db.Column(db.String(5))
    cidade = db.Column(db.String(32))
    estado = db.Column(db.String(2))

    medicamentos = db.Column(db.String(64), default="")
    medico = db.Column(db.String(64), default="")
    doencas = db.Column(db.String(64), default="")

    urgenciaNome = db.Column(db.String(64))
    urgenciaTelefone = db.Column(db.String(11))
    observacao = db.Column(db.String(128))

    matr = db.Column(db.String(14))

    convenio_id = db.Column(db.Integer, db.ForeignKey('CONVENIOS.id'), default=0) #PK

    anamnese = db.relationship('Anamneses', backref='PACIENTES', uselist=False)
    contatos = db.relationship('Contatos', backref='PACIENTES')
    
class Dentista(db.Model):
   __tablename__ = 'DENTISTA'
   cro_dentista = db.Column(db.Integer, primary_key=True)
   nomeDentista =  db.Column(db.String(30))
   especialidadeDentista = db.Columnn(db.String(50))
   telefone = db.Column(db.String(11))
   dataNascimentoDentista = db.Column(db.Date)

class Dentes(db.Model):
    __tablename__ = 'DENTES'
    codigo_dente = db.Column(db.Integer, primary_key=True))
    descricaoDente = db.Column(db.String(50))
    feito = db.Column(db.Boolean) 
    aFazer = db.Column(db.Boolean)

    
class Atendimento(db.Model):
    __tablename__ = 'ATENDIMENTO'
    codigo_atendimento = db.Column(db.Integer, primary_key=True)
    dataHora = db.Column(db.DataTime)
    valorAtendimento = db.Column(db.Float)
    paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id_paciente')) #PK
    dentista_id = db.Column(db.Integer, db.ForeignKey('DENTISTA.id_dentista')) #PK
    dente_cod = db.Column(db.Integer, db.ForeignKey('DENTE.codigo_dente')) #PK
    
class Anamneses(db.Model):
    __tablename__ = 'ANAMNESES'
    id_anamnese = db.Column(db.Integer, primary_key=True)
    bemSaude = db.Column(db.Boolean)
    sobCuidado = db.Column(db.Boolean)
    motivoCuidado = db.Column(db.String(64))
    usaMedicamentos = db.Column(db.Boolean)
    hemorragia = db.Column(db.Boolean)
    fumante = db.Column(db.Boolean)
    tempoFuma = db.Column(db.Interval)
    cigarrosPorDia = db.Column(db.Integer)
    Cardiopatia = db.Column(db.Boolean)
    Alergia = db.Column(db.Boolean)
    Cefaleia = db.Column(db.Boolean)
    Convulsao = db.Column(db.Boolean)
    Gastrite = db.Column(db.Boolean)
    Alcoolismo = db.Column(db.Boolean)
    Nefropatia = db.Column(db.Boolean)
    Diabetes = db.Column(db.Boolean)
    Herpes = db.Column(db.Boolean)
    Asma = db.Column(db.Boolean)
    Labirintite = db.Column(db.Boolean)
    Anemia = db.Column(db.Boolean)
    Hemofilia = db.Column(db.Boolean)
    Glaucoma = db.Column(db.Boolean)
    Hipertensao = db.Column(db.Boolean)
    Enxaqueca = db.Column(db.Boolean)
    Artrite = db.Column(db.Boolean)
    Hepatite    = db.Column(db.Boolean)
    Sinusite = db.Column(db.Boolean)
    Imunodeficiencia = db.Column(db.Boolean)
    Hapatopatia = db.Column(db.Boolean)
    Cancer = db.Column(db.Boolean)
    DisturbioNervoso = db.Column(db.Boolean)
    FebreReatica = db.Column(db.Boolean)
    ###Chaves Estrangeiras###
    paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id_paciente')) #PK
           
class Medicamentos(db.Model):
   __tablename__ = 'MEDICAMENTOS'
   id_medicamentos = db.Column(db.Integer, primary_key=True)
   nomeMedicamentos = db.Column(db.String(50))
   medicoResponsavel = db.Column(db.String(50))
   paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id')) #PK
                                 
class Contatos(db.Model):
    __tablename__ = 'CONTATOS'
    id = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(11))
    paciente_id = db.Column(db.Integer, db.ForeignKey('PACIENTES.id')) #PK

class Convenios(db.Model):
    __tablename__ = 'CONVENIOS'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64))
    tipoPlano = db.Column(db.String(16))
    pacientes = db.relationship('Pacientes', backref='CONVENIOS')

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
