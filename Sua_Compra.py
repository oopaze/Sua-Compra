#BIBLIOTECAS NATIVAS
from tkinter import *
from socket import *
import functools
from time import *

#MINHAS BIBLIOTECAS
from funcoes import *


    
#ABRE TELA COM INFORMAÇÕES DO USUARIO QUE TÁ TENTANDO BATER O PONTO    
def bater_ponto(matricula_entry, senha_entry, destruir1, destruir2, main_frame):
        global bgColor #PEGA AS INFORMAÇÕES DE INTERFACE PARA A FUNÇÃO
        global bgColorButton
        global fgColorButton
        dia_sem, mes, dia, horas, ano = asctime().split() #RETORNA AS HORAS E DATA E AS COLOCA EM VARIÁVEIS
        data = dia + '/' + mes + '/' + ano
        nomeArquivo = 'ponto/{0}.ini'.format(mes) #DEFINE O NOME DO DOCUMENTO QUE VAI RECEBER OS PONTOS A PARTIR DO MES
        if matricula_entry.get(): #TESTA E A MATRICULA É EXISTENTE
            mensagemEnvio = 'funcionario select matricula' 
            matriculas = enviar_socket(mensagemEnvio) #SOLICITA AO SOCKET AS MATRICULAS E AS ARMAZENA EM UMA VARIAVEL
            if matricula_entry.get() in matriculas.split(): #TESTA SE AS MATRICULAS ESTÃO DENTRO DA LISTA DADA PELO O SOCKET
                
                mensagemEnvio = 'funcionario select nome,senha,matricula matricula="{0}"'.format(matricula_entry.get())
                nome, senha, matricula = enviar_socket(mensagemEnvio).split() #SOLICITA AO SOCKET OS DADOS PESSOAIS LIGADOS A MATRICULA E AS ARMAZENA EM UMA VARIAVEL

                if senha_entry.get() == senha: #TESTA SE A SENHA ESTÁ CORRETA
                    destruir1.pack_forget() #DESTROI O FRAME DAS ENTRIES E BOTOES

                    #CRIA NOVOS FRAMES
                    main = Frame(main_frame, bg=bgColor)
                    frameConfirmacaoInfo = Frame(main, bg='White')
                    frameConfirmacaoButton = Frame(main, bg=bgColor)

                    #EMPACOTA OS NOVOS FRAMES
                    main.pack()
                    frameConfirmacaoInfo.pack(pady='5')
                    frameConfirmacaoButton.pack()

                    #CRIA LABELS PARA MOSTRAR AS INFORÇÕES TRAZIDAS PELO SOCKET
                    nomeLab = Label(frameConfirmacaoInfo, text=saving_name(nome, '!', ' '), font=('Times New Roman', '13'), bg = 'White', width='18')
                    matriculaLab = Label(frameConfirmacaoInfo, text=matricula, bg = 'White', font=('Times New Roman', '12'))
                    horaLab = Label(frameConfirmacaoInfo, text=data+' '+horas, bg = 'White', font=('Times New Roman', '12'))

                    #EMPACOTA LABELS NA TELA
                    nomeLab.pack(fill=X, padx='3')
                    matriculaLab.pack(side=LEFT, padx='6')
                    horaLab.pack(side=LEFT, padx='3')

                    #CRIA BUTTONS DE CONFIRMAÇÃO E CANCELAMENTO DO BATIMENTO DO PONTO
                    confirma = Button(frameConfirmacaoButton, width='13', bg=bgColorButton, fg=fgColorButton, text='Confirmar', command= lambda:batendoPonto(nome, data, horas, main, destruir1, destruir2, matricula_entry, senha_entry, mes))
                    cancela = Button(frameConfirmacaoButton, width='13', bg=bgColorButton, fg=fgColorButton,  text='Cancelar', command=lambda:voltar_ponto(main, destruir1, destruir2))

                    #EMPACOTA BOTES
                    confirma.pack(side=LEFT, padx='3', fill=X)
                    cancela.pack(side=LEFT, padx='3', fill=X)

#CRIANDO A TELA DO PONTO
def ponto_tela(main_frame, tela):
    #CHECANDO E ATUALIZANDO O LABEL DE HORA
    def check_hora():
        agora = strftime('%H:%M:%S') #ARMAZONA HORA/MINUTOS/SEGUNDOS EM AGORA
        if (agora != hora['text']): #TESTA SE A VARIAVEL agora É DIFERENTE AO O TEXTO NO LABEL hora
            hora['text'] = agora #FAZ O TEXTO DE hora IGUAL A agora
        hora.after(100, check_hora) #EXECUTA A FUNÇÃO A CADA 1 SEGUNDO
            
    
                
    #DESTRUINDO FRAME ANTERIOR
    main_frame.destroy()

    #CRIANDO FRAMES E CONSTRUINDO NOVA TELA
    main_frame = Frame(bg=bgColor)
    frame_horas = Frame(main_frame, bg=bgColor)
    frame_info = Frame(main_frame, bg=bgColor)
    fundo_info = Frame(frame_info, bg=bgColor)
    fundo_info_label = Frame(fundo_info, bg=bgColor)
    fundo_info_entry = Frame(fundo_info, bg=bgColor)
    
    #CRIANDO LABELS REFERENTE AS INFORMAÇÕES DE HORA E DATA
    data_lb = Label(frame_horas, text=data, bg='White', width='15', font=("MathJax_Main", '15'))   
    hora = Label(frame_horas, text=horas, bg='White', width='15', font=("MathJax_Main", '15'))

    #CRIANDO LABELS REFERENTE OS CAMPOS
    matricula_label = Label(fundo_info_label, text='Matricula', bg=bgColor)
    senha_label = Label(fundo_info_label, text='Senha', bg=bgColor)
    
    #CRIANDO ENTRIES REFERENTE OS CAMPOS
    matricula_entry = Entry(fundo_info_entry)
    senha_entry = Entry(fundo_info_entry, show='*')
    
    #CRIANDO BOTÕES PARA BATER O PONTO E VOLTAR
    bater_ponto_ = Button(frame_info, text='Bater ponto', width='20', bg=bgColorButton, fg='White', command=lambda:bater_ponto(matricula_entry, senha_entry, frame_info, frame_horas, main_frame))
    voltar = Button(frame_info, text='Voltar', width='20', bg=bgColorButton, fg='White', command=lambda: voltar_login(main_frame, empresa_login, contadorGerente, login))

    #EMPACOTANDO FRAMES
    main_frame.pack(pady=70)
    frame_horas.pack()
    frame_info.pack()
    fundo_info.pack(pady='5')
    fundo_info_label.pack(side=LEFT)
    fundo_info_entry.pack(side=LEFT)

    #EMPACOTANDO LABELS
    data_lb.pack(side=LEFT, padx='5')
    hora.pack(side=LEFT, pady='10')
    matricula_label.pack(padx='3')
    senha_label.pack(padx='3', pady='5')

    #EMPACOTANDO ENTRIES
    matricula_entry.pack(padx='3')
    senha_entry.pack(pady='5', padx='3')

    #EMPACOTANDO BOTÕES
    bater_ponto_.pack(side=LEFT, pady='5', padx='5')
    voltar.pack(side=LEFT, padx='5')

    #EXECUTANDO FUNÇÃO QUE ATUALIZA A HORA
    check_hora()


    
