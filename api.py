from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import datetime

app = FastAPI()

# --- CONFIGURAÇÃO DO CORS (Liberando geral pra teste local) ---
origins = ["*"] # "Aceita conexão de qualquer lugar"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------------------------


# --- CRIAÇÃO DO BANCO DE DADOS ---
def init_db():
    """Inicializa o banco e cria a tabela se não existir."""
    
    # Conecta (e cria o arquivo se não existir)
    conn = sqlite3.connect('face_logger.db')
    cursor = conn.cursor()

    # Cria a tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_acesso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            tipo_evento TEXT NOT NULL,
            foto_base64 TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

init_db()

# -----------------------------------------------------------

class LogRecebido(BaseModel):
    evento: str
    imagem_base64: str = ""

# 1. Rota raiz que retorna tela de dashboard
@app.get("/", response_class=HTMLResponse)
def dashboard():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard FaceLogger</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 20px; }
            h1 { text-align: center; color: #00ff88; text-transform: uppercase; letter-spacing: 2px; }
            
            .container { max-width: 900px; margin: 0 auto; }
            
            .card { background-color: #1e1e1e; border-radius: 10px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th { text-align: left; padding: 12px; border-bottom: 2px solid #333; color: #888; font-size: 0.9em; }
            td { padding: 15px 12px; border-bottom: 1px solid #333; vertical-align: middle; }
            
            .time { color: #888; font-size: 0.85em; }
            .event { font-weight: bold; font-size: 1.1em; }
            .img-preview { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; border: 2px solid #333; }
            
            /* Animaçãozinha de entrada */
            tr { animation: fadeIn 0.5s ease; }
            @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Control Center</h1>
            <div class="card">
                <table>
                    <thead>
                        <tr>
                            <th>PIC</th>
                            <th>EVENT</th>
                            <th>DATETIME</th>
                        </tr>
                    </thead>
                    <tbody id="tabela-corpo">
                        </tbody>
                </table>
            </div>
        </div>

        <script>
            async function atualizarLogs() {
                try {
                    const response = await fetch('/logs');
                    const dados = await response.json();
                    
                    const tbody = document.getElementById('tabela-corpo');
                    tbody.innerHTML = ''; // Limpa tabela
                    
                    dados.forEach(log => {
                        const tr = document.createElement('tr');
                        
                        // Foto (se tiver base64, mostra, senao mostra icone)
                        let imgHtml = '<div style="width:50px; height:50px; background:#333; border-radius:50%"></div>';
                        if(log.foto && log.foto.length > 10) {
                            imgHtml = `<img src="data:image/jpeg;base64,${log.foto}" class="img-preview">`;
                        }

                        tr.innerHTML = `
                            <td>${imgHtml}</td>
                            <td class="event" style="color: ${log.evento.includes('Check-In') ? '#00ff88' : '#fff'}">
                                ${log.evento}
                            </td>
                            <td>${log.data}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } catch (error) {
                    console.error("Erro ao buscar logs:", error);
                }
            }

            // Atualiza a cada 2 segundos
            setInterval(atualizarLogs, 2000);
            atualizarLogs(); // Chama a primeira vez na hora
        </script>
    </body>
    </html>
    """
    return html_content

# 2. Rota que lê o banco de dados
@app.get("/logs")
def pegar_logs():
    # Conecta no banco
    conn = sqlite3.connect('face_logger.db')
    cursor = conn.cursor()
    
    # Pega os dados
    cursor.execute("SELECT * FROM logs_acesso ORDER BY id DESC")
    dados_brutos = cursor.fetchall()
    
    conn.close()
    
    # Transformar a Tupla em Dicionário (JSON)
    lista_logs = []
    for linha in dados_brutos:
        log_json = {
            "id": linha[0],
            "data": linha[1],
            "evento": linha[2],
            "foto": linha[3]
        }
        lista_logs.append(log_json)
    
    return lista_logs

# 3. Rota que recebe um log via POST e salva no banco

@app.post("/registrar")
def registrar_log(item: LogRecebido):
    # O 'item' contém o JSON que foi enviado
    msg_evento = item.evento
    
    # Lógica de Banco de Dados 
    conn = sqlite3.connect('face_logger.db')
    cursor = conn.cursor()
    
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO logs_acesso (data_hora, tipo_evento, foto_base64)
        VALUES (?, ?, ?)
    ''', (agora, msg_evento, item.imagem_base64))
    
    conn.commit()
    conn.close()
    
    return {"status": "Sucesso", "mensagem": f"Log '{msg_evento}' salvo!"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("💾 BANCO DE DADOS & DASHBOARD ATIVO!")
    print("👉 Veja os logs aqui: http://localhost:8000")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")