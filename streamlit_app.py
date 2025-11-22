import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
st.set_page_config(page_title="Brand Deal Pitcher", page_icon="💸", layout="centered")

# --- 2. STYLE ---
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

# --- 3. THE BRUTE FORCE GENERATOR ---
def brute_force_generate(api_key, prompt):
    genai.configure(api_key=api_key)
    
    # LIST OF EVERY POSSIBLE MODEL NAME TO TRY
    # We try them in order. The first one to work wins.
    candidate_models = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-1.0-pro",
        "gemini-pro"
    ]
    
    last_error = ""
    
    for model_name in candidate_models:
        try:
            # Try to initialize AND generate
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text # Success! Return the text.
        except Exception as e:
            # If it fails, save error and try the NEXT model
            last_error = str(e)
            continue
            
    # If ALL specific names fail, try to auto-discover from account
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model = genai.GenerativeModel(m.name)
                response = model.generate_content(prompt)
                return response.text
    except Exception as e:
        last_error = str(e)

    # If literally everything fails, return the error
    return f"CRITICAL ERROR: All models failed. Last error: {last_error}"

# --- 4. APP LOGIC ---
st.markdown("<h1>💸 Brand Deal Pitch Writer</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    brand_name = st.text_input("Brand Name", placeholder="e.g. Nike")
    my_niche = st.text_input("My Niche", placeholder="e.g. Fitness")
with col2:
    follower_count = st.text_input("Followers", placeholder="e.g. 15k")
    avg_views = st.text_input("Avg Views", placeholder="e.g. 50k")

password = st.text_input("VIP Password", type="password")

if st.button("✨ Write Winning Email"):
    if password != "collab2025":
        st.error("🔒 Access Denied.")
    elif not brand_name:
        st.warning("Enter the brand name first!")
    else:
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("⚠️ API Key missing in Secrets.")
        else:
            with st.spinner("✨ Drafting your email..."):
                # CALL THE BRUTE FORCE FUNCTION
                result = brute_force_generate(st.secrets["GOOGLE_API_KEY"], f"""
                Act as a Talent Agent. Write a sponsorship pitch.
                To: {brand_name}
                From: Influencer ({my_niche}, {follower_count} followers, {avg_views} views).
                Tone: Professional, High-Converting.
                """)
                
                if "CRITICAL ERROR" in result:
                    st.error(result)
                    # DEBUG: Print available models to help us fix it
                    try:
                        st.write("--- DEBUG INFO ---")
                        st.write("Available models on your account:")
                        st.write([m.name for m in genai.list_models()])
                    except:
                        pass
                else:
                    st.subheader("📩 Pitch Draft:")
                    st.code(result, language="text")
                    st.balloons()
