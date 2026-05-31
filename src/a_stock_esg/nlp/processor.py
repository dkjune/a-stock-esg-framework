"""
中文NLP处理模块
针对A股披露文本优化，支持术语识别、情感分析、信息提取等
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import re


@dataclass
class ESGTerm:
    """ESG术语"""
    term: str
    category: str  # E, S, G
    subcategory: str
    description: str
    keywords: List[str] = field(default_factory=list)


@dataclass
class ExtractedInfo:
    """提取的信息"""
    category: str
    subcategory: str
    content: str
    confidence: float
    source: str = ""


@dataclass
class SentimentResult:
    """情感分析结果"""
    text: str
    sentiment: str  # positive, negative, neutral
    score: float
    keywords: List[str] = field(default_factory=list)


class NLPProcessor:
    """
    中文NLP处理器
    
    针对A股披露文本优化，支持术语识别、情感分析、信息提取等
    """
    
    def __init__(self):
        """初始化NLP处理器"""
        self.esg_terms = self._load_esg_terms()
        self.patterns = self._load_patterns()
    
    def _load_esg_terms(self) -> List[ESGTerm]:
        """加载ESG术语库"""
        terms = [
            # 环境(E)术语
            ESGTerm("碳排放", "E", "碳排放", "温室气体排放", ["CO2", "二氧化碳", "甲烷", "温室气体"]),
            ESGTerm("碳达峰", "E", "碳排放", "碳排放达到峰值", ["碳达峰", "排放峰值"]),
            ESGTerm("碳中和", "E", "碳排放", "碳排放与碳吸收平衡", ["碳中和", "净零排放"]),
            ESGTerm("能源消耗", "E", "能源管理", "能源使用情况", ["电力消耗", "天然气消耗", "综合能耗"]),
            ESGTerm("水资源", "E", "水资源", "水资源管理", ["用水量", "节水措施", "水资源利用"]),
            ESGTerm("废弃物", "E", "废弃物", "废弃物处理", ["固废", "危废", "废弃物处理"]),
            ESGTerm("绿色采购", "E", "绿色供应链", "环保材料采购", ["绿色采购", "环保材料"]),
            ESGTerm("生物多样性", "E", "生态保护", "生物多样性保护", ["生物多样性", "生态保护"]),
            
            # 社会(S)术语
            ESGTerm("员工权益", "S", "员工管理", "员工权益保护", ["员工权益", "劳动保护", "福利保障"]),
            ESGTerm("安全生产", "S", "安全管理", "生产安全管理", ["安全生产", "安全事故", "安全管理"]),
            ESGTerm("供应链", "S", "供应链管理", "供应链ESG管理", ["供应商", "供应链管理"]),
            ESGTerm("乡村振兴", "S", "社区关系", "乡村振兴投入", ["乡村振兴", "扶贫", "公益"]),
            ESGTerm("数据安全", "G", "信息安全管理", "数据安全管理", ["数据安全", "隐私保护"]),
            ESGTerm("知识产权", "G", "知识产权管理", "知识产权保护", ["专利", "商标", "著作权"]),
        ]
        return terms
    
    def _load_patterns(self) -> Dict[str, List[str]]:
        """加载正则表达式模式"""
        return {
            "carbon_emission": [
                r"温室气体|碳排放|CO2|二氧化碳.*?排放|量|数据",
                r"范围1|Scope\s*1.*?排放|量",
                r"范围2|Scope\s*2.*?排放|量",
            ],
            "energy": [
                r"能源消耗|综合能耗|电力消耗|天然气消耗",
                r"单位产品能耗|能耗强度",
            ],
            "water": [
                r"水资源|用水量|节水措施|水资源利用",
                r"取水量|排水量|循环利用率",
            ],
            "employee": [
                r"员工总数|员工人数|性别比例|学历构成",
                r"员工培训|培训投入|培训时长",
                r"员工离职率|员工满意度",
            ],
            "safety": [
                r"安全生产|安全事故|安全投入",
                r"工伤率|安全事故率",
            ],
            "governance": [
                r"董事会|ESG.*?治理|职责|架构",
                r"反腐败|反贿赂|商业道德|廉洁",
            ],
        }
    
    def extract_esg_info(self, text: str) -> List[ExtractedInfo]:
        """
        提取ESG相关信息
        
        Args:
            text: 输入文本
            
        Returns:
            List[ExtractedInfo]: 提取的信息列表
            
        Raises:
            TypeError: 当text不是字符串时
            ValueError: 当text为空时
        """
        # 输入验证
        if not isinstance(text, str):
            raise TypeError(f"text必须是字符串，收到{type(text).__name__}")
        
        if not text.strip():
            return []  # 空文本返回空列表，不抛出异常
        
        extracted = []
        
        # 碳排放信息
        try:
            carbon_matches = self._extract_pattern(text, "carbon_emission")
            if carbon_matches:
                extracted.append(ExtractedInfo(
                    category="E",
                    subcategory="碳排放",
                    content="、".join(carbon_matches),
                    confidence=0.9,
                    source="碳排放关键词匹配",
                ))
        except Exception as e:
            # 记录错误但继续处理
            pass
        
        # 能源信息
        try:
            energy_matches = self._extract_pattern(text, "energy")
            if energy_matches:
                extracted.append(ExtractedInfo(
                    category="E",
                    subcategory="能源管理",
                    content="、".join(energy_matches),
                    confidence=0.85,
                    source="能源关键词匹配",
                ))
        except Exception as e:
            pass
        
        # 水资源信息
        try:
            water_matches = self._extract_pattern(text, "water")
            if water_matches:
                extracted.append(ExtractedInfo(
                    category="E",
                    subcategory="水资源",
                    content="、".join(water_matches),
                    confidence=0.85,
                    source="水资源关键词匹配",
                ))
        except Exception as e:
            pass
        
        # 员工信息
        try:
            employee_matches = self._extract_pattern(text, "employee")
            if employee_matches:
                extracted.append(ExtractedInfo(
                    category="S",
                    subcategory="员工权益",
                    content="、".join(employee_matches),
                    confidence=0.85,
                    source="员工关键词匹配",
                ))
        except Exception as e:
            pass
        
        # 安全信息
        try:
            safety_matches = self._extract_pattern(text, "safety")
            if safety_matches:
                extracted.append(ExtractedInfo(
                    category="S",
                    subcategory="安全生产",
                    content="、".join(safety_matches),
                    confidence=0.85,
                    source="安全关键词匹配",
                ))
        except Exception as e:
            pass
        
        # 治理信息
        try:
            governance_matches = self._extract_pattern(text, "governance")
            if governance_matches:
                extracted.append(ExtractedInfo(
                    category="G",
                    subcategory="公司治理",
                    content="、".join(governance_matches),
                    confidence=0.85,
                    source="治理关键词匹配",
                ))
        except Exception as e:
            pass
        
        return extracted
    
    def _extract_pattern(self, text: str, pattern_type: str) -> List[str]:
        """提取匹配模式的内容"""
        patterns = self.patterns.get(pattern_type, [])
        matches = []
        
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found)
        
        return list(set(matches))[:5]  # 去重并限制数量
    
    def identify_terms(self, text: str) -> List[ESGTerm]:
        """
        识别ESG术语
        
        Args:
            text: 输入文本
            
        Returns:
            List[ESGTerm]: 识别的术语列表
        """
        identified = []
        
        for term in self.esg_terms:
            # 检查主术语
            if term.term in text:
                identified.append(term)
                continue
            
            # 检查关键词
            for keyword in term.keywords:
                if keyword in text:
                    identified.append(term)
                    break
        
        return identified
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        """
        情感分析
        
        Args:
            text: 输入文本
            
        Returns:
            SentimentResult: 情感分析结果
        """
        # 简单的情感分析（基于关键词）
        positive_words = [
            "提升", "增长", "改善", "优化", "加强", "完善", "创新",
            "领先", "优秀", "显著", "积极", "有效", "成功",
        ]
        negative_words = [
            "下降", "减少", "降低", "损失", "风险", "问题", "挑战",
            "困难", "不足", "违规", "处罚", "事故",
        ]
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        total = positive_count + negative_count
        if total == 0:
            sentiment = "neutral"
            score = 0.5
        else:
            score = positive_count / total
            if score > 0.6:
                sentiment = "positive"
            elif score < 0.4:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return SentimentResult(
            text=text[:100] + "..." if len(text) > 100 else text,
            sentiment=sentiment,
            score=round(score, 2),
            keywords=[word for word in positive_words + negative_words if word in text],
        )
    
    def extract_numbers(self, text: str) -> List[Dict]:
        """
        提取数值信息
        
        Args:
            text: 输入文本
            
        Returns:
            List[Dict]: 数值信息列表
        """
        number_pattern = r"(\d+(?:\.\d+)?)\s*(万吨|吨|兆瓦|千瓦|万元|亿元|%|％|人|次)"
        matches = re.findall(number_pattern, text)
        
        results = []
        for value, unit in matches:
            results.append({
                "value": float(value),
                "unit": unit,
                "context": self._get_context(text, f"{value}{unit}"),
            })
        
        return results
    
    def _get_context(self, text: str, keyword: str, window: int = 50) -> str:
        """获取关键词上下文"""
        index = text.find(keyword)
        if index == -1:
            return ""
        
        start = max(0, index - window)
        end = min(len(text), index + len(keyword) + window)
        
        return text[start:end]
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """
        生成摘要
        
        Args:
            text: 输入文本
            max_length: 最大长度
            
        Returns:
            str: 摘要文本
        """
        # 简单的摘要生成（基于关键句提取）
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        # 选择包含ESG关键词的句子
        esg_keywords = ["ESG", "环境", "社会", "治理", "碳排放", "可持续发展"]
        important_sentences = []
        
        for sentence in sentences:
            for keyword in esg_keywords:
                if keyword in sentence:
                    important_sentences.append(sentence)
                    break
        
        if not important_sentences:
            important_sentences = sentences[:3]
        
        summary = "。".join(important_sentences[:3])
        
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary
