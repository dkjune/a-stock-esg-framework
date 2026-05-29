"""
A股ESG框架测试
"""

import pytest
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import (
    AStockESGConfig,
    ComplianceEngine,
    NLPProcessor,
    BenchmarkAnalyzer,
    Visualizer,
    DataCollector,
    KnowledgeGraph,
)
from a_stock_esg.core.config import MarketType, IndustryClassification
from a_stock_esg.compliance.engine import ComplianceStatus
from a_stock_esg.data.collector import CompanyInfo


class TestComplianceEngine:
    """合规检查引擎测试"""
    
    def setup_method(self):
        """测试前准备"""
        self.config = AStockESGConfig(
            market_type=MarketType.MAIN_BOARD,
            industry=IndustryClassification.ELECTRONICS,
        )
        self.engine = ComplianceEngine(self.config)
    
    def test_check_compliance_basic(self):
        """测试基础合规检查"""
        text = "公司温室气体排放总量为100,000吨CO2当量。"
        report = self.engine.check_compliance(
            text, "测试公司", "主板", "电子"
        )
        
        assert report.company_name == "测试公司"
        assert report.total_items > 0
        assert report.compliance_score >= 0
    
    def test_compliance_status(self):
        """测试合规状态"""
        text = "公司碳排放数据已披露，能源消耗数据已披露。"
        report = self.engine.check_compliance(text, "测试公司", "主板", "电子")
        
        # 检查是否有合规项
        statuses = [item.status for item in report.items]
        assert any(s == ComplianceStatus.COMPLIANT for s in statuses)
    
    def test_star_board_requirements(self):
        """测试科创板特殊要求"""
        config = AStockESGConfig(market_type=MarketType.STAR_BOARD)
        engine = ComplianceEngine(config)
        
        text = "公司绿色技术研发投入达1000万元，知识产权保护措施完善。"
        report = engine.check_compliance(text, "测试公司", "科创板", "电子")
        
        # 科创板应有特殊检查项
        assert report.total_items > 0


class TestNLPProcessor:
    """NLP处理器测试"""
    
    def setup_method(self):
        """测试前准备"""
        self.processor = NLPProcessor()
    
    def test_extract_esg_info(self):
        """测试ESG信息提取"""
        text = "公司碳排放量为50,000吨，能源消耗100万千瓦时。"
        info = self.processor.extract_esg_info(text)
        
        assert len(info) > 0
        categories = [i.category for i in info]
        assert "E" in categories
    
    def test_identify_terms(self):
        """测试术语识别"""
        text = "公司积极推进碳中和战略，员工权益保护措施完善。"
        terms = self.processor.identify_terms(text)
        
        assert len(terms) > 0
        term_names = [t.term for t in terms]
        assert "碳中和" in term_names
    
    def test_sentiment_analysis(self):
        """测试情感分析"""
        text = "公司ESG表现优秀，碳排放显著下降。"
        sentiment = self.processor.analyze_sentiment(text)
        
        assert sentiment.sentiment in ["positive", "negative", "neutral"]
        assert 0 <= sentiment.score <= 1


class TestDataCollector:
    """数据收集器测试"""
    
    def setup_method(self):
        """测试前准备"""
        self.collector = DataCollector()
    
    def test_add_company(self):
        """测试添加公司"""
        company = CompanyInfo(
            stock_code="000001",
            company_name="测试公司",
            market_type="主板",
            industry="电子",
        )
        self.collector.add_company(company)
        
        retrieved = self.collector.get_company_info("000001")
        assert retrieved is not None
        assert retrieved.company_name == "测试公司"
    
    def test_get_regulatory_standard(self):
        """测试获取监管标准"""
        standards = self.collector.get_regulatory_standard("主板")
        
        assert len(standards) > 0
    
    def test_data_summary(self):
        """测试数据摘要"""
        summary = self.collector.get_data_summary()
        
        assert "total_companies" in summary
        assert "total_disclosures" in summary


class TestBenchmarkAnalyzer:
    """对标分析器测试"""
    
    def setup_method(self):
        """测试前准备"""
        self.collector = DataCollector()
        company = CompanyInfo(
            stock_code="000001",
            company_name="测试公司",
            market_type="主板",
            industry="电子",
        )
        self.collector.add_company(company)
        self.analyzer = BenchmarkAnalyzer(self.collector)
    
    def test_compare_with_industry(self):
        """测试行业对标"""
        comparison = self.analyzer.compare_with_industry(
            "000001", 75.5, 2024
        )
        
        assert comparison.company_code == "000001"
        assert comparison.company_score == 75.5
    
    def test_differentiation_suggestions(self):
        """测试差异化建议"""
        suggestions = self.analyzer.generate_differentiation_suggestions(
            "000001", "电子", "主板"
        )
        
        assert len(suggestions) > 0


class TestKnowledgeGraph:
    """知识图谱测试"""
    
    def setup_method(self):
        """测试前准备"""
        self.graph = KnowledgeGraph()
    
    def test_build_graph(self):
        """测试构建图谱"""
        company_data = {
            "stock_code": "000001",
            "company_name": "测试公司",
            "market_type": "主板",
            "industry": "电子",
            "esg_metrics": {"碳排放强度": 0.5},
            "financial_metrics": {"ROE": 15.5},
        }
        
        self.graph.build_esg_financial_graph(company_data)
        
        stats = self.graph.get_statistics()
        assert stats["total_nodes"] > 0
        assert stats["total_edges"] > 0
    
    def test_get_network(self):
        """测试获取网络"""
        company_data = {
            "stock_code": "000001",
            "company_name": "测试公司",
            "market_type": "主板",
            "industry": "电子",
            "esg_metrics": {},
            "financial_metrics": {},
        }
        
        self.graph.build_esg_financial_graph(company_data)
        network = self.graph.get_company_esg_network("000001")
        
        assert "nodes" in network
        assert "edges" in network


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
