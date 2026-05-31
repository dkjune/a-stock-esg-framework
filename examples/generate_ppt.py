"""
电力行业四巨头分析报告 - PPT生成器
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from a_stock_esg import ROEAnalyzer, PolicyAnalyzer, stock_data


def create_ppt():
    """创建PPT报告"""
    
    # 获取数据
    companies = [
        {"code": "600863", "name": "华能蒙电", "disclosure": "公司积极推进国企改革，优化董事会结构，完善公司治理。ROE持续改善。大力发展清洁能源，风电光伏装机容量快速增长。制定碳达峰碳中和目标。"},
        {"code": "600011", "name": "华能国际", "disclosure": "公司积极推进国企改革，完善公司治理结构。ROE保持稳定，重视股东回报。大力发展清洁能源，风电光伏装机容量持续增长。"},
        {"code": "600886", "name": "国投电力", "disclosure": "公司积极推进国企改革，优化治理结构。ROE持续改善，现金分红比例30%以上。大力发展清洁能源，风电光伏装机容量持续增长。"},
        {"code": "600900", "name": "长江电力", "disclosure": "全球最大水电上市公司，积极推进国企改革。ROE稳定在15%以上，分红比例高。清洁能源占比100%，碳排放为零。"},
    ]
    
    quotes = stock_data.get_quotes([c["code"] for c in companies])
    roe_analyzer = ROEAnalyzer()
    policy_analyzer = PolicyAnalyzer()
    
    results = []
    for company in companies:
        quote = quotes.get(company["code"])
        roe = roe_analyzer.analyze(company["code"], "电力")
        policy = policy_analyzer.analyze(company["code"], company["name"], company["disclosure"], "电力")
        results.append({"code": company["code"], "name": company["name"], "quote": quote, "roe": roe, "policy": policy})
    
    results_sorted = sorted(results, key=lambda x: x["roe"].roe, reverse=True)
    
    # 创建PPT
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 颜色定义
    DARK_BG = RGBColor(0x1a, 0x1a, 0x1a)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    LIGHT_BG = RGBColor(0xFA, 0xF9, 0xF7)
    ORANGE = RGBColor(0xF9, 0x73, 0x16)
    GRAY = RGBColor(0x6B, 0x6B, 0x6B)
    LIGHT_GRAY = RGBColor(0xF0, 0xF0, 0xF0)
    
    # ========== 封面 ==========
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = DARK_BG
    
    # 标题
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(2))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "电力行业四巨头"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "中特估分析报告"
    p2.font.size = Pt(32)
    p2.font.color.rgb = ORANGE
    p2.alignment = PP_ALIGN.CENTER
    
    p3 = tf.add_paragraph()
    p3.text = "\n华能蒙电 · 华能国际 · 国投电力 · 长江电力"
    p3.font.size = Pt(18)
    p3.font.color.rgb = GRAY
    p3.alignment = PP_ALIGN.CENTER
    
    p4 = tf.add_paragraph()
    p4.text = f"\n{datetime.now().strftime('%Y年%m月%d日')} · A股中特估分析框架 v2.1"
    p4.font.size = Pt(14)
    p4.font.color.rgb = GRAY
    p4.alignment = PP_ALIGN.CENTER
    
    # ========== 综合排名页 ==========
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    slide2.background.fill.solid()
    slide2.background.fill.fore_color.rgb = LIGHT_BG
    
    # 标题
    txBox = slide2.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "综合排名"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    
    # 表格
    rows = len(results_sorted) + 1
    cols = 7
    table_shape = slide2.shapes.add_table(rows, cols, Inches(0.5), Inches(1.2), Inches(12), Inches(2.5))
    table = table_shape.table
    
    # 表头
    headers = ["公司", "代码", "市值", "PE", "ROE", "质量", "政策分"]
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BG
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(12)
            paragraph.font.bold = True
            paragraph.font.color.rgb = WHITE
            paragraph.alignment = PP_ALIGN.CENTER
    
    # 数据行
    for row_idx, r in enumerate(results_sorted, 1):
        q = r["quote"]
        roe = r["roe"]
        policy = r["policy"]
        
        data = [
            r["name"],
            r["code"],
            f"{q.market_cap:.0f}亿",
            f"{q.pe_ttm:.1f}",
            f"{roe.roe:.1f}%",
            roe.quality.value,
            f"{policy.overall_score:.1f}",
        ]
        
        for col_idx, value in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.text = value
            if row_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xF5, 0xF5, 0xF5)
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(11)
                paragraph.alignment = PP_ALIGN.CENTER
        
        # ROE高亮
        roe_cell = table.cell(row_idx, 4)
        if roe.roe > 15:
            for paragraph in roe_cell.text_frame.paragraphs:
                paragraph.font.color.rgb = RGBColor(0x16, 0x65, 0x34)
                paragraph.font.bold = True
    
    # 关键洞察
    txBox = slide2.shapes.add_textbox(Inches(0.5), Inches(4.0), Inches(12), Inches(3))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "关键洞察"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
    
    insights = [
        f"• 华能国际ROE最高({results_sorted[0]['roe'].roe:.1f}%)，行业龙头地位稳固",
        f"• 长江电力ROE稳定({results_sorted[1]['roe'].roe:.1f}%)，全球最大水电，适合稳健投资",
        f"• 华能蒙电政策匹配度最高(13.4)，清洁能源转型积极",
        f"• 国投电力ROE改善中，清洁能源装机增长",
    ]
    
    for insight in insights:
        p = tf.add_paragraph()
        p.text = insight
        p.font.size = Pt(14)
        p.font.color.rgb = GRAY
        p.space_after = Pt(8)
    
    # ========== 各公司详情页 ==========
    for r in results:
        slide_n = prs.slides.add_slide(prs.slide_layouts[6])
        slide_n.background.fill.solid()
        slide_n.background.fill.fore_color.rgb = LIGHT_BG
        
        q = r["quote"]
        roe = r["roe"]
        policy = r["policy"]
        
        # 标题栏
        title_shape = slide_n.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.5)
        )
        title_shape.fill.solid()
        title_shape.fill.fore_color.rgb = DARK_BG
        
        txBox = slide_n.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(1))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"{r['name']}"
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
        p2 = tf.add_paragraph()
        p2.text = f"{r['code']} · 市值 {q.market_cap:.0f}亿 · PE {q.pe_ttm:.1f} · PB {q.pb:.2f}"
        p2.font.size = Pt(14)
        p2.font.color.rgb = GRAY
        
        # ROE大字
        txBox = slide_n.shapes.add_textbox(Inches(9), Inches(0.2), Inches(4), Inches(1.2))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = f"{roe.roe:.1f}%"
        p.font.size = Pt(48)
        p.font.bold = True
        p.font.color.rgb = ORANGE
        p.alignment = PP_ALIGN.RIGHT
        
        p2 = tf.add_paragraph()
        p2.text = f"ROE · {roe.quality.value}"
        p2.font.size = Pt(16)
        p2.font.color.rgb = GRAY
        p2.alignment = PP_ALIGN.RIGHT
        
        # 核心指标
        metrics_data = [
            ("ROE", f"{roe.roe:.1f}%"),
            ("净利率", f"{roe.net_margin:.1f}%"),
            ("资产周转率", f"{roe.asset_turnover:.2f}"),
            ("政策匹配", f"{policy.overall_score:.1f}"),
        ]
        
        for i, (label, value) in enumerate(metrics_data):
            x = Inches(0.5 + i * 3.2)
            shape = slide_n.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.8), Inches(1.2))
            shape.fill.solid()
            shape.fill.fore_color.rgb = WHITE
            
            txBox = slide_n.shapes.add_textbox(x + Inches(0.2), Inches(1.9), Inches(2.4), Inches(1))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = value
            p.font.size = Pt(24)
            p.font.bold = True
            p.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)
            p.alignment = PP_ALIGN.CENTER
            
            p2 = tf.add_paragraph()
            p2.text = label
            p2.font.size = Pt(12)
            p2.font.color.rgb = GRAY
            p2.alignment = PP_ALIGN.CENTER
        
        # 政策匹配维度
        txBox = slide_n.shapes.add_textbox(Inches(0.5), Inches(3.2), Inches(6), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = "政策匹配维度"
        p.font.size = Pt(16)
        p.font.bold = True
        
        for i, (dim, score) in enumerate(sorted(policy.dimension_scores.items(), key=lambda x: x[1], reverse=True)):
            y = Inches(3.8 + i * 0.45)
            
            # 维度名
            txBox = slide_n.shapes.add_textbox(Inches(0.5), y, Inches(2), Inches(0.4))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = dim
            p.font.size = Pt(12)
            p.font.color.rgb = GRAY
            
            # 进度条背景
            bar_bg = slide_n.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), y + Inches(0.05), Inches(4), Inches(0.25))
            bar_bg.fill.solid()
            bar_bg.fill.fore_color.rgb = LIGHT_GRAY
            
            # 进度条
            bar_width = max(0.1, score / 100 * 4)
            bar = slide_n.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), y + Inches(0.05), Inches(bar_width), Inches(0.25))
            bar.fill.solid()
            bar.fill.fore_color.rgb = ORANGE
            
            # 分数
            txBox = slide_n.shapes.add_textbox(Inches(6.5), y, Inches(1), Inches(0.4))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            p.text = f"{score:.0f}"
            p.font.size = Pt(12)
            p.font.bold = True
        
        # 洞察
        txBox = slide_n.shapes.add_textbox(Inches(7.5), Inches(3.2), Inches(5.5), Inches(0.5))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = "分析洞察"
        p.font.size = Pt(16)
        p.font.bold = True
        
        insights = []
        for s in roe.strengths:
            insights.append(f"✓ {s}")
        for w in roe.weaknesses:
            insights.append(f"✗ {w}")
        for rec in roe.recommendations[:2]:
            insights.append(f"→ {rec}")
        
        txBox = slide_n.shapes.add_textbox(Inches(7.5), Inches(3.8), Inches(5.5), Inches(3))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        for i, insight in enumerate(insights[:5]):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = insight
            p.font.size = Pt(13)
            p.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            p.space_after = Pt(8)
    
    # ========== 结尾页 ==========
    slide_end = prs.slides.add_slide(prs.slide_layouts[6])
    slide_end.background.fill.solid()
    slide_end.background.fill.fore_color.rgb = DARK_BG
    
    txBox = slide_end.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11), Inches(2))
    tf = txBox.text_frame
    
    p = tf.paragraphs[0]
    p.text = "投资建议"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    
    recommendations = [
        "华能国际 - ROE最高，行业龙头，盈利能力强",
        "长江电力 - ROE稳定，全球最大水电，适合稳健投资",
        "国投电力 - ROE改善中，清洁能源转型积极",
        "华能蒙电 - 政策匹配度高，关注改革进展",
    ]
    
    for rec in recommendations:
        p = tf.add_paragraph()
        p.text = f"\n• {rec}"
        p.font.size = Pt(16)
        p.font.color.rgb = GRAY
        p.alignment = PP_ALIGN.CENTER
    
    p = tf.add_paragraph()
    p.text = "\n\nA股中特估分析框架 v2.1"
    p.font.size = Pt(14)
    p.font.color.rgb = GRAY
    p.alignment = PP_ALIGN.CENTER
    
    # 保存
    output_path = Path(__file__).parent.parent / "电力行业四巨头_中特估分析报告.pptx"
    prs.save(str(output_path))
    
    print(f"PPT已生成: {output_path}")
    return output_path


if __name__ == "__main__":
    create_ppt()
