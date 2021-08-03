from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, BooleanField, SubmitField, RadioField,DecimalField,FloatField,TextAreaField
from wtforms_alchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField,TimeField
from wtforms.validators import Length, EqualTo, DataRequired,Email,NumberRange

class CadastroUsuarioForm(FlaskForm):
    nome = StringField("Nome completo",[DataRequired()])
    cpf = StringField("CPF",[DataRequired()])
    data_nasc = DateField("Data de nascimento", validators= [DataRequired()],format='%Y-%m-%d')
    email = StringField("Email",[DataRequired(),Length(max=256),Email()])
    nome_usuario = StringField("Nome de usuário",[DataRequired(),Length(min=4,max=16)])
    senha = PasswordField("Senha",validators=[DataRequired()])
    confirm_senha = PasswordField("Confirmação de senha",validators=[DataRequired(),EqualTo('senha')])
    telefone = StringField("Telefone")
    cadastrar = SubmitField("Cadastrar")

class CadastroAdministradorForm(FlaskForm):
    cod_acesso_segredo = PasswordField("Código secreto",[DataRequired()])
    enviar = SubmitField("Enviar")

class LoginUsuarioForm(FlaskForm):
    nome_usuario = StringField("Nome de usuário", validators=[DataRequired(),Length(min=4,max=16)])
    senha = PasswordField("Senha", validators=[DataRequired(),Length(min=4,max=16)])
    login = SubmitField("Logar")

class CadastroCachorroForm(FlaskForm):
    nome = StringField("Nome",[DataRequired()]) 
    idade = IntegerField("Idade",[DataRequired()])
    raca = StringField("Raça",[DataRequired()])
    porte = RadioField("Porte (selecione um tamanho)",choices=[('Pequeno','menor ou igual a 35 cm de altura'),
                                                ('Medio','entre 36 e 49 cm de altura'),
                                                ('Grande','maior que 49 cm de altura')])
    cadastrar_cachorro = SubmitField("Cadastrar")

class CadastroQuartoForm(FlaskForm):
    num_quarto = IntegerField("Número do quarto",[DataRequired()])
    limite_cachorros = IntegerField("Número máximo de cachorros",[DataRequired(),NumberRange(min=1)])
    horario_inicial_funcionamento = TimeField("Aberto após",[DataRequired()],format='%H:%M')
    horario_final_funcionamento = TimeField("Fechado após",[DataRequired()],format='%H:%M')
    preco_hora = FloatField("Preço por hora",[DataRequired()])
    porte_pequeno = BooleanField("Porte pequeno")  
    porte_medio = BooleanField("Porte médio")
    porte_grande = BooleanField("Porte grande")
    criar = SubmitField("criar quarto")

class AgendamentoHospedagemForm(FlaskForm):
    data = DateField("Data da hospedagem", validators= [DataRequired()],format='%Y-%m-%d')
    horario_inicio = TimeField("Inicio da hospedagem",[DataRequired()])
    horario_fim = TimeField("Fim da hospedagem",[DataRequired()])
    cachorro = QuerySelectField("Selecione um cachorro",validators=[DataRequired()],get_label="nome",allow_blank=False)
    agendar = SubmitField("Agendar Hospedagem")
    calcular_preco = SubmitField("Calcular preço hospedagem")

class AvaliacaoNotaForm(FlaskForm):  
    nota = FloatField("Nota do quarto",[DataRequired(),NumberRange(min=0,max=5)])
    enviar = SubmitField("Enviar avaliação")