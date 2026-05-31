"""
A股中特估分析示例
展示精简后的核心功能
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import ROEAnalyzer, PolicyAnalyzer


def analyze_company(code: str, name: str, industry: str, disclosure_text: str):
    """分析单家公司"""
    
    print(f"\n{'='*60}")
    print(f"{name} ({code})")
    print(f"{'='*60}")
    
    # ROE分析
    roe_analyzer = ROEAnalyzer()
    roe_result = roe_analyzer.analyze(code, industry)
    
    print(f"\n【ROE分析】")
    print(f"  ROE: {roe_result.roe:.2f}% (行业平均: {roe_result.industry_avg:.2f}%)")
    print(f"  质量: {roe_result.quality.value} (得分: {roe_result.quality_score})")
    print(f"  百分位: {roe_result.percentile}%")
    print(f"  净利率: {roe_result.net_margin:.2f}% | 资产周转率: {roe_result.asset_turnover:.2f}")
    print(f"  优势: {', '.join(roe_result.strengths)}")
    print(f"  劣势: {', '.join(roe_result.weaknesses)}")
    print(f"  建议: {', '.join(roe_result.recommendations)}")
    
    # 政策匹配
    policy_analyzer = PolicyAnalyzer()
    policy_result = policy_analyzer.analyze(code, name, disclosure_text, industry)
    
    print(f"\n【政策匹配】")
    print(f"  总分: {policy_result.overall_score}")
    print(f"  匹配维度: {', '.join(policy_result.matched) or '无'}")
    print(f"  待提升: {', '.join(policy_result.unmatched)}")
    print(f"  建议: {', '.join(policy_result.recommendations)}")
    
    return roe_result, policy_result


def main():
    """主函数"""
    print("=" * 60)
    print("A股中特估分析框架 v2.1")
    print("=" * 60)
    
    # 电力行业公司
    companies = [
        {
            "code": "600886",
            "name": "国投电力",
            "industry": "电力",
            "disclosure": """
            国投电力积极推进国企改革，优化治理结构，提升经营效率。
            公司董事会设立ESG委员会，完善公司治理体系。
            ROE持续改善，现金分红比例达到30%以上，重视股东回报。
            大力发展清洁能源，风电、光伏装机容量持续增长，积极推进碳中和。
            研发投入强度达到2.5%，技术创新能力不断增强，拥有多项专利。
            公司高度重视环境保护，环保投入逐年增加，碳排放数据已披露。
            """,
        },
        {
            "code": "600863",
            "name": "华能蒙电",
            "industry": "电力",
            "disclosure": """
            华能蒙电积极响应国企改革政策，推进数字化转型和智能制造。
            公司制定了明确的碳达峰碳中和目标，清洁能源占比持续提升。
            资产负债率控制在合理水平，财务结构稳健。
            员工培训投入增加，人均培训时长达到40小时。
            安全生产管理体系完善，全年无重大安全事故。
            公司推进乡村振兴，参与扶贫项目。
            """,
        },
        {
            "code": "600011",
            "name": "华能国际",
            "industry": "电力",
            "disclosure": """
            华能国际是全国最大的上市发电公司之一，积极推进能源结构转型。
            清洁能源占比持续提升，风电、光伏等可再生能源装机快速增长。
            公司ROE保持稳定，盈利能力较强，重视股东回报和市值管理。
            公司治理结构完善，信息披露规范透明，获得多项治理奖项。
            研发投入持续增加，技术创新成果显著，拥有多项发明专利。
            公司高度重视环境保护，环保投入逐年增加。
            """,
        },
    ]
    
    results = []
    for company in companies:
        roe, policy = analyze_company(
            company["code"],
            company["name"],
            company["industry"],
            company["disclosure"],
        )
        results.append({
            "name": company["name"],
            "roe": roe,
            "policy": policy,
        })
    
    # 综合对比
    print(f"\n{'='*60}")
    print("综合对比")
    print(f"{'='*60}")
    
    print(f"\n{'公司':<10} {'ROE':<8} {'质量':<6} {'百分位':<8} {'政策分':<8}")
    print("-" * 45)
    
    for r in results:
        print(f"{r['name']:<10} {r['roe'].roe:<8.2f} {r['roe'].quality.value:<6} {r['roe'].percentile:<8} {r['policy'].overall_score:<8}")
    
    print(f"\n{'='*60}")
    print("分析完成!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
