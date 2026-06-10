import math
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# IMPLEMENTAÇÃO DAS ESTRUTURAS DE DADOS (REQUISITOS 7, 8.1 E 8.2)
# ==============================================================================

class GerenciadorDadosMissao:
    def __init__(self):
        # 1. DICIONÁRIO (Tabela Hash): Status binário dos 6 módulos críticos
        # REQUISITO: Acesso rápido por nome e valores booleanos/binários (0 ou 1)
        self.modulos_criticos = {
            "suporte_vida": 1,      # 1 = Operacional, 0 = Falha
            "energia": 1,
            "comunicacao": 0,       # Simulando falha de comunicação
            "habitat": 1,
            "laboratorio": 1,
            "armazenamento": 1
        }

        # 2. MATRIZ (Lista de Listas): Leituras por horário e variáveis ambientais
        # REQUISITO: Pelo menos 6 horários e variáveis de energia/ambiente
        # Colunas: [Horário, Geração(kWh), Consumo(kWh), Bateria(%), Temperatura(°C), Radiação(mSv/h)]
        self.telemetria_matriz = [
            ["08:00", 30, 20, 80, 15, 0.1],
            ["10:00", 55, 25, 85, 18, 0.2],
            ["12:00", 70, 30, 90, 22, 0.5], # Pico de radiação e geração solar
            ["14:00", 65, 35, 95, 21, 0.4],
            ["16:00", 40, 40, 95, 17, 0.2],
            ["18:00", 5,  45, 90, 12, 0.1]  # Queda de geração, aumento de consumo
        ]
        # (CORREÇÃO) DICIONÁRIO HIERÁRQUICO (Requisito 8.2)
        self.hierarquia_sistemas = {
            "energia": {
                "solar": 1,
                "baterias": 1
            },
            "habitat": {
                "oxigenio": 1,
                "controle_termico": 1
            }
        }

        # (CORREÇÃO) LISTA: Log histórico com 8 eventos (Requisito 7)
        self.log_eventos_passados = [
            "01:00 - Sistema de telemetria iniciado.",
            "02:30 - Modo de economia ativado (rotina noturna).",
            "03:45 - Falha temporária no sensor de radiação.",
            "04:00 - Sensor de radiação reinicializado com sucesso.",
            "05:15 - Mudança de prioridade energética para carregamento.",
            "06:30 - Bateria atingiu 100% de capacidade.",
            "07:20 - Alerta menor: flutuação de temperatura externa.",
            "07:50 - Operações estabilizadas e normais."
        ]

        # 3. FILA (Queue): Organização de alertas pendentes por ordem de chegada (FIFO)
        # REQUISITO: Utilizar fila para alertas por ordem de chegada ou prioridade
        self.fila_alerts = []

        # 4. PILHA (Stack): Registro (Log) dos últimos eventos críticos analisados (LIFO)
        # REQUISITO: Utilizar pilha para registrar os últimos eventos críticos
        self.pilha_logs_criticos = []

    # 5. LISTAS: Extração de Séries Temporais para a Previsão Matemática
    # REQUISITO: Utilizar listas para armazenar séries de dados ao longo do tempo
    def obter_serie_consumo(self):
        """Retorna uma lista linear simples com o histórico de consumo (Coluna 2 da matriz)"""
        lista_consumo = []
        for linha in self.telemetria_matriz:
            lista_consumo.append(linha[2])
        return lista_consumo

    def obter_valores_atuais(self):
        """Retorna o último registro de telemetria da matriz (linha mais recente)"""
        return self.telemetria_matriz[-1]

    #  INCONSISTÊNCIA PROPOSITAL (REQUISITO 7)
    # Cenário: O status do módulo diz que a energia está "OK" (1), mas a bateria 
    # na telemetria atual caiu para um nível crítico (menos de 20%).
    # Isso força o sistema a diagnosticar um conflito de dados.
    def inserir_inconsistencia_dados(self):
        """Força uma inconsistência de dados para testar o sistema"""
        self.telemetria_matriz[-1][3] = 12  # Força a bateria do último horário para 12%
        # Conflito: modulos_criticos['energia'] está 1 (Normal), mas a bateria real está em 12% (Crítico)

    def gerar_grafico_telemetria(self):
        """
        Gera um gráfico comparativo de Geração vs Consumo usando NumPy e Matplotlib.
        """
        # Convertendo a matriz para um array NumPy para facilitar a manipulação
        # Ignoramos a primeira coluna (horários) para cálculos numéricos
        dados_numericos = np.array([linha[1:] for linha in self.telemetria_matriz], dtype=float)
        horarios = [linha[0] for linha in self.telemetria_matriz]
        
        geracao = dados_numericos[:, 0]
        consumo = dados_numericos[:, 1]
        bateria = dados_numericos[:, 2]

        plt.figure(figsize=(10, 6))
        
        # Plotando Geração e Consumo
        plt.plot(horarios, geracao, label='Geração Solar (kWh)', marker='o', color='gold', linewidth=2)
        plt.plot(horarios, consumo, label='Consumo (kWh)', marker='s', color='tomato', linewidth=2)
        
        # Adicionando a Bateria em um eixo secundário para melhor visualização
        plt.bar(horarios, bateria, alpha=0.3, label='Nível Bateria (%)', color='skyblue')

        plt.title('Monitoramento de Energia - Missão Espacial')
        plt.xlabel('Horário')
        plt.ylabel('Valores (kWh / %)')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Salvando o gráfico
        plt.savefig('grafico_telemetria.png')
        print("\n[SISTEMA] Gráfico 'grafico_telemetria.png' gerado com sucesso usando NumPy.")


# ==============================================================================
#  REGRAS LÓGICAS, PREVISÃO E INTERFACE
# (Consumindo as estruturas que você criou acima)
# ==============================================================================

