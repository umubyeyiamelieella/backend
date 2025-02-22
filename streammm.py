import streamlit as st
import requests  # To interact with the backend API

def main():
    st.set_page_config(page_title="AI Literacy Tool", page_icon="🤖", layout="wide")
    
    if 'username' not in st.session_state:
        st.session_state.username = ""
        st.session_state.logged_in = False
        
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard()

def login_page():
    st.title("Welcome to the AI Literacy Tool! 🤖")
    st.write("This tool helps monitor and improve your AI literacy through interactive learning.")
    
    username = st.text_input("Enter a username to get started:")
    if st.button("Start Learning"):
        if username:
            response = requests.post("http://localhost:8000/register_user", json={"username": username})
            if response.status_code == 200:
                st.session_state.username = username
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Error registering user. Please try again.")
        else:
            st.warning("Please enter a username to continue.")

def dashboard():
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    st.sidebar.write("Select your AI literacy level:")
    level = st.sidebar.radio("", ["Beginner", "Intermediate", "Advanced"])
    
    st.title("AI Literacy Learning Dashboard")
    st.write(f"You have selected the **{level}** level.")
    
    response = requests.get(f"http://localhost:8000/get_learning_content/{level}")
    if response.status_code == 200:
        content = response.json()
        st.markdown(content.get("description", "No content available."))
    else:
        st.error("Failed to load learning content.")
    
    st.sidebar.write("---")
    progress_response = requests.get(f"http://localhost:8000/get_user_progress/{st.session_state.username}")
    if progress_response.status_code == 200:
        progress = progress_response.json().get("progress", 0)
        st.sidebar.progress(progress)
    else:
        st.sidebar.progress(0.0)
    
    quiz_section(level)

def quiz_section(level):
    st.subheader("Quick Quiz 📝")
    question = "What is AI?"
    options = ["A programming language", "A system that learns", "A type of hardware"]
    answer = st.radio(question, options)
    if st.button("Submit Answer"):
        response = requests.post("http://localhost:8000/submit_quiz", json={
            "username": st.session_state.username,
            "level": level,
            "answer": answer
        })
        if response.status_code == 200:
            result = response.json()
            st.success(result.get("message", "Answer submitted!"))
        else:
            st.error("Failed to submit answer.")

if __name__ == "__main__":
    main()
