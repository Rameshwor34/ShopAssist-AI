import os
import requests
import streamlit as st


API_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8002"
)


st.set_page_config(
    page_title="ShopAssist AI",
    page_icon="🛍️",
    layout="centered",
)


st.title("🛍️ ShopAssist AI")
st.caption("AI-powered e-commerce customer support")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_message = st.chat_input(
    "How can I help you today?"
)


if user_message:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": user_message},
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "answer",
            "Sorry, I could not generate a response."
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

    except requests.exceptions.RequestException as exc:

        error_message = (
            f"Unable to connect to the ShopAssist backend: {exc}"
        )

        with st.chat_message("assistant"):
            st.error(error_message)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message,
            }
        )