def calcular_previsao_proximo_ciclo(lista_consumo):
    """
    REQUISITO 8.5: Análise e previsão sem bibliotecas (Média Móvel Simples).
    Calcula a média dos 3 últimos consumos para prever o próximo.
    """
    ultimos_3 = lista_consumo[-3:]
    previsao = sum(ultimos_3) / len(ultimos_3)
    return previsao


def processar_regras_e_alertas(db):
    """
    REQUISITO 8.3 e 8.4: Processamento das regras lógicas (AND, OR, NOT)
    e alimentação da Fila e da Pilha criadas por você.
    """
    valores_atuais = db.obter_valores_atuais()
    horario, geracao, consumo, bateria, temp, radiacao = valores_atuais
    # Regra 4: Classificação de Status Geral com IF/ELIF/ELSE (Requisito 8.3)
    if bateria < 20:
        db.fila_alerts.append("CRÍTICO: Bateria em nível de emergência. Iniciar modo de sobrevivência.")
    elif bateria >= 20 and bateria < 50:
        db.fila_alerts.append("ALERTA: Bateria abaixo da metade. Otimizar consumo.")
    else:
        # Tudo ok, não gera alerta, mas cumpre a estrutura lógica pedida
        pass

    # Expressão Booleana Principal de Diagnóstico (Exigida no README)
    # Crítico se: Suporte de Vida falhar OU (Bateria Baixa E Radiação Alta) OU (Comunicação Fora E Habitat Falhar)
    
    # Regra 1: Checagem de Inconsistência Proposital (NOT e AND)
    if db.modulos_criticos["energia"] == 1 and bateria < 20:
        db.fila_alerts.append("CRÍTICO: Conflito de dados! Módulo Energia consta como NORMAL, mas telemetria indica bateria em " + str(bateria) + "%.")
        db.pilha_logs_criticos.append(f"[{horario}] Falha de sensor detectada: Inconsistência de Bateria.")

    # Regra 2: Falha Crítica de Comunicação (Operador NOT)
    if not db.modulos_criticos["comunicacao"]:
        db.fila_alerts.append("ALERTA: Link de comunicação interplanetária offline. Tentando reconexão automática.")

    # Regra 3: Variáveis Ambientais Perigosas (Operador OR)
    if temp > 40 or radiacao > 0.4:
        db.fila_alerts.append("ALERTA: Ambiente externo hostil. Radiação/Temperatura elevada.")


def exibir_painel_controle(db, previsao_consumo):
    """Exibe o resultado das estruturas de dados organizadas na tela."""
    print("=" * 60)
    print("        SISTEMA INTELIGENTE DE MONITORAMENTO ESPACIAL       ")
    print("=" * 60)
    
    # Exibindo o Dicionário
    print("\n[TABELA HASH] Status dos Módulos Críticos:")
    for modulo, status in db.modulos_criticos.items():
        st_texto = "🟢 OPERACIONAL" if status == 1 else "🔴 FALHA/ALERTA"
        print(f" • {modulo.upper().replace('_', ' ')}: {st_texto}")

    # Exibindo os valores extraídos da Matriz
    valores = db.obter_valores_atuais()
    print(f"\n[MATRIZ TELEMETRIA] Última leitura ({valores[0]}):")
    print(f" • Geração Solar: {valores[1]} kWh  |  Consumo Atual: {valores[2]} kWh")
    print(f" • Nível da Bateria: {valores[3]}%  |  Radiação: {valores[5]} mSv/h")

    # Exibindo o resultado do algoritmo de previsão
    print(f"\n[ANÁLISE PREDITIVA] Previsão de consumo para o próximo ciclo: {previsao_consumo:.2f} kWh")
    if previsao_consumo > valores[1]:
        print("  Recomendação: Geração solar será insuficiente. Desligar módulo LABORATÓRIO.")

    # Exibindo a Fila de Alertas (Processando FIFO)
    print("\n[FILA] Alertas Urgentes Detectados (Ordem de Chegada):")
    if not db.fila_alerts:
        print(" • Nenhum alerta pendente. Sistema estável.")
    else:
        while db.fila_alerts:
            alerta = db.fila_alerts.pop(0) # Primeiro a entrar, primeiro a sair
            print(f"  {alerta}")

    # Exibindo a Pilha de Logs (Processando LIFO)
    print("\n[PILHA] Histórico de Logs Críticos (Mais Recente Primeiro):")
    if not db.pilha_logs_criticos:
        print(" • Nenhum log crítico registrado.")
    else:
        while db.pilha_logs_criticos:
            log = db.pilha_logs_criticos.pop() # Último a entrar, primeiro a sair
            print(f"  {log}")
    print("=" * 60)


# ==============================================================================
# EXECUÇÃO DO FLUXO PRINCIPAL DO SOFTWARE
# ==============================================================================
if __name__ == "__main__":
    # 1. Inicializa o sistema de dados (Sua parte)
    sistema_dados = GerenciadorDadosMissao()
    
    # 2. Ativa a inconsistência de dados exigida no projeto
    sistema_dados.inserir_inconsistencia_dados()
    
    # 3. Executa a previsão matemática baseada na lista gerada por você
    serie_historica_consumo = sistema_dados.obter_serie_consumo()
    previsao_futura = calcular_previsao_proximo_ciclo(serie_historica_consumo)
    
    # 4. Processa as regras lógicas alimentando a fila e a pilha
    processar_regras_e_alertas(sistema_dados)
    
    # 5. Imprime o dashboard formatado
    exibir_painel_controle(sistema_dados, previsao_futura)

    # 6. Gera o gráfico usando NumPy
    sistema_dados.gerar_grafico_telemetria()