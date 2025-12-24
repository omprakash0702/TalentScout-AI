import streamlit as st

def apply_global_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0b1120;
            color: #e5e7eb;
        }

        h1 {
            color: #38bdf8;
        }

        .stChatMessage[data-testid="chat-message-user"] {
            background-color: #1e293b;
        }

        .stChatMessage[data-testid="chat-message-assistant"] {
            background-color: #020617;
            border-left: 3px solid #38bdf8;
        }

        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
