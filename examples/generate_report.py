"""
电力行业ESG+中特估分析报告生成器
输出HTML格式的完整分析报告
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import (
    AStockESGConfig,
    ComplianceEngine,
    ChinaValuationPolicyAnalyzer,
    ROEAnalyzer,
    OneFiveRatioAnalyzer,
    DisclosureQualityAnalyzer,
    PersonalInvestorScorer,
    InformationSource,
)
from a_stock_esg.core.config import MarketType, IndustryClassification


def generate_html_report():
    """生成HTML格式的分析报告"""
    
    # 目标公司
    companies = [
        {"code": "600886", "name": "国投电力", "is_soe": True},
        {"code": "600863", "name": "华能蒙电", "is_soe": True},
        {"code": "600011", "name": "华能国际", "is_soe": True},
    ]
    
    # 初始化分析器
    config = AStockESGConfig(
        market_type=MarketType.MAIN_BOARD,
        industry=IndustryClassification.UTILITIES,
    )
    compliance_engine = ComplianceEngine(config)
    policy_analyzer = ChinaValuationPolicyAnalyzer()
    roe_analyzer = ROEAnalyzer()
    ratio_analyzer = OneFiveRatioAnalyzer()
    disclosure_analyzer = DisclosureQualityAnalyzer()
    scorer = PersonalInvestorScorer()
    
    # 模拟披露文本
    disclosure_texts = {
        "600886": """
        国投电力积极推进国企改革，优化治理结构，提升经营效率。
        公司ROE持续改善，2024年达到12.5%，同比提升1.2个百分点。
        公司高度重视股东回报，现金分红比例达到30%以上。
        在绿色发展方面，公司大力发展清洁能源，风电、光伏装机容量持续增长。
        公司研发投入强度达到2.5%，技术创新能力不断增强。
        公司已建立完善的ESG治理体系，董事会设立ESG委员会。
        碳排放数据已披露，2024年温室气体排放总量为50万吨CO2当量。
        """,
        "600863": """
        华能蒙电作为内蒙古地区重要的电力企业，积极响应国企改革政策。
        公司持续推进数字化转型，智能化水平不断提升。
        在碳减排方面，公司制定了明确的碳达峰碳中和目标。
        公司资产负债率控制在合理水平，财务结构稳健。
        公司员工培训投入增加，人均培训时长达到40小时。
        安全生产管理体系完善，全年无重大安全事故。
        """,
        "600011": """
        华能国际是全国最大的上市发电公司之一。
        公司积极推进能源结构转型，清洁能源占比持续提升。
        公司ROE保持稳定，盈利能力较强。
        公司治理结构完善，信息披露规范透明。
        公司研发投入持续增加，技术创新成果显著。
        公司高度重视环境保护，环保投入逐年增加。
        """,
    }
    
    # 模拟财务数据（每家公司数据不同）
    financial_data = {
        "600886": {
            "current": {
                "net_profit": 500000,
                "revenue": 2000000,
                "equity": 4000000,
                "total_assets": 8000000,
                "total_debt": 3600000,  # 负债率45%
                "operating_cash_flow": 800000,
                "rd_expense": 50000,
                "profit_total": 600000,
            },
            "previous": {
                "net_profit": 450000,
                "revenue": 1800000,
                "equity": 3800000,
                "total_assets": 7500000,
                "total_debt": 3500000,
            },
        },
        "600863": {
            "current": {
                "net_profit": 300000,
                "revenue": 1200000,
                "equity": 2500000,
                "total_assets": 5000000,
                "total_debt": 3250000,  # 负债率65%
                "operating_cash_flow": 500000,
                "rd_expense": 30000,
                "profit_total": 350000,
            },
            "previous": {
                "net_profit": 280000,
                "revenue": 1100000,
                "equity": 2400000,
                "total_assets": 4800000,
                "total_debt": 3100000,
            },
        },
        "600011": {
            "current": {
                "net_profit": 800000,
                "revenue": 3000000,
                "equity": 6000000,
                "total_assets": 12000000,
                "total_debt": 7800000,  # 负债率65%
                "operating_cash_flow": 1200000,
                "rd_expense": 80000,
                "profit_total": 900000,
            },
            "previous": {
                "net_profit": 750000,
                "revenue": 2800000,
                "equity": 5800000,
                "total_assets": 11500000,
                "total_debt": 7500000,
            },
        },
    }
    
    # 分析所有公司
    results = []
    
    for company in companies:
        code = company['code']
        name = company['name']
        
        # 合规检查
        compliance_report = compliance_engine.check_compliance(
            document_text=disclosure_texts.get(code, ""),
            company_name=name,
            market_type="主板",
            industry="公用事业",
        )
        
        # 政策匹配度分析
        policy_result = policy_analyzer.analyze_policy_match(
            document_text=disclosure_texts.get(code, ""),
            company_code=code,
            company_name=name,
            industry="公用事业",
            is_soe=company['is_soe'],
        )
        
        # ROE分析
        roe_result = roe_analyzer.analyze_roe(
            company_code=code,
            company_name=name,
            financial_data=financial_data.get(code, {}),
            disclosure_text=disclosure_texts.get(code, ""),
        )
        
        # 一利五率分析
        ratio_result = ratio_analyzer.analyze(
            company_code=code,
            company_name=name,
            financial_data=financial_data.get(code, {}).get("current", {}),
        )
        
        # 披露质量分析
        sources = [
            InformationSource(
                source_id="annual_report",
                source_type="年报",
                content=disclosure_texts.get(code, ""),
                date="2024-04-30",
            ),
        ]
        disclosure_result = disclosure_analyzer.analyze_disclosure_quality(
            company_code=code,
            company_name=name,
            sources=sources,
        )
        
        # 综合评分
        analysis_data = {
            "policy_match_score": policy_result.overall_score,
            "disclosure_quality_score": disclosure_result.overall_score,
            "roe_score": roe_result.sustainability_score,
            "governance_score": ratio_result.overall_score,
            "risk_score": 100 - disclosure_result.consistency_score,
        }
        
        stock_score = scorer.score_stock(
            stock_code=code,
            stock_name=name,
            analysis_data=analysis_data,
        )
        
        results.append({
            "company": company,
            "compliance": compliance_report,
            "policy": policy_result,
            "roe": roe_result,
            "ratio": ratio_result,
            "disclosure": disclosure_result,
            "score": stock_score,
        })
    
    # 生成HTML报告
    html = generate_html_content(results)
    
    # 保存文件
    output_path = Path(__file__).parent.parent / "electricity_esg_report.html"
    output_path.write_text(html, encoding="utf-8")
    
    print(f"报告已生成: {output_path}")
    return output_path


def generate_html_content(results):
    """生成HTML内容"""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 计算排名
    results_sorted = sorted(results, key=lambda x: x['score'].overall_score, reverse=True)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A股电力行业ESG+中特估分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        
        .header {{ background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header .subtitle {{ opacity: 0.9; font-size: 14px; }}
        .header .meta {{ margin-top: 15px; font-size: 12px; opacity: 0.8; }}
        
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); text-align: center; }}
        .summary-card .value {{ font-size: 32px; font-weight: bold; color: #2c5282; }}
        .summary-card .label {{ color: #666; margin-top: 5px; font-size: 14px; }}
        
        .section {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin-bottom: 25px; }}
        .section-title {{ font-size: 20px; font-weight: 600; color: #1a365d; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #e2e8f0; }}
        
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background: #f8fafc; font-weight: 600; color: #4a5568; }}
        tr:hover {{ background: #f7fafc; }}
        
        .rank {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 14px; }}
        .rank-aaa {{ background: #c6f6d5; color: #22543d; }}
        .rank-aa {{ background: #bee3f8; color: #2a4365; }}
        .rank-a {{ background: #e9d8fd; color: #44337a; }}
        .rank-bbb {{ background: #fefcbf; color: #744210; }}
        .rank-bb {{ background: #fed7d7; color: #742a2a; }}
        
        .score-bar {{ height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; }}
        .score-fill {{ height: 100%; background: linear-gradient(90deg, #48bb78, #38a169); transition: width 0.3s; }}
        
        .company-card {{ background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin-bottom: 20px; overflow: hidden; }}
        .company-header {{ background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%); color: white; padding: 20px; }}
        .company-header h3 {{ font-size: 18px; margin-bottom: 5px; }}
        .company-body {{ padding: 20px; }}
        
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .metric {{ text-align: center; padding: 15px; background: #f8fafc; border-radius: 8px; }}
        .metric .value {{ font-size: 24px; font-weight: bold; color: #2c5282; }}
        .metric .label {{ font-size: 12px; color: #666; margin-top: 5px; }}
        
        .insights {{ margin-top: 20px; }}
        .insight-item {{ display: flex; align-items: flex-start; margin-bottom: 10px; padding: 10px; background: #f7fafc; border-radius: 6px; border-left: 3px solid #4299e1; }}
        .insight-icon {{ margin-right: 10px; font-size: 16px; }}
        
        .risk-flag {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px; }}
        .risk-low {{ background: #c6f6d5; color: #22543d; }}
        .risk-medium {{ background: #fefcbf; color: #744210; }}
        .risk-high {{ background: #fed7d7; color: #742a2a; }}
        
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        
        .recommendation {{ padding: 15px; border-radius: 8px; margin-top: 15px; }}
        .rec-buy {{ background: #c6f6d5; border: 1px solid #9ae6b4; }}
        .rec-hold {{ background: #bee3f8; border: 1px solid #90cdf4; }}
        .rec-caution {{ background: #fefcbf; border: 1px solid #f6e05e; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>A股电力行业ESG+中特估分析报告</h1>
            <div class="subtitle">基于中国特色估值体系的投资价值分析</div>
            <div class="meta">
                生成时间: {now} | 分析框架: A股ESG分析框架 v2.0 | 数据来源: 公开披露信息
            </div>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="value">{len(results)}</div>
                <div class="label">分析公司数</div>
            </div>
            <div class="summary-card">
                <div class="value">{sum(r['score'].overall_score for r in results) / len(results):.1f}</div>
                <div class="label">平均综合得分</div>
            </div>
            <div class="summary-card">
                <div class="value">{results_sorted[0]['score'].rank}</div>
                <div class="label">最高评级</div>
            </div>
            <div class="summary-card">
                <div class="value">{sum(1 for r in results if r['roe'].roe_change > 0)}</div>
                <div class="label">ROE提升公司</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">综合排名</div>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>公司</th>
                        <th>股票代码</th>
                        <th>综合得分</th>
                        <th>等级</th>
                        <th>ROE</th>
                        <th>政策匹配</th>
                        <th>建议</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for i, r in enumerate(results_sorted, 1):
        rank_class = f"rank-{r['score'].rank.lower().replace('+', '')}"
        rec_class = "rec-buy" if "推荐" in r['score'].recommendation else ("rec-hold" if "中性" in r['score'].recommendation else "rec-caution")
        
        html += f"""
                    <tr>
                        <td><strong>{i}</strong></td>
                        <td><strong>{r['company']['name']}</strong></td>
                        <td>{r['company']['code']}</td>
                        <td>
                            <div>{r['score'].overall_score:.2f}</div>
                            <div class="score-bar"><div class="score-fill" style="width: {r['score'].overall_score}%"></div></div>
                        </td>
                        <td><span class="rank {rank_class}">{r['score'].rank}</span></td>
                        <td>{r['roe'].current_roe:.2f}%</td>
                        <td>{r['policy'].overall_score:.2f}</td>
                        <td><span class="{rec_class}" style="padding: 5px 10px; border-radius: 5px; font-size: 12px;">{r['score'].recommendation[:15]}...</span></td>
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
"""
    
    # 每家公司的详细分析
    for r in results:
        company = r['company']
        score = r['score']
        policy = r['policy']
        roe = r['roe']
        ratio = r['ratio']
        disclosure = r['disclosure']
        compliance = r['compliance']
        
        html += f"""
        <div class="company-card">
            <div class="company-header">
                <h3>{company['name']} ({company['code']})</h3>
                <div>综合得分: {score.overall_score:.2f} | 等级: {score.rank} | {score.risk_level}</div>
            </div>
            <div class="company-body">
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="value">{roe.current_roe:.2f}%</div>
                        <div class="label">ROE</div>
                    </div>
                    <div class="metric">
                        <div class="value">{ratio.roa:.2f}%</div>
                        <div class="label">ROA</div>
                    </div>
                    <div class="metric">
                        <div class="value">{ratio.debt_ratio:.2f}%</div>
                        <div class="label">资产负债率</div>
                    </div>
                    <div class="metric">
                        <div class="value">{policy.overall_score:.2f}</div>
                        <div class="label">政策匹配度</div>
                    </div>
                    <div class="metric">
                        <div class="value">{disclosure.overall_score:.2f}</div>
                        <div class="label">披露质量</div>
                    </div>
                    <div class="metric">
                        <div class="value">{compliance.compliance_score:.2f}</div>
                        <div class="label">合规评分</div>
                    </div>
                </div>
                
                <div class="insights">
                    <h4 style="margin-bottom: 15px; color: #2c5282;">分析洞察</h4>
