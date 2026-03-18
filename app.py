import streamlit as st

# --- SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0
if 'answer_checked' not in st.session_state:
    st.session_state.answer_checked = False

# --- DATA ---
data = [
    {"book": "The Great Gatsby", "error_excerpt": "In my younger and more vulnerable years my father give me some advice...", "error_word": "give", "correction": "gave"},
    {"book": "Pride and Prejudice", "error_excerpt": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wives.", "error_word": "wives", "correction": "wife"},
    {"book": "Moby-Dick", "error_excerpt": "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, I thought I will sail about a little.", "error_word": "will", "correction": "would"}
]

st.title("📚 Book Mistake Finder")

if st.session_state.current_round < len(data):
    item = data[st.session_state.current_round]
    st.info(f"**From: {item['book']}**\n\n\"{item['error_excerpt']}\"")

    # The Form
    with st.form(key=f"form_{st.session_state.current_round}", clear_on_submit=True):
        user_guess = st.text_input("Type the incorrect word and press Enter:").strip().lower()
        submit_button = st.form_submit_button("Submit Answer")

    # LOGIC: Only runs when they hit Enter/Submit
    if submit_button:
        if user_guess == item['error_word'].lower():
            st.session_state.score += 1
            st.toast("✨ Correct!", icon="✅")
        else:
            st.toast(f"❌ Wrong! It was '{item['error_word']}'", icon="⚠️")
        
        # Move to next round immediately
        st.session_state.current_round += 1
        st.rerun()

else:
    st.balloons()
    st.success(f"Game Over! Final Score: {st.session_state.score} / {len(data)}")
    if st.button("Restart"):
        st.session_state.score = 0
        st.session_state.current_round = 0
        st.rerun()

st.sidebar.metric("Score", st.session_state.score)
