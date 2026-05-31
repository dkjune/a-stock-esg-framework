"""
A股中特估分析框架 v2.2

聚焦核心价值：
- ROE深度分析（杜邦分解）
- 中特估政策匹配度分析
- 实时数据获取（融合a-stock-data）
- 数据验证机制
"""

__version__ = "2.2.0"
__author__ = "A-Stock ESG Team"

from .data import AStockData, stock_data, StockQuote, FinancialSnapshot
from .roe import ROEAnalyzer, ROEResult, ROEQuality
from .policy import PolicyAnalyzer, PolicyMatchResult, PolicyDimension
from .validator import DataValidator, validator, ValidationResult

__all__ = [
    # 数据获取
    "AStockData",
    "stock_data",
    "StockQuote",
    "FinancialSnapshot",
    # ROE分析
    "ROEAnalyzer",
    "ROEResult",
    "ROEQuality",
    # 政策分析
    "PolicyAnalyzer",
    "PolicyMatchResult",
    "PolicyDimension",
    # 数据验证
    "DataValidator",
    "validator",
    "ValidationResult",
]