#ABRE A TELA EMPRESA LOGIN
def empresa_login(login):
    #TENTA FAZER O LOGIN
    def try_login():
        nonlocal mensagem #TRÁS A VARIAVEL MENSAGEM PARA DENTR DESSA FUNCAO 
        if cpf.get() and len(cpf.get()) == 11 and senha.get(): #TESTA SE SENHA ESTÁ DENTRO DO PADRÃO
            mensagem_envio = 'funcionario select cpf,setor,senha cpf="{0}"'.format(cpf.get()) #PREPARA COMANDO AO SOCKET
            try:
                cpfBanco, setorBanco, senhaBanco = enviar_socket(mensagem_envio).split() #SOLICITA E ARMAZENA DADOS SOLICITADOS
            except Exception as e:
                cpfBanco, setorBanco = enviar_socket(mensagem_envio).split()       
            
            varTipo = setor_string(str(setorBanco)) #TRANSFORMA INT DE varTipo EM UMA STRING
        
            if (cpfBanco == cpf.get() and senhaBanco == senha.get()): #TESTA SE O CPF E SENHA PASSADOS CORRESPONDEM AOS DO BANCO
                if varTipo == 'Gerente': #TESTA O TIPO DE LOGIN
                    gerente(main_frame, login, cpf.get()) #EXECUTA FUNÇÃO REFERENTE O TIPO
                elif varTipo == 'Estoquista': #TESTA O TIPO DE LOGIN
                    tela_estoque(main_frame, login, 1) #EXECUTA FUNÇÃO REFERENTE O TIPO
                elif varTipo == 'Caixa': #TESTA O TIPO DE LOGIN
                    telaCaixa(main_frame, login, bgColor, bgColorButton, fgColorButton, 1) #EXECUTA FUNÇÃO REFERENTE O TIPO
            else:
                mensagem["text"] = "CPF OU SENHA INCORRETO" #MOSTRA QUE OS DADOS ESTÃO INCORRETOS
        else:
            mensagem["text"] = "CPF OU SENHA INCORRETO" #MOSTRA QUE OS DADOS ESTÃO INCORRETOS

    #CONFIGURA A JANELA
    login.geometry("400x300+200+150")
    login.title("Sua Compra")
    login.resizable(0, 0)
    login['bg'] =  bgColor

        
    #CRIA FRAMES E SUBFRAMES
    main_frame = Frame(login, bg=bgColor)
    frame_mens = Frame(main_frame, bg=bgColor)
    frame_info = Frame(main_frame, bg=bgColor)
    frame_campos = Frame(frame_info, bg=bgColor)
    frame_campos_label = Frame(frame_campos, bg=bgColor)
    frame_campos_entry = Frame(frame_campos, bg=bgColor)
    frame_button = Frame(frame_info, bg=bgColor, pady='5')
    frame_button_1 = Frame(frame_button, bg=bgColor)
    frame_button_2 = Frame(frame_button, bg=bgColor)

    #EMPACOTA FRAMES E SUBFRAMES
    main_frame.pack(pady='30')
    frame_mens.pack()
    frame_info.pack()
    frame_campos.pack()
    frame_campos_label.pack(side=LEFT)
    frame_campos_entry.pack(side=LEFT)
    frame_button.pack()
    frame_button_1.pack()
    frame_button_2.pack(pady='3')

    #CRIA LABELS COM MENSAGENS E OS TIPOS DE CAMPOS
    mensagem = Label(frame_mens, text="SEJA BEM VINDO!", height='4', font=("MathJax_Main", '15'), bg=bgColor)
    cpfLabel = Label(frame_campos_label, text="CPF", bg=bgColor)
    senhaLabel = Label(frame_campos_label, text="Senha", bg=bgColor)

    #CRIA ENTRADAS DE TEXTO
    cpf = Entry(frame_campos_entry, width="25")
    senha = Entry(frame_campos_entry, width="25", show="*")

    #CRIA DE ENTRAR CADASTRAR E PONTO
    entrar = Button (frame_button_1, width="13", background="#054f77", foreground="White", text="Entrar", command=try_login).pack(side=LEFT, padx='1')
    cadastrar = Button (frame_button_1, width="13", background="#054f77", foreground="White", text="Cadastrar", command=lambda:abrirCadastro(cadastro_funcionario, login, main_frame)).pack(side=LEFT, padx='2', fill=X)
    ponto = Button (frame_button_2, width="28", background="#054f77", foreground="White", text="Ponto", command=lambda: ponto_tela(main_frame, login)).pack(side=LEFT, padx='3')


    #EMPACOTA LABELS
    mensagem.pack()
    cpfLabel.pack(side=TOP, padx='10', pady='3')
    senhaLabel.pack(side=TOP)


    #EMPACOTA ENTRIES
    cpf.pack(side=TOP, pady='5')
    senha.pack(side=TOP)

