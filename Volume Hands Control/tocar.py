import cv2
import mediapipe as mp
import math
import threading
import os
import pygame

# Lista de músicas na pasta
musicas = os.listdir("musicas")
music_pos = 0
flag_acionada = False
volume = 0

# Inicializando o mixer do pygame
pygame.mixer.init()
pygame.mixer.music.load(f"musicas/{musicas[music_pos]}")  # Carregando a primeira música
pygame.mixer.music.set_volume(0.5)  # Definindo o volume inicial (50%)
pygame.mixer.music.play()  # Reproduzindo a música

# Função para tocar música em uma nova thread
def tocar_musica():
    pygame.mixer.music.load(f"musicas/{musicas[music_pos]}")
    pygame.mixer.music.play()

# Inicializando MediaPipe e câmera
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertendo a imagem para RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

#Mão direita ou esquerda

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Identificando se a mão é esquerda ou direita
            hand_label = results.multi_handedness[idx].classification[0].label  # "Left" ou "Right"
            confidence = results.multi_handedness[idx].classification[0].score

            # Exibe a mão e a confiança na tela
            cv2.putText(frame, f"{hand_label} ({confidence:.2f})", (10, 60 + idx * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = frame.shape

            ponto_4 = ponto_8 = None
            ponto_1 = ponto_12 = None

            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                '''
                #Desenha os numeros e pontos de captura
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, str(id), (cx, cy - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
                '''

                if id == 4:
                    ponto_4 = (cx, cy)
                elif id == 8:
                    ponto_8 = (cx, cy)
                elif id == 12:
                    ponto_12 = (cx, cy)
                elif id == 1:
                    ponto_1 = (cx, cy)

            if (ponto_4 and ponto_8) and hand_label == "Right":
                #cv2.line(frame, ponto_4, ponto_8, (255, 255, 255), 2) #Desenha a Linha do Volume
                distancia = math.sqrt((ponto_8[0] - ponto_4[0])**2 + (ponto_8[1] - ponto_4[1])**2)
                if distancia <= 30:
                    distancia = 0
                #print(f"Distância: {distancia:.2f} pixels")
                pygame.mixer.music.set_volume(min(distancia / 100, 1.0))  # Limita o volume a 1.0
                volume = min(distancia / 100, 1.0)
            if ponto_1 and ponto_12:
                distancia_pass = math.sqrt((ponto_12[0] - ponto_1[0])**2 + (ponto_12[1] - ponto_1[1])**2)
                #print(f"Distância: {distancia_pass:.2f} pixels")
                
                if distancia_pass < 50 and flag_acionada:  # Se a distância for menor que 50
                    flag_acionada = False
                    pygame.mixer.music.stop()  # Para a música
                    music_pos += 1
                    if music_pos >= len(musicas):  # Corrigido para usar >=
                        music_pos = 0
                    
                    pygame.mixer.music.load(f"musicas/{musicas[music_pos]}")  # Carrega a próxima música
                    threading.Thread(target=tocar_musica).start()  # Reproduz a próxima música em uma nova thread
                if distancia_pass > 70:
                    flag_acionada = True
    #Print das musicas na tela no canto superior esquerdo        
    cv2.putText(frame,(musicas[music_pos]),(10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 1)
    #Print do volume no canto inferior direito        
    cv2.putText(frame,(f"Volume: {(volume*100):.1f} %"),(430,450),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 1)
    
    # Exibindo o resultado
    cv2.imshow('Music With Hands', frame)

    # Tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
