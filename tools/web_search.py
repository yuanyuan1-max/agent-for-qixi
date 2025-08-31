"""
网络搜索工具模块
"""
import re
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, quote
import requests
from bs4 import BeautifulSoup

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class WebSearchTool:
    """网络搜索工具类"""
    
    def __init__(self):
        self.search_engine = "baidu"  # 改为百度搜索
        self.max_results = settings.MAX_SEARCH_RESULTS
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search(self, query: str, max_results: int = None) -> List[Dict[str, Any]]:
        """执行网络搜索"""
        try:
            max_results = max_results or self.max_results
            logger.info(f"开始搜索: {query}")
            
            if self.search_engine == "baidu":
                results = self._search_baidu(query, max_results)
            else:
                results = self._search_baidu(query, max_results)  # 默认使用百度
            
            # 过滤和清理结果
            cleaned_results = self._clean_search_results(results)
            
            logger.info(f"搜索完成，获得{len(cleaned_results)}个结果")
            return cleaned_results
            
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return []
    
    def _search_baidu(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """使用百度搜索"""
        try:
            # 构建搜索URL
            search_query = f"{query} 七夕 约会 浪漫 情侣"
            encoded_query = quote(search_query)
            search_url = f"https://www.baidu.com/s?wd={encoded_query}&rn={max_results}"
            
            logger.info(f"百度搜索URL: {search_url}")
            
            # 发送请求
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取搜索结果
            results = []
            search_results = soup.find_all('div', class_='result')
            
            for result in search_results[:max_results]:
                try:
                    # 提取标题
                    title_elem = result.find('h3')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # 提取链接
                    link_elem = title_elem.find('a')
                    if not link_elem:
                        continue
                    
                    url = link_elem.get('href', '')
                    
                    # 提取摘要
                    abstract_elem = result.find('div', class_='c-abstract')
                    if abstract_elem:
                        snippet = abstract_elem.get_text(strip=True)
                    else:
                        snippet = "暂无摘要"
                    
                    if title and snippet:
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'url': url,
                            'source': 'baidu'
                        })
                        
                except Exception as e:
                    logger.warning(f"解析搜索结果失败: {e}")
                    continue
            
            # 如果没有找到结果，尝试其他方法
            if not results:
                logger.info("标准解析未找到结果，尝试备用方法...")
                results = self._search_baidu_fallback(response.content, max_results)
            
            logger.info(f"百度搜索找到{len(results)}个结果")
            return results
            
        except Exception as e:
            logger.error(f"百度搜索失败: {e}")
            return []
    
    def _search_baidu_fallback(self, html_content: str, max_results: int) -> List[Dict[str, Any]]:
        """百度搜索备用解析方法"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            results = []
            
            # 查找所有可能包含搜索结果的div
            possible_results = soup.find_all('div', class_=lambda x: x and ('result' in x or 'c-container' in x))
            
            for result in possible_results[:max_results]:
                try:
                    # 查找标题
                    title_elem = result.find(['h3', 'h2', 'a'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    if not title or len(title) < 5:
                        continue
                    
                    # 查找链接
                    link_elem = result.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    
                    # 查找摘要
                    snippet = ""
                    abstract_selectors = ['.c-abstract', '.content', 'p', '.summary']
                    for selector in abstract_selectors:
                        abstract_elem = result.select_one(selector)
                        if abstract_elem:
                            snippet = abstract_elem.get_text(strip=True)
                            break
                    
                    if not snippet:
                        # 如果没有找到摘要，使用其他文本内容
                        text_content = result.get_text(strip=True)
                        if len(text_content) > len(title):
                            snippet = text_content[:200] + "..."
                    
                    if title and snippet:
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'url': url,
                            'source': 'baidu_fallback'
                        })
                        
                except Exception as e:
                    logger.warning(f"备用解析失败: {e}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"备用解析失败: {e}")
            return []
    
    def _clean_search_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """清理和过滤搜索结果"""
        cleaned_results = []
        
        for result in results:
            # 检查是否包含约会相关内容
            if self._is_relevant_content(result):
                # 清理文本
                cleaned_title = self._clean_text(result.get('title', ''))
                cleaned_snippet = self._clean_text(result.get('snippet', ''))
                
                if cleaned_title and cleaned_snippet:
                    cleaned_results.append({
                        'title': cleaned_title,
                        'snippet': cleaned_snippet,
                        'url': result.get('url', ''),
                        'source': result.get('source', 'unknown'),
                        'relevance_score': self._calculate_relevance(result)
                    })
        
        # 按相关性排序
        cleaned_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return cleaned_results
    
    def _is_relevant_content(self, result: Dict[str, Any]) -> bool:
        """检查内容是否相关"""
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        
        # 约会相关关键词
        dating_keywords = [
            '约会', '浪漫', '情侣', '七夕', '情人节', '爱情', '恋爱',
            '餐厅', '电影', '礼物', '惊喜', '烛光晚餐', '花束',
            '约会地点', '约会活动', '约会攻略', '约会建议'
        ]
        
        # 检查是否包含相关关键词
        for keyword in dating_keywords:
            if keyword in title or keyword in snippet:
                return True
        
        return False
    
    def _clean_text(self, text: str) -> str:
        """清理文本内容"""
        if not text:
            return ""
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', '', text)
        
        return text.strip()
    
    def _calculate_relevance(self, result: Dict[str, Any]) -> float:
        """计算内容相关性分数"""
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        
        score = 0.0
        
        # 标题权重更高
        if '约会' in title:
            score += 3.0
        if '七夕' in title:
            score += 2.5
        if '浪漫' in title:
            score += 2.0
        if '情侣' in title:
            score += 1.5
        
        # 内容权重
        if '约会' in snippet:
            score += 2.0
        if '七夕' in snippet:
            score += 1.5
        if '浪漫' in snippet:
            score += 1.0
        if '情侣' in snippet:
            score += 1.0
        
        # 来源权重
        if result.get('source') == 'baidu':
            score += 0.5
        
        return score
    
    def extract_content_from_url(self, url: str) -> Optional[str]:
        """从URL提取内容"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 移除脚本和样式标签
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 提取文本内容
            text = soup.get_text()
            
            # 清理文本
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # 限制长度
            if len(text) > 2000:
                text = text[:2000] + "..."
            
            return text
            
        except Exception as e:
            logger.error(f"从URL提取内容失败: {e}")
            return None
    
    def search_dating_ideas(self, query: str) -> List[Dict[str, Any]]:
        """搜索约会创意"""
        try:
            # 构建约会相关的搜索查询
            dating_queries = [
                f"{query} 约会创意",
                f"{query} 浪漫约会",
                f"{query} 情侣活动",
                f"{query} 约会攻略"
            ]
            
            all_results = []
            for search_query in dating_queries:
                results = self.search(search_query, max_results=5)
                all_results.extend(results)
                
                # 添加延迟避免被限制
                time.sleep(1)
            
            # 去重和排序
            unique_results = self._deduplicate_results(all_results)
            unique_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            return unique_results[:self.max_results]
            
        except Exception as e:
            logger.error(f"搜索约会创意失败: {e}")
            return []
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去重搜索结果"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
