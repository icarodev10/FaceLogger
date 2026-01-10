import sqlite3

# Conecta no arquivo que já existe
conn = sqlite3.connect('face_logger.db')
cursor = conn.cursor()

# O comando SQL para "Selecionar Tudo" da tabela
cursor.execute("SELECT * FROM logs_acesso ORDER BY id DESC") 
# 'ORDER BY id DESC' mostra os mais recentes primeiro

dados = cursor.fetchall() # Pega tudo e joga numa lista

conn.close() # Fecha a conexão

# --- Formatação ---
print("\n📊 DATA CONTROL 📊")
print("-" * 60)
print(f"{'ID':<5} | {'DATETIME':<28} | {'EVENT'}")
print("-" * 60)

for linha in dados:
    # Tupla: (1, '2026-01-07...', 'Rosto...')
    id_log = linha[0]
    data = linha[1]
    evento = linha[2]
    
    print(f"{id_log:<5} | {data:<28} | {evento}")

print("-" * 60)