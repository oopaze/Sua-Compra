import socket
from tkinter.filedialog import askopenfilename
from tkinter import *
import sqlite3

#TROCA O IDENTIFICADOR PELO NOME DO SETOR
def setor_string(setor_int):
    if setor_int == 2 or setor_int == '2': #DESCOBRINDO QUAL SETOR A PARTIR DO INDICE
        setor_int = "Gerente" #TRANSFORMANDO INDICE EM UMA STRING SETOR
        return (setor_int) #RETORNANDO STRING SETOR
    
    if setor_int == 3 or setor_int == '3': #DESCOBRINDO QUAL SETOR A PARTIR DO INDICE
        setor_int = "Caixa" #TRANSFORMANDO INDICE EM UMA STRING SETOR
        return (setor_int) #RETORNANDO STRING SETOR
        
    if setor_int == 4 or setor_int == '4': #DESCOBRINDO QUAL SETOR A PARTIR DO INDICE
        setor_int = "Estoquista" #TRANSFORMANDO INDICE EM UMA STRING SETOR
        return (setor_int) #RETORNANDO STRING SETOR

#BUSCA ARQUIVOS NO PC
def buscar_arquivo():
    filename = askopenfilename() # Isto te permite selecionar um arquivo
    return (filename)

#MUDANDO UM CARACTERE DE UMA STRING POR OUTRO
def saving_name(string, carac_1, carac_2):
    string = string.replace(carac_1, carac_2)
    return string

#FORMATA E CONCATENA STRINGS SALVANDO-AS EM UMA LISTA
def Formata1(i, palavra, saida, lmt):
  if len(palavra) <= lmt:
    saida[i] += (palavra + (lmt - len(palavra)- 1)*" ")+"|"
    print(lmt-len(palavra))

#ENVIA MENSAGEM A UM SOCKET A PARTIR DO HOST
def enviar_socket(mensagem_envio, host=socket.gethostbyname(socket.gethostname())):
    porta = 8000 #DEFINE UMA PORTA PADRÃO PARA CONEXÃO
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #CONFIGURA O PROTOCO DE ENDEREÇO DE IP DE TRANSFÊNCIA TCP NO SOCKET
    while True: #INICIA O LOOP DE ENVIO E RECIMENTO DE RESPOSTA
                cliente.sendto(mensagem_envio.encode(), (host, porta)) #SOLICITA DADOS AO SOCKET
                mensagem_serv, ip_serv = cliente.recvfrom(2048) #RECEBENDO RESPOSTA DA SOLICITAÇÃO
                if mensagem_serv: #TESTA SE HÁ MENSAGEM
                    return(mensagem_serv.decode()) #DECODIFA-A E RETORNA A REPOSTA
                    break #PARA O LOOP
                else:
                    break
                            


#Esta função vai calcular o preço que o cliente vai pagar pelo produtto de acordo com preco que se encontra no banco'''
def calcular(preco,quantidade_valor, valor):
    valor += (preco*quantidade_valor)
    return(valor)

