import cv2
import os
import numpy as np
from PIL import Image
import json

# --- CONFIGURAÇÕES ---
PASTA_DATASET = 'dataset'
ARQUIVO_TREINO = 'trainer.yml'
ARQUIVO_NOMES = 'usuarios.json'
CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Garante que as pastas existem
if not os.path.exists(PASTA_DATASET): os.makedirs(PASTA_DATASET)
if not os.path.exists(ARQUIVO_NOMES): 
    with open(ARQUIVO_NOMES, 'w') as f: json.dump({}, f)

def carregar_nomes():
    with open(ARQUIVO_NOMES, 'r') as f:
        return json.load(f)

def salvar_nome(id, nome):
    nomes = carregar_nomes()
    nomes[str(id)] = nome
    with open(ARQUIVO_NOMES, 'w') as f:
        json.dump(nomes, f)

def pegar_proximo_id():
    nomes = carregar_nomes()
    ids = [int(k) for k in nomes.keys()]
    if not ids: return 1
    return max(ids) + 1

# --- CAPTURAR ---
def capturar_rosto(id, nome):
    cap = cv2.VideoCapture(0)
    print(f"\n📸 Registering {nome} (ID: {id})... Look at the camera!")
    print("Capturing 30 samples...")
    
    count = 0
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = CASCADE.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
            # Salva a foto
            cv2.imwrite(f"{PASTA_DATASET}/User.{id}.{count}.jpg", gray[y:y+h, x:x+w])
            cv2.imshow('Face Registration', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): break
        if count >= 30: break # Tira 30 fotos e para
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Capture finished!")

# --- TREINAR ---
def treinar_modelo():
    print("\n🧠 Training the system with new faces...")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    imagePaths = [os.path.join(PASTA_DATASET, f) for f in os.listdir(PASTA_DATASET)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        try:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faceSamples.append(img_numpy)
            ids.append(id)
        except:
            continue

    recognizer.train(faceSamples, np.array(ids))
    recognizer.write(ARQUIVO_TREINO)
    print(f"✅ Training complete! {len(np.unique(ids))} users in database.")

# --- MENU PRINCIPAL ---
while True:
    print("\n--- 💪 FACE LOGGER MANAGER (ADMIN) ---")
    print("1. Register New User")
    print("2. List Users")
    print("3. Exit")
    op = input("Option: ")

    if op == '1':
        nome = input("Enter user name: ")
        novo_id = pegar_proximo_id()
        capturar_rosto(novo_id, nome)
        salvar_nome(novo_id, nome)
        treinar_modelo() # Já treina logo em seguida
        print(f"\n✨ {nome} registered successfully!")
        
    elif op == '2':
        nomes = carregar_nomes()
        print("\n--- REGISTERED USERS ---")
        for id, nome in nomes.items():
            print(f"ID {id}: {nome}")
            
    elif op == '3':
        break