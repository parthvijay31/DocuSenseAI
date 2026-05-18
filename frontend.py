import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="DocuSenseAI",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stApp {
    background: linear-gradient(to bottom right, #0E1117, #111827);
}

.title {
    font-size: 48px;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
}

.subtitle {
    color: #9CA3AF;
    font-size: 18px;
    margin-bottom: 40px;
}

.upload-box {
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 25px;
}

.answer-box {
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 30px;
}

.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.05);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 14px;
}

.stButton button {
    width: 100%;
    border-radius: 14px;
    padding: 12px;
    background: linear-gradient(90deg, #4F46E5, #7C3AED);
    color: white;
    border: none;
    font-weight: bold;
    font-size: 16px;
}

.stButton button:hover {
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    color: white;
}

hr {
    border-color: rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title(" DocuSenseAI")
    st.write("AI-powered PDF chatbot using RAG.")

    st.markdown("---")

    st.markdown("""
    ### Features
    - PDF Upload
    - Semantic Search
    - AI Answers
    - RAG Pipeline
    - Local LLM
    """)

# Main Title
st.markdown('<div class="title">DocuSenseAI</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Upload documents and chat with them using AI.</div>',
    unsafe_allow_html=True
)

# Upload Section
st.markdown('<div class="upload-box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)

if uploaded_file is not None:

    with st.spinner("Processing PDF..."):

        files = {
            "file": uploaded_file
        }

        response = requests.post(
            "https://docusenseai-backend.onrender.com/upload-pdf",
            files=files
        )

        if response.status_code == 200:
            st.success("PDF uploaded successfully!")

st.markdown('</div>', unsafe_allow_html=True)

# Question Input
question = st.text_input(
    "Ask a question from your document"
)

# Ask Button
if st.button("Ask AI"):

    with st.spinner("Generating answer..."):

        response = requests.get(
            "https://docusenseai-backend.onrender.com/ask",
            params={"query": question}
        )

        data = response.json()

        st.markdown(
            f"""
            <div class="answer-box">
                <h3>🤖 AI Answer</h3>
                <p style="font-size:18px; line-height:1.8;">
                {data["answer"]}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )