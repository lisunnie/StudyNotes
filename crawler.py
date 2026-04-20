# -*- coding: gbk -*-
import requests
from bs4 import BeautifulSoup

def search_and_crawl(article_name):
    """
    根据文章名称，从多个网站搜索并爬取内容
    """
    
    # 方法1：百度百科
    url = f"https://baike.baidu.com/item/{article_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试多个可能的class名称
        content_div = soup.find('div', class_='main-content')
        if not content_div:
            content_div = soup.find('div', class_='lemmaContent')
        if not content_div:
            content_div = soup.find('div', class_='para')
        
        if content_div:
            paragraphs = content_div.find_all('p')
            content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            if len(content) > 100:
                return content
    except:
        pass
    
    # 方法2：搜狗百科
    try:
        url = f"https://baike.sogou.com/v{article_name}.htm"
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_div = soup.find('div', class_='content')
        if content_div:
            paragraphs = content_div.find_all('p')
            content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            if len(content) > 100:
                return content
    except:
        pass
    
    # 方法3：使用百度搜索，抓取第一个结果
    try:
        search_url = f"https://www.baidu.com/s?wd={article_name}"
        response = requests.get(search_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取搜索结果中的内容摘要
        results = soup.find_all('div', class_='c-abstract')
        if results:
            content = '\n'.join([r.get_text().strip() for r in results[:3]])
            if len(content) > 200:
                return content
    except:
        pass
    
    # 方法4：如果都失败了，返回手动输入的提示
    return f"未能自动找到《{article_name}》的相关内容。\n\n你可以：\n1. 手动搜索该文章的内容，粘贴到下方\n2. 或者告诉我更准确的文章名称"