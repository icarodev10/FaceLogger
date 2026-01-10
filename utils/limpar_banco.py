import sqlite3
conn = sqlite3.connect('face_logger.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM logs_acesso") # Apaga tudo
cursor.execute("DELETE FROM sqlite_sequence WHERE name='logs_acesso'") # Reseta o AUTOINCREMENT
conn.commit()
conn.close()
print("Banco limpo! ✨")