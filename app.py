import streamlit as st

# --- 1. PAGE STYLING (The Book Look) ---
st.set_page_config(page_title="The Grammar Detective", page_icon="🕵️‍♂️")

st.markdown("""
    <style>
    .main {
        background-color: #fdf5e6; /* Old Lace / Parchment color */
    }
    .stApp {
        background-color: #fdf5e6;
    }
    h1, h2, h3, p, .stMarkdown {
        font-family: 'Georgia', serif;
        color: #2c241e;
    }
    .stInfo {
        background-color: #fff9f0;
        border: 1px solid #d4c4a8;
        border-radius: 5px;
        padding: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_name_allowed=True)

# --- 2. INITIALISE SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0
if 'phase' not in st.session_state:
    st.session_state.phase = "ASKING" # Two phases: ASKING and FEEDBACK

# --- 3. DATA ---
data = [
    {"book": "The Great Gatsby", "error_excerpt": "In my younger and more vulnerable years my father give me some advice...", "error_word": "give", "correction": "gave"},
    {"book": "Pride and Prejudice", "error_excerpt": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wives.", "error_word": "wives", "correction": "wife"},
    {"book": "Moby-Dick", "error_excerpt": "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, I thought I will sail about a little.", "error_word": "will", "correction": "would"}
]

st.title("📜 The Grammar Detective")

if st.session_state.current_round < len(data):
    item = data[st.session_state.current_round]
    
    # Book Display
    st.markdown(f"### *{item['book']}*")
    st.info(f"\"{item['error_excerpt']}\"")

    # --- THE MAGIC FORM ---
    # This form handles the Enter key for BOTH submission and progression
    with st.form(key=f"game_form_{st.session_state.current_round}", clear_on_submit=(st.session_state.phase == "FEEDBACK")):
        
        if st.session_state.phase == "ASKING":
            user_guess = st.text_input("Which word is the mistake?").strip().lower()
            btn_label = "Check Answer"
        else:
            st.write("✨ Press **Enter** again to continue to the next round...")
            btn_label = "Next Round ➡️"

        submit = st.form_submit_button(btn_label)

        if submit:
            if st.session_state.phase == "ASKING":
                # Check Answer
                if user_guess == item['error_word'].lower():
                    st.session_state.score += 1
                    st.session_state.last_msg = ("success", f"✨ **Correct!** It should be '{item['correction']}'.")
                else:
                    st.session_state.last_msg = ("error", f"❌ **Wrong.** The mistake was '{item['error_word']}'.")
                
                st.session_state.phase = "FEEDBACK"
                st.rerun()
            else:
                # Move to next round
                st.session_state.current_round += 1
                st.session_state.phase = "ASKING"
                st.rerun()

    # Display feedback outside the form for better visibility
    if st.session_state.phase == "FEEDBACK":
        msg_type, msg_text = st.session_state.last_msg
        if msg_type == "success": st.success(msg_text)
        else: st.error(msg_text)

else:
    st.balloons()
    st.header("The End 🖋️")
    st.write(f"Your final score: **{st.session_state.score} / {len(data)}**")
    if st.button("Restart Journey"):
        st.session_state.score = 0
        st.session_state.current_round = 0
        st.session_state.phase = "ASKING"
        st.rerun()

# Sidebar
st.sidebar.markdown("### 🖋️ Ledger")
st.sidebar.metric("Points Earned", st.session_state.score)
