# Nome do Arquivo: teste_integracao_simulada.py
# Função: Testa a lógica completa do controlador principal em um ambiente simulado.

import socket # <-- MUDANÇA: Usa socket em vez de serial
import time
import cv2
import numpy as np
import sistema_visao
import rotinas_gcode

# --- GERENCIADOR DE ESTADO E LÓGICA (Idêntico ao original) ---
alturas_das_pilhas = [0.0] * 9
ALTURAS_CAIXAS = {'vermelho': 8.0, 'verde': 10.0, 'azul': 12.0}
def encontrar_pilha_mais_baixa(alturas):
    return alturas.index(min(alturas))

# --- FUNÇÃO DE COMUNICAÇÃO (Versão para Simulação) ---
def enviar_sequencia(controlador, sequencia):
    print("--- Iniciando Sequencia (SIMULADA) ---")
    for comando in sequencia:
        if not comando: 
            continue
        print("Enviando: {}".format(comando))
        controlador.sendall(comando.encode('utf-8') + b'\n')
        while True:
            resposta = controlador.recv(1024).decode('utf-8').strip()
            if 'ok' in resposta: 
                break
    print("--- Sequencia Concluida ---")

# --- BLOCO PRINCIPAL DE EXECUÇÃO ---
controlador_simulado = None
cap = None
try:
    # --- CONEXÃO COM O ROBÔ VIRTUAL (usando socket) ---
    HOST, PORT = 'localhost', 12345
    print("Conectando ao Robô VIRTUAL...")
    controlador_simulado = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    controlador_simulado.connect((HOST, PORT))
    time.sleep(0.5); controlador_simulado.recv(1024) # Limpa a msg de boas-vindas
    print("Conectado com sucesso!")

    # --- INICIALIZAÇÃO DA CÂMERA ---
    cap = cv2.VideoCapture(1)
    if not cap.isOpened(): 
        raise IOError("Nao foi possivel abrir a camera.")
    print("Camera iniciada. Sistema em operacao simulada.")

    # A lógica daqui para baixo é IDÊNTICA à do seu controlador_principal_REAL.py
    enviar_sequencia(controlador_simulado, rotinas_gcode.criar_rotina_ir_para_repouso())
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        cor_detectada, bbox = sistema_visao.detectar_maior_objeto_por_cor(frame)

        if cor_detectada:
            print("\n!!! OBJETO DETECTADO: {} !!!".format(cor_detectada.upper()))
            enviar_sequencia(controlador_simulado, rotinas_gcode.criar_rotina_pegar())
            indice_pilha = encontrar_pilha_mais_baixa(alturas_das_pilhas)
            altura_atual = alturas_das_pilhas[indice_pilha]
            print("--> Decisao: Colocar na pilha #{}".format(indice_pilha))
            sequencia_soltar = rotinas_gcode.criar_rotina_soltar(indice_pilha, altura_atual)
            enviar_sequencia(controlador_simulado, sequencia_soltar)
            alturas_das_pilhas[indice_pilha] += ALTURAS_CAIXAS.get(cor_detectada, 20.0)
            print("--> Memoria atualizada: {}".format(alturas_das_pilhas))
            enviar_sequencia(controlador_simulado, rotinas_gcode.criar_rotina_ir_para_repouso())
            time.sleep(5)
        
        cv2.imshow('Controlador - MODO SIMULACAO', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
finally:
    if cap: 
        cap.release()
    cv2.destroyAllWindows()
    if controlador_simulado: 
        controlador_simulado.close()
    print("Simulação encerrada.")