import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
from streamlit_webrtc import webrtc_streamer
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os

# --- ၁။ ၂၀၂၆ အဆင့်မြင့် UI နှင့် Layout ---
st.set_page_config(page_title="PPAI 2026 MASTER AI", page_icon="👹", layout="wide")

st.title("👹 PPAI 2026 ULTIMATE MASTER HUB")
st.markdown(f"**Admin:** PPAI | **Date:** 2026.03.21 | **Location:** Live Sync ✅")

# --- ၂။ API Key & Model Configuration ---
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("Master API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3.1-pro')

    # --- ၃။ Tabs စနစ်ဖြင့် Function အားလုံးကို စုစည်းခြင်း ---
    tab_chat, tab_guide, tab_call, tab_data, tab_office = st.tabs([
        "🎙️ AI Voice & Chat", 
        "🗺️ Local Guide Pro", # NEW!
        "📞 Free Call", 
        "📚 Universal Knowledge", 
        "💼 Workspace Agent"
    ])

    # --- TAB 1: AI Chat (အရင်အတိုင်း ပါသည်) ---
    with tab_chat:
        st.subheader("AI Voice Assistant")
        v_input = speech_to_text(language='en', start_prompt="🎤 Speak", stop_prompt="🛑 Send", key='main_v')
        t_input = st.chat_input("PPAI 3.1 Pro ကို မေးပါ...")
        prompt = v_input if v_input else t_input
        if prompt:
            with st.chat_message("assistant"):
                resp = model.generate_content(prompt).text
                st.markdown(resp)
                # Auto TTS
                tts = gTTS(text=resp, lang='en')
                tts.save("r.mp3")
                st.audio("r.mp3", format="audio/mp3", autoplay=True)

    # --- TAB 2: Local Guide Pro (NEW! ခရီးသွားလမ်းညွှန်) ---
    with tab_guide:
        st.subheader("🗺️ Your Personal AI Guide (2026)")
        
        # User Location (၂၀၂၆ မှာ Browser ကနေ Live ယူပါတယ်)
        location = st.text_input("လက်ရှိရောက်ရှိနေသော နေရာ (ဥပမာ- ရန်ကုန်၊ မန္တလေး):", placeholder="Nearby location active...")
        
        # Guide Categories
        category = st.selectbox("ဘာရှာဖွေချင်ပါသလဲ?", ["🍴 စားသောက်ဆိုင်", "🏯 လည်ပတ်စရာနေရာ", "🛍️ ဈေးဝယ်စရာ", "🏨 ဟိုတယ်/တည်းခိုခန်း"])
        
        # User Preferences (စာနဲ့၊ ဒါမှမဟုတ် အသံနဲ့ ပြောလို့ရတယ်)
        preference_v = speech_to_text(language='en', start_prompt="🎤 မိတ်ဆွေ လိုချင်တာကို ပြောပြပါ", stop_prompt="🛑 ပြီးပြီ", key='guide_v')
        preference_t = st.text_input("စိတ်ကြိုက် ညွှန်ကြားချက် (ဥပမာ- 'ဈေးသက်သာတဲ့ ရှမ်းခေါက်ဆွဲဆိုင်')")
        preference = preference_v if preference_v else preference_t

        if st.button("AI လမ်းညွှန်ချက် ရယူရန်"):
            if location and preference:
                with st.spinner(f"{location} တွင် {category} များကို ရှာဖွေနေသည်..."):
                    # ၂၀၂၆ ရဲ့ Google Maps API + Gemini Logic (Simulation)
                    # တကယ့် Maps API Key လိုအပ်ပါတယ် (ထည့်သွင်းရန် လမ်းညွှန်ချက် ပါဝင်သည်)
                    guide_prompt = f"Based on location: {location}. Find {category} based on this preference: {preference}. Provide details on: 1. Name 2. Why it fits preference 3. Estimated Price Range 4. Real-time Reviews 5. Direction Info. Answer in Myanmar language if possible."
                    guide_response = model.generate_content(guide_prompt).text
                    
                    st.success("AI လမ်းညွှန်ချက် ရရှိပါပြီ! ✅")
                    st.markdown("### 📋 Recommendations:")
                    st.write(guide_response)
                    
                    # Optional: Add Live Map Embed here in 2026

    # --- TAB 3: Free App-to-App Call (အရင်အတိုင်း ပါသည်) ---
    with tab_call:
        st.subheader("🚀 P2P Free Call System")
        webrtc_streamer(key="call", audio_receiver_size=1024)

    # --- TAB 4: Universal Knowledge (အရင်အတိုင်း ပါသည်) ---
    with tab_data:
        st.subheader("Web Data Extraction")
        web_link = st.text_input("Website Link:")
        if st.button("Extract"):
            res = requests.get(web_link)
            soup = BeautifulSoup(res.text, 'html.parser')
            extracted = ' '.join([t.text for t in soup.find_all('p')])
            st.session_state['kb'] = extracted
            st.success("Data Extracted to Knowledge Base!")

    # --- TAB 5: Workspace Agent (အရင်အတိုင်း ပါသည်) ---
    with tab_office:
        st.subheader("Google & Microsoft Agent")
        task = st.text_area("အလုပ်ခိုင်းရန်:")
        if st.button("Execute Task"):
            agent_logic = f"As a 2026 Workspace Expert, execute: {task}"
            agent_res = model.generate_content(agent_logic).text
            st.info(agent_res)

else:
    st.warning("⚠️ ရှေ့ဆက်ရန် Sidebar တွင် Master API Key ထည့်သွင်းပေးပါ။")
    
