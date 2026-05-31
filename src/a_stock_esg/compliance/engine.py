"""
A股ESG合规性检查模块
基于A股监管规则引擎，自动扫描企业披露文本，标记缺失项和不符合项
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import re


class ComplianceStatus(Enum):
    """合规状态"""
    COMPLIANT = "合规"
    PARTIAL = "部分合规"
    NON_COMPLIANT = "不合规"
    MISSING = "缺失"


@dataclass
class ComplianceItem:
    """合规检查项"""
    item_id: str
    category: str  # E, S, G
    subcategory: str
    requirement: str
    description: str
    mandatory: bool
    market_types: List[str]  # 适用的市场类型
    status: ComplianceStatus = ComplianceStatus.MISSING
    evidence: str = ""
    recommendation: str = ""


@dataclass
class ComplianceReport:
    """合规检查报告"""
    company_name: str
    market_type: str
    industry: str
    total_items: int
    compliant_items: int
    partial_items: int
    non_compliant_items: int
    missing_items: int
    compliance_score: float
    items: List[ComplianceItem] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class ComplianceEngine:
    """
    A股ESG合规性检查引擎
    
    基于A股监管规则引擎，自动扫描企业披露文本，标记缺失项和不符合项
    """
    
    def __init__(self, config=None):
        """
        初始化合规检查引擎
        
        Args:
            config: AStockESGConfig配置对象
        """
        from ..core.config import AStockESGConfig, MarketType
        self.config = config or AStockESGConfig()
        self.rules = self._load_compliance_rules()
    
    def _load_compliance_rules(self) -> List[ComplianceItem]:
        """加载合规检查规则"""
        rules = []
        
        # 环境(E)维度规则
        env_rules = [
            ComplianceItem(
                item_id="E001",
                category="环境(E)",
                subcategory="碳排放",
                requirement="碳排放数据披露",
                description="披露范围1和范围2温室气体排放数据",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="E002",
                category="环境(E)",
                subcategory="碳排放",
                requirement="碳减排目标",
                description="披露碳达峰、碳中和目标及实施路径",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="E003",
                category="环境(E)",
                subcategory="能源管理",
                requirement="能源消耗数据",
                description="披露综合能源消耗总量及强度指标",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="E004",
                category="环境(E)",
                subcategory="水资源",
                requirement="水资源管理",
                description="披露水资源消耗及节水措施",
                mandatory=False,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="E005",
                category="环境(E)",
                subcategory="废弃物",
                requirement="废弃物处理",
                description="披露固体废弃物产生量及处理方式",
                mandatory=False,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="E006",
                category="环境(E)",
                subcategory="绿色技术",
                requirement="绿色技术研发投入",
                description="披露绿色技术研发投入金额及占比",
                mandatory=True,
                market_types=["科创板"],
            ),
        ]
        
        # 社会(S)维度规则
        social_rules = [
            ComplianceItem(
                item_id="S001",
                category="社会(S)",
                subcategory="员工权益",
                requirement="员工信息披露",
                description="披露员工总数、性别比例、学历构成",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="S002",
                category="社会(S)",
                subcategory="员工权益",
                requirement="员工培训",
                description="披露员工培训投入及培训时长",
                mandatory=False,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="S003",
                category="社会(S)",
                subcategory="安全生产",
                requirement="安全生产管理",
                description="披露安全生产投入及事故情况",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="S004",
                category="社会(S)",
                subcategory="供应链",
                requirement="供应链管理",
                description="披露供应链ESG管理政策及措施",
                mandatory=False,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="S005",
                category="社会(S)",
                subcategory="社区关系",
                requirement="乡村振兴",
                description="披露乡村振兴投入及成效",
                mandatory=False,
                market_types=["主板"],
            ),
            ComplianceItem(
                item_id="S006",
                category="社会(S)",
                subcategory="产品责任",
                requirement="产品质量管理",
                description="披露产品质量管理体系及召回情况",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
        ]
        
        # 治理(G)维度规则
        governance_rules = [
            ComplianceItem(
                item_id="G001",
                category="治理(G)",
                subcategory="董事会",
                requirement="董事会ESG职责",
                description="披露董事会ESG治理架构及职责分工",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="G002",
                category="治理(G)",
                subcategory="商业道德",
                requirement="反腐败政策",
                description="披露反腐败、反贿赂政策及执行情况",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="G003",
                category="治理(G)",
                subcategory="数据安全",
                requirement="数据安全管理",
                description="披露数据安全管理体系及隐私保护措施",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="G004",
                category="治理(G)",
                subcategory="信息披露",
                requirement="ESG信息披露",
                description="建立ESG信息披露制度及流程",
                mandatory=True,
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
            ComplianceItem(
                item_id="G005",
                category="治理(G)",
                subcategory="知识产权",
                requirement="知识产权保护",
                description="披露知识产权管理体系及保护措施",
                mandatory=True,
                market_types=["科创板"],
            ),
            ComplianceItem(
                item_id="G006",
                category="治理(G)",
                subcategory="创新研发",
                requirement="科技创新成果",
                description="披露科技创新投入及成果转化",
                mandatory=True,
                market_types=["科创板"],
            ),
        ]
        
        rules.extend(env_rules)
        rules.extend(social_rules)
        rules.extend(governance_rules)
        
        return rules
    
    def check_compliance(
        self, 
        document_text: str, 
        company_name: str = "",
        market_type: str = "主板",
        industry: str = "电子"
    ) -> ComplianceReport:
        """
        执行合规性检查
        
        Args:
            document_text: 企业披露文档文本
            company_name: 公司名称
            market_type: 市场类型（主板/科创板/创业板）
            industry: 行业分类
            
        Returns:
            ComplianceReport: 合规检查报告
            
        Raises:
            ValueError: 当输入参数无效时
            TypeError: 当document_text不是字符串时
        """
        # 输入验证
        if not isinstance(document_text, str):
            raise TypeError(f"document_text必须是字符串，收到{type(document_text).__name__}")
        
        if not document_text.strip():
            raise ValueError("document_text不能为空或仅包含空白字符")
        
        valid_market_types = ["主板", "科创板", "创业板", "北交所"]
        if market_type not in valid_market_types:
            raise ValueError(f"market_type必须是以下之一: {valid_market_types}，收到'{market_type}'")
        
        # 筛选适用的规则
        applicable_rules = [
            rule for rule in self.rules 
            if market_type in rule.market_types
        ]
        
        if not applicable_rules:
            # 如果没有适用的规则，返回空报告
            return ComplianceReport(
                company_name=company_name,
                market_type=market_type,
                industry=industry,
                total_items=0,
                compliant_items=0,
                partial_items=0,
                non_compliant_items=0,
                missing_items=0,
                compliance_score=0.0,
                items=[],
                recommendations=["未找到适用的合规检查规则，请检查市场类型配置"],
            )
        
        # 检查每一项规则
        checked_items = []
        errors = []
        
        for rule in applicable_rules:
            try:
                status, evidence = self._check_item(rule, document_text)
                rule.status = status
                rule.evidence = evidence
                rule.recommendation = self._generate_recommendation(rule)
                checked_items.append(rule)
            except Exception as e:
                # 记录错误但继续处理其他规则
                errors.append(f"检查规则{rule.item_id}时出错: {str(e)}")
                rule.status = ComplianceStatus.MISSING
                rule.evidence = f"检查出错: {str(e)}"
                rule.recommendation = "请手动检查此项"
                checked_items.append(rule)
        
        # 统计结果
        compliant = sum(1 for item in checked_items if item.status == ComplianceStatus.COMPLIANT)
        partial = sum(1 for item in checked_items if item.status == ComplianceStatus.PARTIAL)
        non_compliant = sum(1 for item in checked_items if item.status == ComplianceStatus.NON_COMPLIANT)
        missing = sum(1 for item in checked_items if item.status == ComplianceStatus.MISSING)
        
        total = len(checked_items)
        score = (compliant * 1.0 + partial * 0.5) / total * 100 if total > 0 else 0
        
        # 生成改进建议
        recommendations = self._generate_recommendations(checked_items)
        
        # 如果有错误，添加到建议中
        if errors:
            recommendations.append(f"检查过程中遇到{len(errors)}个错误，建议检查输入文本格式")
        
        report = ComplianceReport(
            company_name=company_name,
            market_type=market_type,
            industry=industry,
            total_items=total,
            compliant_items=compliant,
            partial_items=partial,
            non_compliant_items=non_compliant,
            missing_items=missing,
            compliance_score=round(score, 2),
            items=checked_items,
            recommendations=recommendations,
        )
        
        return report
    
    def _check_item(
        self, 
        rule: ComplianceItem, 
        document_text: str
    ) -> Tuple[ComplianceStatus, str]:
        """
        检查单个合规项
        
        Args:
            rule: 合规检查规则
            document_text: 文档文本
            
        Returns:
            Tuple[ComplianceStatus, str]: (状态, 证据)
        """
        # 根据规则类型定义关键词和模式
        keyword_patterns = {
            "E001": r"温室气体|碳排放|CO2|二氧化碳.*?排放|量|数据",
            "E002": r"碳达峰|碳中和|双碳.*?目标|路径|计划",
            "E003": r"能源消耗|综合能耗|电力消耗|天然气消耗",
            "E004": r"水资源|用水量|节水措施",
            "E005": r"固废|废弃物|危险废物|处理",
            "E006": r"绿色技术|环保技术|节能技术.*?研发|投入",
            "S001": r"员工总数|员工人数|性别比例|学历构成",
            "S002": r"员工培训|培训投入|培训时长",
            "S003": r"安全生产|安全事故|安全投入",
            "S004": r"供应链|供应商.*?管理|ESG|审核",
            "S005": r"乡村振兴|扶贫|公益|捐赠",
            "S006": r"产品质量|质量管理体系|召回",
            "G001": r"董事会|ESG.*?治理|职责|架构",
            "G002": r"反腐败|反贿赂|商业道德|廉洁",
            "G003": r"数据安全|隐私保护|信息安全",
            "G004": r"ESG.*?披露|信息披露.*?制度",
            "G005": r"知识产权|专利|商标|著作权",
            "G006": r"科技创新|研发投入|成果转化",
        }
        
        pattern = keyword_patterns.get(rule.item_id, "")
        if not pattern:
            return ComplianceStatus.MISSING, "未找到匹配规则"
        
        # 使用正则表达式搜索
        matches = re.findall(pattern, document_text, re.IGNORECASE)
        
        if matches:
            evidence = "、".join(matches[:3])  # 取前3个匹配项
            # 根据匹配数量判断合规程度
            if len(matches) >= 2:
                return ComplianceStatus.COMPLIANT, evidence
            else:
                return ComplianceStatus.PARTIAL, evidence
        else:
            return ComplianceStatus.MISSING, "未找到相关内容"
    
    def _generate_recommendation(self, rule: ComplianceItem) -> str:
        """生成单个规则的改进建议"""
        recommendations = {
            "E001": "建议披露范围1和范围2温室气体排放数据，包括CO2、CH4等主要温室气体",
            "E002": "建议明确碳达峰、碳中和目标年份及实施路径，制定量化减排计划",
            "E003": "建议披露综合能源消耗总量、强度指标及同比变化情况",
            "E004": "建议披露水资源消耗总量、循环利用率及节水措施",
            "E005": "建议披露固体废弃物产生量、处理方式及资源化利用率",
            "E006": "科创板企业建议披露绿色技术研发投入金额、占比及成果",
            "S001": "建议披露员工总数、性别比例、年龄分布及学历构成",
            "S002": "建议披露员工培训投入、人均培训时长及培训覆盖率",
            "S003": "建议披露安全生产投入、安全事故率及应急管理措施",
            "S004": "建议建立供应商ESG评估体系，披露供应链管理措施",
            "S005": "建议披露乡村振兴投入金额、项目成效及受益人数",
            "S006": "建议披露产品质量管理体系、产品召回及客户投诉情况",
            "G001": "建议建立董事会层面的ESG治理架构，明确ESG职责分工",
            "G002": "建议披露反腐败、反贿赂政策及员工培训情况",
            "G003": "建议披露数据安全管理体系、隐私保护措施及安全事件情况",
            "G004": "建议建立ESG信息披露制度，明确披露流程和责任部门",
            "G005": "科创板企业建议披露知识产权管理体系、专利数量及保护措施",
            "G006": "科创板企业建议披露科技创新投入、研发人员占比及成果转化",
        }
        return recommendations.get(rule.item_id, "建议补充相关内容")
    
    def _generate_recommendations(self, items: List[ComplianceItem]) -> List[str]:
        """生成总体改进建议"""
        recommendations = []
        
        # 获取缺失和不合规的项目
        missing_items = [item for item in items if item.status == ComplianceStatus.MISSING]
        non_compliant_items = [item for item in items if item.status == ComplianceStatus.NON_COMPLIANT]
        
        if missing_items:
            recommendations.append(
                f"共有{len(missing_items)}项披露内容缺失，建议优先补充"
            )
        
        if non_compliant_items:
            recommendations.append(
                f"共有{len(non_compliant_items)}项披露内容不符合要求，建议进行整改"
            )
        
        # 按维度统计
        env_missing = [item for item in missing_items if item.category == "环境(E)"]
        social_missing = [item for item in missing_items if item.category == "社会(S)"]
        gov_missing = [item for item in missing_items if item.category == "治理(G)"]
        
        if env_missing:
            recommendations.append(
                f"环境(E)维度缺失{len(env_missing)}项，建议加强环境信息披露"
            )
        if social_missing:
            recommendations.append(
                f"社会(S)维度缺失{len(social_missing)}项，建议加强社会责任信息披露"
            )
        if gov_missing:
            recommendations.append(
                f"治理(G)维度缺失{len(gov_missing)}项，建议完善公司治理信息披露"
            )
        
        return recommendations
    
    def get_missing_items(self, report: ComplianceReport) -> List[ComplianceItem]:
        """获取缺失项列表"""
        return [item for item in report.items if item.status == ComplianceStatus.MISSING]
    
    def get_compliance_summary(self, report: ComplianceReport) -> Dict:
        """获取合规摘要"""
        return {
            "company_name": report.company_name,
            "market_type": report.market_type,
            "industry": report.industry,
            "compliance_score": report.compliance_score,
            "total_items": report.total_items,
            "compliant_items": report.compliant_items,
            "partial_items": report.partial_items,
            "non_compliant_items": report.non_compliant_items,
            "missing_items": report.missing_items,
        }
