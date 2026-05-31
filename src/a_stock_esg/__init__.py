"""
A股中特估分析框架 v3.0（前景理论优化版）

核心优化：
- ROE深度分析（杜邦分解）
- 中特估政策匹配度分析
- 实时数据获取（融合a-stock-data）
- 数据验证机制
- 前景理论优化：估值锚点、损失厌恶、概率化表达
"""

__version__ = "3.0.0"
__author__ = "A-Stock ESG Team"

from .data import AStockData, stock_data, StockQuote, FinancialSnapshot, ValuationAnchor
from .roe import ROEAnalyzer
from .policy import PolicyAnalyzer, PolicyMatchResult

__all__ = [
    # 数据获取
    "AStockData",
    "stock_data",
    "StockQuote",
    "FinancialSnapshot",
    "ValuationAnchor",
    # ROE分析
    "ROEAnalyzer",
    # 政策分析
    "PolicyAnalyzer",
    "PolicyMatchResult",
]
