import cv2
import mediapipe as mp
import math
import threading
import os

#Lista de Musicas pasta
musicas = os.listdir("musicas")

#Definição da variavel contadora de musicas
music_pos= 0


print(f"{musicas[music_pos]}")
'''**************************************************************************************'''
import pygame

# Inicializando o mixer do pygame
pygame.mixer.init()

# Carregando o arquivo de áudio
pygame.mixer.music.load(f"musicas/{musicas[music_pos]}")  # Substitua pelo caminho do seu arquivo

# Definindo o volume (0.0 a 1.0)
pygame.mixer.music.set_volume(0.5)  # 50% do volume

# Reproduzindo o áudio
pygame.mixer.music.play()

'''
# Aguardando até que a reprodução termine
while pygame.mixer.music.get_busy():  # Aguarda enquanto o áudio está sendo reproduzido
    continue
'''
#pygame.quit()  # Finaliza o mixer do pygame

'''**************************************************************************************'''

#Iniciando a Musica
threading.Thread(target=pygame.mixer.music.play(), args=("")).start()

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

    # Verificando se alguma mão foi detectada
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = frame.shape  # Altura e largura da imagem

            # Variáveis para armazenar as coordenadas dos pontos de interesse
            ponto_4 = ponto_8 = None

            for id, lm in enumerate(hand_landmarks.landmark):
                # Convertendo coordenadas normalizadas para pixels
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Desenhando o ponto com cor personalizada (verde)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

                # Exibindo o ID do ponto ao lado dele
                cv2.putText(frame, str(id), (cx, cy - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

                # Armazenando as coordenadas dos pontos 4 e 8
                if id == 4:
                    ponto_4 = (cx, cy)
                elif id == 8:
                    ponto_8 = (cx, cy)
                elif id == 12:
                    ponto_12 = (cx, cy)
                elif id == 1:
                    ponto_1 = (cx, cy)

            # Desenhando uma linha entre os pontos 4 e 8, se ambos existirem
            if ponto_4 and ponto_8:
                cv2.line(frame, ponto_4, ponto_8, (255, 255, 255), 2)

                # Calculando a distância euclidiana entre os dois pontos
                distancia = math.sqrt((ponto_8[0] - ponto_4[0])**2 + (ponto_8[1] - ponto_4[1])**2)
                print(f"Distância: {distancia:.2f} pixels")
                # Definindo o volume (0.0 a 1.0)
                pygame.mixer.music.set_volume(distancia/100)  # 50% do volume
            if ponto_1 and ponto_12:
                distancia_pass = math.sqrt((ponto_12[0] - ponto_1[0])**2 + (ponto_12[1] - ponto_1[1])**2)
                print(f"Distância: {distancia_pass:.2f} pixels")
                
                try:
                    if distancia_pass< 50:
                        pygame.mixer.music.stop()
                        music_pos += 1
                        if music_pos > len(musicas):
                            music_pos = 0 
                            print(musicas[music_pos])
                        pygame.mixer.music.load(f"{musicas[music_pos]}")
                        threading.Thread(target=pygame.mixer.music.play(), args=("")).start()

                except:
                    pass

    # Exibindo o resultado
    cv2.imshow('Reconhecimento de Mão com MediaPipe', frame)

    # Tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
