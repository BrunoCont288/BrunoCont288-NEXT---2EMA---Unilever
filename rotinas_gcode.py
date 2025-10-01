# Nome do Arquivo: rotinas_gcode.py (Versão com Geração Automática de Posições)
# Função: Armazenar e gerar todas as sequências de movimento do robô.
import pprint

# =================================================================================
# 1. PARÂMETROS FÍSICOS DO SEU PROJETO (EM MILÍMETROS)
# ESTA É A ÚNICA SEÇÃO QUE VOCÊ VAI PRECISAR AJUSTAR NO FUTURO!
# Estes são os valores que você irá medir/gravar com o UGS quando o robô estiver pronto.
# =================================================================================

# --- Posições Gerais (Valores de Exemplo) ---
POSICAO_REPOUSO = (10.0, 10.0, 150.0)
ALTURA_SEGURA_Z = 100.0 # Altura Z geral para movimentos de transporte seguros

# --- Posições da Esteira (Valores de Exemplo) ---
POSICAO_ACIMA_ESTEIRA = (120.0, 30.0, 100.0) # Posição segura acima da caixa na esteira
POSICAO_PEGAR_ESTEIRA = (120.0, 30.0, 5.0)   # Posição exata para pegar a caixa

# --- Posições e Dimensões do Pallet (Valores de Exemplo) ---
# Coordenada do CENTRO da PRIMEIRA caixa (posição 0,0,0 - o canto mais próximo de você)
PALLET_ORIGEM_X = 30.0
PALLET_ORIGEM_Y = 150.0
PALLET_ORIGEM_Z = 5.0 # Altura da base para a 1ª camada

# Dimensões da caixa (incluindo uma pequena folga para não bater uma na outra)
TAMANHO_CAIXA_X = 22.0 
TAMANHO_CAIXA_Y = 22.0
ALTURA_CAIXA_Z = 20.0

# =================================================================================
# 2. GERAÇÃO AUTOMÁTICA DO DICIONÁRIO DE COORDENADAS
# Você não precisa editar nada abaixo desta linha.
# =================================================================================

COORDENADAS = {
    "repouso": POSICAO_REPOUSO,
    "acima_esteira": POSICAO_ACIMA_ESTEIRA,
    "pegar_esteira": POSICAO_PEGAR_ESTEIRA,
}

# Loop para gerar as 27 posições do pallet
for z in range(3): # Camadas (0 a 2)
    for y in range(3): # Linhas (0 a 2)
        for x in range(3): # Colunas (0 a 2)
            # Calcula a coordenada X, Y, Z para esta célula do grid
            coord_x = PALLET_ORIGEM_X + (x * TAMANHO_CAIXA_X)
            coord_y = PALLET_ORIGEM_Y + (y * TAMANHO_CAIXA_Y)
            coord_z_soltar = PALLET_ORIGEM_Z + (z * ALTURA_CAIXA_Z)
            
            # Define as chaves para o dicionário (ex: "soltar_pallet_2_1_0")
            chave_soltar = f"soltar_pallet_{z}_{y}_{x}"
            chave_acima = f"acima_pallet_{z}_{y}_{x}"
            
            # Adiciona as coordenadas ao nosso dicionário
            COORDENADAS[chave_soltar] = (coord_x, coord_y, coord_z_soltar)
            COORDENADAS[chave_acima] = (coord_x, coord_y, ALTURA_SEGURA_Z)

# =================================================================================
# 3. BIBLIOTECA DE ROTINAS (Usa o dicionário gerado acima)
# =================================================================================

# Comandos da Garra (ajuste com seus ângulos quando descobrir)
ABRIR_GARRA = "M280 P0 S90"
FECHAR_GARRA = "M280 P0 S10"
PAUSA_GARRA = "G4 P500"

def criar_rotina_pegar():
    """Cria a sequência para pegar uma caixa da esteira."""
    pos_acima = COORDENADAS["acima_esteira"]
    pos_pegar = COORDENADAS["pegar_esteira"]
    
    return [
        ABRIR_GARRA,
        f"G1 X{pos_acima[0]:.2f} Y{pos_acima[1]:.2f} Z{pos_acima[2]:.2f} F3000",
        f"G1 Z{pos_pegar[2]:.2f} F1500",
        FECHAR_GARRA,
        PAUSA_GARRA,
        f"G1 Z{pos_acima[2]:.2f} F1500",
    ]

def criar_rotina_soltar(x_grid, y_grid, z_grid):
    """Cria a sequência para soltar uma caixa em um local específico do pallet."""
    chave_acima = f"acima_pallet_{z_grid}_{y_grid}_{x_grid}"
    chave_soltar = f"soltar_pallet_{z_grid}_{y_grid}_{x_grid}"
    
    pos_acima = COORDENADAS[chave_acima]
    pos_soltar = COORDENADAS[chave_soltar]
    
    return [
        f"G1 X{pos_acima[0]:.2f} Y{pos_acima[1]:.2f} Z{pos_acima[2]:.2f} F3000",
        f"G1 Z{pos_soltar[2]:.2f} F1500",
        ABRIR_GARRA,
        PAUSA_GARRA,
        f"G1 Z{pos_acima[2]:.2f} F1500",
    ]

def criar_rotina_ir_para_repouso():
    """Cria a sequência para levar o robô à posição de repouso."""
    pos_repouso = COORDENADAS["repouso"]
    return [
        f"G1 Z{pos_repouso[2]:.2f} F3000",
        f"G1 X{pos_repouso[0]:.2f} Y{pos_repouso[1]:.2f} F3000",
    ]

# --- Bloco de teste para verificar as coordenadas geradas ---
if __name__ == '__main__':
    print("--- Dicionário de Coordenadas Gerado ---")
    # A função pprint imprime o dicionário de forma organizada
    pprint.pprint(COORDENADAS)
    print("\n--- Exemplo de Rotina Gerada (Soltar na Posição 2,2,2) ---")
    pprint.pprint(criar_rotina_soltar(2, 2, 2))