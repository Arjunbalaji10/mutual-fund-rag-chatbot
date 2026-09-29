import streamlit as st

from rag_pipeline import answer_question, load_resources


st.set_page_config(
    page_title="Mutual Fund FAQ Assistant",
    page_icon="📊",
    layout="centered",
)


@st.cache_resource
def load_rag_resources():
    return load_resources()


chunks, retriever, groq_client = load_rag_resources()


st.title("📊 Mutual Fund FAQ Assistant")

st.write(
    "Ask factual questions about the HDFC mutual fund schemes "
    "covered by this knowledge base."
)

st.info("Facts-only. No investment advice.")


st.subheader("Example questions")

example_questions = [
    "What is the expense ratio of HDFC Large Cap Fund Direct Growth?",
    "What is the minimum investment amount for HDFC Equity Fund Direct Growth?",
    "What is the exit load of HDFC Large Cap Fund Direct Growth?",
]

for question in example_questions:
    if st.button(question):
        st.session_state.selected_question = question


if "messages" not in st.session_state:
    st.session_state.messages = []


if "selected_question" not in st.session_state:
    st.session_state.selected_question = None


if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.selected_question = None
    st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("source_url"):
            with st.expander("Source"):
                st.write(message["source_url"])


question = st.chat_input(
    "Ask a factual mutual fund question..."
)


if st.session_state.selected_question:
    question = st.session_state.selected_question
    st.session_state.selected_question = None


if question:
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    result = answer_question(
        question,
        chunks,
        retriever,
        groq_client,
    )

    with st.chat_message("assistant"):
        st.markdown(result["answer"])

        if result["source_url"]:
            with st.expander("Source"):
                st.write(result["source_url"])

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "source_url": result["source_url"],
        }
    )