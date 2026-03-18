import streamlit as st

# --- 1. INITIALISE SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""

# --- 2. DATA ---
data = [
    {"book": "The Great Gatsby", "error_excerpt": "In my younger and more vulnerable years my father give me some advice...", "error_word": "give", "correction": "gave"},
    {"book": "Pride and Prejudice", "error_excerpt": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wives.", "error_word": "wives", "correction": "wife"},
    {"book": "Moby-Dick", "error_excerpt": "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, I thought I will sail about a little.", "error_word": "will", "correction": "would"}
]

st.title("📚 The Grammar Detective")

# --- 3. GAME LOGIC ---
if st.session_state.current_round < len(data):
    item = data[st.session_state.current_round]
    
    st.info(f"**From: {item['book']}**\n\n\"{item['error_excerpt']}\"")

    # --- PHASE 1: SHOW THE INPUT FORM ---
    if not st.session_state.show_feedback:
        with st.form(key=f"input_form_{st.session_state.current_round}"):
            user_guess = st.text_input("Which word is the mistake? (Press Enter to submit)").strip().lower()
            submit = st.form_submit_button("Check Answer")

            if submit:
                if user_guess == item['error_word'].lower():
                    st.session_state.score += 1
                    st.session_state.last_result = "correct"
                else:
                    st.session_state.last_result = "incorrect"
                
                st.session_state.show_feedback = True
                st.rerun()

    # --- PHASE 2: SHOW FEEDBACK & WAIT FOR ENTER TO CONTINUE ---
    else:
        if st.session_state.last_result == "correct":
            st.success(f"✨ **Correct!** The mistake was '{item['error_word']}'. It should be '{item['correction']}'.")
        else:
            st.error(f"❌ **Wrong.** The mistake was '{item['error_word']}'. It should be '{item['correction']}'.")
        
        # This second form allows the 'Enter' key to trigger the 'Next' action
        with st.form(key=f"next_form_{st.session_state.current_round}"):
            st.write("Press **Enter** or click below to continue...")
            next_button = st.form_submit_button("Next Round ➡️")
            
            if next_button:
                st.session_state.current_round += 1
                st.session_state.show_feedback = False
                st.rerun()

# --- 4. GAME OVER ---
else:
    st.balloons()
    st.header("Game Over! 🎉")
    st.metric("Final Score", f"{st.session_state.score} / {len(data)}")
    if st.button("Play Again"):
        st.session_state.score = 0
        st.session_state.current_round = 0
        st.session_state.show_feedback = False
        st.rerun()

st.sidebar.metric("Total Score", st.session_state.score)
