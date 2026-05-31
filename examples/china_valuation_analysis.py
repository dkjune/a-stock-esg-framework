"""
中特估投资分析示例
分析电力行业国企的中特估投资价值
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import (
    ChinaValuationPolicyAnalyzer,
    ROEAnalyzer,
    OneFiveRatioAnalyzer,
    DisclosureQualityAnalyzer,
    PersonalInvestorScorer,
    StockFactorGenerator,
    InformationSource,
)


def analyze_china_valuation():
    """中特估投资分析"""
    
    print("=" * 70)
    print("A股中特估投资分析报告")
    print("=" * 70)
    
    # 目标公司（电力行业国企）
    companies = [
        {"code": "600886", "name": "国投电力", "is_soe": True},
        {"code": "600863", "name": "华能蒙电", "is_soe": True},
        {"code": "600011", "name": "华能国际", "is_soe": True},
    ]
    
    # 初始化分析器
    policy_analyzer = ChinaValuationPolicyAnalyzer()
    roe_analyzer = ROEAnalyzer()
    ratio_analyzer = OneFiveRatioAnalyzer()
    disclosure_analyzer = DisclosureQualityAnalyzer()
    scorer = PersonalInvestorScorer()
    factor_generator = StockFactorGenerator()
    
    # 模拟披露文本
    disclosure_texts = {
        "600886": """
        国投电力积极推进国企改革，优化治理结构，提升经营效率。
        公司ROE持续改善，2024年达到12.5%，同比提升1.2个百分点。
        公司高度重视股东回报，现金分红比例达到30%以上。
        在绿色发展方面，公司大力发展清洁能源，风电、光伏装机容量持续增长。
        公司研发投入强度达到2.5%，技术创新能力不断增强。
        """,
        "600863": """
        华能蒙电作为内蒙古地区重要的电力企业，积极响应国企改革政策。
        公司持续推进数字化转型，智能化水平不断提升。
        在碳减排方面，公司制定了明确的碳达峰碳中和目标。
        公司资产负债率控制在合理水平，财务结构稳健。
        """,
        "600011": """
        华能国际是全国最大的上市发电公司之一。
        公司积极推进能源结构转型，清洁能源占比持续提升。
        公司ROE保持稳定，盈利能力较强。
        公司治理结构完善，信息披露规范透明。
        """,
    }
    
    # 模拟财务数据
    financial_data = {
        "600886": {
            "current": {
                "net_profit": 500000,
                "revenue": 2000000,
                "equity": 4000000,
                "total_assets": 8000000,
                "total_debt": 4000000,
                "operating_cash_flow": 800000,
                "r&D_expense": 50000,
                "profit_total": 600000,
            },
            "previous": {
                "net_profit": 450000,
                "revenue": 1800000,
                "equity": 3800000,
                "total_assets": 7500000,
                "total_debt": 3700000,
            },
        },
        "600863": {
            "current": {
                "net_profit": 300000,
                "revenue": 1200000,
                "equity": 2500000,
                "total_assets": 5000000,
                "total_debt": 2500000,
                "operating_cash_flow": 500000,
                "r&D_expense": 30000,
                "profit_total": 350000,
            },
            "previous": {
                "net_profit": 280000,
                "revenue": 1100000,
                "equity": 2400000,
                "total_assets": 4800000,
                "total_debt": 2400000,
            },
        },
        "600011": {
            "current": {
                "net_profit": 800000,
                "revenue": 3000000,
                "equity": 6000000,
                "total_assets": 12000000,
                "total_debt": 6000000,
                "operating_cash_flow": 1200000,
                "r&D_expense": 80000,
                "profit_total": 900000,
            },
            "previous": {
                "net_profit": 750000,
                "revenue": 2800000,
                "equity": 5800000,
                "total_assets": 11500000,
                "total_debt": 5700000,
            },
        },
    }
    
    analysis_results = []
    
    for company in companies:
        print(f"\n{'='*70}")
        print(f"分析公司: {company['name']} ({company['code']})")
        print(f"{'='*70}")
        
        # 1. 政策匹配度分析
        print("\n[1] 中特估政策匹配度分析...")
        policy_result = policy_analyzer.analyze_policy_match(
            document_text=disclosure_texts.get(company['code'], ""),
            company_code=company['code'],
            company_name=company['name'],
            industry="公用事业",
            is_soe=company['is_soe'],
        )
        print(f"    政策匹配得分: {policy_result.overall_score:.2f}")
        print(f"    匹配政策数: {len(policy_result.matched_policies)}")
        if policy_result.recommendations:
            print(f"    建议: {policy_result.recommendations[0]}")
        
        # 2. ROE分析
        print("\n[2] ROE核心指标分析...")
        roe_result = roe_analyzer.analyze_roe(
            company_code=company['code'],
            company_name=company['name'],
            financial_data=financial_data.get(company['code'], {}),
            disclosure_text=disclosure_texts.get(company['code'], ""),
        )
        print(f"    当前ROE: {roe_result.current_roe:.2f}%")
        print(f"    ROE变动: {roe_result.roe_change:+.2f}%")
        print(f"    可持续性得分: {roe_result.sustainability_score:.2f}")
        if roe_result.main_drivers:
            print(f"    主要驱动: {roe_result.main_drivers[0]}")
        
        # 3. 一利五率分析
        print("\n[3] 一利五率分析...")
        ratio_result = ratio_analyzer.analyze(
            company_code=company['code'],
            company_name=company['name'],
            financial_data=financial_data.get(company['code'], {}).get("current", {}),
        )
        print(f"    ROE: {ratio_result.roe:.2f}%")
        print(f"    ROA: {ratio_result.roa:.2f}%")
        print(f"    资产负债率: {ratio_result.debt_ratio:.2f}%")
        print(f"    综合得分: {ratio_result.overall_score:.2f}")
        
        # 4. 披露质量分析
        print("\n[4] 披露质量分析...")
        sources = [
            InformationSource(
                source_id="annual_report",
                source_type="年报",
                content=disclosure_texts.get(company['code'], ""),
                date="2024-04-30",
            ),
        ]
        disclosure_result = disclosure_analyzer.analyze_disclosure_quality(
            company_code=company['code'],
            company_name=company['name'],
            sources=sources,
        )
        print(f"    披露质量得分: {disclosure_result.overall_score:.2f}")
        print(f"    信息完整性: {disclosure_result.information_completeness:.2f}%")
        print(f"    一致性得分: {disclosure_result.consistency_score:.2f}")
        print(f"    话术标记数: {len(disclosure_result.rhetoric_flags)}")
        
        # 5. 综合评分
        analysis_data = {
            "policy_match_score": policy_result.overall_score,
            "disclosure_quality_score": disclosure_result.overall_score,
            "roe_score": roe_result.sustainability_score,
            "governance_score": ratio_result.overall_score,
            "risk_score": 100 - disclosure_result.consistency_score,
        }
        
        stock_score = scorer.score_stock(
            stock_code=company['code'],
            stock_name=company['name'],
            analysis_data=analysis_data,
        )
        
        print(f"\n[5] 综合评分:")
        print(f"    总分: {stock_score.overall_score:.2f}")
        print(f"    等级: {stock_score.rank}")
        print(f"    风险: {stock_score.risk_level}")
        print(f"    建议: {stock_score.recommendation}")
        
        analysis_results.append({
            "company": company,
            "policy_result": policy_result,
            "roe_result": roe_result,
            "ratio_result": ratio_result,
            "disclosure_result": disclosure_result,
            "stock_score": stock_score,
        })
    
    # 行业对比
    print(f"\n{'='*70}")
    print("行业对比分析")
    print(f"{'='*70}")
    
    print(f"\n{'公司名称':<12} {'总分':<10} {'等级':<8} {'ROE':<10} {'政策匹配':<10} {'建议'}")
    print("-" * 80)
    
    for r in analysis_results:
        print(f"{r['company']['name']:<12} "
              f"{r['stock_score'].overall_score:<10.2f} "
              f"{r['stock_score'].rank:<8} "
              f"{r['roe_result'].current_roe:<10.2f} "
              f"{r['policy_result'].overall_score:<10.2f} "
              f"{r['stock_score'].recommendation[:20]}")
    
    # 生成选股因子
    print(f"\n{'='*70}")
    print("选股因子生成")
    print(f"{'='*70}")
    
    stock_scores = [r['stock_score'] for r in analysis_results]
    factors = factor_generator.generate_factors(stock_scores)
    
    print(f"\n{'股票代码':<10} {'政策因子':<10} {'披露因子':<10} {'ROE因子':<10} {'综合因子'}")
    print("-" * 60)
    
    for f in factors:
        print(f"{f['stock_code']:<10} "
              f"{f['policy_match_factor']:<10.4f} "
              f"{f['disclosure_quality_factor']:<10.4f} "
              f"{f['roe_sustainability_factor']:<10.4f} "
              f"{f['composite_factor']:.4f}")
    
    # 投资建议
    print(f"\n{'='*70}")
    print("投资建议")
    print(f"{'='*70}")
    
    # 按得分排序
    analysis_results.sort(key=lambda x: x['stock_score'].overall_score, reverse=True)
    
    print(f"\n1. 推荐投资标的:")
    for i, r in enumerate(analysis_results[:2], 1):
        print(f"   {i}. {r['company']['name']} ({r['company']['code']}) - {r['stock_score'].recommendation}")
    
    print(f"\n2. 关键投资逻辑:")
    print(f"   - 政策匹配度高的标的更符合中特估方向")
    print(f"   - ROE持续改善的标的具有价值重估潜力")
    print(f"   - 披露质量高的标的信息透明度更好")
    
    print(f"\n3. 风险提示:")
    print(f"   - 本分析仅供参考，不构成投资建议")
    print(f"   - 投资有风险，入市需谨慎")
    print(f"   - 建议结合基本面、技术面综合判断")
    
    print(f"\n{'='*70}")
    print("分析完成!")
    print(f"{'='*70}")


if __name__ == "__main__":
    analyze_china_valuation()
