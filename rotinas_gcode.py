import pprint

# PARÂMETROS FÍSICOS (A SEREM CALIBRADOS COM O UGS)
POSICAO_REPOUSO = (10.0, 10.0, 150.0)
ALTURA_SEGURA_Z = 100.0
POSICAO_ACIMA_ESTEIRA = (120.0, 30.0, 100.0)
POSICAO_PEGAR_ESTEIRA = (120.0, 30.0, 5.0)
COORDENADAS_BASE_PILHAS = [
    (30.0, 150.0), (52.0, 150.0), (74.0, 150.0),
    (30.0, 172.0), (52.0, 172.0), (74.0, 172.0),
    (30.0, 194.0), (52.0, 194.0), (74.0, 194.0),
]
ALTURA_BASE_PALLET_Z = 5.0

# Comandos da Garra
ABRIR_GARRA, FECHAR_GARRA, PAUSA_GARRA = "M280 P0 S90", "M280 P0 S10", "G4 P500"

# --- BIBLIOTECA DE ROTINAS ---
def criar_rotina_pegar():
    pos_acima, pos_pegar = POSICAO_ACIMA_ESTEIRA, POSICAO_PEGAR_ESTEIRA
    return [
        ABRIR_GARRA,
        "G1 X{:.2f} Y{:.2f} Z{:.2f} F3000".format(pos_acima[0], pos_acima[1], pos_acima[2]),
        "G1 Z{:.2f} F1500".format(pos_pegar[2]),
        FECHAR_GARRA, PAUSA_GARRA,
        "G1 Z{:.2f} F1500".format(pos_acima[2]),
    ]

def criar_rotina_soltar(indice_pilha, altura_atual_pilha):
    base_x, base_y = COORDENADAS_BASE_PILHAS[indice_pilha]
    z_soltar = ALTURA_BASE_PALLET_Z + altura_atual_pilha
    return [
        "G1 X{:.2f} Y{:.2f} Z{:.2f} F3000".format(base_x, base_y, ALTURA_SEGURA_Z),
        "G1 Z{:.2f} F1500".format(z_soltar),
        ABRIR_GARRA, PAUSA_GARRA,
        "G1 Z{:.2f} F1500".format(ALTURA_SEGURA_Z),
    ]

def criar_rotina_ir_para_repouso():
    pos_repouso = POSICAO_REPOUSO
    return [
        "G1 Z{:.2f} F3000".format(pos_repouso[2]),
        "G1 X{:.2f} Y{:.2f} F3000".format(pos_repouso[0], pos_repouso[1]),
    ]

# --- BLOCO DE TESTE ---
if __name__ == '__main__':
    print("--- Teste do Modulo de Rotinas ---")
    print("\n--- Exemplo de Rotina Gerada (Soltar na Pilha #4, altura 40mm) ---")
    exemplo_rotina = criar_rotina_soltar(4, 40.0)
    pprint.pprint(exemplo_rotina)