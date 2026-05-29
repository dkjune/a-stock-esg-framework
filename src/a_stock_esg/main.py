"""
A股适配版富士通AI分析逻辑框架 - 主程序入口
"""

from .core import (
    AStockESGConfig,
    ComplianceEngine,
    DataCollector,
    NLPProcessor,
    BenchmarkAnalyzer,
    Visualizer,
    KnowledgeGraph,
)

__version__ = "1.0.0"
__author__ = "A-Stock ESG Team"

__all__ = [
    "AStockESGConfig",
    "ComplianceEngine",
    "DataCollector",
    "NLPProcessor",
    "BenchmarkAnalyzer",
    "Visualizer",
    "KnowledgeGraph",
]


class AStockESGAnalyzer:
    """
    A股ESG分析器主类
    
    整合所有模块，提供统一的分析接口
    """
    
    def __init__(self, config: AStockESGConfig = None):
        """
        初始化分析器
        
        Args:
            config: 配置对象
        """
        self.config = config or AStockESGConfig()
        self.compliance_engine = ComplianceEngine(self.config)
        self.data_collector = DataCollector()
        self.nlp_processor = NLPProcessor()
        self.visualizer = Visualizer()
        self.knowledge_graph = KnowledgeGraph()
        self.benchmark_analyzer = BenchmarkAnalyzer(self.data_collector)
    
    def analyze_document(
        self, 
        document_text: str,
        company_name: str = "",
        market_type: str = "主板",
        industry: str = "电子"
    ) -> dict:
        """
        分析ESG文档
        
        Args:
            document_text: 文档文本
            company_name: 公司名称
            market_type: 市场类型
            industry: 行业
            
        Returns:
            dict: 分析结果
        """
        # 合规性检查
        compliance_report = self.compliance_engine.check_compliance(
            document_text, company_name, market_type, industry
        )
        
        # NLP信息提取
        extracted_info = self.nlp_processor.extract_esg_info(document_text)
        terms = self.nlp_processor.identify_terms(document_text)
        sentiment = self.nlp_processor.analyze_sentiment(document_text)
        
        return {
            "compliance_report": compliance_report,
            "extracted_info": extracted_info,
            "identified_terms": terms,
            "sentiment": sentiment,
        }
    
    def generate_dashboard(
        self, 
        compliance_report,
        output_path: str = "esg_dashboard.html"
    ) -> str:
        """
        生成可视化看板
        
        Args:
            compliance_report: 合规报告
            output_path: 输出路径
            
        Returns:
            str: 看板文件路径
        """
        return self.visualizer.create_compliance_dashboard(
            compliance_report, output_path
        )
    
    def get_benchmark_comparison(
        self, 
        company_code: str,
        company_score: float,
        year: int = 2024
    ):
        """
        获取行业对标
        
        Args:
            company_code: 公司代码
            company_score: 公司评分
            year: 年份
            
        Returns:
            BenchmarkComparison: 对标结果
        """
        return self.benchmark_analyzer.compare_with_industry(
            company_code, company_score, year
        )
