import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ShopAssist AI",
    page_icon="🛍️",
    layout="centered",
)

st.title("🛍️ ShopAssist AI")
st.caption("AI-powered e-commerce customer support assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask about orders, shipping, returns, refunds, payments, or products..."
)

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": prompt},
            timeout=90,
        )

        if response.status_code == 429:
            data = response.json()

            with st.chat_message("assistant"):
                st.warning(
                    "The AI provider is temporarily rate-limited. "
                    "Please retry after the quota resets."
                )

                with st.expander("Service status"):
                    st.json(data)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "The AI provider is temporarily rate-limited. "
                        "Please retry after the quota resets."
                    ),
                }
            )

        elif response.status_code >= 500:
            data = response.json()

            with st.chat_message("assistant"):
                st.error(
                    "The AI service is temporarily unavailable. "
                    "Please try again later."
                )

                with st.expander("Service status"):
                    st.json(data)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "The AI service is temporarily unavailable. "
                        "Please try again later."
                    ),
                }
            )

        else:
            response.raise_for_status()
            data = response.json()

            answer = data.get(
                "answer",
                "No answer returned."
            )

            with st.chat_message("assistant"):
                st.markdown(answer)

                with st.expander("Routing details"):
                    st.write(
                        "**Intent:**",
                        data.get("intent")
                    )
                    st.write(
                        "**Confidence:**",
                        data.get("confidence")
                    )
                    st.write(
                        "**Sources:**",
                        data.get("sources", [])
                    )
                    st.write(
                        "**Tool used:**",
                        data.get("tool_used", "none")
                    )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

    except requests.exceptions.ConnectionError:
        error_message = (
            "The ShopAssist backend is not running. "
            "Please start the FastAPI server."
        )

        with st.chat_message("assistant"):
            st.error(error_message)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message
            }
        )

    except requests.exceptions.Timeout:
        error_message = (
            "The request timed out. Please try again."
        )

        with st.chat_message("assistant"):
            st.error(error_message)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message
            }
        )

    except requests.exceptions.RequestException as exc:
        error_message = (
            "An unexpected backend error occurred."
        )

        with st.chat_message("assistant"):
            st.error(error_message)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_message
            }
        )

        print(f"Backend request failed: {exc}")
