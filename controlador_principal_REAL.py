# Nome do Arquivo: controlador_principal_REAL.py
# Versão: Compatível (sem f-strings, sem emojis)
# Função: Script final do projeto. Controla o braço robótico físico.
#         Nesta fase, ele é usado para testar a comunicação básica (Etapa 2).

import serial # A biblioteca para conversar com o hardware real via USB
import time

# Futuramente, os imports do OpenCV e NumPy virão aqui, após resolvermos os erros.
# import cv2
# import numpy as np

# --- BLOCO DE COMUNICAÇÃO REAL ---
# Esta é a parte que o torna o código "físico".

# 1. EDITE AQUI: Substitua 'COM3' pela porta serial real do seu robô.
PORTA_SERIAL_REAL = 'COM6' 

# 2. EDITE AQUI (se necessário): Verifique o baud rate do seu firmware G-code.
BAUD_RATE_REAL = 250000

controlador_real = None # Inicializa a variável para a conexão
try:
    print("[CONTROLADOR REAL] Tentando se conectar ao Robo FISICO em {}".format(PORTA_SERIAL_REAL))
    
    # Conecta-se à porta serial do hardware.
    controlador_real = serial.Serial(PORTA_SERIAL_REAL, BAUD_RATE_REAL, timeout=1)
    
    # Espera 1-2 segundos para o firmware do robô (GRBL, etc.) inicializar.
    time.sleep(2)
    print("[CONTROLADOR REAL] Conectado com sucesso ao Robo FISICO!")

    # Limpa qualquer "lixo" de texto que possa estar na porta serial antes de começar.
    controlador_real.flushInput()

except serial.SerialException as e:
    print("ERRO FATAL: Nao foi possivel conectar ao robo fisico.")
    print("   Detalhes: {}".format(e))
    print("   VERIFIQUE: O robo esta conectado? A porta '{}' esta correta? Nenhum outro programa a esta usando?".format(PORTA_SERIAL_REAL))
    exit() # Para o programa se não conseguir conectar.

# --- FIM DO BLOCO DE COMUNICAÇÃO ---


# --- INÍCIO DA LÓGICA PRINCIPAL DO PROJETO ---
# Esta seção irá crescer à medida que adicionamos as próximas etapas.
# Por enquanto, ela apenas testa a conexão.

if controlador_real and controlador_real.is_open:
    try:
        # Comando G-code de teste da Etapa 2
        comando_gcode = "G0 X10 Y10 Z50\n"

        print("[CONTROLADOR REAL] Enviando comando de teste: {}".format(comando_gcode.strip()))
        
        # Envia o comando, convertendo a string de texto para bytes.
        controlador_real.write(comando_gcode.encode('utf-8'))

        # Espera pela resposta "ok" do robô.
        resposta_comando = controlador_real.readline().decode('utf-8').strip()
        print("[CONTROLADOR REAL] Robo FISICO respondeu: '{}'".format(resposta_comando))

        if 'ok' in resposta_comando:
            print("SUCESSO! A comunicacao com o hardware real esta funcionando!")

    except Exception as e:
        print("Ocorreu um erro durante a comunicacao: {}".format(e))
    
    finally:
        # Garante que a conexão seja fechada no final, não importa o que aconteça.
        controlador_real.close()
        print("[CONTROLADOR REAL] Conexao com o Robo FISICO fechada.")
else:
    print("Nao foi possivel iniciar a logica principal pois o controlador nao esta conectado.")