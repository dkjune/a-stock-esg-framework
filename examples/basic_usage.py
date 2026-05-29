"""
A股ESG分析示例脚本
"""

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


def example_compliance_check():
    """示例：合规性检查"""
    print("=" * 60)
    print("示例1：合规性检查")
    print("=" * 60)
    
    # 创建配置
    config = AStockESGConfig(
        market_type=MarketType.MAIN_BOARD,
        industry=IndustryClassification.ELECTRONICS,
    )
    
    # 创建合规检查引擎
    engine = ComplianceEngine(config)
    
    # 模拟ESG报告文本
    sample_text = """
    本公司高度重视环境保护和社会责任。在碳排放方面，2024年公司温室气体排放总量为
    125,000吨CO2当量，较上年下降5%。公司已制定碳达峰、碳中和目标，计划于2030年
    实现碳达峰，2060年实现碳中和。
    
    在员工管理方面，公司现有员工总数5,000人，其中男性占60%，女性占40%。公司重视
    员工培训，年度培训投入达500万元，人均培训时长40小时。
    
    在公司治理方面，公司董事会已设立ESG委员会，负责统筹ESG相关工作。公司制定了
    反腐败政策和数据安全管理规定。
    """
    
    # 执行合规检查
    report = engine.check_compliance(
        document_text=sample_text,
        company_name="示例电子科技有限公司",
        market_type="主板",
        industry="电子",
    )
    
    # 输出结果
    print(f"公司名称: {report.company_name}")
    print(f"市场类型: {report.market_type}")
    print(f"行业: {report.industry}")
    print(f"合规评分: {report.compliance_score}")
    print(f"总检查项: {report.total_items}")
    print(f"合规项: {report.compliant_items}")
    print(f"部分合规: {report.partial_items}")
    print(f"缺失项: {report.missing_items}")
    print()
    print("改进建议:")
    for i, rec in enumerate(report.recommendations, 1):
        print(f"  {i}. {rec}")
    
    return report


def example_nlp_processing():
    """示例：NLP处理"""
    print("\n" + "=" * 60)
    print("示例2：中文NLP处理")
    print("=" * 60)
    
    # 创建NLP处理器
    processor = NLPProcessor()
    
    # 模拟文本
    text = """
    公司积极推进碳中和战略，2024年碳排放量较上年下降8%。公司在绿色技术方面
    加大研发投入，环保技术专利数量达到50项。公司员工总数3,000人，安全生产
    事故率为零。公司建立了完善的数据安全管理体系，通过了ISO27001认证。
    """
    
    # 提取ESG信息
    extracted_info = processor.extract_esg_info(text)
    print("提取的ESG信息:")
    for info in extracted_info:
        print(f"  [{info.category}-{info.subcategory}] {info.content}")
    
    # 识别术语
    terms = processor.identify_terms(text)
    print("\n识别的ESG术语:")
    for term in terms:
        print(f"  {term.term} ({term.category})")
    
    # 情感分析
    sentiment = processor.analyze_sentiment(text)
    print(f"\n情感分析: {sentiment.sentiment} (得分: {sentiment.score})")
    print(f"关键词: {', '.join(sentiment.keywords)}")
    
    # 提取数值
    numbers = processor.extract_numbers(text)
    print("\n提取的数值:")
    for num in numbers:
        print(f"  {num['value']}{num['unit']}")


def example_benchmark_analysis():
    """示例：行业对标分析"""
    print("\n" + "=" * 60)
    print("示例3：行业对标分析")
    print("=" * 60)
    
    # 创建数据收集器
    data_collector = DataCollector()
    
    # 添加示例公司
    from a_stock_esg.data.collector import CompanyInfo
    company = CompanyInfo(
        stock_code="000001",
        company_name="示例电子科技有限公司",
        market_type="主板",
        industry="电子",
    )
    data_collector.add_company(company)
    
    # 创建对标分析器
    analyzer = BenchmarkAnalyzer(data_collector)
    
    # 执行对标分析
    comparison = analyzer.compare_with_industry(
        company_code="000001",
        company_score=75.5,
        year=2024,
    )
    
    print(f"公司名称: {comparison.company_name}")
    print(f"公司评分: {comparison.company_score}")
    print(f"行业平均: {comparison.industry_average}")
    print(f"行业排名: {comparison.industry_rank}/{comparison.total_companies}")
    print(f"百分位: {comparison.percentile}%")
    print()
    print("优势:")
    for s in comparison.strengths:
        print(f"  - {s}")
    print("\n劣势:")
    for w in comparison.weaknesses:
        print(f"  - {w}")
    print("\n建议:")
    for r in comparison.recommendations:
        print(f"  - {r}")
    
    # 获取差异化建议
    suggestions = analyzer.generate_differentiation_suggestions(
        company_code="000001",
        industry="电子",
        market_type="主板",
    )
    
    print("\n差异化建议:")
    for s in suggestions:
        print(f"  [{s.category}] {s.suggestion}")
        print(f"    预期效果: {s.expected_impact}")


def example_knowledge_graph():
    """示例：知识图谱"""
    print("\n" + "=" * 60)
    print("示例4：知识图谱")
    print("=" * 60)
    
    # 创建知识图谱
    graph = KnowledgeGraph()
    
    # 构建ESG-财务关联图谱
    company_data = {
        "stock_code": "000001",
        "company_name": "示例电子科技有限公司",
        "market_type": "主板",
        "industry": "电子",
        "esg_metrics": {
            "碳排放强度": 0.5,
            "能源消耗强度": 1.2,
            "员工满意度": 85,
        },
        "financial_metrics": {
            "ROE": 15.5,
            "营业收入增长率": 12.3,
            "净利润增长率": 8.7,
        },
    }
    
    graph.build_esg_financial_graph(company_data)
    
    # 获取统计信息
    stats = graph.get_statistics()
    print(f"图谱统计:")
    print(f"  节点总数: {stats['total_nodes']}")
    print(f"  边总数: {stats['total_edges']}")
    print(f"  节点类型: {stats['node_types']}")
    
    # 获取公司网络
    network = graph.get_company_esg_network("000001")
    print(f"\n公司ESG网络:")
    for node in network['nodes']:
        print(f"  {node['name']} ({node['type']})")
    
    # 分析相关性
    correlation = graph.analyze_correlation("碳排放强度", "ROE")
    print(f"\n相关性分析:")
    print(f"  碳排放强度 vs ROE")
    print(f"  相关系数: {correlation['correlation']}")
    print(f"  置信度: {correlation['confidence']}")
    print(f"  解释: {correlation['interpretation']}")


def example_visualization(compliance_report):
    """示例：可视化"""
    print("\n" + "=" * 60)
    print("示例5：生成可视化看板")
    print("=" * 60)
    
    # 创建可视化器
    visualizer = Visualizer()
    
    # 生成看板
    output_path = "esg_dashboard.html"
    visualizer.create_compliance_dashboard(compliance_report, output_path)
    
    print(f"看板已生成: {output_path}")
    print("请在浏览器中打开查看")


def main():
    """主函数"""
    print("A股适配版富士通AI分析逻辑框架 - 示例演示")
    print("=" * 60)
    
    # 执行示例
    compliance_report = example_compliance_check()
    example_nlp_processing()
    example_benchmark_analysis()
    example_knowledge_graph()
    example_visualization(compliance_report)
    
    print("\n" + "=" * 60)
    print("所有示例执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
