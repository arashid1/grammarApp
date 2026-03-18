import streamlit as st
import requests
import random

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

# --- 2. AUTOMATED FETCHING (WITH FIXES) ---
# Project Gutenberg blocks requests without a browser 'User-Agent'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

@st.cache_data(ttl=3600)
def get_random_book():
    try:
        # Gutendex usually allows API calls without strict blocking
        page = random.randint(1, 20)
        response = requests.get(f"https://gutendex.com{page}", timeout=10)
        books = response.json().get('results', [])
        return random.choice(books) if books else None
    except:
        return None

def get_excerpt(book_url):
    try:
        # Crucial: Use HEADERS to bypass the "Internal Error" block
        response = requests.get(book_url, headers=HEADERS, timeout=15)
        text = response.text
        
        start = text.find("*** START")
        end = text.find("*** END")
        clean_text = text[start:end] if start != -1 else text
        
        # Split into paragraphs and find one of suitable length
        paras = [p.strip() for p in clean_text.split('\n\n') if 150 < len(p) < 400]
        return random.choice(paras) if paras else None
    except Exception as e:
        return None

def inject_mistake(text):
    swaps = {" was ": " were ", " is ": " are ", " has ": " have ", " their ": " there ", " saw ": " seen "}
    found = [word for word in swaps if word in text.lower()]
    if not found: return None, None, None
    
    target = random.choice(found)
    error = swaps[target].strip()
    original = target.strip()
    error_text = text.replace(target, swaps[target], 1)
    return error_text, original, error

# --- 3. SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'phase' not in st.session_state: st.session_state.phase = "ASKING"
if 'round_data' not in st.session_state: st.session_state.round_data = None

# --- 4. GAME FLOW ---
def load_new_round():
    attempts = 0
    while attempts < 5:
        book = get_random_book()
        if book:
            txt_url = book['formats'].get('text/plain; charset=utf-8')
            if txt_url:
                excerpt = get_excerpt(txt_url)
                if excerpt:
                    err_txt, orig, err = inject_mistake(excerpt)
                    if err_txt:
                        st.session_state.round_data = {
                            "book": book['title'], "text": err_txt, 
                            "orig": orig, "err": err
                        }
                        return
        attempts += 1
    # Hardcoded fallback if the internet fails entirely
    st.session_state.round_data = {
        "book": "The Great Gatsby", 
        "text": "In my younger and more vulnerable years my father give me some advice...",
        "orig": "gave", "err": "give"
    }

if not st.session_state.round_data:
    load_new_round()

st.title("📜 The Grammar Detective")
data = st.session_state.round_data

st.markdown(f"### *{data['book']}*")
st.info(f"\"{data['text']}\"")

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
