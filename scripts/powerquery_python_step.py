# ===============================================================
# WorldSkills Portugal - Profissão P21
# Script para colar em: Power Query > Transformar > Executar Script Python
# 'dataset' é o DataFrame de entrada fornecido pelo Power Query
# ===============================================================

import pandas as pd
import numpy as np

df = dataset

# 1. Tratar valores nulos com interpolação linear (séries cronológicas)
if 'QuantidadeKg' in df.columns:
    df['QuantidadeKg'] = df['QuantidadeKg'].interpolate(method='linear')

# 2. Preencher nulos de desconto com 0
if 'DiscountAmount' in df.columns:
    df['DiscountAmount'] = df['DiscountAmount'].fillna(0)

# 3. Criar coluna calculada TotalGasto
if 'QuantityKg' in df.columns and 'UnitPrice' in df.columns:
    df['TotalGasto'] = df['QuantityKg'] * df['UnitPrice']

# O Power Query deteta a variável de saída
output = df