def cadastro_funcionario(cadastro_empresa, main):
    main.destroy()

    def novo_funcionario ():
        def sim():
            #Compactando strings
            nome_envio = nome.get().replace(' ', '/')
            cidade_envio = cidade.get().replace(' ', '/')

            #Enviando dados para o cadastro
            mensagem_envio ="funcionario "+ "add " + nome_envio + " " + email.get() + " " + senha.get() + " " + cpf.get() + " " + identidade.get() + " " + cidade_envio + " " + varEstado + " " + str(varLogin) + " " + str(varFilial)

            #Recebendo resposta sobre o cadastro
            resposta = enviar_socket(mensagem_envio)

            #Mostrando resposta            
            mensagem["text"] = resposta

            #Limpando campos
            nome.delete(0, END)
            email.delete(0, END)
            senha.delete(0, END)
            senha_confirme.delete(0, END)
            cpf.delete(0, END)
            identidade.delete(0, END)
            cidade.delete(0, END)
            senhaEmpresa.delete(0, END)
            confirme.destroy()
            
        def nao():
            #Destruindo tela de confirme
            confirme.destroy()

        #Testando campos 
        if(nome.get().isalpha and len(nome.get()) > 10):
            if (email.get().isalnum and len(email.get()) > 8):
                if (len(senha.get()) >= 8 and senha.get().isalnum()):
                    if (senha_confirme.get() == senha.get()):
                        if (len(cpf.get()) == 11):
                            if (len(identidade.get()) >= 11):
                                if(cidade.get().isalpha()):
                                    nonlocal varEstado
                                    if(varEstado.isalpha):
                                        nonlocal varLogin
                                        if (varLogin != 0):
                                            nonlocal varFilial
                                            if varFilial:
                                                print(varFilial)
                                                nonlocal chave
                                                print (chave)
                                                if chave == senhaEmpresa.get():
                                                    
                                                    confirme = Tk()
                                                    confirme.geometry("+550+300")
                                                    confirme.title("Sua Compra")
                                                    confirme.resizable(0, 0)

                                                    frame_mensg = Frame(confirme)
                                                    frame_butt = Frame(confirme)
                                                    frame_mensg.pack()
                                                    frame_mensg.pack()
                                                    
                                                    mensagem1 = Label(frame_mensg, text="CONFIRME DADOS", font=("Times", 13)).pack(pady='10')

                                                    sim_button = Button(confirme, width="15", text="SIM", command=sim, background="#054f77", foreground="White").pack(side=LEFT, padx='3', pady='5')
                                                    nao_button = Button(confirme, width="15", text="NAO", command=nao, background="#054f77", foreground="White").pack(side=LEFT, padx='3')
                                                    confirme.mainloop()
                                                    varLogin = 0
                                        else:
                                            mensagem["text"] = "FILIAL INVÁLIDA"    
                                    else:
                                        mensagem["text"] = "ESTADO INVÁLIDO"
                                else:
                                    mensagem["text"] = "CIDADE INVÁLIDA"
                            else:
                                mensagem["text"] = "RG INVÁLIDO"
                        else:
                            mensagem["text"] = "CPF INVÁLIDO"
                    else:
                        mensagem["text"] = "AS SENHAS NÃO COINCIDEM"
                else:
                    mensagem["text"] = "SENHA INCORRETA"
            else:
                mensagem["text"] = "EMAIL INVÁLIDO"
        else:
            mensagem["text"] = "NOME INCORRETO"

    #CRIANDO FUNÇÕES A SEREM EXECUTADAS POR CADA ELEMENTO DE CARGO        
    def opcao_login(value, cargo):
        nonlocal varLogin
        varLogin = value
        setor["text"] = cargo
        setor['background']="#054f77"
        setor['fg']='white'

    #CRIANDO FUNÇÕES A SEREM EXECUTADAS POR CADA ELEMENTO DE ESTADO
    def opcao_estado(value):
        nonlocal varEstado
        varEstado = value
        estado["text"] = value
        estado['background']="#054f77"
        estado['fg']='white'

    #CRIANDO FUNÇÕES A SEREM EXECUTADAS POR CADA ELEMENTO DE ESTADO
    def opcao_filial(value):
        nonlocal chave
        nonlocal varFilial
        varFilial = value
        chave = enviar_socket('filial select senha id="{0}"'.format(varFilial))
        chave = str(chave)
        filial["text"] = value
        filial['background']="#054f77"
        filial['fg']='white'

    
    varLogin = 0
    #CONFIGURA JANELA
    cadastro_empresa.geometry("800x300")
    cadastro_empresa.title("Sua Compra")
    cadastro_empresa.resizable(0, 0)
    cadastro_empresa['bg']= bgColor


    #CRIANDO FRAMES E SUBFRAMES ONDE FRAMES MAIORES SÃO CONTAINERS E SUBFRAMES COLUNAS
    main_ = Frame(cadastro_empresa, bg=bgColor)
    frame_mens = Frame(main_, bg=bgColor)

    frame_dados = Frame(main_, bg=bgColor)
    frame_dados_func = Frame(frame_dados, bg=bgColor)
    frame_tipo_dados = Frame(frame_dados_func, bg=bgColor)

    frame_dados_func_colum1 = Frame(frame_dados_func, bg=bgColor)
    frame_dados_func_label_1 = Frame(frame_dados_func_colum1, bg=bgColor)
    frame_dados_func_entry_1 = Frame(frame_dados_func_colum1, bg=bgColor)


    frame_dados_func_colum2 = Frame(frame_dados_func, bg=bgColor)
    frame_dados_func_label_2 = Frame(frame_dados_func_colum2, bg=bgColor)
    frame_dados_func_entry_2 = Frame(frame_dados_func_colum2, bg=bgColor)

    frame_dados_empresa = Frame(frame_dados, bg=bgColor)
    frame_tipo_dados_2 = Frame(frame_dados_empresa, bg=bgColor)

    frame_dados_empresa_colum1 = Frame(frame_dados_empresa, bg=bgColor)
    frame_dados_empresa_label_1 = Frame(frame_dados_empresa_colum1, bg=bgColor)
    frame_dados_empresa_entry_1 = Frame(frame_dados_empresa_colum1, bg=bgColor)

    frame_dados_empresa_colum2 = Frame(frame_dados_empresa, bg=bgColor)
    frame_dados_empresa_label_2 = Frame(frame_dados_empresa_colum2, bg=bgColor)
    frame_dados_empresa_entry_2 = Frame(frame_dados_empresa_colum2, bg=bgColor)

    frame_button_cadastrar = Frame(main_, bg=bgColor)
    frame_button_voltar = Frame(main_, bg=bgColor)


    #EMPACOTANDO FRAMES E SUBFRAMES
    main_.pack()
    frame_mens.pack()
    frame_dados.pack()

    frame_dados_func.pack(side=LEFT)
    frame_tipo_dados.pack(pady='10')
    frame_dados_func_colum1.pack(side=LEFT, padx='15')
    frame_dados_func_label_1.pack(side=LEFT, padx='10')
    frame_dados_func_entry_1.pack(side=LEFT)

    frame_dados_func_colum2.pack(side=LEFT)
    frame_dados_func_label_2.pack(side=LEFT, padx='10')
    frame_dados_func_entry_2.pack(side=LEFT)

    frame_dados_empresa.pack(side=LEFT, padx='10')
    frame_tipo_dados_2.pack(pady='10')

    frame_dados_empresa_colum1.pack(side=LEFT, padx='15', pady='10')
    frame_dados_empresa_label_1.pack(side=LEFT, padx='10')
    frame_dados_empresa_entry_1.pack(side=LEFT)


    frame_button_voltar.pack(side=RIGHT, pady='30')
    frame_button_cadastrar.pack(side=RIGHT, pady='30')


    #LABELS
    mensagem = Label(frame_mens, text="CADASTRE-SE NO NOSSO APP!", height='2', font=("MathJa_Main", '12'), bg=bgColor)
    pessoais = Label(frame_tipo_dados, text="DADOS PESSOAIS", width="23", background="#054f77", foreground="White", font=("MathJax_Main", 9))
    empresariais = Label(frame_tipo_dados_2, text="DADOS EMPRESARIAIS", width="23", background="#054f77", foreground="White", font=("MathJax_Main", 9))

    #LABEL'S PLACE
    mensagem.pack()
    pessoais.pack()
    empresariais.pack(side=TOP)

    #CRIANDO LABELS DOS CAMPOS LIGADOS A INFORMAÇÕES PESSOAIS
    nomeLabel = Label(frame_dados_func_label_1, text="Nome", bg=bgColor)
    emailLabel = Label(frame_dados_func_label_1, text="Email", bg=bgColor)
    senhaLabel = Label(frame_dados_func_label_1, text="Senha", bg=bgColor)
    senha_confirmeLabel = Label(frame_dados_func_label_1, text="Confirme", bg=bgColor)
    cpfLabel = Label(frame_dados_func_label_2, text="CPF", bg=bgColor)
    identidadeLabel = Label(frame_dados_func_label_2, text="RG", bg=bgColor)
    cidadeLabel = Label(frame_dados_func_label_2, text="Cidade", bg=bgColor)
    estadoLabel = Label(frame_dados_func_label_2, text="Estado", bg=bgColor)

    #ENTRIES PESSOAIS
    nome = Entry(frame_dados_func_entry_1, width="25")
    email = Entry(frame_dados_func_entry_1, width="25")
    senha = Entry(frame_dados_func_entry_1, width="25", show="*")
    senha_confirme = Entry(frame_dados_func_entry_1, width="25", show="*")
    cpf = Entry(frame_dados_func_entry_2, width="20")
    identidade = Entry(frame_dados_func_entry_2, width="20")
    cidade = Entry(frame_dados_func_entry_2, width="20")


    #LABEL EMPRESA
    filialLabel = Label(frame_dados_empresa_label_1, text="Filial", bg=bgColor)
    senhaEmpresaLabel = Label(frame_dados_empresa_label_1, text="Senha", bg=bgColor)
    setorLabel = Label(frame_dados_empresa_label_1, text="Setor", bg=bgColor)
        
    #ENTRIES EMPRESA
    senhaEmpresa = Entry(frame_dados_empresa_entry_1, width="20", show="*")
    setor = Entry(frame_dados_empresa_entry_1, width="20")

    #MENU OPÇÕES
    varLogin = None
    setor = Menubutton(frame_dados_empresa_entry_1, text="", background="white", foreground="Black", width = "19", activebackground="#054f77")
    setor.menu = Menu(setor)
    setor["menu"] = setor.menu

    #OPCOES
    cargos = [['Gerente', 2], ['Caixa', 3], ['Estoque', 4]]

    #ADICIONANDO OPCOES AO MENUBUTTON
    for option in cargos:
        setor.menu.add_command(label=option[0], command= functools.partial(opcao_login, option[1], option[0]))

    #FORMATANDO STRING RECEBIDA
    carac_tirar = ['/', ',', '(', ')', "'"]
    dados = enviar_socket('filial select id,estado')
    print(dados)

    #TROCANDO CARACTERE INDESEJADO
    for carac in carac_tirar:
        if carac == '/':
            dados = saving_name(dados, carac, ' ')
        else:
            dados = saving_name(dados, carac, '')

    #ADICIONANDO ESTADOS DE ATUACAO
    filiais = []
    estados = []
    for e in range(0, len(dados.split())-1):
        if e%2 == 0:
            filiais.append(dados.split()[e])
            estados.append(dados.split()[e+1].upper())
    estados = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MS','MT','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE', 'TO']
    #CRIANDO MENUBUTTON
    varEstado = None
    estado = Menubutton(frame_dados_func_entry_2, background="white", foreground="Black", width = "19", activebackground="#054f77")
    estado.menu = Menu(estado)
    estado["menu"] = estado.menu

    #ADICIONANDO OPCOES DE ESTADOS AO MENU BUTTON
    for UF in estados:
        estado.menu.add_command(label=UF, command=functools.partial(opcao_estado, UF))

    chave = None
    varFilial = None
    filial = Menubutton(frame_dados_empresa_entry_1, background="white", foreground="Black", width = "19", activebackground="#054f77")
    filial.menu = Menu(filial)
    filial["menu"] = filial.menu

    #ADICIONANDO OPCOES DE ESTADOS AO MENU BUTTON
    for fil in filiais:
        filial.menu.add_command(label=fil, command=functools.partial(opcao_filial, fil))


    #LABLES's PLACE PESSOAIS
    nomeLabel.pack(pady='5')
    emailLabel.pack()
    senhaLabel.pack(pady='5')
    senha_confirmeLabel.pack()
    cpfLabel.pack(pady='5')
    identidadeLabel.pack()
    cidadeLabel.pack(pady='5')
    estadoLabel.pack()

    #ENTRIES's PLACE PESSOAIS
    nome.pack(pady='5')
    email.pack()
    senha.pack(pady='5')
    senha_confirme.pack()
    cpf.pack(pady='5')
    identidade.pack()
    cidade.pack(pady='5')
    estado.pack()


    #LABEL'S PLACE EMPRESA
    filialLabel.pack(pady='5')
    senhaEmpresaLabel.pack()
    setorLabel.pack(pady='5')

    #ENTRIES PLACE EMPRESA
    filial.pack(pady='5')
    senhaEmpresa.pack()
    setor.pack(pady='5')

    #BUTTON
    cadastrar = Button (frame_button_cadastrar, width="30", background="#054f77", foreground="White", text="Cadastrar", command = novo_funcionario)
    voltar = Button (frame_button_voltar, width="8", background="#054f77", foreground="White", text="Voltar", command=lambda:voltar_login(main_, empresa_login, contadorGerente, login
    ))
    voltar.pack(side=RIGHT)
    cadastrar.pack(side=RIGHT, padx='150')

    cadastro_empresa.mainloop
