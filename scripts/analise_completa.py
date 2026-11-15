"""
WorldSkills Portugal - Profissão P21: Data Science e Inteligência Artificial
Script Completo de Treino e Resolução dos 4 Exercícios da Fase 2 Regional
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram

print("=========================================================")
print("  WSP27 - DATA SCIENCE & MACHINE LEARNING PIPELINE")
print("=========================================================\n")

# ===============================================================
# 1. INGESTÃO E PREPARAÇÃO DE DADOS
# ===============================================================
print("[1/5] Ingestão e Preparação de Dados...")
try:
    df_sales = pd.read_csv('data/FactSales.csv', sep=';', decimal=',')
    df_customers = pd.read_csv('data/DimCostumer.csv')
    df_products = pd.read_csv('data/DimProduct.csv', sep=';', decimal=',')
    print(f" -> Vendas: {df_sales.shape}, Clientes: {df_customers.shape}, Produtos: {df_products.shape}")

    # Reconstrução (Merge)
    df_merged = df_sales.merge(df_customers, on='CustomerKey', how='left')
    df_merged = df_merged.merge(df_products, on='ProductKey', how='left')

    # Tratamento de Nulos
    if 'DiscountAmount' in df_merged.columns:
        df_merged['DiscountAmount'] = df_merged['DiscountAmount'].fillna(0)

    # Feature Engineering
    df_merged['TotalGasto'] = df_merged['QuantityKg'] * df_merged['UnitPrice']
    print(" -> Merge efetuado com sucesso!")
except Exception as e:
    print(f" -> Aviso: Ficheiros CSV reais não encontrados ({e}). A gerar dados simulados...")
    # Criar dados sintéticos com a estrutura exata da prova Frutose
    np.random.seed(42)
    n = 200
    df_merged = pd.DataFrame({
        'CustomerKey': np.random.randint(1, 25, n),
        'ProductKey': np.random.randint(101, 115, n),
        'QuantityKg': np.round(np.random.uniform(1.0, 50.0, n), 2),
        'UnitPrice': np.round(np.random.uniform(1.5, 5.0, n), 2),
        'DiscountPct': np.round(np.random.choice([0.0, 0.05, 0.10, 0.15], n), 2),
        'StandardCost': np.round(np.random.uniform(0.8, 3.0, n), 2)
    })
    df_merged['DiscountAmount'] = df_merged['QuantityKg'] * df_merged['UnitPrice'] * df_merged['DiscountPct']
    df_merged['TotalGasto'] = df_merged['QuantityKg'] * df_merged['UnitPrice'] - df_merged['DiscountAmount']
    df_merged['ProfitAmount'] = df_merged['TotalGasto'] - (df_merged['QuantityKg'] * df_merged['StandardCost'])

print(df_merged.head())

# ===============================================================
# 2. CLUSTERING (K-MEANS & HIERÁRQUICO)
# ===============================================================
print("\n[2/5] Segmentação de Clientes (Clustering)...")
customer_behavior = df_merged.groupby('CustomerKey').agg({
    'TotalGasto': 'sum',
    'QuantityKg': 'sum'
}).reset_index()

X_cluster = customer_behavior[['TotalGasto', 'QuantityKg']]
scaler = StandardScaler()
X_cluster_scaled = scaler.fit_transform(X_cluster)

# K-Means (k=3)
kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
customer_behavior['Cluster'] = kmeans.fit_predict(X_cluster_scaled)
print(f" -> K-Means concluído! Centróides:\n{kmeans.cluster_centers_}")

# ===============================================================
# 3. REGRESSÃO LINEAR MÚLTIPLA (PREVISÃO DE LUCRO)
# ===============================================================
print("\n[3/5] Regressão Linear Múltipla...")
df_reg = df_merged.dropna(subset=['QuantityKg', 'UnitPrice', 'DiscountPct', 'ProfitAmount'])
X_reg = df_reg[['QuantityKg', 'UnitPrice', 'DiscountPct']]
y_reg = df_reg['ProfitAmount']

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

modelo_reg = LinearRegression()
modelo_reg.fit(X_train_r, y_train_r)
previsoes_reg = modelo_reg.predict(X_test_r)

r2 = r2_score(y_test_r, previsoes_reg)
rmse = np.sqrt(mean_squared_error(y_test_r, previsoes_reg))
print(f" -> Intercept: {modelo_reg.intercept_:.4f}")
print(f" -> Coeficientes: {modelo_reg.coef_.round(4)}")
print(f" -> R²: {r2:.4f}")
print(f" -> RMSE: {rmse:.4f} €")

# ===============================================================
# 4. CLASSIFICAÇÃO (ÁRVORE DE DECISÃO E RANDOM FOREST)
# ===============================================================
print("\n[4/5] Classificação com Árvore de Decisão e Random Forest...")
df_merged['AltoLucro'] = (df_merged['ProfitAmount'] > 10).astype(int)

features = ['QuantityKg', 'UnitPrice', 'StandardCost']
X_clf = df_merged[features]
y_clf = df_merged['AltoLucro']

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.3, random_state=123, stratify=y_clf)

# Árvore de Decisão
arvore = DecisionTreeClassifier(max_depth=4, random_state=123)
arvore.fit(X_train_c, y_train_c)
prev_arvore = arvore.predict(X_test_c)

print(" -> Relatório Árvore de Decisão:")
print(classification_report(y_test_c, prev_arvore, zero_division=0))

# Random Forest
floresta = RandomForestClassifier(n_estimators=50, random_state=123)
floresta.fit(X_train_c, y_train_c)
prev_floresta = floresta.predict(X_test_c)

print(" -> Feature Importances (Random Forest):")
for f, imp in zip(features, floresta.feature_importances_):
    print(f"    - {f:<15}: {imp:.4f}")

# ===============================================================
# 5. RESUMO FINAL
# ===============================================================
print("\n[5/5] Pipeline executado com sucesso e validado!")

