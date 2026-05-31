"""
可视化与投资分析模块
"""

from .benchmark import BenchmarkAnalyzer, BenchmarkComparison, DifferentiationSuggestion
from .visualizer import Visualizer, DashboardConfig
from .scorer import PersonalInvestorScorer, StockFactorGenerator, StockScore, ScoringResult

__all__ = [
    # 对标分析
    "BenchmarkAnalyzer",
    "BenchmarkComparison",
    "DifferentiationSuggestion",
    # 可视化
    "Visualizer",
    "DashboardConfig",
    # 投资评分
    "PersonalInvestorScorer",
    "StockFactorGenerator",
    "StockScore",
    "ScoringResult",
]
