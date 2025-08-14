import cv2
import numpy as np

# Inicializa a captura de vídeo.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

# Dicionário com os intervalos de cor em HSV.
intervalos = {
    'vermelho': [np.array([0, 120, 70]), np.array([10, 255, 255])],
    'verde':    [np.array([36, 100, 100]), np.array([86, 255, 255])],
    'azul':     [np.array([94, 120, 100]), np.array([126, 255, 255])]
}

# Loop principal para processar o vídeo quadro a quadro.
while True:
    # Captura um quadro (frame) da câmera.
    ret, frame = cap.read()

    if not ret:
        print("Não foi possível capturar o quadro.")
        break

    # Converte o quadro para o espaço de cores HSV.
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maior_area = 0
    cor_detectada = None
    melhor_contorno = None

    # Itera sobre cada cor para encontrar o maior objeto.
    for nome_cor, (limite_inferior, limite_superior) in intervalos.items():
        mascara = cv2.inRange(frame_hsv, limite_inferior, limite_superior)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > maior_area:
                maior_area = area
                cor_detectada = nome_cor
                melhor_contorno = contorno

    # Se um objeto grande o suficiente foi detectado, processa e exibe suas informações.
    if maior_area > 500 and melhor_contorno is not None:
        # Obtém as coordenadas do retângulo que envolve o objeto.
        x, y, w, h = cv2.boundingRect(melhor_contorno)
        
        # Desenha o retângulo no frame original.
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Escreve o nome da cor detectada acima do retângulo.
        cv2.putText(frame, cor_detectada.upper(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # --- NOVO: CÁLCULO E VISUALIZAÇÃO DO CENTRO ---
        # 1. Calcula as coordenadas do centro do retângulo.
        centro_x = x + w // 2
        centro_y = y + h // 2

        # 2. Desenha um pequeno círculo vermelho no centro para visualização.
        cv2.circle(frame, (centro_x, centro_y), 5, (0, 0, 255), -1) # -1 preenche o círculo

        # 3. Imprime as informações no terminal. Esta é a "saída" que o robô usaria.
        print(f"Objeto: {cor_detectada.upper()} | Coordenadas do Centro (X, Y): ({centro_x}, {centro_y})")
        # ----------------------------------------------

    # Mostra o frame resultante em uma janela.
    cv2.imshow('Etapa 1: Deteccao e Localizacao (Aperte Q para sair)', frame)

    # Se a tecla 'q' for pressionada, o loop para.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha todas as janelas.
cap.release()
cv2.destroyAllWindows()