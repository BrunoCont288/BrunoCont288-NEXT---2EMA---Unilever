# Nome do Arquivo: robo_virtual_SERVER.py
# Função: Simula o controlador de um robô G-code. Ele espera por comandos
#         em uma porta de rede e responde "ok" para cada um.
#         DEVE SER INICIADO ANTES DO SCRIPT DE CONTROLE.

import socket
import time

# Configurações do nosso servidor de simulação
HOST = 'localhost'  # Endereço local (este computador)
PORT = 12345        # Um número de porta para a comunicação

print("--- [SIMULADOR] Robô Virtual ---")

# Cria o servidor de socket que ficará ouvindo por conexões
# O 'with' garante que o servidor seja fechado corretamente no final
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Esta opção permite que o endereço seja reutilizado rapidamente, evitando erros de "endereço já em uso"
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind((HOST, PORT))
    server.listen()
    print(f"🤖 [SIMULADOR] Robô Virtual Online. Aguardando conexão do Cérebro em {HOST}:{PORT}...")

    # Pausa o programa e espera até que o script do cérebro se conecte
    conn, addr = server.accept()
    with conn:
        print(f"✅ [SIMULADOR] Cérebro conectado a partir de {addr}")
        
        # Envia uma mensagem de boas-vindas, imitando um firmware real
        conn.sendall(b'Marlin 1.0.2 - Virtual Robot Ready\n')
        
        # Loop principal para receber comandos
        while True:
            try:
                # Espera por um comando (até 1024 bytes)
                data = conn.recv(1024)
                if not data:
                    # Se o cérebro desconectar (enviar dados vazios), sai do loop
                    break 
                
                comando_recebido = data.decode('utf-8').strip()
                print(f"➡️  [SIMULADOR] Comando recebido: '{comando_recebido}'")

                # Envia a confirmação "ok" de volta para o cérebro
                conn.sendall(b'ok\n')

            except ConnectionResetError:
                # Isso acontece se o programa principal fechar a conexão abruptamente
                print("⚠️ [SIMULADOR] A conexão foi forçadamente fechada pelo cérebro.")
                break

        print("🔌 [SIMULADOR] Cérebro desconectou.")

print("[SIMULADOR] Robô Virtual Desligado.")