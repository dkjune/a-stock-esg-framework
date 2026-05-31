"""
电力行业四巨头分析报告生成器
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from a_stock_esg import ROEAnalyzer, PolicyAnalyzer, NoiseReportGenerator, stock_data


def generate_report():
    """生成HTML报告"""
    
    companies = [
        {
            "code": "600863",
            "name": "华能蒙电",
            "disclosure": "公司积极推进国企改革，优化董事会结构，完善公司治理。ROE持续改善，现金分红比例提升。大力推进清洁能源发展，风电光伏装机容量快速增长。制定碳达峰碳中和目标，碳排放数据已披露。研发投入增加，技术创新能力增强。推进数字化转型，智能制造水平提升。",
        },
        {
            "code": "600011",
            "name": "华能国际",
            "disclosure": "公司积极推进国企改革，完善公司治理结构，提升经营效率。ROE保持稳定，重视股东回报，现金分红比例高。大力发展清洁能源，风电光伏装机容量持续增长。研发投入持续增加，技术创新成果显著。推进数字化转型，智能化水平提升。",
        },
        {
            "code": "600886",
            "name": "国投电力",
            "disclosure": "公司积极推进国企改革，优化治理结构，提升经营效率。ROE持续改善，现金分红比例30%以上。大力发展清洁能源，风电光伏装机容量持续增长。研发投入强度达到2.5%，技术创新能力增强。推进数字化转型，智能制造水平提升。",
        },
        {
            "code": "600900",
            "name": "长江电力",
            "disclosure": "全球最大水电上市公司，积极推进国企改革，完善公司治理。ROE稳定在15%以上，分红比例高，重视股东回报。清洁能源占比100%，碳排放为零。技术创新能力强，拥有多项专利。推进数字化转型，智能化水平提升。",
        },
    ]
    
    # 获取实时数据
    multi_data = {}
    for c in companies:
        data = stock_data.get_multi_source_data(c["code"])
        if data:
            multi_data[c["code"]] = data
    
    # 分析
    roe_analyzer = ROEAnalyzer()
    policy_analyzer = PolicyAnalyzer()
    noise_gen = NoiseReportGenerator()
    
    results = []
    for company in companies:
        code = company["code"]
        md = multi_data.get(code)
        
        roe = roe_analyzer.analyze(code, "电力")
        roe["name"] = company["name"]
        
        policy = policy_analyzer.analyze(code, company["name"], company["disclosure"], "电力")
        noise = noise_gen.generate(roe, policy)
        
        results.append({
            "code": company["code"],
            "name": company["name"],
            "multi_data": md,
            "roe": roe,
            "policy": policy,
            "noise": noise,
        })
    
    # 按ROE排序
    results_sorted = sorted(results, key=lambda x: x["roe"].get("roe", 0), reverse=True)
    
    # 生成HTML
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>电力行业四巨头 - 中特估分析报告</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', -apple-system, sans-serif; background: #faf9f7; color: #1a1a1a; line-height: 1.6; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 40px 24px; }}
        
        .header {{ background: #fff; border: 1px solid #e5e5e5; padding: 48px; border-radius: 16px; margin-bottom: 32px; text-align: center; }}
        .header h1 {{ font-size: 32px; font-weight: 700; margin-bottom: 12px; letter-spacing: -0.02em; }}
        .header .subtitle {{ color: #6b6b6b; font-size: 16px; margin-bottom: 16px; }}
        .header .meta {{ font-size: 13px; color: #999; padding-top: 16px; border-top: 1px solid #f0f0f0; }}
        
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }}
        .summary-card {{ background: #fff; padding: 24px; border-radius: 12px; border: 1px solid #e5e5e5; text-align: center; }}
        .summary-card .value {{ font-size: 36px; font-weight: 700; letter-spacing: -0.02em; }}
        .summary-card .label {{ color: #6b6b6b; font-size: 13px; margin-top: 4px; }}
        
        .section {{ background: #fff; padding: 32px; border-radius: 12px; border: 1px solid #e5e5e5; margin-bottom: 24px; }}
        .section-title {{ font-size: 18px; font-weight: 600; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #f0f0f0; }}
        
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 14px 16px; text-align: left; border-bottom: 1px solid #f5f5f5; }}
        th {{ font-weight: 600; color: #6b6b6b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }}
        tr:hover {{ background: #faf9f7; }}
        
        .rank {{ display: inline-block; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; }}
        .rank-excellent {{ background: #dcfce7; color: #166534; }}
        .rank-good {{ background: #dbeafe; color: #1e40af; }}
        .rank-fair {{ background: #fef3c7; color: #92400e; }}
        .rank-poor {{ background: #fee2e2; color: #991b1b; }}
        
        .company-card {{ background: #fff; border-radius: 12px; border: 1px solid #e5e5e5; margin-bottom: 24px; overflow: hidden; }}
        .company-header {{ background: #1a1a1a; color: #fff; padding: 24px 32px; display: flex; justify-content: space-between; align-items: center; }}
        .company-header h3 {{ font-size: 20px; font-weight: 600; }}
        .company-header .score {{ font-size: 32px; font-weight: 700; }}
        .company-body {{ padding: 32px; }}
        
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
        .metric {{ text-align: center; padding: 20px; background: #faf9f7; border-radius: 10px; }}
        .metric .value {{ font-size: 28px; font-weight: 700; }}
        .metric .label {{ font-size: 12px; color: #6b6b6b; margin-top: 4px; }}
        
        .dimension {{ display: flex; align-items: center; margin-bottom: 12px; }}
        .dimension .name {{ width: 120px; font-size: 14px; font-weight: 500; }}
        .dimension .bar {{ flex: 1; height: 8px; background: #f0f0f0; border-radius: 4px; overflow: hidden; }}
        .dimension .fill {{ height: 100%; background: #f97316; border-radius: 4px; }}
        .dimension .score {{ width: 60px; text-align: right; font-size: 14px; font-weight: 600; }}
        
        .insight {{ padding: 16px; background: #faf9f7; border-radius: 8px; border-left: 3px solid #f97316; margin-bottom: 12px; font-size: 14px; }}
        
        .footer {{ text-align: center; padding: 32px 0; color: #999; font-size: 13px; border-top: 1px solid #e5e5e5; margin-top: 40px; }}
        
        .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
        .badge-real {{ background: #dcfce7; color: #166534; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>电力行业四巨头 · 中特估分析报告</h1>
            <div class="subtitle">华能蒙电 · 华能国际 · 国投电力 · 长江电力</div>
            <div class="meta">
                {now} · A股中特估分析框架 v2.1 · 数据来源: 腾讯财经API
            </div>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <div class="value">4</div>
                <div class="label">分析公司数</div>
            </div>
            <div class="summary-card">
                <div class="value">{sum(r['roe'].get('roe', 0) for r in results) / len(results):.1f}%</div>
                <div class="label">平均ROE</div>
            </div>
            <div class="summary-card">
                <div class="value">{results_sorted[0]['roe'].get('roe', 0):.1f}%</div>
                <div class="label">最高ROE</div>
            </div>
            <div class="summary-card">
                <div class="value">N/A</div>
                <div class="label">总市值</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">综合排名</div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>公司</th>
                        <th>代码</th>
                        <th>市值</th>
                        <th>PE</th>
                        <th>ROE</th>
                        <th>质量</th>
                        <th>政策分</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for i, r in enumerate(results_sorted, 1):
        md = r.get("multi_data")
        roe = r["roe"]
        policy = r["policy"]
        
        quality_class = {
            "优秀": "rank-excellent",
            "良好": "rank-good",
            "一般": "rank-fair",
            "较差": "rank-poor",
        }.get(roe.get('quality', 'N/A'), "rank-fair")
        
        html += f"""
                    <tr>
                        <td><strong>{i}</strong></td>
                        <td><strong>{r['name']}</strong></td>
                        <td style="color: #6b6b6b;">{r['code']}</td>
                        <td>{md.pe_median if md else 0:.0f}亿 <span class="badge badge-real">实时</span></td>
                        <td>{md.pe_median if md else 0:.1f}</td>
                        <td style="font-weight: 600;">{roe.get('roe', 0):.1f}%</td>
                        <td><span class="rank {quality_class}">{roe.get('quality', 'N/A')}</span></td>
                        <td style="font-weight: 600;">{policy.overall_score:.1f}</td>
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
"""
    
    # 每家公司详情
    for r in results:
        md = r.get("multi_data")
        roe = r["roe"]
        policy = r["policy"]
        
        html += f"""
        <div class="company-card">
            <div class="company-header">
                <div>
                    <h3>{r['name']}</h3>
                    <div style="font-size: 13px; opacity: 0.7; margin-top: 4px;">{r['code']} · 市值 {md.pe_median if md else 0:.0f}亿 · PE {md.pe_median if md else 0:.1f} · PB {md.pb_median if md else 0:.2f}</div>
                </div>
                <div style="text-align: right;">
                    <div class="score">{roe.get('roe', 0):.1f}%</div>
                    <div style="font-size: 13px; opacity: 0.8;">ROE · {roe.get('quality', 'N/A')}</div>
                </div>
            </div>
            <div class="company-body">
                <div class="metrics">
                    <div class="metric">
                        <div class="value">{roe.get('roe', 0):.1f}%</div>
                        <div class="label">ROE</div>
                    </div>
                    <div class="metric">
                        <div class="value">{roe.get('net_margin', 0):.1f}%</div>
                        <div class="label">净利率</div>
                    </div>
                    <div class="metric">
                        <div class="value">{roe.get('asset_turnover', 0):.2f}</div>
                        <div class="label">资产周转率</div>
                    </div>
                    <div class="metric">
                        <div class="value">{policy.overall_score:.1f}</div>
                        <div class="label">政策匹配</div>
                    </div>
                </div>
                
                <h4 style="font-size: 14px; font-weight: 600; margin-bottom: 16px; color: #6b6b6b; text-transform: uppercase; letter-spacing: 0.05em;">政策匹配维度</h4>
