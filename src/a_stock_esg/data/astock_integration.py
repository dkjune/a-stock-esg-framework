"""
A股数据集成模块
基于 simonlin1212/a-stock-data V3.2.1 的数据获取方案
7层架构 · 27端点 · 13数据源
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import time
import random
import requests


@dataclass
class StockBasicInfo:
    """股票基础信息"""
    stock_code: str
    stock_name: str
    industry: str
    market_type: str
    price: float = 0
    pe_ttm: float = 0
    pb: float = 0
    market_cap: float = 0
    float_market_cap: float = 0
    turnover_rate: float = 0
    change_pct: float = 0
    volume_ratio: float = 0


@dataclass
class FinancialData:
    """财务数据"""
    stock_code: str
    pe_ttm: float = 0
    pb: float = 0
    market_cap: float = 0
    eps: float = 0
    roe: float = 0
    revenue: float = 0
    net_profit: float = 0
    debt_ratio: float = 0


# ── 东财防封：全局节流 + 会话复用 ────────────────────────────────────
EM_SESSION = requests.Session()
EM_SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
})
EM_MIN_INTERVAL = 1.0  # 两次东财请求最小间隔(秒)
_em_last_call = [0.0]


def em_get(url: str, params: dict = None, headers: dict = None,
           timeout: int = 15, **kwargs):
    """东财统一请求入口：自动节流 + 复用 session + 默认 UA"""
    wait = EM_MIN_INTERVAL - (time.time() - _em_last_call[0])
    if wait > 0:
        time.sleep(wait + random.uniform(0.1, 0.5))
    try:
        return EM_SESSION.get(url, params=params, headers=headers, timeout=timeout, **kwargs)
    finally:
        _em_last_call[0] = time.time()


def get_prefix(code: str) -> str:
    """6位代码 → 市场前缀"""
    if code.startswith(("6", "9")):
        return "sh"
    elif code.startswith("8"):
        return "bj"
    else:
        return "sz"


class AStockDataIntegrator:
    """
    A股数据集成器
    
    基于 simonlin1212/a-stock-data V3.2.1
    优先使用mootdx/腾讯（不封IP），东财仅用于独有数据
    """
    
    def __init__(self):
        """初始化数据集成器"""
        self._check_dependencies()
    
    def _check_dependencies(self):
        """检查依赖是否安装"""
        required = ["requests"]
        optional = ["mootdx", "pandas", "stockstats"]
        
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                print(f"错误: 缺少必需依赖 {pkg}，请运行: pip install {pkg}")
        
        for pkg in optional:
            try:
                __import__(pkg)
            except ImportError:
                pass  # 静默处理可选依赖
    
    # ═══════════════════════════════════════════════════════════════════
    # Layer 1: 行情层（实时，不封IP）
    # ═══════════════════════════════════════════════════════════════════
    
    def tencent_quote(self, codes: List[str]) -> Dict[str, Dict]:
        """
        批量拉取腾讯财经实时行情（不封IP）
        
        Args:
            codes: 股票代码列表，如["600519", "000858"]
            
        Returns:
            Dict: {code: {name, price, pe_ttm, pb, mcap, ...}}
        """
        prefixed = []
        for c in codes:
            c = c.replace("SH", "").replace("sz", "").replace("SZ", "").split(".")[0]
            if c.startswith(("6", "9")):
                prefixed.append(f"sh{c}")
            elif c.startswith("8"):
                prefixed.append(f"bj{c}")
            else:
                prefixed.append(f"sz{c}")
        
        url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.read().decode("gbk") if hasattr(resp, 'read') else resp.text
            
            result = {}
            for line in data.strip().split(";"):
                if not line.strip() or "=" not in line or '"' not in line:
                    continue
                key = line.split("=")[0].split("_")[-1]
                vals = line.split('"')[1].split("~")
                if len(vals) < 53:
                    continue
                code = key[2:]
                result[code] = {
                    "name": vals[1],
                    "price": float(vals[3]) if vals[3] else 0,
                    "last_close": float(vals[4]) if vals[4] else 0,
                    "change_pct": float(vals[32]) if vals[32] else 0,
                    "pe_ttm": float(vals[39]) if vals[39] else 0,
                    "mcap_yi": float(vals[44]) if vals[44] else 0,
                    "float_mcap_yi": float(vals[45]) if vals[45] else 0,
                    "pb": float(vals[46]) if vals[46] else 0,
                    "turnover_pct": float(vals[38]) if vals[38] else 0,
                    "vol_ratio": float(vals[49]) if vals[49] else 0,
                }
            return result
        except Exception as e:
            print(f"腾讯API请求失败: {e}")
            return {}
    
    def get_stock_info(self, stock_code: str) -> Optional[StockBasicInfo]:
        """
        获取股票基础信息
        
        Args:
            stock_code: 股票代码，如"600519"
            
        Returns:
            Optional[StockBasicInfo]: 股票信息
        """
        if not isinstance(stock_code, str):
            raise TypeError(f"stock_code必须是字符串")
        
        stock_code = stock_code.replace("SH", "").replace("sz", "").replace("SZ", "").split(".")[0]
        
        if not stock_code.isdigit() or len(stock_code) != 6:
            raise ValueError(f"stock_code必须是6位数字，收到'{stock_code}'")
        
        try:
            quotes = self.tencent_quote([stock_code])
            if stock_code in quotes:
                q = quotes[stock_code]
                
                # 确定市场类型
                if stock_code.startswith("6"):
                    market_type = "主板"
                elif stock_code.startswith("002"):
                    market_type = "中小板"
                elif stock_code.startswith("300"):
                    market_type = "创业板"
                elif stock_code.startswith("688"):
                    market_type = "科创板"
                else:
                    market_type = "主板"
                
                return StockBasicInfo(
                    stock_code=stock_code,
                    stock_name=q.get("name", ""),
                    industry="",
                    market_type=market_type,
                    price=q.get("price", 0),
                    pe_ttm=q.get("pe_ttm", 0),
                    pb=q.get("pb", 0),
                    market_cap=q.get("mcap_yi", 0),
                    float_market_cap=q.get("float_mcap_yi", 0),
                    turnover_rate=q.get("turnover_pct", 0),
                    change_pct=q.get("change_pct", 0),
                    volume_ratio=q.get("vol_ratio", 0),
                )
            return None
        except Exception as e:
            print(f"获取股票信息失败: {e}")
            return None
    
    def get_financial_data(self, stock_code: str) -> Optional[FinancialData]:
        """
        获取财务数据
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Optional[FinancialData]: 财务数据
        """
        stock_code = stock_code.replace("SH", "").replace("sz", "").replace("SZ", "").split(".")[0]
        
        if not stock_code.isdigit() or len(stock_code) != 6:
            raise ValueError(f"stock_code必须是6位数字")
        
        try:
            quotes = self.tencent_quote([stock_code])
            if stock_code in quotes:
                q = quotes[stock_code]
                return FinancialData(
                    stock_code=stock_code,
                    pe_ttm=q.get("pe_ttm", 0),
                    pb=q.get("pb", 0),
                    market_cap=q.get("mcap_yi", 0),
                )
            return None
        except Exception as e:
            print(f"获取财务数据失败: {e}")
            return None
    
    # ═══════════════════════════════════════════════════════════════════
    # Layer 2: 研报层
    # ═══════════════════════════════════════════════════════════════════
    
    def get_research_reports(self, stock_code: str, max_pages: int = 3) -> List[Dict]:
        """
        获取个股研报列表（东财reportapi）
        
        Args:
            stock_code: 股票代码
            max_pages: 最大页数
            
        Returns:
            List[Dict]: 研报列表
        """
        REPORT_API = "https://reportapi.eastmoney.com/report/list"
        all_records = []
        
        for page in range(1, max_pages + 1):
            params = {
                "industryCode": "*", "pageSize": "100", "industry": "*",
                "rating": "*", "ratingChange": "*",
                "beginTime": "2000-01-01", "endTime": "2030-01-01",
                "pageNo": str(page), "fields": "", "qType": "0",
                "orgCode": "", "code": stock_code, "rcode": "",
                "p": str(page), "pageNum": str(page), "pageNumber": str(page),
            }
            try:
                r = em_get(REPORT_API, params=params,
                          headers={"Referer": "https://data.eastmoney.com/"}, timeout=30)
                d = r.json()
                rows = d.get("data") or []
                if not rows:
                    break
                all_records.extend(rows)
                if page >= (d.get("TotalPage", 1) or 1):
                    break
            except Exception as e:
                print(f"获取研报失败: {e}")
                break
        
        return [{
            "title": r.get("title", ""),
            "date": (r.get("publishDate") or "")[:10],
            "org": r.get("orgSName", ""),
            "rating": r.get("emRatingName", ""),
            "eps_this_year": r.get("predictThisYearEps"),
            "eps_next_year": r.get("predictNextYearEps"),
        } for r in all_records]
    
    # ═══════════════════════════════════════════════════════════════════
    # Layer 3: 信号层
    # ═══════════════════════════════════════════════════════════════════
    
    def get_concept_blocks(self, stock_code: str) -> Dict:
        """
        获取个股概念板块归属（百度股市通）
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Dict: 行业/概念/地域分类
        """
        BAIDU_HEADERS = {
            "Host": "finance.pae.baidu.com",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/vnd.finance-web.v1+json",
            "Origin": "https://gushitong.baidu.com",
            "Referer": "https://gushitong.baidu.com/",
        }
        
        url = f"https://finance.pae.baidu.com/api/getrelatedblock?code={stock_code}&market=ab&typeCode=all&finClientType=pc"
        
        try:
            r = requests.get(url, headers=BAIDU_HEADERS, timeout=10)
            d = r.json()
            
            if str(d.get("ResultCode", -1)) != "0":
                return {"industry": [], "concept": [], "region": []}
            
            result = {"industry": [], "concept": [], "region": []}
            for block in d.get("Result", []):
                block_type = block.get("type", "")
                for item in block.get("list", []):
                    entry = {
                        "name": item.get("name", ""),
                        "change_pct": item.get("increase", ""),
                    }
                    if "行业" in block_type:
                        result["industry"].append(entry)
                    elif "概念" in block_type:
                        result["concept"].append(entry)
                    elif "地域" in block_type:
                        result["region"].append(entry)
            
            return result
        except Exception as e:
            print(f"获取概念板块失败: {e}")
            return {"industry": [], "concept": [], "region": []}
    
    def get_fund_flow_minute(self, stock_code: str) -> List[Dict]:
        """
        获取个股资金流向（分钟级，东财push2）
        
        Args:
            stock_code: 股票代码
            
        Returns:
            List[Dict]: 资金流向数据
        """
        secid = f"1.{stock_code}" if stock_code.startswith("6") else f"0.{stock_code}"
        url = "https://push2.eastmoney.com/api/qt/stock/fflow/kline/get"
        params = {
            "secid": secid, "klt": 1,
            "fields1": "f1,f2,f3,f7",
            "fields2": "f51,f52,f53,f54,f55,f56,f57",
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://quote.eastmoney.com/",
        }
        
        try:
            r = em_get(url, params=params, headers=headers, timeout=10)
            d = r.json()
            
            rows = []
            for line in d.get("data", {}).get("klines", []):
                parts = line.split(",")
                if len(parts) >= 6:
                    rows.append({
                        "time": parts[0],
                        "main_net": float(parts[1]),
                        "small_net": float(parts[2]),
                        "mid_net": float(parts[3]),
                        "large_net": float(parts[4]),
                        "super_net": float(parts[5]),
                    })
            return rows
        except Exception as e:
            print(f"获取资金流向失败: {e}")
            return []
    
    def get_dragon_tiger(self, stock_code: str, trade_date: str) -> Dict:
        """
        获取龙虎榜数据
        
        Args:
            stock_code: 股票代码
            trade_date: 交易日期 YYYY-MM-DD
            
        Returns:
            Dict: 龙虎榜数据
        """
        DATACENTER_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        
        params = {
            "reportName": "RPT_DAILYBILLBOARD_DETAILSNEW",
            "columns": "ALL",
            "filter": f"(TRADE_DATE>='{trade_date}')(TRADE_DATE<='{trade_date}')(SECURITY_CODE=\"{stock_code}\")",
            "pageNumber": "1",
            "pageSize": "50",
            "sortColumns": "BILLBOARD_NET_AMT",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
        }
        
        try:
            r = em_get(DATACENTER_URL, params=params, timeout=15)
            d = r.json()
            
            if d.get("result") and d["result"].get("data"):
                data = d["result"]["data"]
                return {
                    "records": [{
                        "date": str(row.get("TRADE_DATE", ""))[:10],
                        "reason": row.get("EXPLANATION", ""),
                        "net_buy": round((row.get("BILLBOARD_NET_AMT") or 0) / 10000, 1),
                        "turnover": round(float(row.get("TURNOVERRATE") or 0), 2),
                    } for row in data]
                }
            return {"records": []}
        except Exception as e:
            print(f"获取龙虎榜失败: {e}")
            return {"records": []}
    
    # ═══════════════════════════════════════════════════════════════════
    # Layer 4: 资金面/筹码层
    # ═══════════════════════════════════════════════════════════════════
    
    def get_margin_trading(self, stock_code: str, page_size: int = 30) -> List[Dict]:
        """
        获取融资融券明细
        
        Args:
            stock_code: 股票代码
            page_size: 返回条数
            
        Returns:
            List[Dict]: 融资融券数据
        """
        DATACENTER_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        
        params = {
            "reportName": "RPTA_WEB_RZRQ_GGMX",
            "columns": "ALL",
            "filter": f'(SCODE="{stock_code}")',
            "pageNumber": "1",
            "pageSize": str(page_size),
            "sortColumns": "DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
        }
        
        try:
            r = em_get(DATACENTER_URL, params=params, timeout=15)
            d = r.json()
            
            if d.get("result") and d["result"].get("data"):
                return [{
                    "date": str(row.get("DATE", ""))[:10],
                    "rzye": row.get("RZYE", 0),
                    "rzmre": row.get("RZMRE", 0),
                    "rqye": row.get("RQYE", 0),
                } for row in d["result"]["data"]]
            return []
        except Exception as e:
            print(f"获取融资融券失败: {e}")
            return []
    
    def get_shareholder_count(self, stock_code: str) -> List[Dict]:
        """
        获取股东户数变化
        
        Args:
            stock_code: 股票代码
            
        Returns:
            List[Dict]: 股东户数数据
        """
        DATACENTER_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        
        params = {
            "reportName": "RPT_F10_EH_HOLDERSCOMP",
            "columns": "ALL",
            "filter": f'(SECURITY_CODE="{stock_code}")',
            "pageNumber": "1",
            "pageSize": "10",
            "sortColumns": "END_DATE",
            "sortTypes": "-1",
            "source": "WEB",
            "client": "WEB",
        }
        
        try:
            r = em_get(DATACENTER_URL, params=params, timeout=15)
            d = r.json()
            
            if d.get("result") and d["result"].get("data"):
                return [{
                    "date": str(row.get("END_DATE", ""))[:10],
                    "holder_count": row.get("HOLDER_NUM", 0),
                    "change_rate": row.get("HOLDER_NUM_CHANGE_RATE", 0),
                    "avg_shares": row.get("AVG_FREE_SHARES", 0),
                } for row in d["result"]["data"]]
            return []
        except Exception as e:
            print(f"获取股东户数失败: {e}")
            return []
    
    # ═══════════════════════════════════════════════════════════════════
    # Layer 5: 新闻层
    # ═══════════════════════════════════════════════════════════════════
    
    def get_stock_news(self, stock_code: str, page_size: int = 20) -> List[Dict]:
        """
        获取个股新闻（东财search-api-web）
        
        Args:
            stock_code: 股票代码
            page_size: 返回条数
            
        Returns:
            List[Dict]: 新闻列表
        """
        url = "https://search-api-web.eastmoney.com/search/jsonp"
        params = {
            "cb": "jQuery",
            "param": f'{{"uid":"","keyword":"{stock_code}","type":["cmsArticleWebOld"],"client":"web","clientType":"web","clientVersion":"curr","param":{{"cmsArticleWebOld":{{"searchScope":"default","sort":"default","pageIndex":1,"pageSize":{page_size},"preTag":"<em>","postTag":"</em>"}}}}}}',
        }
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://so.eastmoney.com/",
        }
        
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            text = r.text
            
            # 解析JSONP
            if "(" in text:
                json_str = text[text.index("(") + 1:text.rindex(")")]
                import json
                d = json.loads(json_str)
                
                articles = d.get("result", {}).get("cmsArticleWebOld", {}).get("list", [])
                return [{
                    "title": a.get("title", "").replace("<em>", "").replace("</em>", ""),
                    "date": a.get("date", ""),
                    "source": a.get("mediaName", ""),
                    "url": a.get("url", ""),
                } for a in articles]
            return []
        except Exception as e:
            print(f"获取新闻失败: {e}")
            return []
    
    # ═══════════════════════════════════════════════════════════════════
    # 辅助方法
    # ═══════════════════════════════════════════════════════════════════
    
    def batch_get_quotes(self, stock_codes: List[str]) -> Dict[str, Dict]:
        """
        批量获取股票行情
        
        Args:
            stock_codes: 股票代码列表
            
        Returns:
            Dict: {code: quote_data}
        """
        return self.tencent_quote(stock_codes)
    
    def get_industry_stocks(self, industry: str) -> List[str]:
        """获取行业股票列表（示例）"""
        industry_map = {
            "银行": ["601398", "601939", "601288", "600036", "600016"],
            "电力": ["600886", "600863", "600011", "600900", "601985"],
            "白酒": ["600519", "000858", "000568", "002304", "600809"],
        }
        return industry_map.get(industry, [])
    
    def get_company_filings(self, stock_code: str, filing_type: str = "ESG") -> List[Dict]:
        """获取公司公告（巨潮）"""
        # 简化实现，实际应调用巨潮API
        return []
