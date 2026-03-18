import streamlit as st
import random

# 1. Setup Session State (This keeps your score and round from resetting)
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# 2. Your Book Data
data = [
    {
        "book": "The Great Gatsby",
        "error_excerpt": "In my younger and more vulnerable years my father give me some advice...",
        "error_word": "give",
        "correction": "gave"
    },
    {
        "book": "Pride and Prejudice",
        "error_excerpt": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wives.",
        "error_word": "wives",
        "correction": "wife"
    },
    {
        "book": "Moby-Dick",
        "error_excerpt": "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, I thought I will sail about a little.",
        "error_word": "will",
        "correction": "would"
    }
]

st.title("📚 Book Mistake Finder")
st.subheader("Spot the grammatical error to win!")

# 3. Game Logic
if st.session_state.current_round < len(data):
    item = data[st.session_state.current_round]
    
    st.write(f"**Round {st.session_state.current_round + 1}** | From: *{item['book']}*")
    st.info(f"\"{item['error_excerpt']}\"")

    # 4. The Form (This makes the 'Enter' key work)
    with st.form(key=f"form_{st.session_state.current_round}"):
        user_guess = st.text_input("Which word is incorrect?").strip().lower()
        submit_button = st.form_submit_button(label="Submit Answer")

    if submit_button or st.session_state.submitted:
        st.session_state.submitted = True
        
        if user_guess == item['error_word'].lower():
            st.success(f"✨ Correct! It should be '{item['correction']}'.")
            # Only add to score on the first successful submit
            if submit_button:
                st.session_state.score += 1
        else:
            st.error(f"❌ Not quite. The mistake was '{item['error_word']}'. It should be '{item['correction']}'.")

        # 5. Show 'Next' button only after submitting
        if st.button("Go to Next Round ➡️"):
            st.session_state.current_round += 1
            st.session_state.submitted = False
            st.rerun()

# 6. Game Over Screen
else:
    st.balloons()
    st.header("Game Over! 🎉")
    st.write(f"Your final score: **{st.session_state.score} / {len(data)}**")
    if st.button("Play Again"):
        st.session_state.score = 0
        st.session_state.current_round = 0
        st.session_state.submitted = False
        st.rerun()

# Sidebar Stats
st.sidebar.metric("Current Score", st.session_state.score)
