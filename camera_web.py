import cv2
import os
import time
import json
import base64
import datetime
import requests
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import serial

# Conexão (ajuste a porta COM)
try:
    arduino = serial.Serial('COM3', 9600)
except:
    arduino = None

app = FastAPI()

# --- CONFIGURAÇÕES ---
API_LOGS_URL = "http://127.0.0.1:8000/registrar" # URL da API de logs
ARQUIVO_TREINO = 'trainer.yml'
ARQUIVO_NOMES = 'usuarios.json'
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- CARREGA INTELIGÊNCIA ---
recognizer = cv2.face.LBPHFaceRecognizer_create()
if os.path.exists(ARQUIVO_TREINO): recognizer.read(ARQUIVO_TREINO)
if os.path.exists(ARQUIVO_NOMES):
    with open(ARQUIVO_NOMES, 'r') as f: nomes_cadastrados = json.load(f)

# Variáveis Globais de Controle
camera = cv2.VideoCapture(0)
modo_liberado = False
tempo_inicio_liberacao = 0
frame_congelado = None
DURACAO_TELA_SUCESSO = 4
tempo_ultimo_bloqueio = 0 


def gerar_frames():
    global modo_liberado, tempo_inicio_liberacao, frame_congelado, tempo_ultimo_bloqueio

    while True:
        # Se estiver no modo "Sucesso", mostra a foto congelada
        if modo_liberado:
            tempo_passado = time.time() - tempo_inicio_liberacao
            if tempo_passado < DURACAO_TELA_SUCESSO:
                # Codifica o frame congelado para enviar pro navegador
                ret, buffer = cv2.imencode('.jpg', frame_congelado)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                time.sleep(0.03) 
                continue
            else:
                modo_liberado = False # Acabou o tempo, volta a filmar

        # 2. Captura Normal
        success, frame = camera.read()
        if not success: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.2, 5, minSize=(60, 60))

        alguem_autorizado = False

        for (x, y, w, h) in faces:
            id_predito, confianca = recognizer.predict(gray[y:y+h, x:x+w])

            if confianca < 60:
                # --- RECONHECIDO ---
                            # Rosto identificado!
                if arduino:
                    arduino.write(b'1')
                        
                id_str = str(id_predito)
                nome = nomes_cadastrados.get(id_str, "Unknown")
                hora_atual = datetime.datetime.now().strftime("%H:%M:%S")

                # Prepara frame de sucesso
                frame_sucesso = frame.copy()
                cv2.rectangle(frame_sucesso, (0, frame.shape[0]-100), (frame.shape[1], frame.shape[0]), (0, 200, 0), -1)
                cv2.putText(frame_sucesso, f"Welcome, {nome.upper()}!", (20, frame.shape[0]-60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(frame_sucesso, f"Access Granted at: {hora_atual}", (20, frame.shape[0]-25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                cv2.rectangle(frame_sucesso, (x, y), (x+w, y+h), (0, 255, 0), 3)

                # Congela
                modo_liberado = True
                tempo_inicio_liberacao = time.time()
                frame_congelado = frame_sucesso
                alguem_autorizado = True
                
                # Envia log pra API 
                try:
                    retval, buffer = cv2.imencode('.jpg', frame)
                    img_b64 = base64.b64encode(buffer).decode('utf-8')
                    payload = { "evento": f"Check-In: {nome}", "imagem_base64": img_b64 }
                    requests.post(API_LOGS_URL, json=payload, timeout=0.1)
                except: pass
                
                break # Sai do loop de rostos
            else:
# --- DESCONHECIDO ---
                tempo_atual = time.time()
                
                # COOLDOWN: Só manda o sinal '0' se já passou 2 segundos do último
                if tempo_atual - tempo_ultimo_bloqueio > 2:
                    if arduino:
                        arduino.write(b'0')
                    tempo_ultimo_bloqueio = tempo_atual # Reseta o cronômetro
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "Not Registered", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Codifica o frame atual para enviar
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Multipart(streaming)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# --- ROTAS ---
@app.get("/video_feed")
def video_feed():
    return StreamingResponse(gerar_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
def index():
    # Retorna o HTML direto 
    html_content = """
    <!doctype html>
    <html lang="pt-BR">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>FaceLogger • Acesso</title>
        <style>
            body { margin: 0; background-color: #111; color: white; font-family: sans-serif; display: flex; flex-direction: column; height: 100vh; }
            header { background: #000; padding: 15px; text-align: center; border-bottom: 2px solid #00ff88; }
            h2 { margin: 0; color: #00ff88; text-transform: uppercase; letter-spacing: 2px; }
            .main-container { flex: 1; display: flex; justify-content: center; align-items: center; padding: 20px; }
            .camera-box { 
                border: 2px solid #333; 
                border-radius: 10px; 
                overflow: hidden; 
                box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
                max-width: 100%;
                max-height: 80vh;
            }
            img { width: 100%; height: auto; display: block; }
            footer { text-align: center; padding: 10px; color: #555; font-size: 0.8rem; }
        </style>
    </head>
    <body>
        <header>
            <h2>FaceLogger Access</h2>
        </header>
        <div class="main-container">
            <div class="camera-box">
                <img src="/video_feed" alt="Camera Stream">
            </div>
        </div>
        <footer>
            Sistema de Controle de Acesso Inteligente • V1.0
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*50)
    print("🚀 SISTEMA DE CÂMERA INICIADO!")
    print("👉 Acesse o Totem aqui: http://localhost:5000")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="error")