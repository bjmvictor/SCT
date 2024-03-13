from logSystem import logging as log
from datetime import datetime
import win32ts as sys
import time
import subprocess
import socket
from datetime import datetime
import pytz

# Inicia variáveis para tratamento de login
last_user = None
show_alert = False
path = r"C:/Users/Public/Documents/Python/SCT/Service/userinfo/" #"C:/Users/Public/Documents/Python/SCT/Service/userinfo/"


def obter_data_global(servidor_de_tempo='time.nist.gov', porta=13, fuso_horario='America/Sao_Paulo'):
    # Conectar-se ao servidor de tempo
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((servidor_de_tempo, porta))
        resposta = s.recv(1024).decode('utf-8')

    # Extrair a parte relevante da resposta (hora)
    hora_str = resposta.split()[2]  # Ajuste do índice para obter a parte correta da resposta

    # Obter a data atual
    data_atual = datetime.now().date()

    # Concatenar a hora à data atual para criar um objeto datetime
    data_hora_str = f"{data_atual} {hora_str}"
    data_utc = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")

    # Adicionar informações do fuso horário
    fuso = pytz.timezone(fuso_horario)
    data_global = fuso.localize(data_utc).date()

    return data_global

# Função para obter o usuário atual
def get_logged_in_username():
    session_id = sys.WTSGetActiveConsoleSessionId()
    username = sys.WTSQuerySessionInformation(None, session_id, sys.WTSUserName)
    return username

# Função para obter valores da planilha
def obter_dados():
    try:
        with open(path + get_logged_in_username() + ".info", "r") as user_info:
            # Lê as três primeiras linhas do arquivo
            linhas = user_info.readlines()[:3]

            #Grava nos logs os valores obtidos -Ajuda a identificar problemas com a obtenção dos dados!
            log.info(f"Valores obtidos: {linhas}")

            # Obtém o tempo máximo do usuário
            tempo_usuario = int(linhas[0].strip())

            # Obtém a data de login
            data_login = datetime.strptime(linhas[1].strip(), '%Y-%m-%d').date()

            # Obtém valores do tempo de uso
            tempo_uso = int(linhas[2].strip())

            return tempo_usuario, data_login, tempo_uso

    except FileNotFoundError:
        log.error(f'Arquivo do usuário não encontrado, criando um novo..')
        # Obtem a data atual no formato DD/MM/YYYY
        data_atual = datetime.now().strftime('%Y-%m-%d')
        # Define as informações a serem salvas no arquivo do usuário
        usuario = get_logged_in_username()
        linhas = [f'{3}\n', f'{data_atual}\n', '0\n']
        if usuario == "bjvie":
            linhas = [f'{3}\n', f'{data_atual}\n', '0\n']
        elif usuario == "bvictor":
            linhas = [f'{10}\n', f'{data_atual}\n', '0\n']
        else:
            linhas = [f'{2}\n', f'{data_atual}\n', '0\n']

        with open(path + get_logged_in_username() + ".info", 'w') as file:
            file.writelines(linhas)
        return int(linhas[0]), data_atual, int(linhas[2])

    except Exception as e:
        log.error(f"Arquivo existe mas ocorreu um erro ao obter dados: {e}")
        # Obtem a data atual no formato DD/MM/YYYY
        data_atual = datetime.now().strftime('%Y-%m-%d')
        # Define as informações a serem salvas no arquivo do usuário
        usuario = get_logged_in_username()
        linhas = [f'{3}\n', f'{data_atual}\n', '0\n']
        if usuario == "bjvie":
            linhas = [f'{3}\n', f'{data_atual}\n', '0\n']
        elif usuario == "bvictor":
            linhas = [f'{10}\n', f'{data_atual}\n', '0\n']
        else:
            linhas = [f'{2}\n', f'{data_atual}\n', '0\n']

        # Registrar valores obtidos nos logs após erro
        with open(path + get_logged_in_username() + ".info", "r") as user_info:
            # Lê as três primeiras linhas do arquivo
            linhas = user_info.readlines()[:3]

            #Grava nos logs os valores obtidos
            log.error(f"Valores obtidos: {linhas}")

        with open(path + get_logged_in_username() + ".info", 'w') as file:
            file.writelines(linhas)
        return int(linhas[0]), data_atual, int(linhas[2])


