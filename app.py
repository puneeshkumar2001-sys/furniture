# app.py - IN SPACE FURNITURE - 100% FREE
import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime
import requests

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="IN SPACE FURNITURE",
    page_icon="🪑",
    layout="wide"
)

# ========== SESSION STATE ==========
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'current_product': None,
        'wood_type': None,
        'design': None,
        'room_size': None,
        'order_placed': False,
        'damage_history': []
    }

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .product-box {
        border: 2px solid #2A5C3D;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        background: #f8f9fa;
    }
    .damage-card {
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        background: #fff5f5;
    }
    .free-banner {
        background: linear-gradient(90deg, #2A5C3D, #4CAF50);
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ========== FREE API ==========
def get_weather_data(city):
    """FREE OpenWeatherMap API"""
    API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "demo")
    
    if API_KEY == "demo":
        return {
            'humidity': random.randint(40, 90),
            'temp': random.randint(20, 40),
            'description': 'scattered clouds'
        }
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        return {
            'humidity': data['main']['humidity'],
            'temp': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    except:
        return None

def analyze_climate_for_wood(city):
    """Analyze climate and recommend wood"""
    weather = get_weather_data(city)
    
    if not weather:
        return {
            'wood': 'Mango Wood (Default)',
            'reason': 'Climate data unavailable',
            'issues': ['Unknown climate']
        }
    
    humidity = weather['humidity']
    temp = weather['temp']
    
    issues = []
    wood = 'Mango Wood'
    
    if humidity > 70:
        issues.append('High humidity (warping risk)')
        wood = 'Treated Teak'
    elif humidity > 50:
        issues.append('Moderate humidity')
        wood = 'Sal Wood'
    
    if temp > 35:
        issues.append('High heat (cracking risk)')
        wood = 'Teak with UV protection'
    
    if 'rain' in weather['description']:
        issues.append('Frequent rainfall')
        wood = 'Water-resistant Sheesham'
    
    return {
        'wood': wood,
        'reason': f"Based on {humidity}% humidity, {temp}°C",
        'issues': issues if issues else ['Standard conditions'],
        'weather': weather
    }

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown('<div class="free-banner">🚀 100% FREE</div>', unsafe_allow_html=True)
    st.title("🪑 IN SPACE")
    st.markdown("---")
    
    section = st.selectbox(
        "**SELECT SECTION:**",
        ["1. 🏠 Home", "2. 🔍 Search Product", "3. 📍 Location Analysis", 
         "4. 📏 Room Scan", "5. 🎨 Design Studio", "6. 👁️ AR View", 
         "7. 💰 Order", "8. ⚡ Damage Report", "9. 🔄 Transform Product"]
    )
    
    st.markdown("---")
    st.caption("💚 Free forever")

# ========== SECTION 1: HOME ==========
if section == "1. 🏠 Home":
    st.title("IN SPACE FURNITURE")
    st.markdown("### Your wood's journey from tree to forever-use")
    
    st.markdown('<div class="free-banner">🌟 100% FREE TO USE | OPEN SOURCE</div>', unsafe_allow_html=True)
    
    journey = pd.DataFrame({
        'Stage': ['Tree', 'Sofa', 'Chairs', 'Stool', 'Frame', 'Memory'],
        'Action': ['Harvested', 'Designed by you', 'Made from old sofa', 'Made from chair', 'Made from stool', 'Wood life ends'],
        'Years': [0, 5, 10, 15, 20, 25]
    })
    
    st.dataframe(journey, use_container_width=True, hide_index=True)
    st.info("**Core Idea:** One piece of wood → Multiple products → Until wood dies")

# ========== SECTION 2: SEARCH PRODUCT ==========
elif section == "2. 🔍 Search Product":
    st.title("Step 1: Choose Your Product")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🛋️ SOFA", use_container_width=True):
            st.session_state.user_data['current_product'] = 'Sofa'
            st.success("Selected: Sofa")
    
    with col2:
        if st.button("🪑 CHAIR", use_container_width=True):
            st.session_state.user_data['current_product'] = 'Chair'
            st.success("Selected: Chair")
    
    with col3:
        if st.button("🛏️ BED", use_container_width=True):
            st.session_state.user_data['current_product'] = 'Bed'
            st.success("Selected: Bed")
    
    if st.session_state.user_data['current_product']:
        st.markdown(f"### ✅ Selected: {st.session_state.user_data['current_product']}")

# ========== SECTION 3: LOCATION ==========
elif section == "3. 📍 Location Analysis":
    st.title("Step 2: FREE Location-Based Wood Recommendation")
    
    st.info("💡 Using FREE OpenWeatherMap API")
    
    city = st.text_input("Enter your city:", "Mumbai")
    
    if st.button("🔍 Analyze Climate (FREE)", type="primary"):
        with st.spinner("Fetching real weather data..."):
            analysis = analyze_climate_for_wood(city)
            
            st.markdown(f"### 📍 {city} Analysis")
            
            if 'weather' in analysis:
                w = analysis['weather']
                cols = st.columns(3)
                cols[0].metric("Humidity", f"{w['humidity']}%")
                cols[1].metric("Temperature", f"{w['temp']}°C")
                cols[2].metric("Condition", w['description'])
            
            st.write("**Detected issues:**")
            for issue in analysis['issues']:
                st.write(f"- ⚠️ {issue}")
            
            st.markdown(f"### 🪵 Recommended Wood: **{analysis['wood']}**")
            st.write(f"**Reason:** {analysis['reason']}")
            
            st.session_state.user_data['wood_type'] = analysis['wood']
            st.session_state.user_data['location'] = city

# ========== SECTION 4: ROOM SCAN ==========
elif section == "4. 📏 Room Scan":
    st.title("Step 3: Room Scanning & Placement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        width = st.slider("Room Width (ft)", 8, 30, 15)
    
    with col2:
        length = st.slider("Room Length (ft)", 8, 30, 12)
    
    placement = st.select_slider(
        "Position in room",
        options=["Near window", "Center", "Against wall", "Corner"]
    )
    
    if st.session_state.user_data['current_product'] == 'Sofa':
        sofa_size = 8
        walking_space = width - sofa_size if placement in ["Near window", "Against wall"] else min(width, length) - sofa_size
        
        st.metric("Walking Space", f"{walking_space} ft")
        
        if walking_space >= 4:
            st.success("✅ Good walking space maintained")
        else:
            st.warning("⚠️ Limited walking space")
    
    st.session_state.user_data['room_size'] = f"{width}x{length}ft"
    st.session_state.user_data['placement'] = placement

# ========== SECTION 5: DESIGN ==========
elif section == "5. 🎨 Design Studio":
    st.title("Step 4: FREE AI Design Studio")
    
    st.markdown('<div class="product-box"><h3 style="text-align:center">[YOUR PRODUCT]</h3></div>', unsafe_allow_html=True)
    
    designs = ["Peacock 🦚", "Lion 🦁", "Flowers 🌸", "Geometric ▢", "Tree 🌳", "Birds 🐦"]
    
    selected_designs = st.multiselect("Choose design elements:", designs, default=["Peacock 🦚", "Lion 🦁"])
    
    if selected_designs:
        st.write("**Selected:**", ", ".join(selected_designs))
        
        if st.button("✨ Generate Design (FREE)", type="primary"):
            with st.spinner("Creating your unique design..."):
                time.sleep(1.5)
                
                if "Peacock 🦚" in selected_designs and "Lion 🦁" in selected_designs:
                    st.success("### 🧠 Design Generated!")
                    st.write("**Concept:** Lion sitting under peacock-feather tree")
                    st.image("https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600", caption="Your design concept")
                    st.session_state.user_data['design'] = "Lion under peacock-tree"

# ========== SECTION 6: AR VIEW ==========
elif section == "6. 👁️ AR View":
    st.title("Step 5: FREE Visual Preview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Your Room**")
        uploaded_file = st.file_uploader("Upload room photo", type=['jpg', 'png'])
        if uploaded_file:
            st.image(uploaded_file, caption="Your room", use_container_width=True)
        else:
            st.image("https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400", caption="Example room", use_container_width=True)
    
    with col2:
        st.write("**With Furniture**")
        st.image("https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400", caption="Your furniture in room", use_container_width=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("🔄 Rotate")
    with c2:
        st.button("🔍 Zoom")
    with c3:
        st.button("🌞 Lighting")

# ========== SECTION 7: ORDER ==========
elif section == "7. 💰 Order":
    st.title("Step 6: FREE Quote Request")
    
    st.markdown('<div class="free-banner">NO PAYMENT REQUIRED</div>', unsafe_allow_html=True)
    
    order_data = {
        'Product': [st.session_state.user_data.get('current_product', 'Sofa')],
        'Wood Type': [st.session_state.user_data.get('wood_type', 'Mango Wood')],
        'Design': [st.session_state.user_data.get('design', 'Custom Design')],
        'Room Size': [st.session_state.user_data.get('room_size', '15x12ft')],
        'Est. Price': ['₹25,000 - ₹35,000']
    }
    
    st.dataframe(pd.DataFrame(order_data), use_container_width=True, hide_index=True)
    
    name = st.text_input("Your Name")
    phone = st.text_input("Phone/WhatsApp")
    email = st.text_input("Email")
    
    if st.button("📧 GET FREE QUOTE", type="primary", use_container_width=True):
        if name and phone:
            st.session_state.user_data['order_placed'] = True
            st.session_state.user_data['order_date'] = datetime.now().strftime("%Y-%m-%d")
            st.session_state.user_data['contact_info'] = {'name': name, 'phone': phone, 'email': email}
            
            st.balloons()
            st.success("### ✅ QUOTE REQUESTED!")
            st.write("**Our carpenter will call you within 24 hours**")
        else:
            st.error("Please enter name and phone")

# ========== SECTION 8: DAMAGE ==========
elif section == "8. ⚡ Damage Report":
    st.title("Step 7: FREE Damage Assessment")
    
    if not st.session_state.user_data.get('order_placed'):
        st.warning("Please request a quote first!")
    else:
        st.write(f"Product: {st.session_state.user_data.get('current_product', 'Sofa')}")
        st.write(f"Wood Type: {st.session_state.user_data.get('wood_type', 'Mango Wood')}")
        
        damage_photos = st.file_uploader("Upload damage photos", type=['jpg', 'png'], accept_multiple_files=True)
        
        if damage_photos:
            st.write(f"**Uploaded:** {len(damage_photos)} photos")
            
            if st.button("🔍 FREE Damage Analysis", type="primary"):
                with st.spinner("Analyzing..."):
                    time.sleep(1.5)
                    
                    random.seed(len(damage_photos))
                    good_wood = random.randint(45, 80)
                    damaged_wood = 100 - good_wood
                    
                    st.markdown('<div class="damage-card">', unsafe_allow_html=True)
                    st.markdown("### ⚡ DAMAGE ANALYSIS")
                    
                    cols = st.columns(2)
                    cols[0].metric("Good Wood", f"{good_wood}%")
                    cols[1].metric("Damaged", f"{damaged_wood}%")
                    
                    if good_wood >= 60:
                        new_products = ["2 Chairs", "Coffee Table", "Bookshelf"]
                    elif good_wood >= 40:
                        new_products = ["1 Chair", "Side Table", "Stool"]
                    else:
                        new_products = ["Small Stool", "Picture Frames", "Decorative Box"]
                    
                    st.write("### 🔄 Can be transformed into:")
                    for product in new_products:
                        st.write(f"✓ {product}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.session_state.user_data['current_good_wood'] = good_wood
                    st.session_state.user_data['possible_products'] = new_products

# ========== SECTION 9: TRANSFORM ==========
elif section == "9. 🔄 Transform Product":
    st.title("Step 8: FREE Upcycling")
    
    if not st.session_state.user_data.get('current_good_wood'):
        st.warning("Please analyze damage first!")
    else:
        good = st.session_state.user_data['current_good_wood']
        st.write(f"**Available:** {good}% good wood")
        
        possible = st.session_state.user_data.get('possible_products', ['Chair'])
        new_product = st.selectbox("What to create?", possible)
        
        if new_product:
            st.markdown(f'<div class="product-box"><h3 style="text-align:center">[NEW: {new_product.upper()}]</h3></div>', unsafe_allow_html=True)
            
            if st.button("🚀 REQUEST FREE TRANSFORMATION", type="primary"):
                old = st.session_state.user_data.get('current_product', 'Sofa')
                
                if 'product_history' not in st.session_state.user_data:
                    st.session_state.user_data['product_history'] = []
                
                st.session_state.user_data['product_history'].append({
                    'from': old,
                    'to': new_product,
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'wood_used': good
                })
                
                st.session_state.user_data['current_product'] = new_product
                
                st.balloons()
                st.success(f"### ✅ TRANSFORMATION REQUESTED!")
                
                if 'product_history' in st.session_state.user_data:
                    journey_df = pd.DataFrame(st.session_state.user_data['product_history'])
                    st.dataframe(journey_df, use_container_width=True, hide_index=True)
                
                st.info("**Until the wood dies, we keep making new products from it**")

# ========== FOOTER ==========
st.markdown("---")
st.markdown('<div class="free-banner">🌟 100% FREE & OPEN SOURCE</div>', unsafe_allow_html=True)
