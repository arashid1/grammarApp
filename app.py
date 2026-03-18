import streamlit as st

# --- 1. PAGE STYLING ---
st.set_page_config(page_title="The Grammar Detective", page_icon="🕵️‍♂️")

st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"] { background-color: #fdf5e6 !important; }
    h1, h2, h3, p, span, label, .stMarkdown, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        font-family: 'Georgia', serif !important; color: #2c241e !important;
    }
    .stButton>button, .stFormSubmitButton>button {
        background-color: #e6dcc8 !important; color: #2c241e !important;
        border: 1px solid #d4c4a8 !important; border-radius: 4px; width: 100%;
    }
    .stAlert { background-color: #fff9f0 !important; border: 1px solid #d4c4a8 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISE SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0
if 'phase' not in st.session_state:
    st.session_state.phase = "ASKING"

# --- 3. DATA ---
data = [
    {"book": "The Great Gatsby", "error_excerpt": "In my younger and more vulnerable years my father give me some advice...", "error_word": "give", "correction": "gave"},
    {"book": "Pride and Prejudice", "error_excerpt": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wives.", "error_word": "wives", "correction": "wife"},
    {"book": "Moby-Dick", "error_excerpt": "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, I thought I will sail about a little.", "error_word": "will", "correction": "would"}
]

st.title("📜 The Grammar Detective")

if st.session_state.current_round < len(data):
    item = data[st.session_state.current_round]
    st.markdown(f"### *{item['book']}*")
    st.info(f"\"{item['error_excerpt']}\"")

    # --- THE FORM ---
    # We use a single form for the entire round
    with st.form(key=f"round_form_{st.session_state.current_round}", clear_on_submit=True):
        
        if st.session_state.phase == "ASKING":
            user_guess = st.text_input("Which word is the mistake?").strip().lower()
            button_label = "Check Answer"
        else:
            # We show a dummy input or text so the form stays "active" for the Enter key
            st.write(f"**Result:** {st.session_state.last_msg_text}")
            st.write("✨ Press **Enter** to continue to the next book...")
            button_label = "Next Round ➡️"
            user_guess = "" # Reset variable

        submit = st.form_submit_button(button_label)

        if submit:
            if st.session_state.phase == "ASKING":
                # Logic for checking the answer
                if user_guess == item['error_word'].lower():
                    st.session_state.score += 1
                    st.session_state.last_msg_text = f"✅ Correct! It should be '{item['correction']}'."
                else:
                    st.session_state.last_msg_text = f"❌ Wrong. The mistake was '{item['error_word']}'."
                
                st.session_state.phase = "FEEDBACK"
                st.rerun()
            else:
                # Logic for moving to next round
                st.session_state.current_round += 1
                st.session_state.phase = "ASKING"
                st.rerun()

else:
    st.balloons()
    st.header("The End 🖋️")
    st.write(f"Final score: **{st.session_state.score} / {len(data)}**")
    if st.button("Restart Journey"):
        st.session_state.score = 0
        st.session_state.current_round = 0
        st.session_state.phase = "ASKING"
        st.rerun()

# Sidebar
st.sidebar.markdown("### 🖋️ Ledger")
st.sidebar.metric("Points Earned", st.session_state.score)