def alterar_dado(valor, linha):
    try:
        # Obtém os valores atuais
        tempo_usuario, data_login, tempo_uso = obter_dados()

        # Altera o valor de acordo com a linha especificada
        if linha == 1:
            tempo_usuario = valor
        elif linha == 2:
            data_login = valor
        elif linha == 3:
            tempo_uso = valor
        else:
            log.error(f"Linha não disponível para alteração: linha {linha}")
            return

        # Garante que os valores sejam válidos antes de escrever no arquivo
        tempo_usuario = max(0, tempo_usuario)
        tempo_uso = max(0, tempo_uso)

        # Escreve os novos valores de volta no arquivo
        with open(path + get_logged_in_username() + ".info", 'w') as user_info:
            user_info.write(f"{tempo_usuario}\n{data_login}\n{tempo_uso}\n")

    except FileNotFoundError:
        log.error("Ocorreu um erro ao ler o arquivo principal, arquivo não encontrado.")
    except Exception as e:
        log.error(f"Ocorreu um erro ao atualizar os dados: {e}")

# Loop principal
while True:
    # Obtem o usuário atual da sessão
    usuario = get_logged_in_username()

    # Verifica se o usuário está logado mesmo
    if usuario == 'SISTEMA' or usuario == '' or usuario == None:
        time.sleep(10)
        print(f"Usuário indisponivel para controle de tempo. usuario: {usuario}")
        break

    # Verifica se outro usuário fez login
    if last_user != usuario:
        show_alert = True
        last_user = usuario

    tempoExtra = 15 * 60  # Tempo extra de 15 minutos

    tempoMax, dtLogin, tempoUso = obter_dados()

    # Converte valores relevantes para tipos apropriados
    tempoUso = int(tempoUso)
    tempoMax = int(tempoMax)

    # Realiza a operação matemática
    tempoMax = (tempoMax * 60 * 60) + tempoExtra

    # Obtem a data atual no formato YYYY-MM-DD
    data_atual = obter_data_global()

    # Registra log e verifica se a data de login é diferente da data atual
    ## Se a data for diferente o código atualiza a data e o tempo de uso e sai do loop (reiniciando o código)
    if str(data_atual) != str(dtLogin):
        print(f"DATA ATUAL: {obter_data_global()}, DATA LOGIN: {obter_data_global()}")
        log.info(f'Atualizando a data no banco do usuário: {usuario}')
        try:
            alterar_dado(data_atual, 2)
            alterar_dado(0, 3)
            tempoUso = 0
        except Exception as e:
            log.error(e)

    # Verifica se deve exibir a mensagem sobre o tempo
    if show_alert and tempoUso < tempoMax:
        tempoRestante = tempoMax - tempoUso
        horas_restantes = tempoRestante // 3600
        minutos_restantes = (tempoRestante % 3600) // 60
        log.info(f'O usuário: {usuario} fez login. Tempo restante: {horas_restantes} horas e {minutos_restantes} minutos.')
        #subprocess.run(['msg', usuario, f'Seu tempo de uso é de {horas_restantes} horas e {minutos_restantes} minutos.'])
        show_alert = False

    # Verifica se o tempo de uso esgotou
    if tempoUso >= tempoMax:
        log.info(f'O usuário: {usuario}, chegou ao limite do tempo máximo: {tempoMax // 3600} horas e 15 minutos. Desligando...')

        # Desliga o computador
        subprocess.run(['msg', "*", f'{usuario} Seu tempo acabou, desligando em 10 segundos...'])
        subprocess.run(['shutdown', '/f', '/s', '/t', '10'] )
        subprocess.run(['net user', f'{usuario}', '/active:no'])
        time.sleep(60)
    else:
        time.sleep(10)
        # Continua adicionando tempo à sessão do usuário
        tempoUso += 10
        alterar_dado(tempoUso, 3)
