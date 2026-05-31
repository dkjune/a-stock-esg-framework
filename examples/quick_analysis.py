"""
A股分析示例（噪声优化版）
展示基于《噪声》理论的分析结果
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import ROEAnalyzer, PolicyAnalyzer, NoiseReportGenerator, stock_data


def analyze_company(code: str, name: str, industry: str, disclosure_text: str):
    """分析单家公司（噪声优化版）"""
    
    print(f"\n{'='*70}")
    print(f"  {name} ({code})")
    print(f"{'='*70}")
    
    # ROE分析
    roe_analyzer = ROEAnalyzer()
    roe_result = roe_analyzer.analyze(code, industry)
    roe_result["name"] = name
    
    # 政策匹配
    policy_analyzer = PolicyAnalyzer()
    policy_result = policy_analyzer.analyze(code, name, disclosure_text, industry)
    
    # 噪声报告
    noise_gen = NoiseReportGenerator()
    noise_report = noise_gen.generate(roe_result, policy_result)
    
    # 输出格式（噪声优化版）
    print(f"\n【ROE分析】")
    print(f"  评分: {roe_result['roe']:.2f}% (趋势: {roe_result['roe_trend']:.2f}%)")
    print(f"  质量分级: {roe_result['quality']} - {roe_result['quality_ci']}")
    print(f"  稳定性: {roe_result['stability_tag']} (波动率: {roe_result['roe_volatility']:.1f}%)")
    print(f"  数据质量: {roe_result['data_quality']} ({roe_result['confidence_note']})")
    
    print(f"\n【政策匹配】")
    print(f"  综合得分: {policy_result.overall_score:.1f}/100")
    print(f"  模型A: {policy_result.model_a_score:.1f} | 模型B: {policy_result.model_b_score:.1f}")
    print(f"  模型一致性: {policy_result.model_agreement:.1f}%")
    print(f"  置信度: {policy_result.confidence}")
    print(f"  机会类型: {policy_result.opportunity_type}")
    
    if policy_result.negative_signals:
        print(f"  ⚠️ 负面信号: {', '.join(policy_result.negative_signals[:2])}")
    
    if policy_result.positive_actions:
        print(f"  ✅ 正面行动: {', '.join(policy_result.positive_actions[:2])}")
    
    # 噪声报告
    print(f"\n【噪声评估】")
    print(f"  整体噪声水平: {noise_report.overall_noise_level}")
    print(f"  综合置信度: {noise_report.overall_confidence}")
    print(f"  建议: {noise_report.recommendation}")
    
    if noise_report.risk_warnings:
        print(f"  风险警告:")
        for w in noise_report.risk_warnings[:2]:
            print(f"    {w}")
    
    return roe_result, policy_result, noise_report


def main():
    """主函数"""
    print("=" * 70)
    print("  A股分析框架 v4.0（噪声优化版）")
    print("  基于《噪声》理论（丹尼尔·卡尼曼）")
    print("=" * 70)
    
    # 电力行业公司
    companies = [
        {
            "code": "600886",
            "name": "国投电力",
            "industry": "电力",
            "disclosure": "公司积极推进国企改革，优化治理结构。ROE持续改善，现金分红比例30%以上。大力发展清洁能源，风电光伏装机增长。研发投入增加，技术创新能力增强。"
        },
        {
            "code": "600011",
            "name": "华能国际",
            "industry": "电力",
            "disclosure": "全国最大上市发电公司之一。推进能源结构转型，清洁能源占比提升。ROE保持稳定，盈利能力较强。"
        },
        {
            "code": "600900",
            "name": "长江电力",
            "industry": "电力",
            "disclosure": "全球最大水电上市公司。积极推进国企改革，完善公司治理。ROE稳定在15%以上，分红比例高。"
        },
    ]
    
    results = []
    for company in companies:
        roe, policy, noise = analyze_company(
            company["code"],
            company["name"],
            company["industry"],
            company["disclosure"],
        )
        results.append({
            "name": company["name"],
            "roe": roe,
            "policy": policy,
            "noise": noise,
        })
    
    # 综合对比
    print(f"\n{'='*70}")
    print("  综合对比")
    print(f"{'='*70}")
    
    print(f"\n{'公司':<10} {'ROE':<8} {'质量':<6} {'稳定性':<10} {'政策分':<8} {'噪声':<6} {'置信度'}")
    print("-" * 70)
    
    for r in sorted(results, key=lambda x: x['roe']['roe'], reverse=True):
        roe = r['roe']
        policy = r['policy']
        noise = r['noise']
        
        print(f"{r['name']:<10} {roe['roe']:<8.1f} {roe['quality']:<6} {roe['stability_tag']:<10} {policy.overall_score:<8.1f} {noise.overall_noise_level:<6} {noise.overall_confidence}")
    
    # 决策建议
    print(f"\n{'='*70}")
    print("  决策建议（基于《噪声》理论）")
    print(f"{'='*70}")
    
    for r in results:
        noise = r['noise']
        print(f"\n{r['name']}:")
        print(f"  {noise.recommendation}")
    
    print(f"\n{'='*70}")
    print("  分析完成!")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
