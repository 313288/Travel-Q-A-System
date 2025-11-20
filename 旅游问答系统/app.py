import streamlit as st
from qa_processor import TourismQAProcessor
from config import NEO4J_CONFIG


# 初始化问答处理器
qa_processor = TourismQAProcessor(**NEO4J_CONFIG)

# 页面配置
st.title("🌍 旅游智能问答系统")
st.subheader("基于Neo4j图数据库的旅游咨询助手")
st.write("✅ 支持查询：城市景点、景点美食、住宿交通、景点详情")
st.write("📌 示例问题：北京有什么景点？故宫附近有什么美食？北京有什么交通？外滩的开放时间？北京的介绍,北京烤鸭的描述")

# 用户输入
user_question = st.text_input("请输入您的问题：")

# 查询按钮
if st.button("获取答案"):
    if not user_question.strip():
        st.warning("请输入有效问题！")
    else:
        with st.spinner("正在查询..."):
            answer = qa_processor.process_question(user_question)
        st.success("查询完成！")
        st.write("### 📝 回答：")
        st.write(answer)