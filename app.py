import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 页面基础设置
st.set_page_config(page_title="小学语文学霸笔记生成器", page_icon="📝")
st.title("📝 小学语文学霸笔记生成器")
st.caption("输入课文名称，自动爬取全网公开资料生成笔记")

# 输入框+快捷按钮
lesson_name = st.text_input("课文名称", placeholder="例如：观潮、海底世界、桂花雨、匆匆")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("观潮"): lesson_name = "观潮"
with col2:
    if st.button("海底世界"): lesson_name = "海底世界"
with col3:
    if st.button("桂林山水"): lesson_name = "桂林山水"
with col4:
    if st.button("荷花"): lesson_name = "荷花"

# 核心爬虫逻辑（真正爬取全网笔记）
def get_real_note_content(lesson):
    # 1. 百度搜索相关笔记
    search_url = f"https://www.baidu.com/s?wd={lesson} 小学语文 学霸笔记 完整版"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    
    try:
        # 发送搜索请求
        resp = requests.get(search_url, headers=headers, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 2. 提取第一个有效笔记链接
        note_url = None
        for result in soup.find_all('a', href=True):
            href = result['href']
            # 过滤掉广告和百度自身链接，只保留真实的语文资料站
            if 'baidu' not in href and 'javascript' not in href and '推广' not in result.text:
                note_url = href
                break
        
        if not note_url:
            return "未找到《{}》的公开笔记资料，可换个课文名试试～".format(lesson)
        
        # 3. 爬取笔记页面的真实内容
        note_resp = requests.get(note_url, headers=headers, timeout=15)
        note_resp.encoding = note_resp.apparent_encoding
        note_soup = BeautifulSoup(note_resp.text, 'html.parser')
        
        # 4. 清理内容（去掉广告、导航、无用标签）
        for tag in note_soup(['script', 'style', 'iframe', 'nav', 'footer', 'ad']):
            tag.decompose()
        
        # 提取正文内容
        content = note_soup.get_text()
        # 清理多余换行和空格
        content = re.sub(r'\s+', '\n', content).strip()
        # 只保留前3000字（避免内容太长）
        content = content[:3000]

        # 5. 整理成结构化笔记格式
        final_note = f"""# 《{lesson}》学霸笔记（全网资料整合）

## 一、字词整理
{[line for line in content.split('\n') if '近义词' in line or '反义词' in line or '生字' in line or '词语' in line][:10]}

## 二、课文解析
{[line for line in content.split('\n') if '主要内容' in line or '中心思想' in line or '段落' in line][:10]}

## 三、学习提示
{[line for line in content.split('\n') if '朗读' in line or '背诵' in line or '练习' in line][:5]}

---
📚 资料来源：{note_url}
"""
        return final_note
    
    except Exception as e:
        return f"爬取《{lesson}》笔记时出错：{str(e)}\n\n可重试或换个课文名～"

# 生成按钮逻辑
if st.button("开始生成笔记", type="primary"):
    if not lesson_name:
        st.warning("请输入课文名称！")
        st.stop()
    
    with st.spinner("正在全网爬取《{}》的笔记资料... 约10秒".format(lesson_name)):
        # 调用爬虫获取真实内容
        real_note = get_real_note_content(lesson_name)
        # 显示笔记
        st.markdown("---")
        st.markdown(real_note)
        # 下载按钮
        st.download_button(
            label="💾 下载笔记（Markdown格式）",
            data=real_note,
            file_name=f"{lesson_name}学霸笔记.md",
            mime="text/markdown"
        )
        st.success("✅ 笔记生成完成！")