def dadosEstoque():
    mensagem_envio = 'estoque select'
    produtos = enviar_socket(mensagem_envio)
    return produtos.split()

def matrizProdutos():
    produtosDivididos = []
    produtosEstoque = dadosEstoque() 
    x = 0
    for i in range(len(produtosEstoque)):
        x += 1
        if x == 5:
            print(produtosEstoque[i])
            subLista = []
            subLista.append(produtosEstoque[i])
            subLista.append(produtosEstoque[i-1])
            subLista.append(produtosEstoque[i-2])
            subLista.append(produtosEstoque[i-3])
            subLista.append(produtosEstoque[i-4])
            print(subLista)
            produtosDivididos.append(subLista)
            x = 0
    return produtosDivididos

#COLOCANDO VALORES DENTRO DE UM LIST BOX
def escrevendoList(lista_produtos):
    lista_produtos.delete(0, END) #LIMPANDO LISTBOX
    for linha in (matrizProdutos()): #PERCORRENDO A MATRIZ COM AS INFORMAÇÕES DE PRODUTOS
        if int(linha[1]) > 0: #TESTANDO AINDA HÁ PRODUTOS DAQUELA QUANTIDADE
            linha[2] = linha[2].replace('!', ' ') #TROCANDO CARACTERE DO NOME DO PRODUTO
            string = '{0} - {1} {2} - {3} - {4} R$'.format(linha[4], linha[2], linha[3], linha[1], linha[0].replace('.', ',')) #CONCATENANDO STRING APARITR DOS DADOS DA LINHA
            lista_produtos.insert(END, string) #ADICIONANDO LINHA A LISTBOX


