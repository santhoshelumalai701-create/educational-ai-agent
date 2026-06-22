
# -------------------------------
# CONFIG
# -------------------------------
import streamlit as st
from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)
# -------------------------------
# PAGE
# -------------------------------
st.set_page_config(
    page_title="Educational AI Agent",
    page_icon="🎓"
)

st.title("🎓 Educational AI Agent")
st.write("Ask educational questions from basic to advanced level.")
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -------------------------------
# CHAT HISTORY
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# USER INPUT
# -------------------------------
if prompt := st.chat_input("Ask an educational question..."):

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Greetings
    greetings = [
        "hi", "hello", "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    thanks_words = [
        "thanks",
        "thank you",
        "thankyou",
        "thx",
        "ty"
    ]

    if prompt.lower() in greetings:
        response = (
            "👋 Hello! I'm your Educational AI Assistant. "
            "Ask me anything about academics."
        )

    elif prompt.lower() in thanks_words:
        response = (
            "😊 You're welcome! Happy learning."
        )

    else:

        system_prompt = f"""
You are an Educational AI Assistant.

Answer ONLY educational questions.

Allowed topics:
- Mathematics
- Physics
- Chemistry
- Biology
- Programming
- Computer Science
- Engineering
- History
- Geography
- Economics

If the question is unrelated to education, reply exactly:

I can only answer educational questions.
Please ask a learning-related question.

Question:
{prompt}
"""

        try:

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": system_prompt
                    }
                ]
            )

            response = (
                completion
                .choices[0]
                .message.content
            )

        except Exception as e:
            response = f"⚠️ Error: {e}"

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )   