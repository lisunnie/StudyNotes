import asyncio
import streamlit as st
import requests
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

def search_lesson_note_url(lesson_name):
    search_key = f"{lesson_name} 小学语文 学霸笔记"
    search_url = f"https://www.baidu.com/s?wd={search_key}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for result in soup.find_all('div', class_='result-op'):
            a_tag = result.find('a')
            if a_tag and a_tag.get('href'):
                return a_tag.get('href')
        return None
    except:
        return None

async def crawl_clean_content(url):
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig()
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
        return result.markdown

def main():
    st.set_page_config(page_title="语文笔记生成器", page_icon="📝")
    st.title("📝 语文笔记生成器")
    st.caption("输入课文名称，自动爬全网资料生成学霸笔记")

    lesson_name = st.text_input("课文名称", placeholder="例如：海底世界、观潮、桂花雨")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("海底世界"): lesson_name = "海底世界"
    with col2:
        if st.button("观潮"): lesson_name = "观潮"
    with col3:
        if st.button("桂林山水"): lesson_name = "桂林山水"
    with col4:
        if st.button("匆匆"): lesson_name = "匆匆"

    if st.button("开始生成笔记", type="primary"):
        if not lesson_name:
            st.warning("请输入课文名称！")
            return

        with st.spinner("正在全网搜索资料并抓取..."):
            note_url = search_lesson_note_url(lesson_name)
            if not note_url:
                st.error("未找到相关笔记，请换个名称试试")
                return

            raw_content = asyncio.run(crawl_clean_content(note_url))
            if not raw_content:
                st.error("抓取失败，请重试")
                return

            final_note = f"# 《{lesson_name}》学霸笔记\n\n{raw_content}"
            st.markdown("---")
            st.markdown(final_note)

            st.download_button(
                label="💾 下载笔记（Markdown格式）",
                data=final_note,
                file_name=f"{lesson_name}笔记.md",
                mime="text/markdown"
            )
            st.success("✅ 笔记生成完成！可复制 / 可下载")

if __name__ == "__main__":
    main()