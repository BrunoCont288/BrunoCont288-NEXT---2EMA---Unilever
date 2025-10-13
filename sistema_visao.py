import cv2
import numpy as np

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera...")
    exit()

intervalos = {
    'vermelho': [np.array([0, 120, 70]), np.array([10, 255, 255])],
    'verde':    [np.array([36, 100, 100]), np.array([86, 255, 255])],
    'azul':     [np.array([94, 120, 100]), np.array([126, 255, 255])]
}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível capturar o quadro da câmera.")
        break

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maior_area = 0
    cor_detectada = None
    melhor_contorno = None

    for nome_cor, (limite_inferior, limite_superior) in intervalos.items():
        mascara = cv2.inRange(frame_hsv, limite_inferior, limite_superior)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > maior_area:
                maior_area = area
                cor_detectada = nome_cor
                melhor_contorno = contorno

    if maior_area > 500 and melhor_contorno is not None:
        x, y, w, h = cv2.boundingRect(melhor_contorno)
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.putText(frame, cor_detectada.upper(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        # A saída de dados agora é apenas a cor, como o projeto precisa.
        print(f"Cor detectada: {cor_detectada.upper()}")

    cv2.imshow('Sistema de Visao Simplificado (Aperte Q para sair)', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()