#TELA ESTOQUE
def tela_estoque(tela, main, indice):    
    #ESQUECE A POSIÇÃO DE TODOS OS ELEMENTOS D0 FRAME A PARTIR DO INDEX DO CONTADOR USADO
    def hide_subframe(controle):
        if controle == 0:
            frame_mudar.pack_forget()
        elif controle == 1:
            frame_list.pack_forget()
        elif controle == 2:
            frame_att.pack_forget()
        elif controle == 3:
            frame_del.pack_forget()
        elif controle == 4:
            frame_add.pack_forget()

    #MUDAR O PREÇO
    def mudar_preco():
        if codigo_mudar.get() and preco_mudar.get():
            if (codigo_mudar.get().isnumeric()) and (preco_mudar.get()): 
                mensagem_envio = 'estoque change preco '+ str(preco_mudar.get())+' '+ str(codigo_mudar.get()) 
                lb_mensagem['text'] = enviar_socket(mensagem_envio)
        codigo_mudar.delete(0,END)
        preco_mudar.delete(0,END)
        global produtos
        escrevendoList(lista_produtos)
        
    #ATUALIZAR QUANTIDADE
    def atualizar_quantidade():
        if codigo_att.get() and quantidade_entrada_att.get():
            dados = []
            mensagem_envio = 'estoque select quantidade id={0}'.format(str(codigo_att.get()))
            dados = [enviar_socket(mensagem_envio)]
            print(dados)
            quantidade = int(dados[0]) + int(quantidade_entrada_att.get())
            if (codigo_att.get().isnumeric()) and (quantidade_entrada_att.get()):
                mensagem_envio = 'estoque change quantidade '+ str(quantidade)+' '+ str(codigo_att.get()) 
                lb_mensagem['text'] = enviar_socket(mensagem_envio)
        codigo_att.delete(0,END)
        quantidade_entrada_att.delete(0,END)
        escrevendoList(lista_produtos)

    #ADICIONA NOVO PRODUTO
    def add():
        if codigo_add.get() and quantidade_add.get():
            if (codigo_add.get()).isnumeric() and (quantidade_add.get()).isnumeric():
                descricao = descricao_add.get().replace(' ', '!')
                mensagem_envio ='estoque add ' + str(codigo_add.get()) + ' ' + str(descricao) +' '+ str(marca_add.get()) +' '+ str(quantidade_add.get()) +' '+ str(preco_add.get())
                lb_mensagem['text'] = enviar_socket(mensagem_envio)
        escrevendoList(lista_produtos)

        #LIMPANDO CAMPOS
        codigo_add.delete (0, END)
        descricao_add.delete (0, END)
        marca_add.delete (0, END)
        quantidade_add.delete (0, END)
        preco_add.delete (0, END)
                    

    	
    #POSICIONA OS ELEMENTOS DO FRAME MUDAR_PREÇO
    def show_mudar_preco():
        #FRAMES
        frame_mudar.pack()
        frame_info_mudar.pack(ipadx='5', ipady='5')
        frame_lb_mudar.pack(side=LEFT)
        frame_entry_mudar.pack(side=LEFT)
        #LABELS
        lb_codigo_mudar.pack(padx='5', pady='5', fill=X)
        lb_preco_mudar.pack(padx='5', fill=X)
        #ENTRIES
        codigo_mudar.pack(padx='5', pady='5')
        preco_mudar.pack()
        #BUTTON
        bt_mudar.pack(padx='5', pady='5', fill=X)

    #POSICIONA OS ELEMENTOS DO FRAME LISTA DE PRODUTOS    
    def show_lista_produtos():
        #FRAMES
        frame_list.pack()
        frame1.pack(fill=Y, pady='5')
        frame2.pack()
        frame3.pack()
        #LABELS
        lb_lista.pack(side=LEFT, fill=X, anchor=E)
        lb_lista1.pack(side=LEFT, fill=X)
        lb_lista2.pack(side=LEFT, fill=X)
        lb_lista3.pack(side=LEFT, fill=X)
        lb_lista4.pack(side=LEFT, fill=X, anchor=W)
        #SCROLLBAR
        scrolbar.pack(side=RIGHT, fill=Y)
        #LISTBAR
        lista_produtos.pack(side=TOP, fill=BOTH, expand=True)

    
    #POSICIONA OS ELEMENTOS DO FRAME ATUALIZAR QUANTIDADE
    def show_atualizar_produto():
        #FRAMES
        frame_att.pack()
        frame_geral_att.pack(ipadx='5', ipady='5')
        frame_info_att.pack(ipady='5')
        frame_lb_att.pack(side=LEFT, padx='5')
        frame_entry_att.pack(side=LEFT)
        frame_bt_att.pack()
        #LABELS
        lb_codigo_att.pack(side=TOP, fill=X)
        lb_quantidade_att.pack(side=TOP, pady='5', fill=X)
        #ENTRIES
        codigo_att.pack(side=TOP)
        quantidade_entrada_att.pack(side=TOP, pady='5')
        #BUTTON
        bt_att.pack(padx='5', fill=X)    


    #POSICIONA OS ELEMENTOS DO FRAME ADD NOVO PRODUTO
    def show_novo_produto():
        #FRAMES
        frame_add.pack(ipady='5')
        frame_info_add.pack()
        frame_lb_add.pack(side=LEFT, padx='5')
        frame_entry_add.pack(side=LEFT, padx='5')
        #LABELS
        lb_codigo_add.pack(fill=X, pady='5')
        lb_descricao_add.pack(fill=X)
        lb_marca_add.pack(fill=X, pady='5')
        lb_quantidade_add.pack(fill=X)
        lb_preco_add.pack(fill=X, pady='5')
        #ENTRIES
        codigo_add.pack(pady='7')
        descricao_add.pack()
        marca_add.pack(pady='7')
        quantidade_add.pack()
        preco_add.pack(pady='7')
        #BUTTON
        bt_adicionar_produto_add.pack(fill=X, padx='5')
 

    #ESCONDE FRAMES INATIVAS
    def tela_off():
        global contador_dic
        x = 0 #CONTADOR INDEX DE FRAMES
        for e in contador_dic: #PROCURANDO QUE FRAME ESTÀ ATIVO
            if contador_dic[e] == False: #TESTANDO SE OS FRAMES TÃO ATIVOS A PARTIR DE CADA CONTADOR
                    hide_subframe(x) #ESCONDE O FRAME QUE ESTÁ ATIVO 
            x += 1 #PASSA PARA O PRÓXIMO INDEX
            
    #CONTROLA QUAL FRAME PODERÁ SER ATIVADO
    def contador_on (contador):  
        global contador_dic
        if contador_dic[contador]: #TESTA SE A CONTADOR CHAMADO É VÁLIDO
            for outros_contador in contador_dic: #INICIA O TESTE CONTADOR POR CONTADOR
                if contador != outros_contador: #A PARTIR DOS CONTADORES, ACHA OS FRAMES QUE NÃO HÁ TENTATIVA DE ABERTURA
                    tela_off() #ESCONDE FRAMES QUE ESTÃO ABERTAS
                    contador_dic[outros_contador] = True #DEIXA FRAME VÁLIDA PARA ABERTURA
                    
                elif contador == outros_contador: #A PARTIR DO CONTADOR, ACHA O FRAME QUE DESEJA ABRIR
                    tela_off() #LIMPA FRAME ANTERIOR
                    contador_dic[outros_contador] = False #TORNA FRAME NÃO ATIVÁVEL 
            return True #ATIVA FRAME
        return False
        

    #CHAMA FRAME DA LISTA PRODUTO
    def lista_produto_():
        lb_mensagem.pack_forget()
        if contador_on('contador_produtos'):
            escrevendoList(lista_produtos)
            show_lista_produtos()

    #CHAMA FRAME REFERENTE A FUNCÃO QUE DESEJA
    def chamar_frame(contador, funcao):
        if contador_on(contador): #TESTA SE O FRAME JÁ ESTÁ ATIVADA
            funcao() #POSICIONA ELEMENTOS DO FRAME NA TELA
        else:
            lb_mensagem['text'] = 'Tela já está ativa' #AVISA QUE O FRAME JÁ ESTÁ ATIVO

 
        
    '''__________________________TELA INICIAL______________________________'''
    tela.destroy()
    #CONFIGS DA JANELA
    try:
        main['bg'] = bgColor
        main.title('Sua Compra')
        main.geometry('600x300')
    except:
        print()
    #FRAMES
    main_frame = Frame(main, bg = bgColor)
    frame_button = Frame(main_frame, bg = bgColor)
    frame_info = Frame(main_frame, bg = bgColor)
    canvas_info = Canvas(frame_info, width='400', height='250', bg='White')    
    frame_canvas = Frame(frame_info, bg = bgColor)
    
    #BOTOES
    lb_mensagem = Label(frame_canvas, bg = bgColor, text='BOM DIA!')
    bt_novo_produto = Button(frame_button, bg = bgColorButton, fg = fgColorButton, text='Novo produto',command= functools.partial(chamar_frame, 'contador_novo_produto', show_novo_produto), width='17', font=("Arial", '10'))
    bt_atualizar = Button(frame_button, bg = bgColorButton, fg = fgColorButton, text='Atualizar Produto', width='17',command = functools.partial(chamar_frame, 'contador_att', show_atualizar_produto), font=("Arial", '10'))
    bt_produtos_estoque = Button(frame_button, bg = bgColorButton, fg = fgColorButton,text='Listar Produtos', width='17',command=lista_produto_, font=("Arial", '10'))
    bt_mudar_preco = Button(frame_button, bg = bgColorButton, fg = fgColorButton,text='Mudar Preço Unitário', width='17',command=functools.partial(chamar_frame, 'contador_mudar_preco', show_mudar_preco), font=("Arial", '10'))
    bt_sair = Button(frame_button, bg = bgColorButton, fg = fgColorButton, text='Sair', width='17',command=lambda:voltar_login(main_frame, empresa_login, contadorGerente, login), font=("Arial", '10'))

    #FRAMES PACK
    main_frame.pack(pady='20', padx='10')
    frame_button.pack(side=LEFT)
    frame_info.pack(side=LEFT)
    canvas_info.grid(row=0, column=2)
    frame_canvas.grid(row=0, column=2)

    #BOTOES PACK
    bt_mudar_preco.pack()
    bt_produtos_estoque.pack(padx='8', pady='10')
    bt_atualizar.pack()
    bt_novo_produto.pack(padx='8', pady='10')
    if indice == 1:
        bt_sair.pack()




    '''_________________FRAME ATUALIZAR PRODUTOS___________________'''
    #FRAMES
    frame_att = Frame(frame_canvas, bg = bgColor)
    frame_geral_att = Frame(frame_att, bg = bgColor)
    frame_info_att = Frame(frame_geral_att, bg = bgColor)
    frame_lb_att = Frame(frame_info_att, bg = bgColor)
    frame_entry_att = Frame(frame_info_att, bg = bgColor)
    frame_bt_att = Frame(frame_geral_att, bg = bgColor)
    #LABELS
    lb_codigo_att = Label(frame_lb_att,text='Código', bg=bgColorButton, fg='white')
    lb_quantidade_att = Label(frame_lb_att,text='Quantidade', bg=bgColorButton, fg='white')
    #ENTRIES
    codigo_att = Entry(frame_entry_att,width='20', bg=bgColor)    
    quantidade_entrada_att = Entry(frame_entry_att,width='20', bg=bgColor)
    #BUTTONS
    bt_att = Button(frame_bt_att,text='Atualizar', width='27', bg=bgColorButton, fg='white', command=atualizar_quantidade)



    '''____________________FRAME ALTERAR PREÇO______________________'''
    #FRAMES
    frame_mudar = Frame(frame_canvas, bg=bgColor)
    frame_info_mudar = Frame(frame_mudar, bg=bgColor)
    frame_lb_mudar = Frame(frame_info_mudar, bg=bgColor)
    frame_entry_mudar = Frame(frame_info_mudar, bg=bgColor)
    #LABELS
    lb_codigo_mudar = Label(frame_lb_mudar, text='Código', bg=bgColorButton, fg='white')
    lb_preco_mudar = Label(frame_lb_mudar,text='Novo Preço', bg=bgColorButton, fg='white')
    #ENTRIES
    codigo_mudar = Entry(frame_entry_mudar,width='25', bg=bgColor)
    preco_mudar = Entry(frame_entry_mudar,width='25', bg=bgColor)
    #BT
    bt_mudar = Button(frame_mudar,text='Mudar Preço',command=mudar_preco, bg=bgColorButton, fg='white')


    '''_________________FRAME ADICIONAR NOVO PRODUTO_________________'''
    #FRAMES
    frame_add = Frame(frame_canvas, bg=bgColor)
    frame_info_add = Frame(frame_add, bg=bgColor)
    frame_lb_add = Frame(frame_info_add, bg=bgColor)
    frame_entry_add = Frame(frame_info_add, bg=bgColor)
    #LABELS
    lb_codigo_add = Label(frame_lb_add,text='Código', bg=bgColorButton, fg='white')
    lb_descricao_add = Label(frame_lb_add,text='Descrição', bg=bgColorButton, fg='white')
    lb_marca_add = Label(frame_lb_add,text='Marca', bg=bgColorButton, fg='white')
    lb_quantidade_add = Label(frame_lb_add,text='Quantidade', bg=bgColorButton, fg='white')
    lb_preco_add = Label(frame_lb_add,text='Preço', bg=bgColorButton, fg='white')
    #ENTRY
    codigo_add = Entry(frame_entry_add, width='25', bg=bgColor)
    descricao_add = Entry(frame_entry_add, width='25', bg=bgColor)
    marca_add = Entry(frame_entry_add, width='25', bg=bgColor)
    quantidade_add = Entry(frame_entry_add, width='25', bg=bgColor)
    preco_add = Entry(frame_entry_add, width='25', bg=bgColor)
    #BT
    bt_adicionar_produto_add = Button(frame_add,text='Adicionar Produto',command=add, bg=bgColorButton, fg='white')



    '''___________________FRAME LISTAR PRODUTOS_____________________'''
    #FRAMES
    frame_list = Frame(frame_canvas, bg='white')
    frame1 = Frame(frame_list, bg='White')
    frame2 = Frame(frame_list, bg='White')
    frame3 = Frame(frame_list, bg='white')

    #LABELS
    lb_lista = Label(frame1,text='Código', bg=bgColorButton, fg='white', width='13')
    lb_lista1 = Label(frame1,text='Descrição', bg=bgColorButton, fg='white', width='8')
    lb_lista2 = Label(frame1,text='Marca', bg=bgColorButton, fg='white', width='7')
    lb_lista3 = Label(frame1,text='Quantidade', bg=bgColorButton, fg='white', width='11')
    
    #VARIAVEIS
    cod = None
    descricao = None
    marca = None
    quantidade = None
    preco = None
    x = 0

    #LISTBOX E SCROLL BAR   
    lb_lista4 = Label(frame1,text='Preço', bg=bgColorButton, fg='white', width='7')
    scrolbar = Scrollbar(frame2)
    lista_produtos = Listbox (frame2, width='30', height='7', font=("Arial", '14'), bg='#f8f8ff')
    
    lista_produtos.config(yscrollcommand=scrolbar.set)
    scrolbar.config(command=lista_produtos.yview)
    


