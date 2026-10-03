from pathlib import Path
import streamlit as st
import streamlit_authenticator as stauth
import json
import bcrypt


USERS_FILE = Path("data/users.json")
USERS_FILE.parent.mkdir(exist_ok=True)

def load_users():
    if not USERS_FILE.exists():
        return {}
    try:
        return json.loads(USERS_FILE.read_text())
    except Exception:
        return {}

def save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2))

def show_auth():
    st.markdown("""
    <div style="text-align:center;padding:40px 0 20px;">
        <div style="font-size:42px;">🎬</div>
        <h1>AI Content Studio</h1>
        <p style="opacity:.65;">
            Your AI-powered content creation workspace
        </p>
    </div>
    """, unsafe_allow_html=True)

    users = load_users()
    st.session_state["users"] = users

    tab1, tab2 = st.tabs(["🔐 Login", "✨ Create Account"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button("Login", use_container_width=True):
            users = st.session_state.get("users", {})

            if (
                username in users
                and bcrypt.checkpw(
                    password.encode(),
                    users[username]["password"].encode()
                )
            ):
                st.session_state["authenticated"] = True
                st.session_state["current_user"] = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        name = st.text_input("Full name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        username = st.text_input("Choose username", key="signup_username")
        password = st.text_input(
            "Create password",
            type="password",
            key="signup_password",
        )

        if st.button("Create Account", use_container_width=True):
            if not name or not email or not username or not password:
                st.warning("Please fill in all fields.")
            elif username in st.session_state.get("users", {}):
                st.error("Username already exists.")
            else:
                password_hash = bcrypt.hashpw(
                    password.encode(),
                    bcrypt.gensalt()
                ).decode()

                users[username] = {
                    "name": name,
                    "email": email,
                    "password": password_hash,
                }
                save_users(users)
                st.session_state["users"] = users
                st.success("Account created successfully. You can now log in.")
