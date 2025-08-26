# Nome do Arquivo: gcode_generator.py
# Função: Biblioteca de movimentos do robô. Contém todas as funções que
#         criam sequências de G-code para controlar o braço robótico
#         com firmware Marlin.

# --- CONFIGURAÇÕES DA GARRA ---
# ATENÇÃO: Estes são valores de EXEMPLO! Você precisa descobrir os valores
# corretos para o seu robô com o script 'teste_garra.py' e ATUALIZAR AQUI.
ANGULO_GARRA_ABERTA = 90 # Exemplo: Ângulo para a garra estar totalmente aberta.
ANGULO_GARRA_FECHADA = 10  # Exemplo: Ângulo para segurar a caixa com firmeza.
SERVO_INDEX_GARRA = 0      # O índice do servo da garra no controlador (geralmente 0).
# -----------------------------

# --- Funções Ferramenta (As peças básicas) ---

def mover_para(x, y, z, velocidade=3000):
    """
    Gera um único comando G-code para um movimento linear (G1).
    
    Args:
        x (float): Coordenada X em mm.
        y (float): Coordenada Y em mm.
        z (float): Coordenada Z em mm.
        velocidade (int): Velocidade de avanço (Feed rate) em mm/minuto.
        
    Returns:
        str: O comando G-code formatado.
    """
    # G1 -> Mova em linha reta
    # X, Y, Z -> Coordenadas de destino
    # F -> Velocidade (Feed rate)
    return f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F{velocidade}"

def controlar_garra(estado):
    """
    Gera o comando M280 correto para a garra, usando os ângulos da configuração.
    
    Args:
        estado (str): 'abrir' ou 'fechar'.
        
    Returns:
        str: O comando M-code formatado para controlar o servo.
    """
    if estado == 'abrir':
        angulo = ANGULO_GARRA_ABERTA
    elif estado == 'fechar':
        angulo = ANGULO_GARRA_FECHADA
    else:
        return "" # Ignora estado inválido
    
    # Formata o comando M280, padrão do Marlin para controlar servos:
    # M280 P<indice_do_servo> S<angulo>
    return f"M280 P{SERVO_INDEX_GARRA} S{angulo}"

def pausa_ms(milissegundos):
    """
    Gera um comando G-code para uma pausa (dwell).
    
    Args:
        milissegundos (int): O tempo de pausa em milissegundos.
        
    Returns:
        str: O comando G-code de pausa.
    """
    # G4 -> Pausa
    # P -> Período em milissegundos
    return f"G4 P{milissegundos}"

def obter_posicao_atual():
    """Retorna o comando para perguntar a posição atual ao Marlin."""
    return "M114"

# --- Sequências Complexas (As Tarefas do Robô) ---

def gerar_sequencia_pegar(x, y, z_coleta, z_seguro):
    """
    Gera uma lista completa de comandos G-code para pegar um objeto.
    
    Args:
        x (float): Coordenada X do objeto.
        y (float): Coordenada Y do objeto.
        z_coleta (float): Altura Z exata para pegar o objeto.
        z_seguro (float): Altura Z segura para se mover sem colidir com nada.
        
    Returns:
        list: Uma lista de strings, onde cada string é um comando G-code.
    """
    sequencia = [
        controlar_garra('abrir'),      # Garante que a garra está aberta
        mover_para(x, y, z_seguro),    # Move para uma posição segura ACIMA do objeto
        mover_para(x, y, z_coleta),    # Desce até a altura do objeto
        controlar_garra('fechar'),     # Fecha a garra para segurar o objeto
        pausa_ms(500),                 # Espera meio segundo para a garra fechar completamente
        mover_para(x, y, z_seguro)     # Sobe de volta para a altura segura, agora com o objeto
    ]
    return sequencia

def gerar_sequencia_soltar(x, y, z_soltar, z_seguro):
    """
    Gera uma lista completa de comandos G-code para soltar um objeto em um pallet.
    
    Args:
        x (float): Coordenada X do local de entrega.
        y (float): Coordenada Y do local de entrega.
        z_soltar (float): Altura Z exata para soltar o objeto.
        z_seguro (float): Altura Z segura para se mover.
        
    Returns:
        list: Uma lista de strings de comandos G-code.
    """
    sequencia = [
        mover_para(x, y, z_seguro),    # Move para uma posição segura ACIMA do local de entrega
        mover_para(x, y, z_soltar),    # Desce até a altura de empilhamento no pallet
        controlar_garra('abrir'),      # Abre a garra para soltar o objeto
        pausa_ms(500),                 # Espera meio segundo para garantir que o objeto foi solto
        mover_para(x, y, z_seguro)     # Sobe de volta para a altura segura, sem o objeto
    ]
    return sequencia