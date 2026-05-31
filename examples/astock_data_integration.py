"""
A股数据集成示例
展示如何使用 a-stock-data 数据源进行ESG分析
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import (
    AStockESGConfig,
    ComplianceEngine,
    NLPProcessor,
    AStockDataIntegrator,
    ESGDataPipeline,
)


def example_stock_data_integration():
    """示例：股票数据集成"""
    print("=" * 60)
    print("示例1：A股数据集成")
    print("=" * 60)
    
    # 创建数据集成器
    integrator = AStockDataIntegrator()
    
    # 获取股票信息（示例：贵州茅台）
    stock_code = "600519"
    print(f"\n获取股票 {stock_code} 信息...")
    
    stock_info = integrator.get_stock_info(stock_code)
    if stock_info:
        print(f"股票名称: {stock_info.stock_name}")
        print(f"所属行业: {stock_info.industry}")
        print(f"市场类型: {stock_info.market_type}")
        print(f"总市值: {stock_info.market_cap} 亿")
    
    # 获取财务数据
    print(f"\n获取股票 {stock_code} 财务数据...")
    financial = integrator.get_financial_data(stock_code)
    if financial:
        print(f"PE(TTM): {financial.pe_ttm}")
        print(f"PB: {financial.pb}")
        print(f"总市值: {financial.market_cap} 亿")
    
    return stock_info, financial


def example_esg_pipeline():
    """示例：ESG数据管道"""
    print("\n" + "=" * 60)
    print("示例2：ESG数据管道")
    print("=" * 60)
    
    # 创建数据管道
    pipeline = ESGDataPipeline()
    
    # 准备ESG分析数据
    stock_code = "600519"
    print(f"\n准备股票 {stock_code} 的ESG分析数据...")
    
    esg_data = pipeline.prepare_esg_analysis(stock_code)
    
    print(f"公司名称: {esg_data['company_name']}")
    print(f"所属行业: {esg_data['industry']}")
    print(f"市场类型: {esg_data['market_type']}")
    print(f"\n财务指标:")
    print(f"  PE(TTM): {esg_data['financial_metrics']['pe_ttm']}")
    print(f"  PB: {esg_data['financial_metrics']['pb']}")
    print(f"  总市值: {esg_data['financial_metrics']['market_cap']} 亿")
    print(f"\nESG公告:")
    for filing in esg_data['esg_filings']:
        print(f"  - {filing['title']} ({filing['date']})")
    print(f"\nESG研报:")
    for report in esg_data['esg_reports']:
        print(f"  - {report['title']} ({report['institution']})")
    
    return esg_data


def example_industry_comparison():
    """示例：行业ESG对比"""
    print("\n" + "=" * 60)
    print("示例3：行业ESG对比")
    print("=" * 60)
    
    # 创建数据管道
    pipeline = ESGDataPipeline()
    
    # 获取银行行业股票
    industry = "银行"
    stock_codes = ["601398", "601939", "601288", "600036", "600016"]
    
    print(f"\n获取 {industry} 行业ESG对比数据...")
    
    comparison = pipeline.get_industry_esg_comparison(industry, stock_codes)
    
    print(f"行业: {comparison['industry']}")
    print(f"公司数量: {comparison['average_metrics']['company_count']}")
    print(f"平均PE: {comparison['average_metrics']['avg_pe']:.2f}")
    print(f"平均PB: {comparison['average_metrics']['avg_pb']:.2f}")
    
    print(f"\n各公司数据:")
    for company in comparison['companies']:
        print(f"  {company['stock_code']}: PE={company['financial_metrics']['pe_ttm']}, PB={company['financial_metrics']['pb']}")
    
    return comparison


def example_esg_compliance_with_data():
    """示例：结合数据的ESG合规检查"""
    print("\n" + "=" * 60)
    print("示例4：结合数据的ESG合规检查")
    print("=" * 60)
    
    # 创建配置
    config = AStockESGConfig()
    
    # 创建合规检查引擎
    engine = ComplianceEngine(config)
    
    # 创建NLP处理器
    nlp = NLPProcessor()
    
    # 模拟ESG报告文本
    sample_text = """
    贵州茅台酒股份有限公司（股票代码：600519）高度重视环境保护和社会责任。
    
    在碳排放方面，2024年公司温室气体排放总量为50,000吨CO2当量，较上年下降3%。
    公司已制定碳达峰、碳中和目标，计划于2030年实现碳达峰，2060年实现碳中和。
    
    在员工管理方面，公司现有员工总数30,000人，其中男性占55%，女性占45%。
    公司重视员工培训，年度培训投入达2,000万元，人均培训时长50小时。
    
    在公司治理方面，公司董事会已设立ESG委员会，负责统筹ESG相关工作。
    公司制定了反腐败政策和数据安全管理规定。
    
    公司积极响应国家乡村振兴战略，2024年投入5,000万元用于乡村扶贫项目。
    """
    
    # 执行合规检查
    print("\n执行ESG合规检查...")
    report = engine.check_compliance(
        document_text=sample_text,
        company_name="贵州茅台酒股份有限公司",
        market_type="主板",
        industry="食品饮料",
    )
    
    # NLP信息提取
    print("\n执行NLP信息提取...")
    extracted_info = nlp.extract_esg_info(sample_text)
    terms = nlp.identify_terms(sample_text)
    sentiment = nlp.analyze_sentiment(sample_text)
    
    # 输出结果
    print(f"\n合规检查结果:")
    print(f"  合规评分: {report.compliance_score}")
    print(f"  合规项: {report.compliant_items}")
    print(f"  部分合规: {report.partial_items}")
    print(f"  缺失项: {report.missing_items}")
    
    print(f"\nNLP提取结果:")
    for info in extracted_info:
        print(f"  [{info.category}-{info.subcategory}] {info.content}")
    
    print(f"\n识别的ESG术语:")
    for term in terms:
        print(f"  {term.term} ({term.category})")
    
    print(f"\n情感分析: {sentiment.sentiment} (得分: {sentiment.score})")
    
    return report, extracted_info


def main():
    """主函数"""
    print("A股数据集成示例")
    print("=" * 60)
    
    # 执行示例
    stock_info, financial = example_stock_data_integration()
    esg_data = example_esg_pipeline()
    comparison = example_industry_comparison()
    report, extracted = example_esg_compliance_with_data()
    
    print("\n" + "=" * 60)
    print("所有示例执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