"""
        
        for dim, score in sorted(policy.dimension_scores.items(), key=lambda x: x[1], reverse=True):
            html += f"""
                <div class="dimension">
                    <div class="name">{dim}</div>
                    <div class="bar"><div class="fill" style="width: {score}%"></div></div>
                    <div class="score">{score:.1f}</div>
                </div>
"""
        
        html += """
                <h4 style="font-size: 14px; font-weight: 600; margin: 24px 0 16px; color: #6b6b6b; text-transform: uppercase; letter-spacing: 0.05em;">分析洞察</h4>
"""
        
        for s in roe.get('strengths', []):
            html += f"""
                <div class="insight">✓ {s}</div>
"""
        
        for w in roe.get('weaknesses', []):
            html += f"""
                <div class="insight" style="border-left-color: #ef4444;">✗ {w}</div>
"""
        
        for rec in roe.get('recommendations', [])[:2]:
            html += f"""
                <div class="insight" style="border-left-color: #3b82f6;">→ {rec}</div>
"""
        
        html += """
            </div>
        </div>
"""
    
    # 免责声明和页脚
    html += f"""
        <div class="section" style="background: #faf9f7; border: none; padding: 24px;">
            <p style="color: #6b6b6b; font-size: 13px; line-height: 1.8;">
                <strong>免责声明：</strong>本报告基于公开信息生成，仅供参考，不构成投资建议。投资有风险，入市需谨慎。
                数据来源：腾讯财经API（实时行情）。
            </p>
        </div>
        
        <div class="footer">
            <p style="margin-bottom: 8px;">A股中特估分析框架 v2.1</p>
            <p style="color: #ccc;">Powered by A-Stock ESG Framework</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存文件
    output_path = Path(__file__).parent.parent / "electricity_report.html"
    output_path.write_text(html, encoding="utf-8")
    
    print(f"报告已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_report()
