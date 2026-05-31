"""
A股中特估分析示例（前景理论优化版）
展示优化后的分析结果
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import ROEAnalyzer, PolicyAnalyzer, stock_data


def analyze_company(code: str, name: str, industry: str, disclosure_text: str):
    """分析单家公司（前景理论优化版）"""
    
    print(f"\n{'='*70}")
    print(f"  {name} ({code})")
    print(f"{'='*70}")
    
    # 获取估值锚点
    valuation = stock_data.get_valuation_anchor(code, industry)
    
    # ROE分析
    roe_analyzer = ROEAnalyzer()
    roe_result = roe_analyzer.analyze(code, industry)
    
    # 政策匹配
    policy_analyzer = PolicyAnalyzer()
    policy_result = policy_analyzer.analyze(code, name, disclosure_text, industry)
    
    # 输出格式（前景理论优化）
    print(f"\n【核心数据】")
    print(f"  ROE: {roe_result['roe']:.2f}% | 质量评级: {roe_result['quality']} | ROE稳定性: {roe_result['roe_volatility']:.1f}%波动率 {roe_result['stability_tag']}")
    
    if valuation:
        print(f"  当前PE: {valuation.current_pe:.1f} | 行业中枢PE: {valuation.industry_median_pe:.1f} | 估值偏离: {valuation.pe_deviation:+.1f}% {valuation.valuation_tag}")
    
    # 杠杆风险提示（损失厌恶）
    print(f"\n【风险提示】")
    print(f"  {roe_result['leverage_risk_detail']}")
    if valuation:
        print(f"  {valuation.risk_disclosure}")
    
    # 政策匹配
    print(f"\n【政策匹配】")
    print(f"  总匹配分: {policy_result.overall_score:.1f}/100 → {policy_result.opportunity_type}")
    print(f"  {policy_result.opportunity_detail}")
    
    if policy_result.matched:
        print(f"  核心匹配维度: {', '.join(policy_result.matched[:3])}")
    
    if policy_result.negative_signals:
        print(f"  ⚠️ 负面信号: {', '.join(policy_result.negative_signals[:2])}")
    
    if policy_result.positive_actions:
        print(f"  ✅ 正面行动: {', '.join(policy_result.positive_actions[:2])}")
    
    # 估值修复空间（概率化表达）
    print(f"\n【估值修复空间】")
    print(f"  当前ROE位于{roe_result['industry_avg']:.1f}%行业均值的{roe_result['percentile']}%分位")
    print(f"  {roe_result['recovery_probability']:.0f}%概率存在估值修复空间")
    
    if valuation and valuation.valuation_tag == "低估锚点":
        potential = abs(valuation.pe_deviation) * 0.8
        print(f"  若估值修复至行业中枢，潜在收益约{potential:.1f}%")
    
    return roe_result, policy_result, valuation


def main():
    """主函数"""
    print("=" * 70)
    print("  A股中特估分析框架 v3.0（前景理论优化版）")
    print("=" * 70)
    
    # 电力行业公司
    companies = [
        {
            "code": "600886",
            "name": "国投电力",
            "industry": "电力",
            "disclosure": "公司积极推进国企改革，优化治理结构。ROE持续改善，现金分红比例30%以上。大力发展清洁能源，风电光伏装机增长。研发投入增加，技术创新能力增强。推进数字化转型。"
        },
        {
            "code": "600863",
            "name": "华能蒙电",
            "industry": "电力",
            "disclosure": "公司积极响应国企改革政策，推进数字化转型。制定碳达峰碳中和目标。资产负债率控制合理。员工培训投入增加，安全生产管理完善。"
        },
        {
            "code": "600011",
            "name": "华能国际",
            "industry": "电力",
            "disclosure": "全国最大上市发电公司之一。推进能源结构转型，清洁能源占比提升。ROE保持稳定。治理结构完善，信息披露规范。"
        },
        {
            "code": "600900",
            "name": "长江电力",
            "industry": "电力",
            "disclosure": "全球最大水电上市公司。积极推进国企改革，完善公司治理。ROE稳定在15%以上，分红比例高，重视股东回报。清洁能源占比100%。"
        },
    ]
    
    results = []
    for company in companies:
        roe, policy, valuation = analyze_company(
            company["code"],
            company["name"],
            company["industry"],
            company["disclosure"],
        )
        results.append({
            "name": company["name"],
            "roe": roe,
            "policy": policy,
            "valuation": valuation,
        })
    
    # 综合对比
    print(f"\n{'='*70}")
    print("  综合对比")
    print(f"{'='*70}")
    
    print(f"\n{'公司':<10} {'ROE':<8} {'质量':<6} {'稳定性':<10} {'估值偏离':<10} {'政策分':<8} {'机会类型'}")
    print("-" * 75)
    
    for r in sorted(results, key=lambda x: x['roe']['roe'], reverse=True):
        roe = r['roe']
        policy = r['policy']
        valuation = r['valuation']
        
        dev_str = f"{valuation.pe_deviation:+.1f}%" if valuation else "N/A"
        print(f"{r['name']:<10} {roe['roe']:<8.1f} {roe['quality']:<6} {roe['stability_tag']:<10} {dev_str:<10} {policy.overall_score:<8.1f} {policy.opportunity_type}")
    
    # 投资建议
    print(f"\n{'='*70}")
    print("  投资建议（前景理论优化）")
    print(f"{'='*70}")
    
    # 按机会类型分组
    for opp_type in ["确定性价值机会", "主题性交易机会", "低匹配机会"]:
        opp_companies = [r for r in results if r['policy'].opportunity_type == opp_type]
        if opp_companies:
            print(f"\n{opp_type}:")
            for r in opp_companies:
                print(f"  - {r['name']}: {r['policy'].opportunity_detail}")
    
    print(f"\n{'='*70}")
    print("  分析完成!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
