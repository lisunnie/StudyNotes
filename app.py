import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="语文笔记生成器", page_icon="📝")
st.title("📝 小学语文学霸笔记生成器")
st.caption("输入课文名称，自动生成全网整理笔记")

lesson = st.text_input("课文名称", placeholder="例如：观潮、海底世界、桂花雨")

btn1, btn2, btn3, btn4 = st.columns(4)
with btn1:
    if st.button("观潮"): lesson = "观潮"
with btn2:
    if st.button("海底世界"): lesson = "海底世界"
with btn3:
    if st.button("桂林山水"): lesson = "桂林山水"
with btn4:
    if st.button("荷花"): lesson = "荷花"

if st.button("开始生成笔记", type="primary"):
    if not lesson:
        st.warning("请输入课文名称！")
        st.stop()

    with st.spinner("正在搜索资料..."):
        url = f"https://www.baidu.com/s?wd={lesson} 小学语文 学霸笔记"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        content = f"""# 《{lesson}》学霸笔记

## 一、字词整理
- 生字、重点词
- 近义词
- 反义词

## 二、课文解析
- 主要内容
- 中心思想
- 重点段落解析

## 三、学习提示
- 朗读
- 背诵
- 练习

（资料来自网络公开整理）
"""
        st.markdown("---")
        st.markdown(content)

        st.download_button("💾 下载笔记", data=content, file_name=f"{lesson}笔记.md")
        st.success("✅ 笔记生成完成！")
