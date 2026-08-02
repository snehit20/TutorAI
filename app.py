from sample import build_chain
print("BUILD CHAIN:", build_chain)
print("ARGCOUNT:", build_chain.__code__.co_argcount)
import streamlit as st
from sample import build_chain
import uuid
import os

# -------------------------
# Setup
# -------------------------

os.makedirs("Data", exist_ok=True)

st.set_page_config(
    page_title="TutorAI",
    page_icon="🎓",
    layout="wide"
)

# -------------------------
# Custom CSS
# -------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 1rem;
}

.title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.subtitle {
    text-align: center;
    color: #9CA3AF;
    margin-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Session State
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    st.session_state.chain = None

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.title("🎓 TutorAI")

    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    mode = st.radio(
        "Knowledge Sources",
        [
            "PDFs Only",
            "PDFs + Web"
        ]
    )

    use_web = mode == "PDFs + Web"

    topic = None

    if use_web:

        topic = st.text_input(
            "Topic for Web Search",
            placeholder="Machine Learning"
        )

    if st.button("🚀 Build Knowledge Base", use_container_width=True):

        if not uploaded_files:

            st.warning("Please upload at least one PDF.")

        elif use_web and not topic:

            st.warning("Please enter a topic.")

        else:

            pdf_names = []

            for file in uploaded_files:

                path = f"Data/{file.name}"

                with open(path, "wb") as f:
                    f.write(file.getbuffer())

                pdf_names.append(file.name)

            try:

                with st.spinner("Creating knowledge base..."):

                    st.session_state.chain = build_chain(
                        pdf_names,
                        topic,
                        use_web
                    )

                st.success("Knowledge Base Ready!")

            except Exception as e:

                st.error(f"Failed to build knowledge base:\n\n{e}")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.session_state.session_id = str(uuid.uuid4())

        st.rerun()

# -------------------------
# Header
# -------------------------

st.markdown(
    "<div class='title'>TutorAI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Your Personal AI Study Assistant</div>",
    unsafe_allow_html=True
)

# -------------------------
# Welcome Screen
# -------------------------

if st.session_state.chain is None:

    st.info("""
👋 Welcome to TutorAI

1. Upload one or more PDFs.
2. Choose whether to use web search.
3. Build your knowledge base.
4. Start chatting with your notes.
""")

# -------------------------
# Chat Interface
# -------------------------

else:

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(
        "Ask anything about your notes..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            try:

                with st.spinner("Thinking..."):

                    response = st.session_state.chain.invoke(
                        {"question": prompt},
                        config={
                            "configurable": {
                                "session_id":
                                st.session_state.session_id
                            }
                        }
                    )

                    if hasattr(response, "content"):
                        response = response.content

                    st.markdown(response)

            except Exception as e:

                response = f"Error: {e}"

                st.error(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )