"""
A股适配版富士通AI分析逻辑框架
针对A股ESG披露的监管要求和企业痛点的智能分析系统
"""

__version__ = "1.0.0"
__author__ = "A-Stock ESG Team"

from .core.config import AStockESGConfig
from .compliance.engine import ComplianceEngine
from .data.collector import DataCollector
from .data.parser import DocumentParser
from .data.astock_integration import AStockDataIntegrator, ESGDataPipeline
from .nlp.processor import NLPProcessor
from .visualization.benchmark import BenchmarkAnalyzer
from .visualization.visualizer import Visualizer
from .knowledge_graph.graph import KnowledgeGraph

__all__ = [
    "AStockESGConfig",
    "ComplianceEngine",
    "DataCollector",
    "DocumentParser",
    "AStockDataIntegrator",
    "ESGDataPipeline",
    "NLPProcessor",
    "BenchmarkAnalyzer",
    "Visualizer",
    "KnowledgeGraph",
]
