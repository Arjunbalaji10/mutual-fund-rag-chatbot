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


model, collection, groq_client = load_rag_resources()


st.title("📊 Mutual Fund FAQ Assistant")

st.caption(
    "Factual information about the HDFC mutual fund schemes "
    "covered by this knowledge base."
)


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("source_url"):
            with st.expander("Source"):
                st.write(message["source_url"])


# Chat input
question = st.chat_input(
    "Ask a factual mutual fund question..."
)


if question:
    # Display user question
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Get RAG answer
    result = answer_question(
        question,
        model,
        collection,
        groq_client,
    )

    # Display assistant answer
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