'''Esta função vai calcular o preço que o cliente vai pagar pelo produtto de acordo com preco que se encontra no banco'''
def calcular(preco,quantidade_valor, valor):
    valor += (preco*quantidade_valor)
    return(valor)
'''Esta função passa os parametros que sera utilizado para fazer a seleção do produto no banco de dados'''
def parametros_produtos(codigo, quantidade, lb_valor, lb_produto, lista_produtos):
    '''Validação dos valores informados pelos caixa'''
    if codigo.get() and quantidade.get():
        if ((codigo.get()).isnumeric()) and ((quantidade.get()).isnumeric()):
            quantidade_saida = int(quantidade.get())
        elif ((codigo.get()).isnumeric()) and (((quantidade.get())=='')):
            quantidade_saida = 1
            
        '''Valores recuperados do banco'''

        mensagem_envio = 'estoque select * id="{0}"'.format(codigo.get())
        cod, descricao, marca, quantidadeBanco, preco = enviar_socket(mensagem_envio).split()
        
        
        valores = (quantidade_saida, float(preco), descricao, cod)
        quantidadeSalvar = int(quantidadeBanco) - quantidade_saida

        if int(quantidadeSalvar) > 0:    
            mensagem_envio = 'estoque change quantidade {0} "{1}"'.format(quantidadeSalvar, codigo.get())
            enviar_socket(mensagem_envio) 


            '''Lista da compra'''
            produtos.append(valores)
            
            preco = valores[0]
            quantidade_valor = valores[1]
            descricao = valores[2]

            '''o valor da compra sera armazenado na variavel pagar'''
            pagar = calcular(preco,quantidade_valor,valor)
            conta_por_produto = float(pagar)
            
            '''valor da conta do cliente'''
            global conta
            conta += conta_por_produto
            
            lb_valor['text'] = 'Valor Total: '.format(float(conta))
            lb_valor['text'] += '%.2f R$'%(float(conta))
            lb_produto['text'] = 'Produto: '.format(descricao.upper())
            lb_produto['text'] += '{0}'.format(descricao.upper())

            stringListbox = ''
            stringListbox = '{3} - {0} Unidades de {1} - {2} R$'.format(quantidade_saida, descricao, pagar, cod)
            lista_produtos.insert(END, stringListbox)

            '''Apagando os valores dos campus'''
            codigo.delete(0,END)
            quantidade.delete(0,END)

            return conta

def remover(caixa, caixaMenu, bg, lb_valor, lb_produto, bgColor, fgColorButton, bgColorButton, lista_produtos):
    
    def removerP(lb_valor, lb_produto, bgColor, bgColorButton, fgColorButton, lista_produtos):
        if codigo_r.get() and quantidade_produtos_r.get():
            codigo = int(codigo_r.get())
            quantidade_produtos = int(quantidade_produtos_r.get())
            '''Validaç~~ao dos valores'''
            if quantidade_produtos == '':
                quantidade_produtos = 1
                
            '''dar baixa no banco de dados '''
            mensagem_envio = 'estoque select * id="{0}"'.format(codigo) #SOLICITANDO DADOS DO BANCO
            cod, descricao, marca, quantidadeBanco, preco = enviar_socket(mensagem_envio).split() #ARMAZENANDO DADOS EM VARIAVEIS
        
            quantidadeBanco = int(quantidadeBanco) + quantidade_produtos #ATUALIZANDO A QUANTIDADE

            mensagem_envio = 'estoque change quantidade {0} "{1}"'.format(quantidadeBanco, codigo) #SOLICITANDO COMANDO NO BANCO
            enviar_socket(mensagem_envio) #EXCUTANDO COMANDO
            

            
            '''faz busca do preço o banco de dados'''
            mensagem_envio = 'estoque select preco id="{0}"'.format(codigo)
            preco_p = enviar_socket(mensagem_envio)
            preco_p = preco_p.replace(' ', '')
            preco_p = float(preco_p)

            ''' dar  baixa no conta geral do cliente'''
            global conta
            conta = float(conta)
            conta -= float(preco_p*quantidade_produtos)
            print(conta)
            
            '''percorrenndo valores da tupla e atribuindo a uma lista'''
            produtosFinais = []
            global produtos
            produto = produtos
            produtos = []
            for l in produto:
                produtoFinal = []
                for c in l:
                    produtoFinal.append(c)
                    produtosFinais.append(c)
                produtos.append(produtoFinal)
                         
            '''Atualizando valores da lista, quantidade removida'''
            valor_codigo_lista = (produtosFinais.index(str(codigo)))
            local_quantidade_lista  = valor_codigo_lista - 2
            valor_quantidade_lista = produtosFinais[local_quantidade_lista]
            quantidade_lista = (valor_quantidade_lista  - quantidade_produtos)
            produtosFinais[local_quantidade_lista] = quantidade_lista

            
            '''apagando valores dos campos de remover'''
            lb_valor['text'] = 'Total: %.2f R$'%(float(conta))
                
            codigo_r.delete(0,END)
            quantidade_produtos_r.delete(0,END)
            
            lista_produtos.delete(0, END)
            precoUnitario = None 
            descricaoMudar = None
            
            for linha in range(len(produtos)):
                if descricao in produtos[linha]:
                    produtos[linha][0] -= quantidade_produtos
                    
            for linha in range(len(produtos)):
                if not (produtos[linha][0] == 0):
                    quantidade_produtos = produtos[linha][0]
                    precoUnitario = produtos[linha][1]
                    descricao = produtos[linha][2]
                    codProd = produtos[linha][3]
                    print(linha)
                    lista_produtos.insert(END, '{3} - {0} Unidades de {1} - {2} R$'.format(quantidade_produtos, descricao, float(float(quantidade_produtos)*float(precoUnitario)), codProd))
                    

    '''Tela remover'''
    caixa.pack_forget()
    caixa_remove = Frame(caixaMenu, bg=bg)
    caixaInfo = Frame(caixa_remove, bg=bg)
    caixaInfoLb = Frame(caixaInfo, bg=bg)
    caixaInfoEn = Frame(caixaInfo, bg=bg)
    caixaBt = Frame(caixa_remove, bg=bg)
    
    caixa_remove.pack()
    caixaInfo.pack(side=LEFT, padx='65')
    caixaInfoLb.pack(side=LEFT, padx='5')
    caixaInfoEn.pack(side=LEFT)
    caixaBt.pack(side=LEFT, padx='10')

    lb_codigo = Label(caixaInfoLb,text='Código', font=("Arial", '10'), bg = bgColor)
    lb_quantidade_produtos = Label(caixaInfoLb,text='Quantidade', font=("Arial", '10'), bg = bgColor)

    lb_codigo.pack(fill=X, pady='3')
    lb_quantidade_produtos.pack(fill=X)
    
    codigo_r = Entry(caixaInfoEn, width='25', font=("Arial", '10'))
    quantidade_produtos_r = Entry(caixaInfoEn, width='25', font=("Arial", '10'))

    codigo_r.pack( pady='3')
    quantidade_produtos_r.pack()

    bt_remover = Button(caixaBt,text='Remover',command=lambda:removerP(lb_valor, lb_produto, bgColor, bgColorButton, fgColorButton, lista_produtos), width='14', font=("Arial", '10'), bg= bgColorButton, fg = fgColorButton)
    bt_finalizar = Button(caixaBt,text='Voltar',command=lambda:voltar(caixa, caixa_remove), font=("Arial", '10'), bg= bgColorButton, fg = fgColorButton)

    bt_remover.pack(fill=X, pady='5')
    bt_finalizar.pack(fill=X)
    

