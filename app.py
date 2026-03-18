import streamlit as st
import random

# 1. Initialize game state so data persists across reruns
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0

# 2. Example data (The "Database")
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
    }
]

st.title("📚 Book Mistake Finder")
st.subheader("Spot the grammatical error to win!")

# 3. Game Logic: Check if there are rounds left
if st.session_state.current_round < len(data):
    item = data[st.session_state.current_round]
    
    st.write(f"**Round {st.session_state.current_round + 1}** | From: *{item['book']}*")
    st.info(f"\"{item['error_excerpt']}\"")

    # 4. User Interaction
    user_guess = st.text_input("Enter the word that is incorrect:", key=f"input_{st.session_state.current_round}")
    
    if st.button("Submit Answer"):
        if user_guess.lower().strip() == item['error_word'].lower():
            st.success(f"✨ Correct! It should be '{item['correction']}'.")
            st.session_state.score += 1
        else:
            st.error(f"❌ Not quite. The mistake was '{item['error_word']}'. It should be '{item['correction']}'.")
        
        # Increment round in state
        st.session_state.current_round += 1
        if st.button("Next Round"):
            st.rerun() # Forces the page to refresh and show the next item

# 5. Ending the game
else:
    st.balloons()
    st.header("Game Over! 🎉")
    st.write(f"Your final score: **{st.session_state.score} / {len(data)}**")
    if st.button("Restart Game"):
        st.session_state.score = 0
        st.session_state.current_round = 0
        st.rerun()

# 6. Sidebar for tracking
st.sidebar.metric("Current Score", st.session_state.score)