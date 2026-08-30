# Projeto_Calculo_Numerico
# MMQ - Visualizador de Ajuste de Curvas

O **Visualizador de Ajuste de Curvas** é uma ferramenta gráfica desenvolvida em Python para auxiliar na análise e modelagem de dados. O objetivo principal do projeto é aplicar o **Método dos Mínimos Quadrados (MMQ)** para encontrar a equação polinomial que melhor se ajusta a um conjunto de pontos bidimensionais (X, Y) fornecidos pelo usuário.

## Base Matemática
1. **Matriz de Vandermonde:** O sistema organiza os valores de X em uma matriz conforme o grau do polinômio escolhido.
2. **Equação Normal:** O modelo resolve a equação $(X^T X)^{-1} X^T Y$ para extrair os coeficientes exatos da curva.
3. **Coeficiente de Determinação ($R^2$):** O programa calcula a proporção da variância nos dados para indicar o quão bem a curva se adapta aos pontos reais.

## Funcionalidades Principais
* **Ajuste Dinâmico:** Geração de polinômios variando do grau 1 (regressão linear) até o grau 4[cite: 1].
* **Flexibilidade na Entrada de Dados:** Os dados podem ser inseridos ponto a ponto manualmente pela interface ou importados em lote através de arquivos `.csv`.
* **Retorno Analítico:** Exibição imediata da equação da curva formatada e do seu nível de precisão matemática ($R^2$).
* **Módulo de Previsão:** Permite ao usuário informar um novo valor de X. O aplicativo utiliza a equação gerada para estimar o valor de Y correspondente e plota uma estrela de destaque no gráfico indicando essa previsão.
* **Interface Gráfica Moderna:** Construída em tema escuro, possui um gráfico incorporado que atualiza em tempo real, diferenciando visualmente os dados originais, a curva de ajuste e as previsões geradas.

## Tecnologias Utilizadas
* **Python**
* **CustomTkinter:** Construção de uma interface gráfica (GUI).
* **NumPy:** Responsável por todo o processamento de matrizes e resolução dos cálculos de álgebra linear.
* **Pandas:** Realiza a leitura e a extração de dados estruturados a partir de arquivos CSV.
* **Matplotlib:** Renderiza a área do gráfico bidimensional integrado à janela do aplicativo.
