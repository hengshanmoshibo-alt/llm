# chat_robot.py
import streamlit as st
import ollama

st.set_page_config(page_title="DeepSeek 聊天", page_icon="🤖", layout="centered")

MODEL = "deepseek-r1:1.5b"

# 侧边栏只留参数和清空按钮
with st.sidebar:
    st.title("⚙️ 设置")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.8, 0.1)
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Max Tokens", 64, 2048, 512, 64)
    if st.button("🗑️ 清空对话"):
        st.session_state.messages = []
        st.rerun()

# 历史消息
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title(f"💬 DeepSeek-R1 1.5B 聊天")
st.caption(f"温度：{temperature}")

# 渲染历史
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 输入&生成
if prompt := st.chat_input("请输入问题"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        full = ""
        for chunk in ollama.chat(
            model=MODEL,
            messages=st.session_state.messages,
            stream=True,
            options={"temperature": temperature, "top_p": top_p, "num_predict": max_tokens}
        ):
            full += chunk["message"]["content"]
            placeholder.markdown(full + "▌")
        placeholder.markdown(full)
    st.session_state.messages.append({"role": "assistant", "content": full})