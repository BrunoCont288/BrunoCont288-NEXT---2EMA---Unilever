# Nome do Arquivo: gcode_generator.py (VERSÃO ATUALIZADA PARA MARLIN)
# Função: Biblioteca de movimentos do robô, falando o "idioma" do Marlin 1.0.2

# --- CONFIGURAÇÕES DA GARRA ---
# ATENÇÃO: Você precisará descobrir estes valores experimentalmente!
# Mude os números abaixo depois de fazer o teste.
ANGULO_GARRA_ABERTA = 90
ANGULO_GARRA_FECHADA = 10
SERVO_INDEX_GARRA = 0 # O primeiro servo na placa (geralmente 0)
# -----------------------------

# --- Ferramentas Básicas (Building Blocks) ---

def mover_para(x, y, z, velocidade=3000):
    """Gera um único comando G-code para um movimento linear (G1)."""
    return f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F{velocidade}"

def controlar_garra(estado):
    """
    Gera o comando M280 correto para abrir ou fechar a garra,
    usando os ângulos definidos na configuração.
    """
    if estado == 'abrir':
        angulo = ANGULO_GARRA_ABERTA
    elif estado == 'fechar':
        angulo = ANGULO_GARRA_FECHADA
    else:
        return "" # Ignora estado inválido
    
    # Formata o comando M280: M280 P<indice_do_servo> S<angulo>
    return f"M280 P{SERVO_INDEX_GARRA} S{angulo}"

def pausa_ms(milissegundos):
    """Gera um comando G-code para uma pausa (dwell)."""
    return f"G4 P{milissegundos}"

def obter_posicao_atual():
    """Retorna o comando para perguntar a posição atual ao Marlin."""
    return "M114"

# --- Sequências Complexas (Tarefas do Robô) ---

def gerar_sequencia_pegar(x, y, z_coleta, z_seguro):
    """Gera uma lista completa de comandos G-code para pegar um objeto."""
    sequencia = [
        controlar_garra('abrir'),
        mover_para(x, y, z_seguro),
        mover_para(x, y, z_coleta),
        controlar_garra('fechar'),
        pausa_ms(500),
        mover_para(x, y, z_seguro)
    ]
    return sequencia

def gerar_sequencia_soltar(x, y, z_soltar, z_seguro):
    """Gera uma lista completa de comandos G-code para soltar um objeto."""
    sequencia = [
        mover_para(x, y, z_seguro),
        mover_para(x, y, z_soltar),
        controlar_garra('abrir'),
        pausa_ms(500),
        mover_para(x, y, z_seguro)
    ]
    return sequencia