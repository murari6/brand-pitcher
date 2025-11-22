import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ---
st.set_page_config(page_title="Brand Deal Pitcher", page_icon="💸", layout="centered")

# --- 2. STYLE (Luxury Gold/Black) ---
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

# --- 3. APP LOGIC ---
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
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                
                # Try to force the newest model, fallback if needed
                model = genai.GenerativeModel('gemini-1.5-flash') 
                
                prompt = f"""
                Act as a Talent Agent. Write a sponsorship pitch.
                To: {brand_name}
                From: Influencer ({my_niche}, {follower_count} followers, {avg_views} views).
                Tone: Professional, High-Converting.
                """
                
                # CLEANER LOADING MESSAGE HERE 👇
                with st.spinner("✨ Drafting your email..."):
                    response = model.generate_content(prompt)
                    st.subheader("📩 Pitch Draft:")
                    st.code(response.text, language="text")
                    st.balloons()
                    
            except Exception as e:
                st.error(f"Error: {e}")
