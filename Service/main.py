from logSystem import logging as log
from datetime import datetime
import win32ts as sys
import time
import subprocess
import socket
from datetime import datetime
import pytz
import sqlite3

# Inicia variáveis para tratamento de login
last_user = None
show_alert = False
tempoExtra = 15                                        # Minutos
path = r"C:\Users\benjamin.vieira\Documents\Python\SCT\Service"  # Diretório do programa
database_dir = path + r"/database.db"                   # Nome do banco .db

# Obtem a data da rede utilizando o fuso horário de São Paulo
def obter_data_global(servidor_de_tempo='time.nist.gov', porta=13, fuso_horario='America/Sao_Paulo'):
    # Conecta ao servidor de tempo
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((servidor_de_tempo, porta))
        resposta = s.recv(1024).decode('utf-8')

    # Extrai o horário do resultado
    hora_str = resposta.split()[2]

    # Obtem a data atual
    data_atual = datetime.now().date()

    # Concatenar a hora à data atual para criar um objeto datetime
    data_hora_str = f"{data_atual} {hora_str}"
    data_utc = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")

    # Adicionar informações do fuso horário
    fuso = pytz.timezone(fuso_horario)
    data_global = fuso.localize(data_utc).date()

    return data_global

# Função para obter o atual usuário logado no sistema
def get_logged_in_username():
    session_id = sys.WTSGetActiveConsoleSessionId()
    username = sys.WTSQuerySessionInformation(None, session_id, sys.WTSUserName)
    return username

# Função para obter valores da planilha
def obter_dados(usuario):
    try:
        ##\DEBUG
        ##-\print(f"Realizando consulta no banco: {database_dir}")
        # Conectar ao banco de dados
        conn = sqlite3.connect(database_dir)
        cursor = conn.cursor()

        # Execute a consulta pelas informaçoes do usuário
        cursor.execute(f"SELECT nm_usuario, tempo_maximo, data_login, tempo_uso FROM usuarios WHERE login_usuario = '{usuario}'")

        # Recupera resultados da consulta
        resultados = cursor.fetchall()

        # Feche a conexão com o banco de dados
        conn.close()

        #Retorna os valores na ordem: Tempo máximo, Data de login, Tempo de uso(atual)
        return resultados[0][0], resultados[0][1], resultados[0][2], resultados[0][3]

    #Salvar log em caso de erros
    except Exception as e:
        log.error(f"Ocorreu um erro ao obter os dados do usuário '{usuario}' \n erro:{e}")
        subprocess.run(["msg", "*", f"Ocorreu um erro ao obter os dados do usuário '{usuario}' \n ERRO:{e}"])

# Função para alterar dados do usuário no banco
def alterar_dados(usuario=None, nome=None, data_login=None, tempo_uso=None, tempo_maximo=None):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(database_dir)
        cursor = conn.cursor()

        # Cria uma lista para armazenar os valores
        novos_valores = []

        # Inicia o comando SQL
        sql = "UPDATE usuarios SET "

        # Define o SQL dinamicamente de acordo com as valores fornecidos
        if usuario is not None:
            if nome is not None:
                sql += "nm_usuario=?, "
                novos_valores.append(nome)
            if data_login is not None:
                sql += "data_login=?, "
                novos_valores.append(data_login)
            if tempo_uso is not None:
                sql += "tempo_uso=?, "
                novos_valores.append(tempo_uso)
            if tempo_maximo is not None:
                sql += "tempo_maximo=?, "
                novos_valores.append(tempo_maximo)

            # Remove a vírgula no final do SQL e adiciona o WHERE
            sql = sql.rstrip(', ') + " WHERE login_usuario=?"

            # Adicione o cd_usuario à lista de valores
            novos_valores.append(usuario)

            # Execute inserção
            cursor.execute(sql, novos_valores)

            # Commit para salvar as alterações
            conn.commit()

            # Fecha a conexão com o banco
            conn.close()
        else:
            log.error("Falha, o usuário não foi referenciado ao chamar a função: alterar_dados()")
    except Exception as e:
        log.error(f"Ocorreu um erro ao atualizar dados do usuário. Erro: {e}")

