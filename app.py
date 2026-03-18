import streamlit as st

# --- 1. PAGE STYLING ---
st.set_page_config(page_title="The Grammar Detective", page_icon="🕵️‍♂️")

st.markdown("""
    <style>
    /* Main Background & Sidebar */
    .stApp, [data-testid="stSidebar"] { 
        background-color: #fdf5e6 !important; 
    }
    
    /* Apply Font to text BUT EXCLUDE Icons */
    h1, h2, h3, p, span, label, .stMarkdown, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        font-family: 'Georgia', serif !important; 
        color: #2c241e !important;
    }

    /* FIX: Stop icons from turning into words like 'keyboard_double' */
    .st-emotion-cache-1dfm2sy, i, .material-icons, [data-testid="stIcon"] {
        font-family: 'Material Icons' !important;
    }

    /* Button Styling */
    button { 
        background-color: #e6dcc8 !important; 
        color: #2c241e !important; 
        border: 1px solid #d4c4a8 !important; 
        width: 100%; 
    }

    /* Info Box parchment look */
    .stAlert { 
        background-color: #fff9f0 !important; 
        border: 1px solid #d4c4a8 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_round' not in st.session_state: st.session_state.current_round = 0
if 'phase' not in st.session_state: st.session_state.phase = "ASKING"

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

    # --- PHASE 1: ASKING ---
    if st.session_state.phase == "ASKING":
        with st.form(key=f"ask_{st.session_state.current_round}", clear_on_submit=True):
            user_guess = st.text_input("Which word is the mistake?").strip().lower()
            if st.form_submit_button("Check Answer"):
                if user_guess == item['error_word'].lower():
                    st.session_state.score += 1
                    st.session_state.feedback = ("success", f"✅ Correct! It should be '{item['correction']}'.")
                else:
                    st.session_state.feedback = ("error", f"❌ Wrong. The mistake was '{item['error_word']}'.")
                st.session_state.phase = "FEEDBACK"
                st.rerun()

    # --- PHASE 2: FEEDBACK ---
    else:
        f_type, f_msg = st.session_state.feedback
        if f_type == "success": st.success(f_msg)
        else: st.error(f_msg)
        
        with st.form(key=f"next_{st.session_state.current_round}"):
            st.write("✨ Press **Enter** to continue...")
            if st.form_submit_button("Next Round ➡️"):
                st.session_state.current_round += 1
                st.session_state.phase = "ASKING"
                st.rerun()

else:
    st.balloons()
    st.header("The End 🖋️")
    st.write(f"Final score: **{st.session_state.score} / {len(data)}**")
    if st.button("Restart Journey"):
        st.session_state.score = 0; st.session_state.current_round = 0; st.session_state.phase = "ASKING"
        st.rerun()

st.sidebar.markdown("### 🖋️ Ledger")
st.sidebar.metric("Points Earned", st.session_state.score)
