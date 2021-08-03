from app import app,db,login
from flask import render_template,redirect, request, flash
from app.forms import CadastroAdministradorForm
from app.forms import CadastroCachorroForm
from app.forms import CadastroUsuarioForm
from app.forms import LoginUsuarioForm
from app.forms import CadastroQuartoForm
from app.forms import AgendamentoHospedagemForm
from app.forms import AvaliacaoNotaForm
from app.models import Usuario,Cachorro,Quarto,Agendamento
from flask_login import login_user,logout_user
from flask_login import login_required, current_user
from app.config import Config
from datetime import timedelta,datetime,date,time


@login.user_loader
def load_user(nome_usuario):
    return Usuario.query.get(str(nome_usuario))

@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html",title="Home")

@app.route('/cadastrar_usuario', methods=['get','post'])
def cadastrar_usuario():
    form = CadastroUsuarioForm()
    if request.method == "POST":
        usuario = Usuario(email=form.email.data,telefone=form.telefone.data,
                          data_nasc=form.data_nasc.data,nome=form.nome.data,
                          nome_usuario=form.nome_usuario.data,quantidade_cachorros=0,
                          isAdmin=False)
        usuario.set_cpf(form.cpf.data)
        usuario.set_senha(form.senha.data)
        try:
            db.session.add(usuario)
            db.session.commit()
            return redirect("/index")           
        except:
            return "Houve um erro no cadastro"    
    elif request.method == "GET":
        return render_template("cadastro_usuario.html",title="Cadastrar Usuario",form=form)

@app.route('/perfil_usuario',methods=['get','post'])
@login_required
def perfil_usuario():
    cachorros = Cachorro.query.filter_by(cpf_dono=current_user.cpf).all()
    return render_template("perfil.html",cachorros=cachorros)

@app.route('/logar_usuario',methods=['get','post'])
def logar_usuario():
    form = LoginUsuarioForm()
    erro = None
    if request.method == "POST":
        user = Usuario.query.filter_by(nome_usuario=form.nome_usuario.data).first()
        if user is not None:
            if user.check_password(form.senha.data):
                login_user(user)
                return redirect("/")
            else:
                erro = "Senha inválida"
        else:
            erro = "Usuário inválido"
    return render_template("login_usuario.html", title="Login", form=form, erros = erro)


@app.route('/logout_usuario',methods=['get','post'])
@login_required
def logout_usuario():
    logout_user()
    return redirect('/')

@app.route('/cadastrar_cachorro',methods=['get','post'])
@login_required
def cadastrar_cachorro():
    form = CadastroCachorroForm()
    if request.method == "POST":
        cachorro = Cachorro(nome=form.nome.data,idade=form.idade.data,
                            raca=form.raca.data,porte=form.porte.data,
                            cpf_dono=current_user.cpf,id=(current_user.nome_usuario+"_"+str(current_user.quantidade_cachorros+1)),
                            nome_dono=current_user.nome_usuario)
        try:
            db.session.add(cachorro)
            current_user.quantidade_cachorros = current_user.quantidade_cachorros + 1 
            db.session.commit()
            return redirect("/index")           
        except:
            return "Houve um erro no cadastro"  
        
    return render_template("cadastro_cachorro.html",title="Cadastro Cachorro",form=form)

@app.route('/deletar_cachorro/<string:id>',methods=['get','post'])
@login_required
def deletar_cachorro(id):
    deletar = Cachorro.query.get_or_404(id)
    try:
        db.session.delete(deletar)
        db.session.commit()
        return redirect('/perfil_usuario')
    except:
        return "Erro ao deletar Cachorro"

@app.route('/modificar_cachorro/<string:id>',methods=['get','post'])
@login_required
def modificar_cachorro(id):
    cachorro = Cachorro.query.get_or_404(id)
    form = CadastroCachorroForm()
    form.nome.default = cachorro.nome
    form.idade.default = cachorro.idade
    form.raca.default = cachorro.raca
    form.porte.default = cachorro.porte
    if request.method == "POST":
        cachorro.nome = form.nome.data
        cachorro.idade = form.idade.data
        cachorro.raca = form.raca.data
        cachorro.porte = form.porte.data

        try:
            db.session.commit()
            return redirect("/index")           
        except:
            return "Houve um erro na modificação do cachorro"  
        
    return render_template("modificar_cachorro.html",title="Modificar Cachorro",form=form,cachorro=cachorro)

@app.route('/modo_admin',methods=['get','post'])
@login_required
def modo_admin():
    form = CadastroAdministradorForm()
    erros = False
    config = Config()
    if request.method == "POST":
        if form.cod_acesso_segredo.data == config.get_segredo():
            current_user.isAdmin = True
            db.session.commit()
            return redirect("/")
        else:
            erros = "Código inválido"
    return render_template("virar_admin.html",title="Modo Administrador", erros = erros, form = form)

@app.route('/logout_admin',methods=['get','post'])
@login_required
def logout_admin():
    if current_user.isAdmin:
        current_user.isAdmin = False
        db.session.commit()
        return redirect('/')
    return "Erro ao sair do modo administrador"