#FINALIZANDO COMPRA
def finalizar(lb_valor, lb_produto, lbTroco, enPago, lista_produtos):
    global valor #TRÁS VARIAVEIS GERAIS A FUNÇÃO
    global conta
    global pagar
    global conta_por_produto
    global produto
    global vendas
    
    vendas += conta #SOMANDO CONTA A VENDAS
    mensagemEnvio = 'filial change vendido {0} {1}'.format(vendas, 1) #SOLICITANDO AO SOCKET O ARMAZENAMENTO DESSE VALOR
    enviar_socket(mensagemEnvio) #ARMAZENANDO NO BANCO O VALOR VENDIDO

    #REINICIANDO VARIAVEIS 
    valor = 0
    pagar = 0
    conta_por_produto = 0
    conta = 0
    vendas = 0
    produto = []
    lb_valor['text'] = 'Valor Total: '
    lb_produto['text'] = 'Produto: '
    lbTroco ['text'] = 'Troco: 0,00 R$'
    enPago.delete(0, END)
    lista_produtos.delete(0, END)
    
def telaCaixa(mainDestroy, janela_caixa, bgColor, bgColorButton, fgColorButton, indice):
    '''Tela inicial'''
    mainDestroy.destroy()
    try:
        janela_caixa.geometry('550x430')
    except:
        print()

    #FRAMES E SUBFRAMES
    main = Frame(janela_caixa, bg=bgColor)
    caixaMenu = Frame(main, bg=bgColor)
    caixa = Frame(caixaMenu, bg=bgColor)
    caixaInfo = Frame(caixa, bg=bgColor)
    caixaInfoLb = Frame(caixaInfo, bg=bgColor)
    caixaInfoEntry = Frame(caixaInfo, bg=bgColor)
    caixaBt = Frame(caixa, bg=bgColor)
    caixaInfoProd = Frame(main, bg='White')
    caixaF = Frame(main)
    
    #EMPACOTANDO FRAMES E SUBFRAMES
    main.pack(pady='20')
    caixaMenu.pack()
    caixa.pack()
    caixaInfo.pack(side=LEFT, anchor=W, padx='63')
    caixaInfoLb.pack(side=LEFT)
    caixaInfoEntry.pack(side=LEFT, padx='10', pady='10')
    caixaBt.pack(side=RIGHT, anchor=E, padx='20')
    caixaInfoProd.pack(anchor=NW, padx='20', pady='5')
    caixaF.pack()

    #CRIANDO LABELS
    lb_codigo = Label(caixaInfoLb,text='Código', font=("Arial", '10'), fg='Black', bg=bgColor)
    lb_quantidade = Label(caixaInfoLb,text='Quantidade', font=("Arial", '10'), fg='Black', bg=bgColor)

    #EMPACOTANDO LABELS
    lb_codigo.pack(fill=X, pady='5')
    lb_quantidade.pack(fill=X)

    #CRIANDO ENTRIES
    codigo = Entry(caixaInfoEntry, width='25', font=("Arial", '10'))
    quantidade = Entry(caixaInfoEntry, width='25', font=("Arial", '10'))
    enPago = Entry(main)
    
    #EMPACOTANDO ENTRIES
    codigo.pack(pady='5')
    quantidade.pack()

    global conta
    #CRIANDO BOTOES
    bt_adicionar = Button(caixaBt,text='Adicionar Produto', width='15',command=lambda: parametros_produtos(codigo, quantidade, lb_valor, lb_produto, lista_produtos), bg= bgColorButton, fg = fgColorButton, font=("Arial", '10'))
    bt_remover = Button(caixaBt,text='Remover', width='15', command=lambda: remover(caixa, caixaMenu, bgColor, lb_valor, lb_produto, bgColor, fgColorButton, bgColorButton, lista_produtos), font=("Arial", '10'), bg= bgColorButton, fg = fgColorButton)
    bt_finalizar = Button(caixaBt,text='Finalizar', width='15', font=("Arial", '10'), command= lambda: finalizar(lb_valor, lb_produto, lbTroco, enPago, lista_produtos), bg= bgColorButton, fg = fgColorButton)
    btFecharCompra = Button((main), text='OK', width='9',command=lambda:mudarText(lbTroco, (float(enPago.get())-float(conta))), bg= bgColorButton, fg = fgColorButton)
    btVoltar = Button(main, text = 'Sair', command = lambda: voltar_login(main, empresa_login, contadorGerente, login), width='15', bg= bgColorButton, fg = fgColorButton)

    #EMPACOTANDO BOTOES
    bt_adicionar.pack(fill = X)
    bt_remover.pack(fill = X, pady='3')
    bt_finalizar.pack(fill = X)

    #EMPACOTADO LABELS PRINCIPAIS
    lb_valor = Label(caixaInfoProd, text='Valor Total: ', font=("MathJa_Main", '20'),  bg='White', width='40', anchor=W, fg='Black')
    lb_produto = Label(caixaInfoProd, text='Produto: ', font=("MathJa_Main", '20'), bg='White', width='40', anchor=W, fg='Black')
    lbPago = Label(main, text='Total Pago: ', fg='Black', bg=bgColor)
    lbTroco = Label(main, text='Troco: {0} R$'.format('0,00'), fg='Black', bg=bgColor)
    lb_valor.pack()
    
    #CRIANDO SCROLLBAR E LISTBOX DE PRODUTOS COMPRADOS
    scrolbar = Scrollbar(caixaInfoProd)
    lista_produtos = Listbox(caixaInfoProd, width='90', height='8', font=("Arial", '14'), bg='#f8f8ff')
    lista_produtos.config(yscrollcommand=scrolbar.set)
    scrolbar.config(command=lista_produtos.yview)

    #EMPACOTANDO LISTBOX E SCROLBAR
    scrolbar.pack(side=RIGHT)
    lista_produtos.pack(side=LEFT, padx='2', pady='2')

    #TESTANDO SE A TELA TA SENDO CHAMADA DA TELA DO GERENTE OU DO CAIXA APARTIR DE UM INDICE PASSADO
    if indice == 1:
        btVoltar.pack(side=LEFT, padx='20')   #DESEMPACOTANDO SAIR
    

    #EMPACOTANDO LABELS PRINCIPAIS
    btFecharCompra.pack(side=RIGHT, padx='20') 
    lbTroco.pack(side=RIGHT)
    enPago.pack(side=RIGHT, padx='10')
    lbPago.pack(side=RIGHT)
    janela_caixa.mainloop()


def abrirTela(tela, mainDestroy, subUnpack1, subUnpack2, local):
    global bgColor
    global bgColorButton
    global fgColorButton
    global contadorGerente
    if tela == 'Caixa':
        subUnpack1.pack_forget()
        subUnpack2.pack_forget()
        local.pack_forget()
        local.pack()
        if contadorGerente[0][1] == False:
            contadorGerente[0][1] = True
            telaCaixa(mainDestroy, local, bgColor, bgColorButton, fgColorButton, 2)
    elif tela == 'Estoque':
        subUnpack1.pack_forget()
        subUnpack2.pack_forget()
        local.pack_forget()
        local.pack()
        if contadorGerente[1][1] == False:
            contadorGerente[1][1] = True
            tela_estoque(mainDestroy, local, 2)
    if tela == 'Ponto':
        subUnpack1.pack_forget()
        subUnpack2.pack_forget()
        local.pack_forget()
        local.pack()
        global gerandoPonto
        framePonto(mainDestroy, local, gerandoPonto())

def vendasTotal(lb):
    total = enviar_socket('filial select vendido 1')
    lb['text'] = '%.2f R$'%(float(total))

def framePonto(destruir, main, pontos):
    destruir.destroy()
    mainFrame = Frame(main)
        
    mainFrame.pack()

    scrolbar = Scrollbar(mainFrame)
    listaPonto = Listbox(mainFrame, width='90', height='25', font=("Arial", '11'), bg='#f8f8ff')
    listaPonto.config(yscrollcommand=scrolbar.set)
    scrolbar.config(command=listaPonto.yview)
    for linha in pontos:
        string = ''
        for elem in linha:
            string += elem.replace('!', ' ') + ' ' 
        listaPonto.insert(END, string)
    scrolbar.pack(side=RIGHT, fill=Y)
    listaPonto.pack()

    lbTamanho = Label(mainFrame, text='', width='85', height='30', bg='White')
    lbTamanho.pack()

