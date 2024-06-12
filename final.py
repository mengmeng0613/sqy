# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import jieba
import requests
import streamlit as st
from streamlit_echarts import st_echarts
from collections import Counter
from streamlit.logger import get_logger
import re
import string

LOGGER = get_logger(__name__)


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
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


# 读取文本文件示例
def display_text_file():
    st.write('示例: 读取文本文件内容')
    from pathlib import Path
    file_path = Path(__file__).parent / "example.txt"
    if file_path.is_file():
        with open(file_path, 'r') as f:
            content = f.read()
            st.write(content)
    else:
        st.write("文件未找到")


# 运行主程序
def main():
    st.set_page_config(
        page_title="文本处理示例",
        page_icon="📝",
    )

    st.title("欢迎使用 Streamlit 文本处理示例 📝")

    url = st.text_input('请输入 URL:')

    if url:
        response = requests.get(url)
        response.encoding = 'utf-8'
        html_content = response.text

        text = extract_main_text(html_content)
        text = remove_noise(text)
        text = preprocess_text(text)
        words = word_segmentation(text)
        word_count = Counter(words)

        most_common_words = word_count.most_common(20)

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

    display_text_file()


if __name__ == "__main__":
    main()