"""
        
        # 添加洞察
        if roe.roe_change > 0:
            html += f"""
                    <div class="insight-item">
                        <span class="insight-icon">📈</span>
                        <span>ROE同比提升{roe.roe_change:+.2f}%，经营改善趋势向好</span>
                    </div>
"""
        
        if policy.overall_score > 60:
            html += f"""
                    <div class="insight-item">
                        <span class="insight-icon">🎯</span>
                        <span>政策匹配度较高，符合中特估改革方向</span>
                    </div>
"""
        
        if disclosure.rhetoric_flags:
            html += f"""
                    <div class="insight-item">
                        <span class="insight-icon">⚠️</span>
                        <span>发现{len(disclosure.rhetoric_flags)}处话术标记，建议关注披露真实性</span>
                    </div>
"""
        
        if compliance.compliant_items > 0:
            html += f"""
                    <div class="insight-item">
                        <span class="insight-icon">✅</span>
                        <span>合规检查通过{compliance.compliant_items}项，信披规范性较好</span>
                    </div>
"""
        
        # 添加建议
        html += f"""
                </div>
                
                <div class="recommendation {'rec-buy' if '推荐' in score.recommendation else 'rec-hold'}">
                    <strong>投资建议:</strong> {score.recommendation}
                </div>
            </div>
        </div>
"""
    
    # 添加免责声明
    html += """
        <div class="section">
            <div class="section-title">免责声明</div>
            <p style="color: #666; font-size: 14px;">
                本报告基于公开信息生成，仅供参考，不构成投资建议。投资有风险，入市需谨慎。
                报告中的分析结论和建议应结合个人风险承受能力和投资目标综合考虑。
            </p>
        </div>
        
        <div class="footer">
            <p>A股ESG分析框架 v2.0 | 中特估投资分析模块</p>
            <p>Generated by A-Stock ESG Framework</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html


if __name__ == "__main__":
    generate_html_report()