def gerandoPonto():
    arquivo = open('ponto/dec.ini', 'r')
    pontos = arquivo.readlines()
    nomeP, dataP, horaP, tipoP = 0, 0, 0, 0
    pontosEntrada = []
    pontosSaida = []
    pontoIO = []
    indice = 0
    for e in pontos:
        print(e)
        if e != '\n':
            nome, data, hora, tipo = e.split('-')
            if tipo == 'Entrada\n' or tipo == 'Entrada':
                nomeP, dataP, horaP, tipoP = e.split('-')
                tipoP = tipoP.replace('\n', '')
                sublista = [nomeP, dataP, horaP, tipoP]
                pontosEntrada.append(sublista)
            elif tipo == 'Saida\n' or tipo == 'Saida':
                nomeP, dataP, horaP, tipoP = e.split('-')
                tipoP = tipoP.replace('\n', '')
                sublista = [nomeP, dataP, horaP, tipoP]
                pontosSaida.append(sublista)
                
    for i in range(len(pontosSaida)):
        nomeP = pontosSaida[i][0]
        dataP = pontosSaida[i][1]
        horaP = pontosSaida[i][2]
        tipoP = pontosSaida[i][3]
        
        for l in range(len(pontosEntrada)):
            nome = pontosEntrada[i][0]
            data = pontosEntrada[i][1]
            hora = pontosEntrada[i][2]
            tipo = pontosEntrada[i][3]
            if nome == nomeP and data == dataP:
                sublista = [nome, data, hora, tipo, horaP, tipoP]
                pontoIO.append(sublista)
                break
    pontosEntrada = []
    pontosSaida = []
    for linha in pontoIO:
        for elem in linha:
            print(elem, end=' ')
        print()
    return pontoIO
    
            
def gerente(janelaFechar, janela, cpf): 
    global bgColor
    global bgColorButton
    global fgColorButton
    
    janelaFechar.destroy()
    janela.geometry('800x500')
    janela['bg'] = bgColor

    main = Frame(janela, bg=bgColor)
    framePessoais = Frame(main, bg='White')
    frameButton = Frame(main, bg=bgColor)
    
    mainFrameInfo = Frame(main, bg=bgColor)
    frameInfo = Frame(mainFrameInfo, bg=bgColor)
    frameInfoEstoque = Frame(mainFrameInfo, bg=bgColor)
    frameInfoCaixa = Frame(mainFrameInfo, bg=bgColor)
    frameInfoPonto = Frame(mainFrameInfo, bg=bgColor)

    main.pack()
    frameButton.pack(pady='10', padx='100')
    framePessoais.pack(side=LEFT, pady='10', padx='10', ipady='20')
    mainFrameInfo.pack(side=RIGHT, pady='10', padx='10')
    frameInfo.pack()
    frameInfoEstoque.pack()
    frameInfoCaixa.pack()
    frameInfoPonto.pack()
    
    caixa = Button(frameButton, text='Caixa', width='15', command = lambda: abrirTela('Caixa', frameInfo, frameInfoEstoque, frameInfoPonto , frameInfoCaixa), bg=bgColorButton, fg=fgColorButton)
    estoque = Button(frameButton, text='Estoque', width='15', command = lambda: abrirTela('Estoque', frameInfo, frameInfoCaixa, frameInfoPonto, frameInfoEstoque), bg=bgColorButton, fg=fgColorButton)
    ponto = Button(frameButton, text='Ponto', width='15',bg=bgColorButton, fg=fgColorButton, command=lambda: abrirTela('Ponto', frameInfo, frameInfoCaixa, frameInfoEstoque, frameInfoPonto))
    atualizar = Button(frameButton, text='Atualizar', width='15', command = lambda: vendasTotal(vendidoFLabel), bg=bgColorButton, fg=fgColorButton)
    sair = Button(frameButton, text='Sair', width='15', command= lambda: voltar_login(main, empresa_login, contadorGerente, login), bg=bgColorButton, fg=fgColorButton)

    mensagemEnvio = 'funcionario select * cpf="{0}"'.format(cpf)
    idP, nome, email, senha, cpf, rg, cidade, estado, matricula, cargo, filial = enviar_socket(mensagemEnvio).split()
    nome = nome.replace('!',' ')

    
    mensagemEnvio = 'filial select'
    idF, emailF, senhaF, cidadeF, estadoF, vendido = enviar_socket(mensagemEnvio).split()
    frameMatriculaCargo = Frame(framePessoais, bg='White')
    
    pessoaisLabel = Label(framePessoais, text='Informações Pessoais: ', font=('Times New Roman', '12'), bg='White')
    nomeLabel = Label(framePessoais, text=nome, bg='White')
    emailLabel = Label(framePessoais, text=email, bg='White')
    cidadeLabel = Label(framePessoais, text=cidade+'-'+estado, bg='White')
    matriculaLabel= Label(frameMatriculaCargo, text=matricula, bg='White')
    cargoLabel = Label(frameMatriculaCargo, text=setor_string(cargo), bg='White')

    pessoaisLabel.pack(anchor=W)
    nomeLabel.pack(anchor=W, padx='5')
    emailLabel.pack(anchor=W, padx='5')
    cidadeLabel.pack(anchor=W, padx='5')
    frameMatriculaCargo.pack(fill=X, padx='5')
    matriculaLabel.pack(anchor=W, side=LEFT)
    cargoLabel.pack(anchor=E, side=LEFT)

    filialLabel = Label(framePessoais, text='Informações Empresariais', font=('Times New Roman', '12'), bg='White')
    emailFLabel = Label(framePessoais, text=emailF, bg='White')
    cidadeFLabel = Label(framePessoais, text=cidadeF+'-'+estadoF, bg='White')
    vendidoFLabel = Label(framePessoais, text='%.2f R$'%(float(vendido)), bg=bgColorButton, fg=fgColorButton, font=('Times New Roman', '18'), width='10')
    
    filialLabel.pack(anchor=W)
    emailFLabel.pack(anchor=W, padx='5')
    cidadeFLabel.pack(anchor=W, padx='5')
    vendidoFLabel.pack(anchor=CENTER, padx='15', pady='50')

    
    lbTamanhoInfo = Label(frameInfo, text='', width='85', height='30', bg='White')
    lbTamanhoPessoais = Label(framePessoais, text='', width='25', height='30', bg='White')

    lbTamanhoInfo.pack()
    lbTamanhoPessoais.pack()

    caixa.pack(side=LEFT)
    estoque.pack(side=LEFT, padx='5')
    ponto.pack(side=LEFT)
    atualizar.pack(side=LEFT, padx='5')
    sair.pack(side=LEFT)
    

#LISTAS
contador_dic = {'contador_mudar_preco': True, 'contador_produtos': True, 'contador_att': True, 'contador_excluir': True, 'contador_novo_produto': True}
contadorGerente = [['Caixa', False],['Estoque', False]]
opcoes = [['Gerente', 2], ['Caixa', 3], ['Estoque', 4]]

#VARIAVEIS PONTO
ponto = ['Dec']
dia_sem, mes, dia, horas, ano = asctime().split()
data = '{0} / {1} / {2}'.format(dia, mes, ano)


#GERANDO ARQUIVO PONTO POR MÊS
mes = mes.lower()
nomeArquivo = mes
if mes == nomeArquivo:
    try:
        arquivo = open('ponto/{0}.ini'.format(nomeArquivo), 'r')
    except FileNotFoundError:
        arquivo = open('ponto/{0}.ini'.format(nomeArquivo), 'w')


#VARIAVEIS CORES INTERFACE
bgColor = '#ccccff'
bgColorButton = "#054f77"
fgColorButton = 'White'   

#VARIAVEIS CAIXA
valor = 0
pagar = 0
conta_por_produto = 0
conta = 0
vendas = 0 
#VARIAVEIS ESTOQUE
produtosEstoque = None
produtos = []

#CONFIGURAÇÕES PADRÃO DA JANELA
login = Tk()
login.geometry("400x300+200+150")
login.title("Sua Compra")
login.resizable(0, 0)
login['bg'] =  bgColor

#INICIANDO...
empresa_login(login)
login.mainloop()

