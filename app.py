import streamlit as st
import requests
import random
import re

# --- 1. PAGE STYLING ---
st.set_page_config(page_title="The Grammar Detective", page_icon="🕵️‍♂️")
st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"] { background-color: #fdf5e6 !important; }
    h1, h2, h3, p, span, label, .stMarkdown, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        font-family: 'Georgia', serif !important; color: #2c241e !important;
    }
    button { background-color: #e6dcc8 !important; color: #2c241e !important; border: 1px solid #d4c4a8 !important; width: 100%; }
    .stAlert { background-color: #fff9f0 !important; border: 1px solid #d4c4a8 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTOMATED EXCERPT FETCHING ---
@st.cache_data(ttl=3600) # Cache for 1 hour to save bandwidth
def get_random_book():
    """Fetches a random popular book from Gutendex API."""
    try:
        # Get a random page of popular books (1-10)
        page = random.randint(1, 10)
        response = requests.get(f"https://gutendex.com{page}")
        books = response.json()['results']
        return random.choice(books)
    except:
        return None

def get_excerpt(book_url):
    """Downloads book text and finds a suitable paragraph."""
    try:
        text = requests.get(book_url).text
        # Clean Gutenberg headers/footers roughly
        start = text.find("*** START")
        end = text.find("*** END")
        clean_text = text[start:end] if start != -1 else text
        
        # Split into paragraphs and find one between 150-350 characters
        paras = [p.strip() for p in clean_text.split('\n\n') if 150 < len(p) < 350]
        return random.choice(paras)
    except:
        return "The detective found no clues in this book."

def inject_mistake(text):
    """Automatically swaps a common word for a grammatical error."""
    swaps = {" was ": " were ", " is ": " are ", " has ": " have ", " their ": " there ", " saw ": " seen "}
    found = [word for word in swaps if word in text.lower()]
    if not found: return None, None, None
    
    target = random.choice(found)
    error = swaps[target].strip()
    original = target.strip()
    # Replace only the first occurrence to keep it fair
    error_text = text.replace(target, swaps[target], 1)
    return error_text, original, error

# --- 3. SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'phase' not in st.session_state: st.session_state.phase = "ASKING"
if 'round_data' not in st.session_state: st.session_state.round_data = None

# --- 4. GAME FLOW ---
def load_new_round():
    with st.spinner("Sourcing a new mystery..."):
        book = get_random_book()
        if book:
            txt_url = book['formats'].get('text/plain; charset=utf-8')
            if txt_url:
                excerpt = get_excerpt(txt_url)
                err_txt, orig, err = inject_mistake(excerpt)
                if err_txt:
                    st.session_state.round_data = {
                        "book": book['title'], "text": err_txt, 
                        "orig": orig, "err": err
                    }
                    return
    # Fallback if no mistake could be injected
    st.session_state.round_data = {"book": "Internal Error", "text": "Something went wrong. Press Enter to try again.", "orig": "err", "err": "err"}

if not st.session_state.round_data:
    load_new_round()

st.title("📜 The Grammar Detective")
data = st.session_state.round_data

st.markdown(f"### *{data['book']}*")
st.info(f"\"{data['text']}\"")

# Form logic for Double-Enter
if st.session_state.phase == "ASKING":
    with st.form(key="ask_form", clear_on_submit=True):
        guess = st.text_input("Which word is the mistake?").strip().lower()
        if st.form_submit_button("Check Answer"):
            if guess == data['err'].lower():
                st.session_state.score += 1
                st.session_state.feedback = ("success", f"✅ Correct! It should be '{data['orig']}'.")
            else:
                st.session_state.feedback = ("error", f"❌ Wrong. The mistake was '{data['err']}'.")
            st.session_state.phase = "FEEDBACK"
            st.rerun()
else:
    f_type, f_msg = st.session_state.feedback
    if f_type == "success": st.success(f_msg)
    else: st.error(f_msg)
    
    with st.form(key="next_form"):
        st.write("✨ Press **Enter** to continue...")
        if st.form_submit_button("Next Round ➡️"):
            st.session_state.round_data = None
            st.session_state.phase = "ASKING"
            st.rerun()

st.sidebar.metric("Points Earned", st.session_state.score)
