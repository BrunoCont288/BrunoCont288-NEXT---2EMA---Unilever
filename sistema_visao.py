import cv2
import numpy as np

INTERVALOS = {
    'vermelho': [np.array([0, 120, 70]), np.array([10, 255, 255])],
    'verde':    [np.array([36, 100, 100]), np.array([86, 255, 255])],
    'azul':     [np.array([94, 120, 100]), np.array([126, 255, 255])]
}
AREA_MINIMA = 500

def detectar_maior_objeto_por_cor(frame):
    if frame is None:
        return None, None

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maior_area = 0
    cor_detectada_final = None
    melhor_contorno = None
    
    for nome_cor, (limite_inferior, limite_superior) in INTERVALOS.items():
        mascara = cv2.inRange(frame_hsv, limite_inferior, limite_superior)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > maior_area:
                maior_area = area
                cor_detectada_final = nome_cor
                melhor_contorno = contorno
    
    if maior_area > AREA_MINIMA:
        x, y, w, h = cv2.boundingRect(melhor_contorno)
        return cor_detectada_final, (x, y, w, h)
    
    return None, None

if __name__ == '__main__':
    CAMERA_INDEX = 1
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Erro ao abrir a camera.")
    else:
        while True:
            ret, frame = cap.read()
            if not ret: 
                break
            cor_encontrada, bbox = detectar_maior_objeto_por_cor(frame)
            if cor_encontrada:
                print("Cor detectada: {}".format(cor_encontrada.upper()))
                (x, y, w, h) = bbox
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('Sistema de Visao - Modo de Teste', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
        cap.release()
        cv2.destroyAllWindows()