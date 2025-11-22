import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
st.set_page_config(page_title="Brand Deal Pitcher", page_icon="💸", layout="centered")

# --- 2. LUXURY AESTHETIC (Gold & Black) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #D4AF37; }
    .stTextInput > div > div > input { 
        background-color: #1a1a1a !important; color: white !important; border: 1px solid #D4AF37 !important; 
    }
    .stButton > button {
        background: linear-gradient(45deg, #D4AF37, #F8F8F8);
        color: black !important; font-weight: bold; border: none; width: 100%; padding: 15px;
    }
    h1 { text-align: center; text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.5); }
    .stCode { background-color: #1a1a1a !important; border: 1px solid #D4AF37; }
    </style>
""", unsafe_allow_html=True)

# --- 3. AUTO-DETECT MODEL FUNCTION ---
def get_working_model(api_key):
    genai.configure(api_key=api_key)
    # Try the list of known models in order
    model_list = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro', 'gemini-1.0-pro']
    
    for model_name in model_list:
        try:
            # Just test if we can initialize it
            model = genai.GenerativeModel(model_name)
            return model
        except:
            continue
    # Fallback if all specific names fail, ask the API for ANY valid model
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        return None

# --- 4. APP LOGIC ---
st.markdown("<h1>💸 Brand Deal Pitch Writer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Get paid what you deserve. Write professional sponsorship emails in seconds.</p>", unsafe_allow_html=True)

# Inputs
col1, col2 = st.columns(2)
with col1:
    brand_name = st.text_input("Brand Name", placeholder="e.g. Nike / Boat")
    my_niche = st.text_input("My Niche", placeholder="e.g. Fitness / Tech")
with col2:
    follower_count = st.text_input("Followers", placeholder="e.g. 15k")
    avg_views = st.text_input("Avg Reel Views", placeholder="e.g. 50k")

# PASSWORD LOCK
password = st.text_input("VIP Password", type="password")

if st.button("✨ Write Winning Email"):
    if password != "collab2025":
        st.error("🔒 Access Denied. Pay ₹199 to unlock.")
    elif not brand_name:
        st.warning("Enter the brand name first!")
    else:
        # Check for API Key
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("⚠️ System Error: Google API Key is missing in Secrets.")
        else:
            try:
                # Use the Smart Model Finder
                model = get_working_model(st.secrets["GOOGLE_API_KEY"])
                
                if model is None:
                     st.error("Could not find a working Gemini model. Check API Key.")
                else:
                    prompt = f"""
                    Act as a Top Talent Agent. Write a persuasive, professional sponsorship pitch email.
                    
                    To: Marketing Manager at {brand_name}
                    From: An Influencer in {my_niche} niche with {follower_count} followers and {avg_views} avg views.
                    
                    Goal: Convince them to send free products or pay for a Reel.
                    Tone: Professional, Confident, Business-casual (Not desperate).
                    Structure:
                    1. Strong Subject Line.
                    2. Who I am (Numbers).
                    3. Why {brand_name} fits my audience.
                    4. Creative Idea (One sentence).
                    5. Call to Action.
                    """
                    
                    with st.spinner("Drafting million-dollar email..."):
                        response = model.generate_content(prompt)
                        st.subheader("📩 Copy & Send This:")
                        st.code(response.text, language="text")
                        st.balloons()
                        
            except Exception as e:
                st.error(f"Error: {e}")
