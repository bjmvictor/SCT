import sqlite3

# Conecte-se ao banco de dados (se não existir, será criado)
conexao = sqlite3.connect('database.db')
cursor = conexao.cursor()

# Crie a tabela de usuários
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    cd_usuario INTEGER PRIMARY KEY,
                    login_usuario TEXT,
                    nm_usuario TEXT,
                    data_login TEXT,
                    tempo_uso INTEGER,
                    tempo_maximo INTEGER,
                    sn_admin INTEGER
                  )''')
