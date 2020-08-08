from funcoes import *
from sqlite_funcoes import *
import socket
import sqlite3

'''
               BANCO DE DADOS - SUA COMPRA v.0.1
________________________________________________________________________

      A comunicação aplicativo-banco se dá por meio da biblioteca socket
que permite enviar uma mensagem em binario através de uma porta e um IP.
Atualmente, esse banco só faz comunicação com o local host.
      Para que as mensagens sejam entendidas, elas após decodificadas
(passadas para binário), devem corresponder a uma String onde a primeira
palavra é a tabela a qual deseja utilizar, a segunda a função que deseja
executar e o resto os dados necessários para execução da função, como
segue o exemplo:

   1°.Mensagem_Envio = 'funcionario select * cpf="00000000000"')

   2°.'funcionario' a tabela,

   3°.'select' a função,

   4°.'* e cpf="00000000000"' as informações necessários para a execução
   da função.
   
      As funções utilizadas neste banco estão todas descritas e pron-
tas em outro arquivo chamado sqlite_funcoes.py.
_______________________________________________________________________
'''


#Configurando Socket
host = socket.gethostbyname(socket.gethostname())
port = 8000
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((host, port))
#Inicializando Banco
print("conectando...")  
while True:
      #Recebendo mensagem
      mensagem_bytes, endereco_ip_cliente = servidor.recvfrom(2048)
      #Decodificando mensagem
      mensagem_ = mensagem_bytes.decode()
      #Mostrando IP da máquina conectada
      print('\n\n{0} - CONECTADO'.format(endereco_ip_cliente[0]))
      dados = []
      #Testando se foi recebido algo
      if mensagem_:
            #Adicionando dados da mensagem na lista dados
            for info in mensagem_.split(" "):
                  dados.append(info)
            #Selecionando tabela filial
            if (dados[0] == 'filial'):
                    #Selecionando função select
                    if (dados[1] == "select"):                          
                          try: #VENDO SE O SELECT PASSANDO ESTÁ COMPLETO
                                if dados[2]: #TESTANDO SE HÁ RESTRIÇÕES NO SELECT
                                        mensagem_resposta = select_data(dados[0], dados[2], dados[3]) #SELECIONANDO E ARMAZENANDO EM RESPOSTA
                                        mensagem_resposta_string = "" 
                                        dados_select = [] #CRIANDO LISTA PARA TRABALHAR DADOS
                                        for e in mensagem_resposta: #PERCORRENDO A RESPOSTA
                                          dados_select.append(e) #ADICINANDO TERMO EM DADOS
                                        print('Resposta: {0}'.format(dados_select)) #MOSTRANDO DADOS
                                        for i in dados_select: 
                                          if i:
                                            i = str(i)
                                            mensagem_resposta_string += saving_name(i, ' ', '/')
                                        servidor.sendto(mensagem_resposta_string.encode(), endereco_ip_cliente) #ENVIANDO MENSAGEM

                          except IndexError:
                              #Selecionando dados
                              if len(dados) == 2: #TESTANDO SE É SOMENTE SELECT
                                  mensagem_resposta = select_data(dados[0])  #SELECIONANDO E ARMAZENANDO DADOS
                                  mensagem_resposta_string = " "
                                  dados_select = ['']
                                  dados_selec_ = ['']
                                  for e in mensagem_resposta: #PERCORRENDO MENSAGEM
                                    e = str(e)
                                    dados_select.append(e) #ADICIONANDO DADOS A dados_select
                                    dados_selec_[0] += e+' ' #CONCATENANDO DADOS A dados_select[0]
                                  print('Resposta: {0}'.format(dados_selec_[0])) #MOSTRANDO RESPOSTA A SER ENVIADA
                                  for i in dados_select: #ADICIONANDO DADOS A MENSAGEM DE RESPOSTA
                                    if i:
                                      i = str(i)
                                      mensagem_resposta_string += " " + saving_name(i, ' ', '/')
                                  servidor.sendto(mensagem_resposta_string.encode(), endereco_ip_cliente) #ENVIANDO MENSAGEM
                                  
                              else:
                                  mensagem_resposta = select_data(dados[0], dados[2]) #SELECIONANDO E ARMAZENANDO DADOS
                                  mensagem_resposta_string = " "
                                  dados_select = ['']
                                  dados_selec_ = ['']
                                  for e in mensagem_resposta: #ADICIONANDO DADOS A dados_select
                                    e = str(e)
                                    dados_select.append(e)
                                    dados_selec_[0] += e+' '
                                  print('Resposta: {0}'.format(dados_selec_[0])) #MOSTRANDO RESPOSTA A SER ENVIADA
                                  for i in dados_select:
                                    if i:
                                      i = str(i)
                                      mensagem_resposta_string += " " + saving_name(i, ' ', '/') 
                                  servidor.sendto(mensagem_resposta_string.encode(), endereco_ip_cliente) #ENVIANDO MENSAGEM
                    #SELECIONANDO FUNÇÃO DE MUDAR DADOS
                    elif (dados[1] == 'change'):
                          if change_data('vendido', dados[3], 1, dados[0]): #TESTANDO SE O DADO FOI MUDADO
                                mensagemResposta = "CAMPO ATUALIZADO COM SUCESSO" 
                                print('Resposta: {0}'.format(mensagemResposta)) #MOSTRANDO RESPOSTA
                                servidor.sendto(mensagemResposta.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA
                                
            #SELECIONANDO TABELA ESTOQUE
            elif (dados[0] == 'estoque'):
                    #SELECIONANDO FUNÇÃO ADICIONAR
                    if dados[1] == 'add':
                                  preco = dados[6].replace('.', ',') #TROCANDO PONTO POT VIRGULA NO PREÇO
                                  if add_dados_estoque(dados[2], dados[3], dados[4], dados[5], dados[6]): #ADICIONANDO DADOS AO ESTOQUE
                                    mensagem_resposta = "PRODUTO ADICIONADO" 
                                    print('Resposta: PRODUTO ADICIONADO') #IMPRIMINDO RESPOSTA
                                    servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA
                                  else:
                                    mensagem_resposta = "ERRO NA ADIÇÃO DO PRODUTO"
                                    print('Resposta: {0}'.format(mensagem_resposta)) #IMPRIMINDO RESPOSTA
                                    servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA

                    #SELECIONANDO FUNÇÃO MUDAR
                    elif dados[1] == 'change':
                                  if change_data(dados[2], dados[3], dados[4], dados[0]): #TESTANDO SE PRODUTO FOI MUDADO
                                    mensagem_resposta = "CAMPO ATUALIZADO COM SUCESSO"
                                    print('Resposta: {0}'.format(mensagem_resposta)) #IMPRIMINDO MENSAGEM
                                    servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente) #ENVIANDO MENSAGEM
                                  else:
                                    mensagem_resposta = False
                                    print('Resposta: CODIGO INCORRETO') #IMPRIMINDO MENSAGEM
                                    servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente) #ENVIANDO MENSAGEM

                    #SELECIONANDO FUNÇÃO SELECT
                    elif dados[1] == 'select':
                                #VENDO SE SELEÇÃO TEM RESTRIÇÃO
                                try:
                                        dados = select_data(dados[0], dados[2], dados[3]) #SELECIONANDO E ARMAZENANDO DADOS 
                                        mensagem_resposta = ' '
                                        if dados: #TESTANDO SE HÁ DADOS
                                              for i in dados: #PERCORRENDO DADOS
                                                mensagem_resposta += str(i) + ' ' #COCATENANDO DADOS PARA RESPOSTA
                                        print('Resposta: {0}'.format(mensagem_resposta)) #IMPRIMINDO RESPOSTA
                                        servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA
                                #VERIFICANDO SE MENSAGEM ESTÁ SEM SELEÇÃO
                                except IndexError:
                                        dados = select_data(dados[0]) #SELECIONANDO DADOS E ARMAZENANDO
                                        mensagem_resposta = ' '
                                        for i in dados:
                                                mensagem_resposta += str(i) + ' ' #COCATENANDO RESPOSTA
                                        print('Resposta: {0}'.format(mensagem_resposta)) #IMPRIMINDO RESPOSTA
                                        servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA

                  
            #Trabalhando com a tabela funcionario      
            elif (dados[0] == "funcionario"):
                    #Selecionando função
                    if(dados[1] == "add"):
                          if len(dados) > 6:
                                  nome = saving_name(dados[2], "/", " ") #TROCANDO AS BARRAS ESPAÇOS POR ESPAÇOS VAZIOS 

                                  #Realizando cadastro
                                  if add_dados_funcionario(nome, dados[3], dados[4], dados[5], dados[6], dados[7], dados[8], dados[9], dados[10]): #TESTANDO SE FOI ADICIONADO DADOS
                                    mensagem_resposta = "CADASTRO REALIZADO COM SUCESSO!" 
                                    print('Resposta: {0}'.format(mensagem_resposta)) #IMPRIMINDO RESPOSTA
                                    servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA

                                  #Retornando CPF já cadastrado
                                  else:
                                    mensagem_resposta = "CPF JÁ CADASTRADO"
                                    print('Resposta: {0}'.format(mensagem_resposta)) #IMPRIMINDO RESPOSTA
                                    servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA
                          
                    #Selecionando função
                    elif(dados[1] == "login"):

                                  #Testando dados Login
                                  if (select_data(dados[0], "cpf, senha, setor", "cpf = '{0}' and senha = '{1}' and setor = '{2}'".format(dados[2], dados[3], dados[4]))):
                                    mensagem_resposta = "LOGANDO..."
                                    print('Resposta: {0}'.format(mensagem_resposta))
                                    servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente)
                                  
                                  else:
                                    mensagem_resposta = "SENHA OU CPF INCORRETO"
                                    print('Resposta: {0}'.format(mensagem_resposta))
                                    servidor.sendto(mensagem_resposta.encode(), endereco_ip_cliente)

                    #Selecionando função
                    elif(dados[1] == "select"):
                          if len(dados) >= 4:
                                  mensagem_resposta = select_data(dados[0], dados[2], dados[3]) #SALVANDO DADOS EM MENSAGEM RESPOSTA
                                  mensagem_resposta_string = ""
                                  if mensagem_resposta:  #TESTANDO SE HÁ MENSAGEM RESPOSTA
                                    for a in range(0, len(mensagem_resposta)-1): #TRANSFORMANDO TUDO EM STRING
                                      mensagem_resposta[a] = str(mensagem_resposta[a])

                                    for i in range(0, len(mensagem_resposta)-1): #TROCANDO ESPAÇOS POR EXCLAMAÇÃO
                                      mensagem_resposta[i] = saving_name(mensagem_resposta[i], ' ', '!')


                                    for e in mensagem_resposta: #COCATENANDO RESPOSTA
                                      mensagem_resposta_string += ' '+e
                                    print('Resposta: {0}'.format(mensagem_resposta_string)) #IMPRIMINDO RESPOSTA
                                    servidor.sendto(mensagem_resposta_string.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA
                                  else:
                                    mensagemResposta = 'DADOS INVÁLIDOS'
                                    print('Resposta: {0}'.format(mensagemResposta)) #IMPRIMINDO RESPOSTA
                                    servidor.sendto(mensagemResposta.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA

                          else:
                              try:
                                  #Selecionando dados
                                  mensagem_resposta = select_data(dados[0], '*', 'cpf = "{1}"'.format(dados[2])) #SALVANDO DADOS EM MENSAGEM RESPOSTA
                                  mensagem_resposta_string = ""
                                  if mensagem_resposta: #TESTANDO SE HÁ MENSAGEM RESPOSTA
                                    for a in range(0, len(mensagem_resposta)-1): #TRANSFORMANDO TUDO EM STRING
                                      mensagem_resposta[a] = str(mensagem_resposta[a])
                                      mensagem_resposta[a] = str(mensagem_resposta[a])
                                    for i in range(0, len(mensagem_resposta)-1): #TROCANDO ESPAÇOS POR EXCLAMAÇÃO
                                      mensagem_resposta[i] = saving_name(mensagem_resposta[i], ' ', '!')

                                    for e in mensagem_resposta: #ADICIONANDO DADOS A MENSAGEM
                                      mensagem_resposta_string += ' '+e
                                    print('Resposta: {0}'.format(mensagem_resposta_string))
                                    servidor.sendto(mensagem_resposta_string.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA
                              except IndexError:
                                  #Selecionando dados
                                  if len(dados) == 4:
                                        mensagem_resposta = select_data(dados[0], '*', '{0}'.format(dados[3])) #ADICIONANDO DADOS A MENSAGEM
                                        mensagem_resposta_string = ""
                                        if mensagem_resposta:
                                          for a in range(0, len(mensagem_resposta)-1): #TRANSFORMANDO DADOS EM STRING
                                            mensagem_resposta[a] = str(mensagem_resposta[a]) 
                                            mensagem_resposta[a] = str(mensagem_resposta[a])
                                          for i in range(0, len(mensagem_resposta)-1): #TROCANDO ESPAÇOS EM BANCO POR EXCLAMAÇÃO
                                            mensagem_resposta[i] = saving_name(mensagem_resposta[i], ' ', '!')

                                          for e in mensagem_resposta:
                                            mensagem_resposta_string += ' '+e
                                          print('Resposta: {0}'.format(mensagem_resposta_string))
                                          servidor.sendto(mensagem_resposta_string.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA
                                  elif len(dados) == 3:
                                        mensagem_resposta = select_data(dados[0], '{0}'.format(dados[2])) #SELECIONANDO E ADICIONANDO EM MENSAGEM RESPOSTA
                                        mensagem_resposta_string = ""
                                        if mensagem_resposta:
                                          for a in range(0, len(mensagem_resposta)-1): #TRANSFORMANDO DADOS EM STRING
                                            mensagem_resposta[a] = str(mensagem_resposta[a])
                                            mensagem_resposta[a] = str(mensagem_resposta[a])
                                          for i in range(0, len(mensagem_resposta)-1):
                                            mensagem_resposta[i] = saving_name(mensagem_resposta[i], ' ', '!') #TROCANDO ESPAÇOS EM BANCO POR EXCLAMAÇÃO

                                          for e in mensagem_resposta:
                                            mensagem_resposta_string += ' '+e
                                          print('Resposta: {0}'.format(mensagem_resposta_string))
                                          servidor.sendto(mensagem_resposta_string.encode(), endereco_ip_cliente) #ENVIANDO RESPOSTA
                                       
                                  
                    

                    else:
                                  print('Função {0} não encontrada'.format(dados[1]))
            else:
                  print('Tabela {0} não encontrada'.format(dados[1]))
