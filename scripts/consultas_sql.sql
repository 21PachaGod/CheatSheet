-- ===============================================================
-- WorldSkills Portugal - Profissão P21 (Data Science / IA)
-- Scripts e Consultas SQL Server / SQLEXPRESS
-- ===============================================================

-- 1. Criar base de dados se necessário
CREATE DATABASE FrutoseDB;
GO

USE FrutoseDB;
GO

-- 2. Consulta de Agregação de Vendas por Cliente com Margem %
SELECT 
    f.CustomerKey,
    c.CustomerName,
    COUNT(f.SalesKey) AS NrTransacoes,
    SUM(f.QuantityKg) AS TotalKg,
    SUM(f.QuantityKg * f.UnitPrice) AS ReceitaBruta,
    SUM(ISNULL(f.DiscountAmount, 0)) AS TotalDesconto,
    SUM(f.ProfitAmount) AS LucroTotal,
    ROUND(SUM(f.ProfitAmount) / NULLIF(SUM(f.QuantityKg * f.UnitPrice), 0) * 100, 2) AS MargemLucroPct
FROM FactSales f
LEFT JOIN DimCostumer c ON f.CustomerKey = c.CustomerKey
GROUP BY f.CustomerKey, c.CustomerName
ORDER BY ReceitaBruta DESC;

-- 3. Identificação de Produtos com Rutura de Stock
SELECT 
    p.ProductKey,
    p.ProductName,
    p.StandardCost,
    s.StockActual,
    s.PontoReposicao,
    CASE 
        WHEN s.StockActual = 0 THEN 'Rutura Crítica'
        WHEN s.StockActual < s.PontoReposicao THEN 'Reposição Necessária'
        ELSE 'Stock Confortável'
    END AS EstadoStock
FROM DimProduct p
INNER JOIN StockPolo s ON p.ProductKey = s.ProductKey
WHERE s.StockActual < s.PontoReposicao
ORDER BY s.StockActual ASC;

-- 4. Criação de Vista Analítica (Boa prática de Engenharia de Dados)
CREATE OR ALTER VIEW vw_DashboardVendas AS
SELECT 
    d.DateKey,
    d.FullDateAlternateKey AS Data,
    d.CalendarYear AS Ano,
    d.MonthNumberOfYear AS Mes,
    p.ProductName AS Produto,
    p.CategoryName AS Categoria,
    c.CustomerName AS Cliente,
    s.StoreName AS Loja,
    f.QuantityKg,
    f.UnitPrice,
    (f.QuantityKg * f.UnitPrice) AS TotalVenda,
    f.ProfitAmount AS Lucro
FROM FactSales f
JOIN DimDate d ON f.DateKey = d.DateKey
JOIN DimProduct p ON f.ProductKey = p.ProductKey
JOIN DimCostumer c ON f.CustomerKey = c.CustomerKey
JOIN DimStore s ON f.StoreKey = s.StoreKey;
GO

