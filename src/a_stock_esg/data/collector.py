"""
A股数据源层
处理企业内部数据、监管标准数据、行业对标数据、第三方数据
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from datetime import datetime
from pathlib import Path
import json


@dataclass
class CompanyInfo:
    """公司基本信息"""
    stock_code: str  # 股票代码
    company_name: str  # 公司名称
    market_type: str  # 市场类型：主板/科创板/创业板/北交所
    industry: str  # 行业分类
    list_date: Optional[str] = None  # 上市日期
    total_shareholders: Optional[int] = None  # 股东总数


@dataclass
class ESGDisclosure:
    """ESG披露信息"""
    company_code: str
    disclosure_type: str  # 年报/ESG报告/社会责任报告
    disclosure_date: str
    year: int
    content: Dict[str, any] = field(default_factory=dict)
    compliance_score: Optional[float] = None


@dataclass
class IndustryBenchmark:
    """行业对标数据"""
    industry: str
    market_type: str
    year: int
    average_score: float
    top_performers: List[str] = field(default_factory=list)
    disclosure_items: Dict[str, float] = field(default_factory=dict)


@dataclass
class RegulatoryStandard:
    """监管标准"""
    standard_id: str
    name: str
    issuer: str  # 发布机构
    effective_date: str
    requirements: List[str] = field(default_factory=list)
    market_types: List[str] = field(default_factory=list)


class DataCollector:
    """
    A股数据收集器
    
    整合企业内部数据、监管标准数据、行业对标数据、第三方数据
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化数据收集器
        
        Args:
            data_dir: 数据目录路径
        """
        self.data_dir = Path(data_dir) if data_dir else Path("data")
        self.companies: Dict[str, CompanyInfo] = {}
        self.disclosures: Dict[str, List[ESGDisclosure]] = {}
        self.benchmarks: Dict[str, IndustryBenchmark] = {}
        self.standards: Dict[str, RegulatoryStandard] = {}
        
        # 初始化监管标准
        self._init_regulatory_standards()
    
    def _init_regulatory_standards(self):
        """初始化A股监管标准"""
        self.standards = {
            "SZSE_2024": RegulatoryStandard(
                standard_id="SZSE_2024",
                name="深圳证券交易所上市公司自律监管指引第1号——主板上市公司规范运作",
                issuer="深圳证券交易所",
                effective_date="2024-01-01",
                requirements=[
                    "环境管理目标",
                    "碳排放数据",
                    "能源消耗情况",
                    "员工权益保护",
                    "安全生产管理",
                    "商业道德政策",
                ],
                market_types=["主板"],
            ),
            "SSE_STAR_2024": RegulatoryStandard(
                standard_id="SSE_STAR_2024",
                name="上海证券交易所科创板上市公司自律监管指引第11号——信息披露",
                issuer="上海证券交易所",
                effective_date="2024-01-01",
                requirements=[
                    "绿色技术研发投入",
                    "科技创新成果",
                    "知识产权保护",
                    "核心技术自主可控",
                ],
                market_types=["科创板"],
            ),
            "CSRC_ESG_2024": RegulatoryStandard(
                standard_id="CSRC_ESG_2024",
                name="上市公司ESG信息披露指引",
                issuer="中国证券监督管理委员会",
                effective_date="2024-01-01",
                requirements=[
                    "ESG治理架构",
                    "环境绩效指标",
                    "社会责任履行",
                    "公司治理结构",
                ],
                market_types=["主板", "科创板", "创业板", "北交所"],
            ),
        }
    
    def add_company(self, company: CompanyInfo):
        """添加公司信息"""
        self.companies[company.stock_code] = company
    
    def add_disclosure(self, disclosure: ESGDisclosure):
        """添加披露信息"""
        if disclosure.company_code not in self.disclosures:
            self.disclosures[disclosure.company_code] = []
        self.disclosures[disclosure.company_code].append(disclosure)
    
    def add_benchmark(self, benchmark: IndustryBenchmark):
        """添加行业对标数据"""
        key = f"{benchmark.industry}_{benchmark.market_type}_{benchmark.year}"
        self.benchmarks[key] = benchmark
    
    def load_data_from_file(self, file_path: str):
        """从文件加载数据"""
        path = Path(file_path)
        
        if path.suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._process_loaded_data(data)
        elif path.suffix == ".csv":
            import pandas as pd
            df = pd.read_csv(path, encoding="utf-8")
            self._process_dataframe(df)
    
    def _process_loaded_data(self, data: Dict):
        """处理加载的数据"""
        if "companies" in data:
            for company_data in data["companies"]:
                company = CompanyInfo(**company_data)
                self.add_company(company)
        
        if "disclosures" in data:
            for disc_data in data["disclosures"]:
                disclosure = ESGDisclosure(**disc_data)
                self.add_disclosure(disclosure)
    
    def _process_dataframe(self, df):
        """处理DataFrame数据"""
        # 根据DataFrame列名自动识别数据类型
        if "stock_code" in df.columns and "company_name" in df.columns:
            for _, row in df.iterrows():
                company = CompanyInfo(
                    stock_code=row["stock_code"],
                    company_name=row["company_name"],
                    market_type=row.get("market_type", "主板"),
                    industry=row.get("industry", "电子"),
                )
                self.add_company(company)
    
    def get_company_info(self, stock_code: str) -> Optional[CompanyInfo]:
        """获取公司信息"""
        return self.companies.get(stock_code)
    
    def get_company_disclosures(
        self, 
        stock_code: str, 
        year: Optional[int] = None
    ) -> List[ESGDisclosure]:
        """获取公司披露信息"""
        disclosures = self.disclosures.get(stock_code, [])
        
        if year:
            disclosures = [d for d in disclosures if d.year == year]
        
        return disclosures
    
    def get_industry_benchmark(
        self, 
        industry: str, 
        market_type: str, 
        year: int
    ) -> Optional[IndustryBenchmark]:
        """获取行业对标数据"""
        key = f"{industry}_{market_type}_{year}"
        return self.benchmarks.get(key)
    
    def get_regulatory_standard(
        self, 
        market_type: str
    ) -> List[RegulatoryStandard]:
        """获取适用的监管标准"""
        standards = []
        for standard in self.standards.values():
            if market_type in standard.market_types:
                standards.append(standard)
        return standards
    
    def export_data(self, output_path: str):
        """导出数据"""
        data = {
            "companies": [
                {
                    "stock_code": c.stock_code,
                    "company_name": c.company_name,
                    "market_type": c.market_type,
                    "industry": c.industry,
                }
                for c in self.companies.values()
            ],
            "disclosures": [
                {
                    "company_code": d.company_code,
                    "disclosure_type": d.disclosure_type,
                    "disclosure_date": d.disclosure_date,
                    "year": d.year,
                    "content": d.content,
                }
                for disclosures in self.disclosures.values()
                for d in disclosures
            ],
            "standards": {
                k: {
                    "standard_id": v.standard_id,
                    "name": v.name,
                    "issuer": v.issuer,
                    "effective_date": v.effective_date,
                    "requirements": v.requirements,
                    "market_types": v.market_types,
                }
                for k, v in self.standards.items()
            },
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_data_summary(self) -> Dict:
        """获取数据摘要"""
        return {
            "total_companies": len(self.companies),
            "total_disclosures": sum(len(d) for d in self.disclosures.values()),
            "total_benchmarks": len(self.benchmarks),
            "total_standards": len(self.standards),
            "market_types": list(set(c.market_type for c in self.companies.values())),
            "industries": list(set(c.industry for c in self.companies.values())),
        }
