import streamlit as st
import qianfan


with st.sidebar:
    model : str = st.selectbox(
    '请选择一个模型：',
    ('🆓XuanYuan-70B-Chat-4bit', '🆓Qianfan-Chinese-Llama-2-13B',
     '🚌ERNIE-Bot-turbo-AI', '🚌Llama-2-13b-chat','🚌BLOOMZ-7B', 
     '🚌AquilaChat-7B', '🚌Qianfan-BLOOMZ-7B-compressed', '🚌Llama-2-7b', '🚌ChatGLM2-6B-32K',
     '🚌Qianfan-Chinese-Llama-2-7B','🚕ERNIE-Bot', '🚕ERNIE-Bot-4',  '🚁Llama-2-70b-chat', '🚁ERNIE-Bot-8k', 
     '🚀ERNIE-Bot-turbo'))
    
    access_key : str = st.text_input("千帆AccessKey :")
    secret_key : str = st.text_input("千帆SecretKey :")
    
    temperature : float = st.number_input("temperature :", 
                                          help="较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定", 
                                          min_value=0.0, max_value=1.0, step=0.1, value=0.5)
    request_timeout : int = st.number_input("请求超时时间（秒）:", min_value=1, max_value=120, value=60)

st.title("💡 神灯")

role_avator = {
    "assistant": "🤖",
    "user": "🤔"
}

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "本宝子知无不言，开始问吧。"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar=role_avator[msg["role"]]).write(msg["content"])

if prompt := st.chat_input():
    if not access_key or secret_key:
        st.info("请输入百度千帆平台的 AccessKey、SecretKey后访问。")
        st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🤔").write(prompt)

    chat_comp = qianfan.ChatCompletion()
    # 调用默认模型，即 ERNIE-Bot-turbo
    resp = chat_comp.do(model=model[1:], 
                        request_timeout = request_timeout,
                        temperature=temperature, 
                        messages=st.session_state.messages[1:])
    ai_echo = resp.body['result']
    st.session_state.messages.append({"role": "assistant", "content": ai_echo})
    st.chat_message("assistant", avatar="🤖").write(ai_echo)

