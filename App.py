import streamlit as st
from groq import Groq

# ───────────────────────────────────────────────
# Page setup
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="Sankalp",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("💬 Sankalp")
st.caption("🚀 A fast & smart chatbot – powered by Groq")

# ───────────────────────────────────────────────
# Sidebar – API key & model selection
# ───────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your key → https://console.groq.com/keys"
    )

    model = st.selectbox(
        "Model",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ],
        index=0,
        help="70B models = smarter | 8B = faster"
    )

    temperature = st.slider(
        "Temperature (creativity)",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.1
    )

    if st.button("🧹 Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ───────────────────────────────────────────────
# Initialize chat history
# ───────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are Sankalp — a friendly, helpful, determined, and slightly witty AI assistant. Be concise when possible, but thorough when needed. Use emojis sparingly 😄"
        }
    ]

# ───────────────────────────────────────────────
# Show chat history
# ───────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ───────────────────────────────────────────────
# Main chat input + generation
# ───────────────────────────────────────────────
if api_key.strip() == "":
    st.info("👈 Please add your Groq API key in the sidebar to start chatting.")
    st.stop()

client = Groq(api_key=api_key)

if prompt := st.chat_input("Talk to Sankalp..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate streaming response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=2048,
            stream=True,
        )

        response_container = st.empty()
        full_response = ""

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response + "▌")

        response_container.markdown(full_response)

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": full_response})
