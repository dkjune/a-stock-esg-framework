"""
A股电力行业ESG分析
分析国投电力、华能蒙电、华能国际三家公司
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
    BenchmarkAnalyzer,
    DataCollector,
)
from a_stock_esg.core.config import MarketType, IndustryClassification
from a_stock_esg.data.collector import CompanyInfo


def analyze_electricity_companies():
    """分析电力行业公司"""
    
    print("=" * 70)
    print("A股电力行业ESG分析报告")
    print("=" * 70)
    
    # 目标公司
    companies = [
        {"code": "600886", "name": "国投电力"},
        {"code": "600863", "name": "华能蒙电"},
        {"code": "600011", "name": "华能国际"},
    ]
    
    # 初始化组件
    integrator = AStockDataIntegrator()
    pipeline = ESGDataPipeline()
    config = AStockESGConfig(
        market_type=MarketType.MAIN_BOARD,
        industry=IndustryClassification.UTILITIES,
    )
    compliance_engine = ComplianceEngine(config)
    nlp = NLPProcessor()
    
    results = []
    
    for company in companies:
        print(f"\n{'='*70}")
        print(f"分析公司: {company['name']} ({company['code']})")
        print(f"{'='*70}")
        
        # 1. 获取股票基础信息
        print("\n[1] 获取股票基础信息...")
        stock_info = integrator.get_stock_info(company['code'])
        if stock_info:
            print(f"    股票名称: {stock_info.stock_name}")
            print(f"    所属行业: {stock_info.industry}")
            print(f"    市场类型: {stock_info.market_type}")
            print(f"    总市值: {stock_info.market_cap:.2f} 亿")
        else:
            print("    获取失败，使用默认信息")
            stock_info = None
        
        # 2. 获取财务数据
        print("\n[2] 获取财务数据...")
        financial = integrator.get_financial_data(company['code'])
        if financial:
            print(f"    PE(TTM): {financial.pe_ttm:.2f}")
            print(f"    PB: {financial.pb:.2f}")
            print(f"    总市值: {financial.market_cap:.2f} 亿")
        else:
            print("    获取失败")
            financial = None
        
        # 3. 模拟ESG报告内容进行合规检查
        print("\n[3] 执行ESG合规检查...")
        
        # 模拟ESG报告文本（电力行业特色）
        esg_text = f"""
        {company['name']}高度重视环境保护和社会责任。
        
        在碳排放方面，公司作为电力企业，2024年温室气体排放总量较高，
        主要来自火力发电。公司已制定碳减排目标，计划通过增加清洁能源
        占比、提高发电效率等措施降低碳排放强度。
        
        在能源管理方面，公司积极推进能源结构转型，风电、光伏等可再生
        能源装机容量持续增长。2024年清洁能源发电占比达到30%以上。
        
        在员工管理方面，公司现有员工总数约5000人，重视员工培训和
        职业发展，建立了完善的薪酬福利体系。
        
        在公司治理方面，公司董事会已设立ESG委员会，制定了安全生产
        管理制度和商业道德准则。
        """
        
        try:
            report = compliance_engine.check_compliance(
                document_text=esg_text,
                company_name=company['name'],
                market_type="主板",
                industry="公用事业",
            )
            
            print(f"    合规评分: {report.compliance_score:.2f}")
            print(f"    总检查项: {report.total_items}")
            print(f"    合规项: {report.compliant_items}")
            print(f"    部分合规: {report.partial_items}")
            print(f"    缺失项: {report.missing_items}")
        except Exception as e:
            print(f"    合规检查出错: {e}")
            report = None
        
        # 4. NLP信息提取
        print("\n[4] NLP信息提取...")
        try:
            extracted_info = nlp.extract_esg_info(esg_text)
            print(f"    提取到 {len(extracted_info)} 项ESG信息")
            for info in extracted_info[:3]:  # 只显示前3项
                print(f"      - [{info.category}-{info.subcategory}] {info.content[:50]}...")
        except Exception as e:
            print(f"    NLP提取出错: {e}")
            extracted_info = []
        
        # 5. 情感分析
        print("\n[5] 情感分析...")
        try:
            sentiment = nlp.analyze_sentiment(esg_text)
            print(f"    情感倾向: {sentiment.sentiment}")
            print(f"    情感得分: {sentiment.score:.2f}")
        except Exception as e:
            print(f"    情感分析出错: {e}")
            sentiment = None
        
        # 保存结果
        results.append({
            "company": company,
            "stock_info": stock_info,
            "financial": financial,
            "compliance_report": report,
            "sentiment": sentiment,
        })
    
    # 6. 行业对比分析
    print(f"\n{'='*70}")
    print("行业对比分析")
    print(f"{'='*70}")
    
    # 创建数据收集器和对标分析器
    data_collector = DataCollector()
    for r in results:
        if r['stock_info']:
            company_info = CompanyInfo(
                stock_code=r['company']['code'],
                company_name=r['company']['name'],
                market_type="主板",
                industry="公用事业",
            )
            data_collector.add_company(company_info)
    
    benchmark_analyzer = BenchmarkAnalyzer(data_collector)
    
    # 对比分析
    print("\n财务指标对比:")
    print("-" * 60)
    print(f"{'公司名称':<12} {'股票代码':<10} {'PE(TTM)':<10} {'PB':<10} {'总市值(亿)':<12}")
    print("-" * 60)
    
    for r in results:
        pe = r['financial'].pe_ttm if r['financial'] else 0
        pb = r['financial'].pb if r['financial'] else 0
        market_cap = r['financial'].market_cap if r['financial'] else 0
        print(f"{r['company']['name']:<12} {r['company']['code']:<10} {pe:<10.2f} {pb:<10.2f} {market_cap:<12.2f}")
    
    print("\nESG合规对比:")
    print("-" * 60)
    print(f"{'公司名称':<12} {'合规评分':<10} {'合规项':<10} {'缺失项':<10}")
    print("-" * 60)
    
    for r in results:
        if r['compliance_report']:
            report = r['compliance_report']
            print(f"{r['company']['name']:<12} {report.compliance_score:<10.2f} {report.compliant_items:<10} {report.missing_items:<10}")
        else:
            print(f"{r['company']['name']:<12} {'N/A':<10} {'N/A':<10} {'N/A':<10}")
    
    # 7. 生成差异化建议
    print(f"\n{'='*70}")
    print("差异化建议")
    print(f"{'='*70}")
    
    for r in results:
        print(f"\n{r['company']['name']}:")
        
        if r['compliance_report']:
            missing = r['compliance_report'].missing_items
            if missing > 3:
                print(f"  - 建议重点补充ESG披露内容，当前缺失{missing}项")
            elif missing > 0:
                print(f"  - 建议完善ESG信息披露，当前缺失{missing}项")
            else:
                print(f"  - ESG披露较为完善")
        
        # 电力行业特定建议
        print(f"  - 作为电力企业，建议重点披露碳排放数据和清洁能源转型进展")
        print(f"  - 建议披露Scope 1和Scope 2温室气体排放数据")
        print(f"  - 建议披露可再生能源装机容量和发电占比")
    
    # 8. 保存HTML报告
    print(f"\n{'='*70}")
    print("生成可视化报告...")
    print(f"{'='*70}")
    
    try:
        from a_stock_esg import Visualizer
        visualizer = Visualizer()
        
        # 为第一家公司生成示例报告
        if results[0]['compliance_report']:
            output_path = "electricity_esg_dashboard.html"
            visualizer.create_compliance_dashboard(
                results[0]['compliance_report'],
                output_path
            )
            print(f"可视化报告已生成: {output_path}")
    except Exception as e:
        print(f"生成报告出错: {e}")
    
    print(f"\n{'='*70}")
    print("分析完成!")
    print(f"{'='*70}")


if __name__ == "__main__":
    analyze_electricity_companies()