@app.route('/cadastrar_quarto',methods=['get','post'])
@login_required
def cadastrar_quarto():
    if current_user.isAdmin:
        form = CadastroQuartoForm()
        if request.method == "POST":
            quarto = Quarto(numero=form.num_quarto.data,limite_cachorros=form.limite_cachorros.data,
                            horario_inicio=form.horario_inicial_funcionamento.data,quant_avaliacao=0,nota_total=0.0,
                            horario_fim=form.horario_final_funcionamento.data,quant_hospedagem=0,nota_media="0.0",
                            suporta_pequeno=form.porte_pequeno.data,suporta_medio=form.porte_medio.data,
                            suporta_grande=form.porte_grande.data,preco_hora=str(form.preco_hora.data),
                            )
            try:
                db.session.add(quarto)
                db.session.commit()
                return redirect("/")  
            except:
                return "Houve um erro no cadastro"
        return render_template("cadastro_quarto.html",form=form,title="Cadastrar Quarto")    
    else:
        return "Acesso negado. Você precisa estar no modo Administrador para criar um quarto "

@app.route('/quartos',methods=['get','post'])
@login_required
def quartos():
    quartos = Quarto.query.order_by(Quarto.preco_hora).all()
    return render_template("quartos.html",quartos=quartos,title="Quartos")

@app.route('/deletar_quarto/<int:numero>',methods=['get','post'])
@login_required
def deletar_quarto(numero):
    if current_user.isAdmin:
        deletar = Quarto.query.get_or_404(numero)
        try:
            db.session.delete(deletar)
            db.session.commit()
            return redirect('/quartos')
        except:
            return "Erro ao deletar quarto"
    else:
        return "Acesso negado"

@app.route('/modificar_quarto/<int:numero>',methods=['get','post'])
@login_required
def modificar_quarto(numero):
    if current_user.isAdmin:
        quarto = Quarto.query.get_or_404(numero)
        form = CadastroQuartoForm()

        form.num_quarto.data = quarto.numero
        form.limite_cachorros.default = quarto.limite_cachorros
        form.horario_inicial_funcionamento.default = quarto.horario_inicio
        form.horario_final_funcionamento.default = quarto.horario_fim
        form.preco_hora.default = quarto.preco_hora
        form.porte_pequeno.default = quarto.suporta_pequeno
        form.porte_medio.default = quarto.suporta_medio
        form.porte_grande.default = quarto.suporta_grande

        if request.method == "POST":
            quarto.numero = form.num_quarto.data
            quarto.limite_cachorros = form.limite_cachorros.data
            quarto.horario_inicio = form.horario_inicial_funcionamento.data
            quarto.horario_fim = form.horario_final_funcionamento.data
            quarto.preco_hora = form.preco_hora.data
            quarto.suporta_pequeno = form.porte_pequeno.data
            quarto.suporta_medio = form.porte_medio.data
            quarto.suporta_grande = form.porte_grande.data

            try:
                db.session.commit()
                return redirect('/quartos')

            except:
                return "Erro ao modificar dados do quarto"

        return render_template('modificar_quarto.html',form=form,quarto=quarto,title="Modificar Quarto")
    else:
        return "Acesso negado"

