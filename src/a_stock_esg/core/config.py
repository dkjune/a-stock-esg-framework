"""
A股ESG框架配置模块
定义A股监管规则、行业分类、数据源配置等
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class MarketType(Enum):
    """A股市场类型"""
    MAIN_BOARD = "主板"
    STAR_BOARD = "科创板"
    GEM = "创业板"
    BSE = "北交所"


class IndustryClassification(Enum):
    """行业分类（申万一级）"""
    BANKING = "银行"
    SECURITIES = "证券"
    INSURANCE = "保险"
    REAL_ESTATE = "房地产"
    CONSTRUCTION = "建筑"
    BUILDING_MATERIALS = "建筑材料"
    CHEMICAL = "化工"
    STEEL = "钢铁"
    NONFERROUS_METALS = "有色金属"
    ELECTRONICS = "电子"
    COMPUTER = "计算机"
    COMMUNICATION = "通信"
    MEDIA = "传媒"
    PHARMACEUTICAL = "医药生物"
    FOOD_BEVERAGE = "食品饮料"
    TEXTILE_CLOTHING = "纺织服饰"
    LIGHT_INDUSTRIY = "轻工制造"
    AUTOMOBILE = "汽车"
    HOUSEHOLD_APPLIANCES = "家用电器"
    MECHANICAL_EQUIPMENT = "机械设备"
    UTILITIES = "公用事业"
    TRANSPORTATION = "交通运输"
    COAL = "煤炭"
    PETROLEUM = "石油石化"
    AGRICULTURE = "农林牧渔"
    MILITARY = "国防军工"


@dataclass
class DisclosureRequirements:
    """披露要求配置"""
    mandatory_items: List[str] = field(default_factory=list)
    recommended_items: List[str] = field(default_factory=list)
    conditional_items: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class AStockESGConfig:
    """A股ESG框架主配置"""
    
    # 市场配置
    market_type: MarketType = MarketType.MAIN_BOARD
    industry: IndustryClassification = IndustryClassification.ELECTRONICS
    
    # 监管规则配置
    csrc_guidelines_version: str = "2024"
    exchange_rules_version: str = "2024"
    
    # 数据源配置
    data_sources: Dict[str, str] = field(default_factory=lambda: {
        "annual_report": "年报",
        "semi_annual_report": "半年报",
        "esg_report": "ESG报告",
        "social_responsibility_report": "社会责任报告",
        "sustainability_report": "可持续发展报告",
    })
    
    # ESG评级机构配置
    rating_agencies: List[str] = field(default_factory=lambda: [
        "中证ESG",
        "华证ESG",
        "商道融绿",
        "Wind ESG",
    ])
    
    # 披露维度配置
    disclosure_dimensions: Dict[str, List[str]] = field(default_factory=lambda: {
        "环境(E)": [
            "碳排放",
            "能源消耗",
            "水资源管理",
            "废弃物处理",
            "生物多样性",
            "绿色采购",
        ],
        "社会(S)": [
            "员工权益",
            "安全生产",
            "产品质量",
            "供应链管理",
            "社区关系",
            "乡村振兴",
        ],
        "治理(G)": [
            "董事会结构",
            "商业道德",
            "数据安全",
            "知识产权",
            "反腐败",
            "信息披露",
        ],
    })
    
    # 科创板/创业板特殊要求
    star_gem_requirements: Dict[str, List[str]] = field(default_factory=lambda: {
        "科创板": [
            "绿色技术研发投入",
            "科技创新成果",
            "知识产权保护",
            "核心技术自主可控",
        ],
        "创业板": [
            "成长性指标",
            "创新研发投入",
            "新旧动能转换",
        ],
    })
    
    # 双碳目标配置
    dual_carbon_config: Dict[str, any] = field(default_factory=lambda: {
        "peak_carbon_year": 2030,
        "carbon_neutral_year": 2060,
        "scope1_required": True,
        "scope2_required": True,
        "scope3_recommended": True,
    })
    
    def get_disclosure_requirements(self) -> DisclosureRequirements:
        """获取当前市场和行业的披露要求"""
        requirements = DisclosureRequirements()
        
        # 基础披露要求（所有A股上市公司）
        requirements.mandatory_items = [
            "环境管理目标",
            "碳排放数据",
            "能源消耗情况",
            "员工人数及构成",
            "安全生产情况",
            "董事会ESG职责",
            "商业道德政策",
        ]
        
        # 推荐披露项
        requirements.recommended_items = [
            "Scope 3碳排放",
            "供应链ESG管理",
            "生物多样性保护",
            "社区投资",
            "妇女儿童权益保护",
        ]
        
        # 条件披露项（根据市场类型）
        if self.market_type in [MarketType.STAR_BOARD, MarketType.GEM]:
            requirements.conditional_items = self.star_gem_requirements.get(
                self.market_type.value, []
            )
        
        return requirements
    
    def get_industry_focus(self) -> Dict[str, List[str]]:
        """获取行业重点关注领域"""
        industry_focus = {
            IndustryClassification.BANKING: ["绿色金融", "普惠金融", "消费者权益保护"],
            IndustryClassification.SECURITIES: ["投资者保护", "信息安全管理"],
            IndustryClassification.INSURANCE: ["保险赔付", "客户隐私保护"],
            IndustryClassification.REAL_ESTATE: ["绿色建筑", "物业管理", "业主权益"],
            IndustryClassification.CHEMICAL: ["安全生产", "污染排放", "职业健康"],
            IndustryClassification.STEEL: ["碳排放", "能源消耗", "废弃物处理"],
            IndustryClassification.ELECTRONICS: ["有害物质管理", "电子废弃物回收"],
        }
        return industry_focus.get(self.industry, [])
    
    def validate(self) -> List[str]:
        """
        验证配置有效性
        
        Returns:
            List[str]: 错误列表，空列表表示配置有效
        """
        errors = []
        
        # 验证市场类型
        if not isinstance(self.market_type, MarketType):
            errors.append(f"market_type必须是MarketType枚举类型，收到{type(self.market_type).__name__}")
        
        # 验证行业分类
        if not isinstance(self.industry, IndustryClassification):
            errors.append(f"industry必须是IndustryClassification枚举类型，收到{type(self.industry).__name__}")
        
        # 验证监管规则版本格式
        import re
        version_pattern = r"^\d{4}$"
        if not re.match(version_pattern, self.csrc_guidelines_version):
            errors.append(f"csrc_guidelines_version格式无效，应为4位数字年份，收到'{self.csrc_guidelines_version}'")
        if not re.match(version_pattern, self.exchange_rules_version):
            errors.append(f"exchange_rules_version格式无效，应为4位数字年份，收到'{self.exchange_rules_version}'")
        
        # 验证数据源配置
        if not isinstance(self.data_sources, dict):
            errors.append(f"data_sources必须是字典类型，收到{type(self.data_sources).__name__}")
        elif len(self.data_sources) == 0:
            errors.append("data_sources不能为空")
        
        # 验证评级机构配置
        if not isinstance(self.rating_agencies, list):
            errors.append(f"rating_agencies必须是列表类型，收到{type(self.rating_agencies).__name__}")
        elif len(self.rating_agencies) == 0:
            errors.append("rating_agencies不能为空列表")
        
        # 验证双碳配置
        if not isinstance(self.dual_carbon_config, dict):
            errors.append(f"dual_carbon_config必须是字典类型，收到{type(self.dual_carbon_config).__name__}")
        else:
            if "peak_carbon_year" in self.dual_carbon_config:
                peak_year = self.dual_carbon_config["peak_carbon_year"]
                if not isinstance(peak_year, int) or peak_year < 2020 or peak_year > 2050:
                    errors.append(f"peak_carbon_year应在2020-2050之间，收到{peak_year}")
            
            if "carbon_neutral_year" in self.dual_carbon_config:
                neutral_year = self.dual_carbon_config["carbon_neutral_year"]
                if not isinstance(neutral_year, int) or neutral_year < 2040 or neutral_year > 2100:
                    errors.append(f"carbon_neutral_year应在2040-2100之间，收到{neutral_year}")
        
        return errors
    
    @classmethod
    def create_validated(
        cls,
        market_type: MarketType = MarketType.MAIN_BOARD,
        industry: IndustryClassification = IndustryClassification.ELECTRONICS,
        **kwargs
    ) -> "AStockESGConfig":
        """
        创建并验证配置
        
        Args:
            market_type: 市场类型
            industry: 行业分类
            **kwargs: 其他配置参数
            
        Returns:
            AStockESGConfig: 验证通过的配置对象
            
        Raises:
            ValueError: 当配置验证失败时
        """
        config = cls(market_type=market_type, industry=industry, **kwargs)
        errors = config.validate()
        
        if errors:
            error_msg = "配置验证失败:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValueError(error_msg)
        
        return config
