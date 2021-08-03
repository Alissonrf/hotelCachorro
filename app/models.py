from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app.config import Config

class Usuario(UserMixin,db.Model):
    data_nasc = db.Column(db.String, nullable=False)
    email = db.Column(db.String(256))
    telefone = db.Column(db.String(16))
    cpf = db.Column(db.String(20),primary_key=True)
    nome = db.Column(db.String,nullable=False)
    nome_usuario = db.Column(db.String(16),unique=True,nullable=False)
    senha_hash = db.Column(db.String(256))
    data_criado = db.Column(db.DateTime,default=datetime.utcnow)
    quantidade_cachorros = db.Column(db.Integer,nullable=False)
    isAdmin = db.Column(db.Boolean)

    def get_id(self):
        return self.cpf

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)  
    def set_cpf(self,cpf):
        if self.validar_cpf(cpf):
            self.cpf = cpf
    def validar_cpf(self,cpf):
        if type(cpf) == int:
            cpf = str(cpf)

        cpf = cpf.strip()

        if "-" in cpf:
            cpf = cpf.replace("-","")
        
        if "." in cpf:
            cpf = cpf.replace(".","")
        
        #segmenta o cpf em duas partes
        cpf_sem_verific = cpf[:9]
        digitos_ver = cpf[9:]

        #geração do suposto primeiro digito verificador 
        soma1 = 0
        contagem1 = 10
        for numero in cpf_sem_verific:
            soma1 += int(numero) * contagem1
            contagem1 -= 1

        resto_soma1 = soma1%11
        if resto_soma1 < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto_soma1
        
        digito1 = str(digito1)
        segundo_passo = cpf_sem_verific + digito1

        soma2 = 0
        contagem2 = 11
        for numero in segundo_passo:
            soma2 += int(numero) * contagem2
            contagem2 -= 1
        
        resto_soma2 = soma2%11
        if resto_soma2 < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto_soma2
        
        digito2 = str(digito2)
        
        if digito1 == digitos_ver[0] and digito2 == digitos_ver[1]:
            return True
        return False

    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'

class Cachorro(db.Model):
    id = db.Column(db.String,primary_key=True)
    nome = db.Column(db.String,nullable=False)
    idade = db.Column(db.Integer,nullable=False)
    raca = db.Column(db.String,nullable=False)
    porte = db.Column(db.String,nullable=False)
    cpf_dono = db.Column(db.String,db.ForeignKey('usuario.cpf'),nullable=False)
    nome_dono = db.Column(db.String,db.ForeignKey('usuario.nome_usuario'),nullable=False)

    def __repr__(self):
        return f'<Cachorro {self.id} do dono {self.nome_dono}>'


class Quarto(db.Model):
    numero = db.Column(db.Integer,nullable=False,primary_key=True)
    limite_cachorros = db.Column(db.Integer,nullable=False)
    horario_inicio = db.Column(db.Time,nullable=False)
    horario_fim = db.Column(db.Time,nullable=False)
    preco_hora = db.Column(db.String,nullable=False)
    nota_media = db.Column(db.String,default='0.0')
    nota_total = db.Column(db.Float,default=0.0)
    quant_hospedagem = db.Column(db.Integer,default=0)
    quant_avaliacao = db.Column(db.Integer,default=0)
    suporta_pequeno = db.Column(db.Boolean)
    suporta_medio = db.Column(db.Boolean)
    suporta_grande = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'<Quarto {self.numero}>'

class Agendamento(db.Model):
    id = db.Column(db.String,primary_key=True)
    data = db.Column(db.Date,nullable=False)
    horario_inicio = db.Column(db.Time,nullable=False)
    horario_fim = db.Column(db.Time,nullable=False)
    id_cachorro = db.Column(db.String,db.ForeignKey('cachorro.id'),nullable=False) 
    num_quarto = db.Column(db.Integer,db.ForeignKey('quarto.numero'),nullable=False)
    preco_total = db.Column(db.Float)
    cpf = db.Column(db.String,db.ForeignKey('usuario.cpf'),nullable=False)
    avaliado = db.Column(db.Boolean,default=False)
    permissao_avaliar = db.Column(db.Boolean,default=False)
    contabilizado = db.Column(db.Boolean,default=False)

    def __repr__(self):
        return f'<Agendamento {id}>'