#PROCESSO DE ESCOLHA PARA QUAL TIPO DE PONTO BATER (ENTRADA\SAIDA) E POR QUEM
def batendoPonto(nome, data, hora, main, frame_info, frame_horas, entry1, entry2, mes):
    controleSemNome = [] #CRIANDO VARIAVEL PARA CONTROLAR QUEM AINDA NÃO TEM O NOME NO ARQUIVO DE PONTO
    indice = 0 #CRIANDO INDICE PRA FACILITAR O ACESSO A LISTA
    arquivo = open('ponto/{0}.ini'.format(mes), 'r') #ABRINDO ARQUIVO DOS PONTOS
    ponto = arquivo.readlines()  #ARMAZENANDO UMA MATRIZ EM PONTO, SENDO SUAS LINHA CADA LINHA DO ARQUIVO.INI 
    if ponto: #TESTA SE HÁ LINHAS
        for lin in range(0, -(len(ponto)), -1): #COMECA A CONTAGEM COM NUMEROS NEGATIVOS
            linha = ponto[lin] #PERCORRE AS LINHAS DA MATRIZ PONTO
            if nome in linha.split('-') and 'Entrada' in linha.split('-'): #TESTA SE O NOME PASSADA É IGUAL O DA LINHA E SE O TIPO É IGUAL ENTRADA
                diaP = linha.split('-')[1].split('/')[0] #ARMAZENA O DIA VINDO DO PONTO BATIDO EM diaP
                dia = data.split('/')[0] #ARMAZENA O DIA APARTIR DA DATA PASSA EM dia
                if dia != diaP: #TESTA SE O DIA QUE O PONTO FOI BATIDO É DIFERENTE DO DIA PASSADO(HOJE)
                    escrevendo(nome, data, hora, 'Entrada', mes) #BATE A ENTRADA

                elif dia == diaP: #TESTA SE O DIA QUE O PONTO FOI BATIDO É DIFERENTE DO DIA PASSADO(HOJE)
                    escrevendo(nome, data, hora, 'Saida', mes) #BATE A SAIDA
                    
                if nome in controleSemNome: #TESTA SE O NOME DA PESSOA QUE TA TENTANDO BATER O PONTO ESTA NA LISTA DAS PESSOAS QUE NÃO TENHAM BATIDO AINDA 
                    controleSemNome.remove(nome) #APOS BATER SEU PONTO A REMOVE DA LISTA
                break #QUEBRA O LAÇO
            
            elif nome in linha.split('-') and 'Saida' in linha.split('-'): #TESTA SE O NOME FOI ACHADO E SE O TIPO FOI IGUAL A SAIDA
                escrevendo(nome, data, hora, 'Entrada', mes) #BATENDO ENTRADA
                if nome in controleSemNome: #TESTA SE O NOME ESTÁ EM controleSemNome
                    controleSemNome.remove(nome) #RETIRA NOME DA LISTA
                break #QUEBRA LOOP
            
            elif nome not in linha and nome not in controleSemNome: #TESTA SE NOME NÃO ESTÁ NEM NO ARQUIVO PONTO, NEM NA LISTA controleSemNome
                controleSemNome.append(nome) #ADICIONA NOME NÃO ACHADO NA LISTA controleSemNome
            indice += 1 #ADICIONA MAIS 1 EM INDICE

            
        if nome in controleSemNome: #TESTA SE NOME ESTA EM controleSemNome
            escrevendo(nome, data, hora, 'Entrada', mes) #BATE PRIMEIRA ENTRADA 
            controleSemNome.remove(nome) #REMOVE O NOME DA LISTA
    else: #SE O ARQUIVO NÃO TIVER NADA
        escrevendo(nome, data, hora, 'Entrada', mes) #BATE A ENTRADA       
    entry1.delete(0, END) #LIMPA A PRIMEIRA E ASEGUNDA ENTRTY
    entry2.delete(0, END)
    voltar_ponto(main, frame_info, frame_horas) #FECHA TELA ATUAL E ABRE TELA ANTERIOR

#ESCREVE DADOS DO PONTO NO ARQUIVO.INI
def escrevendo(nome, data, hora, tipo, mes):
    arquivo = open('ponto/{0}.ini'.format(mes), 'a') #O NOME DO ARQUIVO É DEFINIDO PELO MÊS
    arquivo.write('\n{0}-{1}-{2}-{3}'.format(nome, data, hora, tipo)) #ESCREVENDO NA ULTIMA LINHA DO ARQUIVO
    arquivo.close() #FECHANDO ARQUIVO

#VOLTAR PRA TELA DE BATER PONTO
def voltar_ponto(destruir, mostrar1, mostrar2):
        mostrar2.pack() #MOSTRA 2 ITENS
        mostrar1.pack() 
        destruir.destroy() #DESTRUI UM FRAME

#ABRE CADASTRO
def abrirCadastro(funcao, telaEsconder, frameMostrar):
    funcao(telaEsconder, frameMostrar) #EXECUTA FUNCAO DE CADASTRO

#SAIR DE UM FRAME E ENTRANDO EM OUTRO
def voltar(sair, entrar):
    sair.pack() #EMPACOTA NOVO FRAME
    entrar.pack_forget() #DESEMPACOTA VELHO FRAME

#REINICIA CONTADORES DAS SUBTELAS DE UMA TELA PRINCIPAL
def reiniciarContador(contador): 
    for e in contador: #PERCORRE CONTADOR POR CONTADOR
        e[1] = False #TORNA-OS IGUAL A FALSE

#VOLTA ATÉ A TELA LOGIN
def voltar_login(mainFrameFechar, login, contador, main):
    mainFrameFechar.destroy() #DESTRUINDO FRAME ABERTO NO MOMENTO (TELA ANTERIOR)
    reiniciarContador(contador) #REINICIANDO CONTADOR DE SUBTELA DA TELA ANTERIOR    
    login(main) #ABRINDO TELA DE LOGIN (NOVA TELA)

#MUDA TEXT DE UM LABEL
def mudarText(lb, text):
    lb['text'] = 'Troco: %.2f R$'%(float(text))