# Função para registrar histórico de login dos usuários
def registrar_login(usuario, nm_usuario, tempo_restante, dt_login):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(database_dir)
        cursor = conn.cursor()

        # Comando SQL para inserção dos dados
        sql = "INSERT INTO historico_login (login_usuario, nm_usuario, tempo_restante, dt_login) VALUES (?, ?, ?, ?)"
        
        # Executa o comando, inserindo os dados no banco
        cursor.execute(sql, (usuario, nm_usuario, tempo_restante, dt_login))

        # Commit para salvar as alterações
        conn.commit()

        # Fecha a conexão com o banco
        conn.close()
    
    # Em caso de erro na execução, registra o erro no log
    except Exception as e:
        log.error(f"Ocorreu uma problema ao registrar o histórico de login do usuário: {nm_usuario}. Erro: {e}")
        

# Loop principal
while True:
    # Obtem o usuário atual da sessão
    usuario = get_logged_in_username()

    # Verifica se o usuário está logado
    if usuario == 'SISTEMA' or usuario == '' or usuario == None:
        log.log(f"Usuário '{usuario}' indisponível para controle de tempo.")
        print(f"Usuário '{usuario}' indisponível para controle de tempo.")
        time.sleep(10)
        break

    # Verifica se deve exibir a mensagem de tempo restante
    if last_user != usuario:
        show_alert = True
        last_user = usuario

    # Calcula e transforma o tempo extra (minutos para segundos)
    tempoExtra *= 60

    # Obtem os valores do usuário
    nmUsuario, tempoMax, dtLogin, tempoUso = obter_dados('bvictor')

    # Converte os valores para inteiro (Garante que não aconteça exceções na execução)
    tempoUso = int(tempoUso)
    tempoMax = int(tempoMax)

    # Adiciona o tempo extra ao tempo restante
    tempoMax += tempoExtra

    ##\DEBUG
    ##-\print(f"TEMPO RESTANTE: {tempoMax}")

    # Obtem a data atual no formato global: YYYY-MM-DD
    data_atual = obter_data_global()

    # Registra log e verifica se a data de login é diferente da data atual
    ## Se a data for diferente o código atualiza a data e o tempo de uso e sai do loop (reiniciando o código)
    if str(data_atual) != str(dtLogin):
        ##\DEBUG
        ##-\print(f"DATA ATUAL: {obter_data_global()}, DATA LOGIN: {obter_data_global()}")
        log.info(f'Atualizando a data no banco do usuário: {usuario}')
        try:
            alterar_dados(usuario=usuario, data_login=str(data_atual), tempo_uso=0)
            tempoUso = 0
        except Exception as e:
            log.error(e)

    # Verifica se deve exibir a mensagem sobre o tempo
    if show_alert and tempoUso < tempoMax:
        tempoRestante = tempoMax - tempoUso
        horas_restantes = tempoRestante // 3600
        minutos_restantes = (tempoRestante % 3600) // 60
        registrar_login(usuario, nmUsuario, f"Tempo restante: {horas_restantes} horas e {minutos_restantes} minutos.", str(data_atual))
        log.info(f'O usuário: {usuario} fez login. Tempo restante: {horas_restantes} horas e {minutos_restantes} minutos.')
        subprocess.run(['msg', '*',  f'Seu tempo de uso é de {horas_restantes} horas e {minutos_restantes} minutos.'])
        show_alert = False

    # Verifica se o tempo de uso esgotou
    if tempoUso >= tempoMax:
        log.info(f'O usuário: {usuario}, chegou ao limite do tempo máximo: {tempoMax // 3600} horas e 15 minutos. Desligando...')

        # Desliga o computador
        subprocess.run(['msg', '*', f'Seu tempo acabou, desligando...'])
        subprocess.run(['shutdown', '/f', '/s', '/t', '0'])
        time.sleep(60)

        # Após executar o desligamento, sai do loop principal
        break
    else:
        if (tempoUso+15) >= tempoMax:
            subprocess.run(['msg', '*', f'Desligando em 15 segundos.'])
        time.sleep(10)

        # Continua adicionando tempo à sessão do usuário
        tempoUso += 10
        alterar_dados(usuario=usuario, tempo_uso=tempoUso)