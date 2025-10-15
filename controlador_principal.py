import serial
import time
import cv2
import numpy as np # Necessário para o OpenCV funcionar corretamente
import sistema_visao
import rotinas_gcode

# --- GERENCIADOR DE ESTADO E LÓGICA ---
alturas_das_pilhas = [0.0] * 9
ALTURAS_CAIXAS = {'vermelho': 8.0, 'verde': 10.0, 'azul': 12.0}
def encontrar_pilha_mais_baixa(alturas):
    return alturas.index(min(alturas))
def enviar_sequencia(controlador, sequencia):
    print("--- Iniciando Sequencia de Movimento ---")
    for comando in sequencia:
        if not comando: 
            continue
        print("Enviando: {}".format(comando))
        controlador.write(comando.encode('utf-8') + b'\n')
        while True:
            resposta = controlador.readline().decode('utf-8').strip()
            if 'ok' in resposta:
                break
    print("--- Sequencia Concluida ---")

# --- BLOCO PRINCIPAL DE EXECUÇÃO ---
controlador_real = None
cap = None
try:
    # --- CONEXÃO COM O ROBÔ ---
    PORTA_SERIAL = 'COM6' 
    BAUD_RATE = 250000
    print("Conectando ao Robô em {}...".format(PORTA_SERIAL))
    controlador_real = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=2)
    time.sleep(2)
    controlador_real.flushInput()
    print("Robô conectado com sucesso!")

    # --- INICIALIZAÇÃO DA CÂMERA ---
    CAMERA_INDEX = 1
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise IOError("Nao foi possivel abrir a camera.")
    print("Câmera iniciada. Sistema em operacao.")

    enviar_sequencia(controlador_real, rotinas_gcode.criar_rotina_ir_para_repouso())

    # --- LOOP DE OPERAÇÃO CONTÍNUA ---
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Alerta: Nao foi possivel capturar o frame.")
            continue

        cor_detectada, bbox = sistema_visao.detectar_maior_objeto_por_cor(frame)

        if cor_detectada:
            print("\n!!! OBJETO DETECTADO: {} !!!".format(cor_detectada.upper()))
            
            print("--> Acionando rotina para PEGAR.")
            enviar_sequencia(controlador_real, rotinas_gcode.criar_rotina_pegar())

            indice_pilha = encontrar_pilha_mais_baixa(alturas_das_pilhas)
            altura_atual = alturas_das_pilhas[indice_pilha]
            print("--> Decisao: Colocar na pilha #{} (altura atual: {}mm)".format(indice_pilha, altura_atual))

            sequencia_soltar = rotinas_gcode.criar_rotina_soltar(indice_pilha, altura_atual)
            enviar_sequencia(controlador_real, sequencia_soltar)

            altura_caixa = ALTURAS_CAIXAS.get(cor_detectada, 20.0)
            alturas_das_pilhas[indice_pilha] += altura_caixa
            print("--> Memoria atualizada. Novas alturas: {}".format(alturas_das_pilhas))
            
            print("--> Retornando para a posicao de repouso.")
            enviar_sequencia(controlador_real, rotinas_gcode.criar_rotina_ir_para_repouso())

            print("\nCiclo completo. Aguardando proximo objeto...")
            time.sleep(5)
        
        if frame is not None:
             if bbox:
                 (x, y, w, h) = bbox
                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
             cv2.imshow('Controlador Principal - Visao do Robo', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print("ERRO CRITICO NO LOOP PRINCIPAL: {}".format(e))
finally:
    if cap: 
        cap.release()
    cv2.destroyAllWindows()
    if controlador_real and controlador_real.is_open:
        enviar_sequencia(controlador_real, rotinas_gcode.criar_rotina_ir_para_repouso())
        controlador_real.close()
        print("Conexao e camera desligadas.")