"""
深度分析示例
展示ROE深度分析和政策匹配度分析
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import (
    ROEDeepAnalyzer,
    ChinaValuationDeepAnalyzer,
    AStockDataIntegrator,
)


def analyze_company(company_code: str, company_name: str, industry: str):
    """深度分析单家公司"""
    
    print(f"\n{'='*70}")
    print(f"深度分析: {company_name} ({company_code})")
    print(f"{'='*70}")
    
    # 获取真实数据
    integrator = AStockDataIntegrator()
    info = integrator.get_stock_info(company_code)
    financial = integrator.get_financial_data(company_code)
    
    if info:
        print(f"\n市场数据:")
        print(f"  市值: {info.market_cap:.2f}亿")
        print(f"  PE(TTM): {info.pe_ttm:.2f}")
        print(f"  PB: {info.pb:.2f}")
    
    # 模拟财务数据（基于市值和估值估算）
    market_cap = info.market_cap * 100000000 if info else 0
    pb = info.pb if info else 1.5
    pe = info.pe_ttm if info else 15
    
    equity = market_cap / pb if pb > 0 else market_cap * 0.6
    total_assets = equity * 1.8
    total_debt = total_assets * 0.45
    net_profit = market_cap / pe if pe > 0 else market_cap * 0.08
    
    # 1. ROE深度分析
    print(f"\n{'='*70}")
    print("ROE深度分析 (杜邦分析)")
    print(f"{'='*70}")
    
    roe_analyzer = ROEDeepAnalyzer()
    
    current_data = {
        "net_profit": net_profit,
        "revenue": net_profit * 4,
        "total_assets": total_assets,
        "equity": equity,
        "total_debt": total_debt,
        "gross_profit": net_profit * 1.5,
        "operating_profit": net_profit * 1.2,
        "interest_expense": total_debt * 0.05,
        "inventory": total_assets * 0.15,
        "receivables": net_profit * 0.5,
    }
    
    decomposition = roe_analyzer.analyze_roe(
        current_data=current_data,
        industry=industry,
        company_name=company_name,
    )
    
    print(f"\n核心指标:")
    print(f"  ROE: {decomposition.roe:.2f}%")
    print(f"  净利率: {decomposition.net_margin:.2f}%")
    print(f"  资产周转率: {decomposition.asset_turnover:.2f}")
    print(f"  权益乘数: {decomposition.equity_multiplier:.2f}")
    
    print(f"\nROE质量: {decomposition.quality.value} (得分: {decomposition.quality_score:.1f})")
    
    print(f"\n盈利能力因素:")
    for k, v in decomposition.profitability_factors.items():
        print(f"  {k}: {v:.2f}%")
    
    print(f"\n运营效率因素:")
    for k, v in decomposition.efficiency_factors.items():
        print(f"  {k}: {v:.2f}")
    
    print(f"\n杠杆因素:")
    for k, v in decomposition.leverage_factors.items():
        print(f"  {k}: {v:.2f}")
    
    print(f"\n优势:")
    for s in decomposition.strengths:
        print(f"  ✓ {s}")
    
    print(f"\n劣势:")
    for w in decomposition.weaknesses:
        print(f"  ✗ {w}")
    
    # 行业对标
    benchmark = roe_analyzer.benchmark_against_industry(decomposition.roe, industry)
    print(f"\n行业对标:")
    print(f"  行业平均ROE: {benchmark.industry_avg:.2f}%")
    print(f"  行业中位数: {benchmark.industry_median:.2f}%")
    print(f"  行业TOP10: {benchmark.industry_top10:.2f}%")
    print(f"  百分位排名: {benchmark.percentile}%")
    print(f"  差距分析: {benchmark.gap_analysis}")
    
    # 投资洞察
    insights = roe_analyzer.generate_investment_insights(decomposition, benchmark=benchmark)
    print(f"\n投资洞察:")
    print(f"  质量评估: {insights['quality_assessment']}")
    print(f"  可持续性: {insights['sustainability']}")
    print(f"  投资价值: {insights['investment_value']}")
    
    if insights['risk_factors']:
        print(f"  风险因素: {', '.join(insights['risk_factors'])}")
    
    if insights['catalysts']:
        print(f"  催化剂: {', '.join(insights['catalysts'])}")
    
    # 2. 政策匹配度分析
    print(f"\n{'='*70}")
    print("中特估政策匹配度分析")
    print(f"{'='*70}")
    
    # 模拟披露文本
    disclosure_text = f"""
    {company_name}积极推进国企改革，优化治理结构，提升经营效率。
    公司ROE持续改善，盈利能力稳步提升。
    公司高度重视股东回报，现金分红比例保持稳定。
    在绿色发展方面，公司积极推进碳减排，清洁能源占比持续提升。
    公司研发投入持续增加，技术创新能力不断增强。
    公司已建立完善的ESG治理体系。
    """
    
    policy_analyzer = ChinaValuationDeepAnalyzer()
    policy_result = policy_analyzer.analyze_policy_match(
        document_text=disclosure_text,
        industry=industry,
    )
    
    print(f"\n政策匹配总分: {policy_result.overall_score:.1f}")
    
    print(f"\n各维度得分:")
    for dim, score in policy_result.dimension_scores.items():
        status = "✓" if score > 30 else "✗"
        print(f"  {status} {dim}: {score:.1f}")
    
    print(f"\n匹配的维度: {', '.join(policy_result.matched_dimensions)}")
    print(f"未匹配的维度: {', '.join(policy_result.unmatched_dimensions)}")
    
    if policy_result.evidence:
        print(f"\n证据:")
        for dim, evi in policy_result.evidence.items():
            if evi:
                print(f"  {dim}:")
                for e in evi[:2]:
                    print(f"    - {e}")
    
    print(f"\n建议:")
    for rec in policy_result.recommendations:
        print(f"  • {rec}")
    
    return decomposition, benchmark, policy_result


def main():
    """主函数"""
    print("=" * 70)
    print("A股中特估深度分析报告")
    print("=" * 70)
    
    # 分析电力行业公司
    companies = [
        ("600886", "国投电力", "电力"),
        ("600863", "华能蒙电", "电力"),
        ("600011", "华能国际", "电力"),
    ]
    
    results = []
    for code, name, industry in companies:
        decomp, bench, policy = analyze_company(code, name, industry)
        results.append({
            "code": code,
            "name": name,
            "decomposition": decomp,
            "benchmark": bench,
            "policy": policy,
        })
    
    # 综合对比
    print(f"\n{'='*70}")
    print("综合对比")
    print(f"{'='*70}")
    
    print(f"\n{'公司':<12} {'ROE':<10} {'质量':<8} {'百分位':<10} {'政策匹配':<10}")
    print("-" * 55)
    
    for r in results:
        d = r['decomposition']
        b = r['benchmark']
        p = r['policy']
        print(f"{r['name']:<12} {d.roe:<10.2f} {d.quality.value:<8} {b.percentile:<10} {p.overall_score:<10.1f}")
    
    print(f"\n{'='*70}")
    print("分析完成!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
