import sqlite3
import config

# Função para obter valores da planilha
def obter_dados(usuario):
    # Conecte-se ao banco de dados
    conn = sqlite3.connect('Service\database.db')
    cursor = conn.cursor()

    # Execute a consulta SQL
    cursor.execute(f"SELECT tempo_maximo, data_login, tempo_uso FROM usuarios WHERE login_usuario = '{usuario}'")

    # Recupere os resultados da consulta
    resultados = cursor.fetchall()

    info = []
    print(resultados[0][0], resultados[0][1], resultados[0][2])
    # Imprima os resultados
    for linha in resultados:
        print(linha[0])

    # Feche a conexão com o banco de dados
    conn.close()

# Função para alterar dados do usuário no banco
def alterar_dados(usuario=None, nome=None, data_login=None, tempo_uso=None, tempo_maximo=None):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(config.database_dir)
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
            print("Falha, o usuário não foi referenciado ao chamar a função: alterar_dados()")
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar dados do usuário. Erro: {e}")

obter_dados('bvictor')

alterar_dados(usuario="bvictor", tempo_uso="40")

obter_dados("bvictor")