import socket
from tkinter.filedialog import askopenfilename
import sqlite3

#TROCA O IDENTIFICADOR PELO NOME DO SETOR
def setor_string(setor_int):
    if setor_int == 2 or setor_int == '2':
        setor_int = "Gerente"
        return (setor_int)
    
    if setor_int == 3 or setor_int == '3':
        setor_int = "Caixa"
        return (setor_int)
        
    if setor_int == 4 or setor_int == '4':
        setor_int = "Estoquista"
        return (setor_int)

#BUSCA ARQUIVOS NO PC
def buscar_arquivo():
    filename = askopenfilename() # Isto te permite selecionar um arquivo
    return (filename)

#DESCOMPACTAR NOME A PARTIR DAS BARRAS
def saving_name(string, carac_1, carac_2):
    string = string.replace(carac_1, carac_2)
    return string
    
#TROCA ESPAÇOS EM BRANCO
def compacta_string(string, carac1, carac2):
    string_envio = string.replace(carac1, carac2)
    return(string_envio)

#FORMATA E CONCATENA STRINGS SALVANDO-AS EM UMA LISTA
def Formata1(i, palavra, saida, lmt):
  if len(palavra) <= lmt:
    saida[i] += (palavra + (lmt - len(palavra)- 1)*" ")+"|"
    print(lmt-len(palavra))
    
def enviar_socket(mensagem, host=socket.gethostbyname(socket.gethostname())):
    host = socket.gethostbyname(socket.gethostname())
    porta = 8000
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    desconectado = True
    while True:
                mensagem_envio = mensagem
                cliente.sendto(mensagem_envio.encode(), (host, porta))
                mensagem_serv, ip_serv = cliente.recvfrom(2048)
                if mensagem_serv:
                    return(mensagem_serv.decode())
                    break
                else:
                    break
                            


#Esta função vai calcular o preço que o cliente vai pagar pelo produtto de acordo com preco que se encontra no banco'''
def calcular(preco,quantidade_valor, valor):
    valor += (preco*quantidade_valor)
    return(valor)

