from funcoes import *
import sqlite3
def create_database_estoque():
        conn = sqlite3.connect('dados.db')
        cursor = conn.cursor()
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS estoque (
            id INTERGER PRIMARY KEY,
            descricao VARCHAR(20),
            marca VARCHAR(20),
            quantidade INTEGER,
            preco FLOAT);
        """)
        conn.commit()
        conn.close()

def create_database_filial():        
  conn = sqlite3.connect('dados.db')
  cursor = conn.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS filial(
      id INTEGER PRIMARY KEY NOT NULL,
      email VARCHAR(30) NOT NULL,
      senha VARCHAR(11) NOT NULL,
      cidade VARCHAR(15)  NOT NULL,
      estado VARCHAR(15) NOT NULL,
      vendido VARCHAR(15))
    ''')
  conn.commit()
  cursor.close

 #CRIA TABELA FUNCIONARIOS CASO NÃO EXISTA
def create_database_funcionario():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionario(
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      nome VARCHAR(30) NOT NULL,
      email VARCHAR(11) NOT NULL,
      senha VARCHAR(30) NOT NULL,
      cpf VARCHAR(15)  NOT NULL,
      rg VARCHAR (15) NOT NULL,
      cidade VARCHAR(15) NOT NULL,
      estado VARCHAR(15) NOT NULL,
      matricula VARCHAR(10) NOT NULL,
      setor VARHCAR(20) NOT NULL,
      filial VARCHAR(20))
    ''')
    conn.commit()
    cursor.close

#ADICIONANDO DADOS AO ESTOQUE 
def add_dados_estoque(id_, descricao, marca, quantidade, preco):
  conn = sqlite3.connect('dados.db')
  cursor = conn.cursor()
  print('COMMAND: INSERT INTO estoque(id, descricao, marca, quantidade, preco) VALUES(?, ?, ?, ?, ?)', (id_, descricao, marca, quantidade, preco))
  cursor.execute('''
    INSERT INTO estoque(id, descricao, marca, quantidade, preco)
      VALUES(?, ?, ?, ?, ?)
    ''', (id_, descricao, marca, quantidade, preco))
  conn.commit()
  cursor.close
  return True
  

# Gerando número da matricula
def gerando_matricula():
  conn = sqlite3.connect('dados.db')
  cursor = conn.cursor()
  matricula = 0
  matriculas_cadastradas = []
  cursor.execute('''
    SELECT matricula FROM funcionario
    ''')
  matriculas = cursor.fetchall()
  if matriculas:
    for i in matriculas:
        matriculas_cadastradas.append(i[0])
        ultima_matricula =  matriculas_cadastradas[len(matriculas_cadastradas)-1]
        matricula = int(ultima_matricula)+1
  else:
        matricula = 10000
  return (matricula)


 #ADICIONA NOVOS FUNCIONARIOS AO BANCO
def add_dados_funcionario(nome, email, senha, cpf, rg, cidade, estado, setor, filial):

  if(setor == 2):
    setor = "Gerente"
  elif(setor == 1):
    setor = 'Cliente'
  elif(setor == 3):
    setor = 'Caixa'
  elif(setor == 4):
    setor = 'Estoquista'
    
  conn = sqlite3.connect('dados.db')
  cursor = conn.cursor()
  #Testando se já está cadastrado
  cursor.execute("SELECT * FROM funcionario WHERE cpf = '{0}' or rg = '{1}'""".format(cpf, rg))
  dados = cursor.fetchone()
  if not dados:
    print('''COMMAND: INSERT INTO funcionario(nome, email, senha, cpf, rg, cidade, estado, matricula, setor, filial) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (nome, email, senha, cpf, rg, cidade, estado, gerando_matricula(), setor, filial))
    # Inserindo dados no banco      
    cursor.execute('''
      INSERT INTO funcionario(nome, email, senha, cpf, rg, cidade, estado, matricula, setor, filial)
      VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ''', (nome, email, senha, cpf, rg, cidade, estado, gerando_matricula(), setor, filial))
    conn.commit()
    cursor.close
    return True
  else:
    return False



 
#INSERT
def insert_data(tabela, campos, values, banco='dados.db'):
  conn = sqlite3.connect(banco)
  cursor = conn.cursor()
  if values[1]:
    print('''COMMAND: INSERT INTO {0}({1}) VALUES({2})'''.format(tabela, campos, values))
    cursor.execute('''
      INSERT INTO {0}({1})
      VALUES({2} )
      '''.format(tabela, campos, values))
  else:
    print('''COMMAND: INSERT INTO {0}({1}) VALUES('{2}', ) '''.format(tabela, campos, values))
    cursor.execute('''
      INSERT INTO {0}({1})
      VALUES('{2}', )
      '''.format(tabela, campos, values))
  conn.commit()
  cursor.close
  
  
#SELECT
def select_data(tabela, campos="*", restricao=None, banco='dados.db'):
  conn = sqlite3.connect(banco)
  cursor = conn.cursor()
  if restricao:
    print("COMMAND: SELECT {0} FROM {1} WHERE {2}".format(campos, tabela, restricao))
    cursor.execute("SELECT {0} FROM {1} WHERE {2}".format(campos, tabela, restricao))
  else:
    print("COMMAND: SELECT {0} FROM {1}".format(campos, tabela))
    cursor.execute("SELECT {0} FROM {1}".format(campos, tabela))
    
  dados = cursor.fetchall()
  if dados:
    dados_list = []
    for e in dados:
      for i in e:
        dados_list.append(i)
    return (dados_list) 
  else:
    return False

#ADD COLUMN
def add_column(tabela, column, carac, banco='dados.db'):
  conn = sqlite3.connect(banco)
  cursor = conn.cursor()
  print('''COMMAND: ALTER TABLE {0} ADD {1} {2}'''.format(tabela, column, carac))
  cursor.execute('''
    ALTER TABLE {0}
      ADD {1} {2}
    '''.format(tabela, column, carac))
  dados = cursor.fetchone()
  conn.commit()
  cursor.close
  
#DELETE  
def delete_data(identificador, tabela, banco='dados.db'):
  conn = sqlite3.connect(banco)
  cursor = conn.cursor()
  if tabela == 'funcionario':
    cpf, rg = identificador.split()
    print("COMMAND: DELETE FROM {2} WHERE cpf = '{0}' AND rg = '{1}'".format(cpf, rg, tabela))
    cursor.execute("DELETE FROM {2} WHERE cpf = '{0}' AND rg = '{1}'".format(cpf, rg, tabela))
  elif tabela == 'estoque':
    print("DELETE FROM {0} WHERE id = '{1}'".format(tabela, identificador))
    cursor.execute("DELETE FROM {0} WHERE id = '{1}'".format(tabela, identificador))    
  dados = cursor.fetchone()
  conn.commit()
  cursor.close

#CHANGE
def change_data(campo, dadoAtualizado, identificador, tabela, banco='dados.db'):
  conn = sqlite3.connect(banco)
  cursor = conn.cursor()
  if (campo == 'cpf' or campo == 'nome' or campo == 'rg' or campo == "matricula"):
    return False
  else:
  
    if (tabela == "funcionario"): 
      print('''COMMAND: UPDATE funcionario SET {0} = "{1}" WHERE cpf = "{2}"'''.format(campo, dadoAtualizado, identificador))
      cursor.execute('''UPDATE funcionario
                        SET {0} = "{1}"
                        WHERE cpf = "{2}"'''.format(campo, dadoAtualizado, identificador))
      conn.commit()  
      cursor.close
      return True

    elif (tabela == 'estoque'):
      print('''COMMAND: UPDATE estoque SET {0} = "{1}" WHERE id = {2}'''.format(campo, dadoAtualizado, identificador))
      cursor.execute('''UPDATE estoque
                        SET {0} = "{1}"
                        WHERE id = {2}'''.format(campo, dadoAtualizado, identificador))
      cursor.execute('''SELECT id,{0} FROM estoque WHERE id = {1}'''.format(campo, identificador))
      conn.commit()
      cursor.close
      return True

    elif (tabela == 'filial'):
      print('''COMMAND: UPDATE filial SET {0} = "{1}" WHERE id = {2}'''.format(campo, dadoAtualizado, identificador))
      cursor.execute('''UPDATE filial
                        SET {0} = "{1}"
                        WHERE id = {2}'''.format(campo, dadoAtualizado, identificador))
      cursor.execute('''SELECT id,{0} FROM filial WHERE id = {1}'''.format(campo, identificador))
      conn.commit()
      cursor.close
      return True
      


def add_varios_dados(campo, dadoAtualizado, tabela, banco='dados.db'):
        conn = sqlite3.connect(banco)
        cursor = conn.cursor()
        if tabela == 'funcionario':
          print('''COMMAND: SELECT cpf, {0} FROM {1}'''.format(campo, tabela))
          cursor.execute('''SELECT cpf, {0} FROM {1}'''.format(campo, tabela))
          dados = []
          for e in cursor.fetchall():
            dados.append(e)
          for i in dados:
            change_data(campo, dadoAtualizado, i[0], tabela)
        elif tabela == 'estoque':
                
           print('''COMMAND: SELECT id, {0} FROM {1}'''.format(campo, tabela))
           cursor.execute('''SELECT id, {0} FROM {1}'''.format(campo, tabela))
           dados = []
           for e in cursor.fetchall():
             dados.append(e)
           for i in dados:
             change_data(campo, dadoAtualizado, i[0], tabela)

create_database_estoque()
create_database_filial()
create_database_funcionario()


