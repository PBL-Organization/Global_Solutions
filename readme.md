# Global Solution - READ ME - Sistema Inteligente de Monitoramento Espacial

## Integrantes

- Allan Victor Santos de Almeida Jesus (RM573218)
- Gustavo Veloso Marchese dos Santos (RM568930)
- José Elias Aleixo Lopes (RM568858)
- Sarah Mendes Machado De Oliveira (RM570514)

---

# Resumo do Problema

Este projeto simula um Sistema Inteligente de Monitoramento Espacial responsável por monitorar módulos críticos de uma missão, analisar dados de telemetria, detectar inconsistências, gerar alertas automáticos e realizar previsões de consumo energético.

O sistema utiliza estruturas de dados, regras lógicas e análise preditiva para auxiliar na tomada de decisões em um ambiente espacial, permitindo identificar situações de risco e sugerir ações para manter a missão em funcionamento seguro.

---

# Estruturas de Dados Utilizadas

## 1. Dicionário (Tabela Hash)

Utilizado para armazenar o status dos módulos críticos da missão.

Módulos monitorados:

- suporte_vida
- energia
- comunicacao
- habitat
- laboratorio
- armazenamento

Valores utilizados:

- 1 = Operacional
- 0 = Falha

Essa estrutura permite acesso rápido às informações dos módulos pelo nome.

---

## 2. Dicionário Hierárquico

Utilizado para representar a hierarquia dos sistemas da missão.

Exemplo:

Energia:
- Solar
- Baterias

Habitat:
- Oxigênio
- Controle térmico

Essa estrutura atende ao requisito de representação hierárquica solicitado no projeto.

---

## 3. Matriz (Lista de Listas)

Utilizada para armazenar os dados de telemetria.

Cada linha representa um horário e cada coluna representa uma variável monitorada.

### Variáveis monitoradas

- Horário
- Geração Solar (kWh)
- Consumo (kWh)
- Bateria (%)
- Temperatura (°C)
- Radiação (mSv/h)

A matriz possui 6 registros de monitoramento.

---

## 4. Lista

Utilizada para armazenar o histórico de eventos da missão.

Foram cadastrados 8 registros de eventos:

1. Sistema de telemetria iniciado.
2. Modo de economia ativado.
3. Falha temporária no sensor de radiação.
4. Sensor reinicializado com sucesso.
5. Mudança de prioridade energética.
6. Bateria atingiu capacidade máxima.
7. Flutuação de temperatura detectada.
8. Operações estabilizadas.

---

## 5. Fila (FIFO)

Utilizada para armazenar alertas gerados pelo sistema.

Funcionamento:

- Inserção com append()
- Remoção com pop(0)

Primeiro alerta inserido é o primeiro alerta processado.

---

## 6. Pilha (LIFO)

Utilizada para armazenar logs críticos.

Funcionamento:

- Inserção com append()
- Remoção com pop()

Último evento registrado é o primeiro evento exibido.

---

# Dados Simulados Utilizados

## Status dos Módulos

| Módulo | Status |
|----------|----------|
| Suporte à Vida | 1 |
| Energia | 1 |
| Comunicação | 0 |
| Habitat | 1 |
| Laboratório | 1 |
| Armazenamento | 1 |

---

## Telemetria

| Horário | Geração | Consumo | Bateria | Temperatura | Radiação |
|----------|----------|----------|----------|----------|----------|
| 08:00 | 30 | 20 | 80 | 15 | 0.1 |
| 10:00 | 55 | 25 | 85 | 18 | 0.2 |
| 12:00 | 70 | 30 | 90 | 22 | 0.5 |
| 14:00 | 65 | 35 | 95 | 21 | 0.4 |
| 16:00 | 40 | 40 | 95 | 17 | 0.2 |
| 18:00 | 5 | 45 | 90 | 12 | 0.1 |

---

# Inconsistência Proposital

Foi criada uma inconsistência para testar a capacidade de diagnóstico do sistema.

O módulo de energia permanece operacional:

```text
energia = 1
```

Porém a bateria é alterada para:

```text
bateria = 12%
```

Isso gera um conflito entre o status do módulo e os dados reais de telemetria.

O sistema detecta automaticamente essa inconsistência e gera alertas.

---

# Regras Lógicas Implementadas

## Operador AND

Utilizado para detectar inconsistência entre energia operacional e bateria crítica.

Condição:

```text
energia operacional AND bateria abaixo de 20%
```

Ação:

Geração de alerta crítico por conflito de dados.

---

## Operador NOT

Utilizado para verificar falha de comunicação.

Condição:

