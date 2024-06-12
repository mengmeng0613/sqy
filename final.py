import jieba
import requests
import streamlit as st
from streamlit_echarts import st_echarts
from collections import Counter
from bs4 import BeautifulSoup
import re
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 清理文本函数
def preprocess_text(text):
    text = re.sub(r'\s+', '', text)  # 去除空白字符
    text = re.sub(r'[\n\r]', '', text)  # 去除换行符
    return text.strip()

# 分词函数
def word_segmentation(text):
    stopwords = set(
        ['的', '了', '在', '是', '我', '你', '他', '她', '它', '们', '这', '那', '之', '与', '和', '或', '虽然', '但是', '然而', '因此'])
    text = re.sub(r'[^\w\s]', '', text)  # 去除标点符号
    words = jieba.lcut(text)
    return [word for word in words if word not in stopwords]

# 移除标点和数字
def remove_noise(text):
    text = re.sub(r'[' + string.punctuation + ']+', '', text)
    return re.sub(r'\d+', '', text)

# 提取正文文本
def extract_main_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

# 生成词云图
def generate_wordcloud(word_counts):
    wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400).generate_from_frequencies(word_counts)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# 运行主程序
def main():
    st.set_page_config(
        page_title="文本处理示例",
        page_icon="📝",
    )

    st.title("欢迎使用 Streamlit 文本处理示例 📝")

    url = st.text_input('请输入 URL:')

    if url:
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'
            html_content = response.text

            st.write("网页内容获取成功")

            text = extract_main_text(html_content)
            st.write("提取的正文文本：", text[:500])  # 仅展示前500字符

            text = remove_noise(text)
            st.write("去除噪音后的文本：", text[:500])

            text = preprocess_text(text)
            st.write("预处理后的文本：", text[:500])

            words = word_segmentation(text)
            st.write("分词结果：", words[:50])  # 仅展示前50个词

            word_count = Counter(words)
            most_common_words = word_count.most_common(20)

            st.write("词频统计结果：", most_common_words)

            chart_options = {
                "tooltip": {"trigger": 'item', "formatter": '{b} : {c}'},
                "xAxis": [{
                    "type": "category",
                    "data": [word for word, count in most_common_words],
                    "axisLabel": {"interval": 0, "rotate": 45}
                }],
                "yAxis": [{"type": "value"}],
                "series": [{
                    "type": "bar",
                    "data": [count for word, count in most_common_words]
                }]
            }

            st_echarts(chart_options, height='500px')

            # 生成词云图
            st.write("词云图：")
            generate_wordcloud(dict(most_common_words))

        except Exception as e:
            st.error(f"出现错误: {e}")

if __name__ == "__main__":
    main()