@app.route('/agendar/<int:numero>', methods=['get','post'])
@login_required
def agendar(numero):
    form = AgendamentoHospedagemForm()
    form.cachorro.query = Cachorro.query.filter_by(cpf_dono=current_user.cpf).all()
    quarto = Quarto.query.get_or_404(numero)
    preco = None
    erro = []
    if request.method == "POST":
        if form.agendar.data:
            data_hoje = date.today()
            hora_agora = datetime.now().time()
            cachorro = form.cachorro.data
            h1 = str(form.horario_inicio.data).replace(":","")
            h2 = str(form.horario_fim.data).replace(":","")
            id_criado = str((cachorro.id)+"_"+str(numero)+"_"+str(form.data.data)+"_"+h1+"_"+h2)
            #verifica porte se bate com o permitido pelo quarto
            if (cachorro.porte == "Pequeno" and quarto.suporta_pequeno) or (cachorro.porte == "Medio" and quarto.suporta_medio) or (cachorro.porte == "Grande" and quarto.suporta_grande):
                #não permitir agendar pro passado
                if (form.data.data > data_hoje) or (form.data.data == data_hoje and form.horario_inicio.data > hora_agora):
                    #não permitir colocar o horário final menor que o inicial
                    if form.horario_inicio.data < form.horario_fim.data:
                        #verificar se o horário bate com a disponibilidade do quarto
                        if form.horario_inicio.data >= quarto.horario_inicio and form.horario_fim.data <= quarto.horario_fim:
                            #verificar se o quarto não vai estar lotado nesse dia, baseado no limite do quarto 
                            agend_nesse_dia = Agendamento.query.filter_by(data=form.data.data,num_quarto=quarto.numero).all()
                            if len(agend_nesse_dia) < quarto.limite_cachorros:
                                #verificar se o cachorro já não vai estar ocupado nesse dia (em outro horário já marcado)
                                agend_cachorros_nesse_horario = Agendamento.query.filter_by(id_cachorro=cachorro.id,data=form.data.data,num_quarto=quarto.numero).all()
                                conflito_de_data = False
                                for agend in agend_cachorros_nesse_horario:
                                    if (form.horario_inicio.data >= agend.horario_inicio and form.horario_inicio.data <= agend.horario_fim) or (form.horario_fim.data >= agend.horario_inicio and form.horario_fim.data <= agend.horario_fim) or (form.horario_inicio.data <= agend.horario_inicio and form.horario_fim.data >= agend.horario_fim):
                                        conflito_de_data = True
                                        break

                                if not conflito_de_data:
                                    agendamento = Agendamento(horario_inicio = form.horario_inicio.data, horario_fim = form.horario_fim.data,
                                    preco_total = float(quarto.preco_hora) * calcular_intervalo_hora(form.horario_inicio.data,form.horario_fim.data),
                                    id_cachorro= cachorro.id, num_quarto= numero, cpf = current_user.cpf,data=form.data.data,id = id_criado)

                                    try:
                                        db.session.add(agendamento)
                                        db.session.commit()
                                        return redirect('/')
                                    
                                    except:
                                        erro = "Valores inválidos."

                                else:
                                    erro="O cachorro já tem um agendamento para esse horário"
                            else:
                                erro = "O número de vagas do quarto para essa data está cheio"
                        else:
                                erro = "O horário escolhido não está dentro do horário de funcionamento do quarto"
                    else:
                        erro = "O horário de início da hospedagem deve ser menor que o horário final"
                else:
                    erro = "A data e/ou hora solicitada já passou"
            else:
                erro = "Porte não suportado nesse quarto. Tente em outro"
        elif form.calcular_preco.data:
            preco =  float(quarto.preco_hora) * calcular_intervalo_hora(form.horario_inicio.data,form.horario_fim.data)
    return render_template("agendar.html",title="Agendar",form = form,quarto = quarto,preco = preco,erro = erro)

def calcular_intervalo_hora(comeco, fim):
    if comeco > fim:
        comeco, fim = fim, comeco

    delta = (fim.hour - comeco.hour) + (fim.minute - comeco.minute)/60 + (fim.second - comeco.second)/3600
    #print(f"DELTA DE {fim} - {comeco} = {delta}")
    return delta


@app.route('/agendamentos',methods=['get','post'])
@login_required
def agendamentos():
    agendamentos = Agendamento.query.filter_by(cpf = current_user.cpf).all()
    hoje = datetime.today()
    for agendamento in agendamentos:
        agend_data = agendamento.data
        agend_fim = agendamento.horario_fim
        quarto = Quarto.query.filter_by(numero=agendamento.num_quarto).first()
        if hoje.date() >= agend_data and hoje.time() >= agend_fim:
            if not agendamento.contabilizado:
                quarto.quant_hospedagem += 1
                agendamento.contabilizado = True 
                db.session.commit()

            if not agendamento.avaliado:
                agendamento.permissao_avaliar = True
            
    try:
        db.session.commit()
    except:
        return "Erro ao carregar agendamentos"
    return render_template("agendamentos.html",agendamentos=agendamentos, cachorro = Cachorro,title = "Agendamentos")

@app.route('/deletar_agendamento/<string:id>',methods=['get','post'])
@login_required
def deletar_agendamento(id):
    deletar = Agendamento.query.get_or_404(id)
    try:
        db.session.delete(deletar)
        db.session.commit()
        return redirect('/agendamentos')
    except:
        return "Erro ao deletar Agendamento"

@app.route('/avaliar_hospedagem/<string:id>',methods=['get','post'])
@login_required
def avaliar_hospedagem(id):
    form = AvaliacaoNotaForm()
    agendamento = Agendamento.query.get_or_404(id)
    agend_data = agendamento.data
    agend_fim = agendamento.horario_fim
    quarto = Quarto.query.filter_by(numero=agendamento.num_quarto).first()
    hoje = datetime.today()  
    if (hoje.year >= agend_data.year) and (hoje.month >= agend_data.month) and (hoje.day >= agend_data.day) and (hoje.hour >= agend_fim.hour) and not agendamento.avaliado:
        agendamento.permissao_avaliar = True
        if request.method == "POST":
            quarto.nota_total = quarto.nota_total + form.nota.data
            quarto.quant_avaliacao = quarto.quant_avaliacao + 1
            quarto.nota_media = str(quarto.nota_total / quarto.quant_avaliacao)
            agendamento.avaliado = True
            agendamento.permissao_avaliar = False
            try:
                db.session.commit()
                return redirect('/agendamentos')
            except:
                return "Erro ao avaliar quarto"
    
    return render_template("avaliacao_hospedagem.html",title="Avaliar Quarto",form=form,agendamento=agendamento)

@app.route("/sobre",methods=['get','post'])
def sobre():
    return render_template("sobre.html",title="Sobre")