from http.client import responses

import ollama
import streamlit as st
from click import prompt

# 打印版本信息
print("Ollama 当前可用模型：", ollama.list())
print("Streamlit 版本：", st.__version__)

# 建立客户端
client = ollama.Client(host="http://localhost:11434")

# 查看模型详情
info = client.show("deepseek-r1:1.5b")   # 注意你本地模型名是 1.5b 不是 1.5
print(info)


while True:
    prompt = input("请输入问题：")
    if prompt.strip() == "exit":
        break

    # 非流式调用
    resp = client.chat(
        model="deepseek-r1:1.5b",
        messages=[{"role": "user", "content": prompt}]
    )
    print("助手：", resp["message"]["content"])
    print("-" * 40)
