"""
可视化看板模块
展示企业ESG合规进度、行业排名、风险点分布
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class DashboardConfig:
    """看板配置"""
    title: str = "A股ESG分析看板"
    width: str = "100%"
    height: str = "800px"
    theme: str = "default"
    language: str = "zh-CN"


class Visualizer:
    """
    可视化看板
    
    展示企业ESG合规进度、行业排名、风险点分布
    """
    
    def __init__(self, config: Optional[DashboardConfig] = None):
        """
        初始化可视化器
        
        Args:
            config: 看板配置
        """
        self.config = config or DashboardConfig()
    
    def create_compliance_dashboard(
        self, 
        compliance_report: Any,
        output_path: str = "compliance_dashboard.html"
    ) -> str:
        """
        创建合规性看板
        
        Args:
            compliance_report: 合规检查报告
            output_path: 输出路径
            
        Returns:
            str: 生成的HTML文件路径
        """
        # 计算统计数据
        summary = {
            "company_name": compliance_report.company_name,
            "market_type": compliance_report.market_type,
            "industry": compliance_report.industry,
            "compliance_score": compliance_report.compliance_score,
            "total_items": compliance_report.total_items,
            "compliant_items": compliance_report.compliant_items,
            "partial_items": compliance_report.partial_items,
            "non_compliant_items": compliance_report.non_compliant_items,
            "missing_items": compliance_report.missing_items,
        }
        
        # 生成HTML
        html_content = self._generate_dashboard_html(summary, compliance_report.items, compliance_report.recommendations)
        
        # 写入文件
        output_file = Path(output_path)
        output_file.write_text(html_content, encoding="utf-8")
        
        return str(output_file)
    
    def _generate_dashboard_html(self, summary: Dict, items: List, recommendations: List = None) -> str:
        """生成看板HTML"""
        # 统计各维度得分
        e_items = [i for i in items if i.category == "环境(E)"]
        s_items = [i for i in items if i.category == "社会(S)"]
        g_items = [i for i in items if i.category == "治理(G)"]
        
        e_score = self._calculate_dimension_score(e_items)
        s_score = self._calculate_dimension_score(s_items)
        g_score = self._calculate_dimension_score(g_items)
        
        # 生成合规项列表HTML
        items_html = self._generate_items_html(items)
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config.title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f5f7fa;
            color: #333;
        }}
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-card .value {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-card .label {{
            color: #666;
            margin-top: 5px;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .chart-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }}
        .items-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .items-table th, .items-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        .items-table th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
        .status-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }}
        .status-compliant {{
            background-color: #d4edda;
            color: #155724;
        }}
        .status-partial {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .status-non-compliant {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .status-missing {{
            background-color: #e2e3e5;
            color: #383d41;
        }}
        .recommendations {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .recommendation-item {{
            padding: 10px;
            border-left: 4px solid #667eea;
            margin-bottom: 10px;
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>{self.config.title}</h1>
            <div class="subtitle">
                {summary['company_name']} | {summary['market_type']} | {summary['industry']}
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value">{summary['compliance_score']}</div>
                <div class="label">合规评分</div>
            </div>
            <div class="stat-card">
                <div class="value">{summary['compliant_items']}</div>
                <div class="label">合规项</div>
            </div>
            <div class="stat-card">
                <div class="value">{summary['partial_items']}</div>
                <div class="label">部分合规</div>
            </div>
            <div class="stat-card">
                <div class="value">{summary['missing_items']}</div>
                <div class="label">缺失项</div>
            </div>
        </div>
        
        <div class="chart-row">
            <div class="chart-container">
                <div class="section-title">维度得分</div>
                <div id="dimension-chart"></div>
            </div>
            <div class="chart-container">
                <div class="section-title">合规状态分布</div>
                <div id="status-chart"></div>
            </div>
        </div>
        
        <div class="chart-container">
            <div class="section-title">合规检查项详情</div>
            <table class="items-table">
                <thead>
                    <tr>
                        <th>编号</th>
                        <th>类别</th>
                        <th>要求</th>
                        <th>状态</th>
                        <th>证据</th>
                        <th>建议</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
        </div>
        
        <div class="recommendations">
            <div class="section-title">改进建议</div>
            {self._generate_recommendations_html(recommendations)}
        </div>
    </div>
    
    <script>
        // 维度得分图表
        var dimensionData = [{{
            type: 'bar',
            x: ['环境(E)', '社会(S)', '治理(G)'],
            y: [{e_score}, {s_score}, {g_score}],
            marker: {{
                color: ['#4CAF50', '#2196F3', '#FF9800']
            }}
        }}];
        
        var dimensionLayout = {{
            yaxis: {{ title: '得分', range: [0, 100] }},
            margin: {{ t: 20, b: 40, l: 40, r: 20 }}
        }};
        
        Plotly.newPlot('dimension-chart', dimensionData, dimensionLayout);
        
        // 合规状态分布图表
        var statusData = [{{
            type: 'pie',
            labels: ['合规', '部分合规', '不合规', '缺失'],
            values: [{summary['compliant_items']}, {summary['partial_items']}, {summary['non_compliant_items']}, {summary['missing_items']}],
            marker: {{
                colors: ['#4CAF50', '#FFC107', '#F44336', '#9E9E9E']
            }}
        }}];
        
        var statusLayout = {{
            margin: {{ t: 20, b: 20, l: 20, r: 20 }}
        }};
        
        Plotly.newPlot('status-chart', statusData, statusLayout);
    </script>
</body>
</html>
"""
        return html
    
    def _calculate_dimension_score(self, items: List) -> float:
        """计算维度得分"""
        if not items:
            return 0
        
        compliant = sum(1 for i in items if i.status.value == "合规")
        partial = sum(1 for i in items if i.status.value == "部分合规")
        
        return round((compliant * 100 + partial * 50) / len(items), 2)
    
    def _generate_items_html(self, items: List) -> str:
        """生成合规项HTML"""
        html = ""
        for item in items:
            status_class = f"status-{item.status.value}"
            html += f"""
                    <tr>
                        <td>{item.item_id}</td>
                        <td>{item.category}</td>
                        <td>{item.requirement}</td>
                        <td><span class="status-badge {status_class}">{item.status.value}</span></td>
                        <td>{item.evidence}</td>
                        <td>{item.recommendation}</td>
                    </tr>
"""
        return html
    
    def _generate_recommendations_html(self, report) -> str:
        """生成建议HTML"""
        html = ""
        for rec in report.recommendations:
            html += f"""
            <div class="recommendation-item">{rec}</div>
"""
        return html
    
    def create_benchmark_chart(
        self, 
        comparison_data: Dict,
        output_path: str = "benchmark_chart.html"
    ) -> str:
        """
        创建行业对标图表
        
        Args:
            comparison_data: 对标数据
            output_path: 输出路径
            
        Returns:
            str: 生成的HTML文件路径
        """
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>行业对标分析</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="benchmark-chart"></div>
    <script>
        var data = [{{
            type: 'bar',
            x: ['公司得分', '行业平均', '行业最高'],
            y: [{comparison_data.get('company_score', 0)}, 
                {comparison_data.get('industry_average', 0)}, 
                {comparison_data.get('industry_max', 100)}],
            marker: {{
                color: ['#667eea', '#4CAF50', '#FF9800']
            }}
        }}];
        
        var layout = {{
            title: '行业对标分析',
            yaxis: {{ title: 'ESG评分' }}
        }};
        
        Plotly.newPlot('benchmark-chart', data, layout);
    </script>
</body>
</html>
"""
        
        output_file = Path(output_path)
        output_file.write_text(html, encoding="utf-8")
        
        return str(output_file)
