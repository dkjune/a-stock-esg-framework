"""
A股中特估分析框架 v4.0（噪声优化版）

基于《噪声》理论（丹尼尔·卡尼曼）：
- 决策卫生：规则替代直觉
- 多源聚合：降低测量噪声
- 置信区间：输出不确定性
- 双模型校验：独立验证
"""

__version__ = "4.0.0"
__author__ = "A-Stock ESG Team"

from .data import AStockData, stock_data, MultiSourceData, ROETrendData, ValuationAnchor
from .roe import ROEAnalyzer
from .policy import PolicyAnalyzer, PolicyMatchResult
from .noise_report import NoiseReportGenerator, NoiseReport

__all__ = [
    # 数据获取
    "AStockData",
    "stock_data",
    "MultiSourceData",
    "ROETrendData",
    "ValuationAnchor",
    # ROE分析
    "ROEAnalyzer",
    # 政策分析
    "PolicyAnalyzer",
    "PolicyMatchResult",
    # 噪声报告
    "NoiseReportGenerator",
    "NoiseReport",
]
