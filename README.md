# WSP27 - Data Science & IA Cheat Sheet

Cheat Sheet interativo para a prova **WorldSkills Portugal - Profissão P21 (Data Science e Inteligência Artificial)**.

Cobre os **Módulos 2 (Dashboards BI)** e **Módulo 3 (AI/ML)** da Fase 2 Regional, com código Python pronto a copiar, fórmulas DAX e um assistente Gemini integrado.

## Páginas

| Página | Conteúdo |
|--------|----------|
| **Python: Ingestão e Preparação** | Importação CSV, merge, tratamento de nulos, interpolação linear, Feature Engineering, correlação de Pearson, RFE |
| **ML: Clustering e Segmentação** | K-Means, Clustering Hierárquico (Single/Complete Linkage), dendrogramas, Silhouette Score, Elbow Method |
| **ML: Classificação (Árvores)** | Decision Tree, Random Forest, Matriz de Confusão, F1-Score, Feature Importance |
| **ML: Regressão Linear e Logística** | Regressão Linear Múltipla, Regressão Logística, R², RMSE, previsão de probabilidades |
| **ML: Q-Learning (Reforço)** | Aprendizagem por Reforço, Tabela Q, Equação de Bellman, Política Epsilon-Greedy |
| **Power BI e DAX** | Modelo Star Schema, medidas DAX (vendas, lucro, time intelligence, rankings), Power Query ETL, boas práticas de dashboards |
| **Python no PBI & SQL** | Visuais Python no Power BI, Scripts Power Query (M), Tabela Calendário DAX completa, Queries SQL Server e scripts R |
| **Assistente Gemini (IA)** | Chatbot interativo com a API Gemini, prompts rápidos para Python/DAX, fallback automático de modelos |

## Pasta `scripts/`

- `analise_completa.py`: Script Python com o pipeline ponta a ponta (ingestão, merges, K-Means, árvores, random forest, regressão) pronto a executar no VS Code.
- `consultas_sql.sql`: Queries de agregação, ruturas de stock e criação de Views para o SQLEXPRESS.
- `powerquery_python_step.py`: Bloco de código para colar no "Executar Script Python" do Power Query.

## Como usar

1. Abrir `index.html` no browser (ou publicar no GitHub Pages).
2. Cada página tem botões **"Copiar código"** para copiar diretamente blocos de Python ou DAX.
3. O assistente Gemini requer uma API Key gratuita do [Google AI Studio](https://aistudio.google.com/app/apikey).

## Datasets esperados

Os exercícios referem os ficheiros CSV do grupo **Frutose**:
- `FactSales.csv` (separador `;`, decimal `,`)
- `DimCostumer.csv`
- `DimProduct.csv` (separador `;`, decimal `,`)
- `DimStore.csv`
- `DimDate.csv`