```text
NOT comunicacao
```

Ação:

Geração de alerta de comunicação offline.

---

## Operador OR

Utilizado para detectar condições ambientais perigosas.

Condição:

```text
temperatura > 40 OR radiacao > 0.4
```

Ação:

Geração de alerta ambiental.

---

# Estrutura IF, ELIF e ELSE

Utilizada para classificar o estado da bateria.

### Regras

- Bateria menor que 20% → CRÍTICO
- Bateria entre 20% e 49% → ALERTA
- Bateria acima de 50% → NORMAL

---

# Expressão Booleana Principal do Diagnóstico

O sistema considera uma situação crítica quando:

```text
(energia == 1 AND bateria < 20)
OR
(NOT comunicacao)
OR
(temperatura > 40 OR radiacao > 0.4)
```

Essa expressão combina operadores AND, OR e NOT para identificar situações críticas da missão.

---

# Técnica de Previsão Utilizada

O sistema realiza uma previsão de consumo energético utilizando Média Móvel Simples.

Os valores de consumo registrados são:

```text
20, 25, 30, 35, 40, 45
```

Os três últimos valores são:

```text
35, 40, 45
```

Cálculo:

```text
(35 + 40 + 45) / 3
```

Resultado:

```text
40 kWh
```

Previsão de consumo para o próximo ciclo:

```text
40 kWh
```

Essa previsão é utilizada para auxiliar decisões relacionadas ao gerenciamento energético.

---

# Recomendações Geradas Pelo Sistema

Quando a previsão de consumo é maior que a geração disponível, o sistema recomenda:

- Desligar o módulo LABORATÓRIO.
- Priorizar sistemas essenciais.
- Reduzir consumo energético.
- Preservar energia para suporte à vida e habitat.

Além disso:

- Bateria abaixo de 20% → Ativar modo de sobrevivência.
- Comunicação offline → Tentar reconexão automática.
- Ambiente hostil → Reforçar protocolos de segurança.

---

# Bibliotecas Utilizadas

## NumPy

Utilizado para manipulação dos dados numéricos da matriz de telemetria.

```python
import numpy as np
```

## Matplotlib

Utilizado para geração do gráfico de monitoramento.

```python
import matplotlib.pyplot as plt
```

---

# Gráfico Gerado

O sistema gera automaticamente o arquivo:

```text
grafico_telemetria.png
```

O gráfico apresenta:

- Geração Solar
- Consumo Energético
- Nível da Bateria

---

# Como Executar

Abra o terminal na pasta do projeto e execute:

```bash
python src/sistema.py
```

Pré-requisitos:

```bash
pip install numpy matplotlib
```

---

# Exemplo de Entrada

```text
Energia = 1
Comunicação = 0
Bateria = 12%
Temperatura = 12°C
Radiação = 0.1 mSv/h
```

---

# Exemplo de Saída

```text
CRÍTICO: Bateria em nível de emergência.

CRÍTICO: Conflito de dados! Módulo Energia consta como NORMAL, mas telemetria indica bateria em 12%.

ALERTA: Link de comunicação interplanetária offline. Tentando reconexão automática.

Previsão de consumo para o próximo ciclo: 40.00 kWh

Recomendação: Geração solar será insuficiente. Desligar módulo LABORATÓRIO.
```

---

# Fluxo de Execução

1. Inicialização das estruturas de dados.
2. Inserção da inconsistência proposital.
3. Extração da série histórica de consumo.
4. Cálculo da previsão de consumo.
5. Processamento das regras lógicas.
6. Geração dos alertas.
7. Exibição do painel de controle.
8. Exibição dos logs críticos.
9. Geração do gráfico de telemetria.

---

# Resultado Esperado

Ao executar o programa, o sistema deverá:

- Exibir o status dos módulos críticos.
- Exibir os dados de telemetria.
- Detectar inconsistências.
- Gerar alertas automáticos.
- Registrar logs críticos.
- Calcular previsão de consumo.
- Gerar o gráfico de monitoramento.

---

# Link do Vídeo


# Conclusão

O projeto permitiu aplicar conceitos de estruturas de dados, lógica booleana, análise preditiva e monitoramento operacional em um cenário inspirado na indústria espacial.

A solução desenvolvida demonstra como sistemas computacionais podem interpretar dados, identificar falhas, gerar alertas automáticos e fornecer recomendações para apoiar a tomada de decisões em ambientes críticos.

Além do desenvolvimento técnico, o projeto contribuiu para o entendimento da importância da organização dos dados, da automação de diagnósticos e da utilização de previsões para aumentar a segurança e a eficiência das operações.
