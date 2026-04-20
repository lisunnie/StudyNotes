# -*- coding: gbk -*-
import streamlit as st
import sys
import io
from openai import OpenAI

# 强制设置编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gbk', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='gbk', errors='replace')

# 页面配置
st.set_page_config(
    page_title="学霸笔记生成器", 
    page_icon="??",
    layout="centered"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 主标题样式 */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
        border-bottom: 2px solid #1e3c72;
        padding-bottom: 1rem;
    }
    /* 笔记卡片样式 */
    .note-card {
        background-color: #fef9e6;
        border-left: 5px solid #1e3c72;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    /* 生成按钮样式 */
    .stButton > button {
        background-color: #1e3c72;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #2a5298;
        color: white;
    }
    /* 输入框样式 */
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    .stTextArea > div > div > textarea {
        border-radius: 8px;
    }
    /* 成功提示样式 */
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    /* 笔记内容样式 */
    .notes-content {
        background-color: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        line-height: 1.8;
    }
    .notes-content h1 {
        color: #1e3c72;
        border-left: 4px solid #1e3c72;
        padding-left: 1rem;
        margin-top: 1.5rem;
    }
    .notes-content h2 {
        color: #2a5298;
        border-bottom: 2px solid #ddd;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .notes-content h3 {
        color: #333;
        margin-top: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #999;
        font-size: 0.8rem;
        border-top: 1px solid #ddd;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 标题区域
st.markdown('<div class="main-title">?? 学霸笔记生成器</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">粘贴文章内容 · AI智能整理 · 一键生成学霸笔记</div>', unsafe_allow_html=True)

# 侧边栏 - 配置信息
with st.sidebar:
    st.markdown("### ?? 配置")
    st.markdown("---")
    
    # API Key 输入
    api_key = st.text_input(
        "?? SiliconFlow API Key", 
        type="password", 
        help="去 https://siliconflow.cn/ 注册获取，免费",
        placeholder="输入你的API Key"
    )
    
    st.markdown("---")
    st.markdown("### ?? 使用说明")
    st.markdown("""
    1. 输入文章/课文名称
    2. 从网上复制文章内容粘贴到下方
    3. 点击「? 生成笔记」
    4. 下载Markdown格式笔记
    """)
    
    st.markdown("---")
    st.markdown("### ?? 小贴士")
    st.markdown("""
    - 支持古诗、课文、文章等
    - 内容越详细，笔记质量越高
    - 生成的笔记可下载保存
    """)

# 主要内容区域
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    # 文章名称输入
    article_name = st.text_input(
        "?? 文章/课文名称", 
        placeholder="例如：静夜思、吃水不忘挖井人、背影...",
        key="article_name"
    )
    
    st.markdown("---")
    
    # 文章内容输入
    st.markdown("#### ?? 文章内容")
    article_content = st.text_area(
        "",
        placeholder="【使用说明】\n1. 打开浏览器搜索文章\n2. 复制文章全文\n3. 粘贴到下方\n\n【示例】\n床前明月光，疑是地上霜。\n举头望明月，低头思故乡。\n\n【注释】\n静夜思：静静的夜里产生的思绪。\n疑：好像。\n举头：抬头。\n\n【译文】\n明亮的月光洒在床前，好像地上泛起了一层白霜...",
        height=300,
        key="article_content"
    )
    
    st.markdown("---")
    
    # 生成按钮
    generate = st.button("? 生成学霸笔记", type="primary", use_container_width=True)

# 笔记生成逻辑
if generate:
    if not article_name:
        st.warning("?? 请输入文章/课文名称")
    elif not api_key:
        st.warning("?? 请输入 SiliconFlow API Key（去 https://siliconflow.cn/ 注册免费获取）")
    elif not article_content:
        st.warning("?? 请粘贴文章内容")
    else:
        with st.spinner("?? AI 正在分析文章并整理笔记，请稍候..."):
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.siliconflow.cn/v1"
                )
                
                prompt = f"""你是一位优秀的小学语文老师，擅长整理学习笔记。请根据以下《{article_name}》的内容，生成一份专业、工整的学霸笔记。

## 要求：
1. 格式清晰，层次分明
2. 内容详实，便于学习
3. 使用Markdown格式

## 输出格式（请严格按照以下结构）：

# 《{article_name}》学霸笔记

## 一、字词整理

### 1. 生字与重点词
| 词语 | 拼音 | 解释 |
|:---|:---|:---|
| xxx | xxx | xxx |

### 2. 近义词
- xxx → xxx

### 3. 反义词
- xxx → xxx

## 二、课文解析

### 1. 主要内容
[用2-3句话概括文章大意]

### 2. 中心思想
[文章想要表达的核心思想和道理]

### 3. 重点段落解析
[选取1-2个重要段落，逐句解析]

## 三、学习提示

### 1. 朗读/背诵要点
- [要点1]
- [要点2]

### 2. 练习题
1. [题目1]
2. [题目2]
3. [题目3]

### 3. 参考答案
1. [答案1]
2. [答案2]
3. [答案3]

---
原文内容：
{article_content}"""

                response = client.chat.completions.create(
                    model="Qwen/Qwen2.5-7B-Instruct",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                notes = response.choices[0].message.content
                
                # 显示成功提示
                st.markdown(f"""
                <div class="success-box">
                ? 笔记生成成功！《{article_name}》的学霸笔记已整理完成。
                </div>
                """, unsafe_allow_html=True)
                
                # 显示笔记
                st.markdown('<div class="notes-content">', unsafe_allow_html=True)
                st.markdown(notes)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 下载按钮
                st.markdown("---")
                col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
                with col_dl2:
                    st.download_button(
                        label="?? 下载笔记（Markdown格式）",
                        data=notes,
                        file_name=f"{article_name}_学霸笔记.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"? 生成失败：{e}")
                st.info("请检查 API Key 是否正确，或稍后重试")

# 页脚
st.markdown("""
<div class="footer">
    ?? 学霸笔记生成器 | AI智能整理 | 免费使用
</div>
""", unsafe_allow_html=True)