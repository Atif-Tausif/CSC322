import streamlit as st

st.set_page_config(page_title="EBA Express", layout="wide")
#atifs a 
# Inject at root level
st.html("""
    <style>
        #custom-navbar {
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 65px;
            padding: 12px 25px;
            background: white;
            border-bottom: 1px solid #ccc;
            display: flex;
            align-items: center;
            justify-content: space-between;
            z-index: 999999 !important;
        }

        .navbar-left {
            display: flex;
            align-items: center;
            gap: 18px;
        }

        .hamburger {
            cursor: pointer;
            font-size: 26px;
            padding: 4px 8px;
            border-radius: 6px;
            transition: background 0.2s;
            user-select: none;
        }
        .hamburger:hover {
            background: #eeeeee;
        }

        .navbar-title {
            font-size: 26px;
            font-weight: bold;
            position: relative;
            left: -5px;
        }

        .navbar-center {
            flex: 1;
            display: flex;
            justify-content: center;
        }
        .navbar-center input {
            width: 60%;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #bbb;
        }

        .navbar-right {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .icon-btn {
            font-size: 24px;
            cursor: pointer;
            padding: 6px;
            border-radius: 6px;
            transition: background 0.2s;
            user-select: none;
        }
        .icon-btn:hover {
            background: #f0f0f0;
        }

        .profile-pic {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 1px solid #888;
            object-fit: cover;
            cursor: pointer;
        }
    </style>

    <div id="custom-navbar">
        <div class="navbar-left">
            <div class="hamburger">☰</div>
            <div class="navbar-title">EBA Express</div>
        </div>

        <div class="navbar-center">
            <input type="text" placeholder="Search menu...">
        </div>

        <div class="navbar-right">
            <div class="icon-btn" onclick="window.alert('Cart clicked!')">🛒</div>
            <img src="https://placehold.co/40x40" class="profile-pic" onclick="window.alert('Profile clicked!')">
        </div>
    </div>
""")

# Push content down so it doesn't overlap
st.write("")
st.write("")
st.write("")
st.write("")

# --- Sidebar (AI Assistant) ---
st.sidebar.title("Assistant")
ai_mode = st.sidebar.button("Ask AI")

if ai_mode:
    st.sidebar.write("AI mode activated (placeholder).")
    user_question = st.sidebar.text_input("Ask a question:")
    if user_question:
        st.sidebar.write("AI response will appear here...")
else:
    st.sidebar.write("Press the button to ask the AI.")

# --- Main Page Content ---
st.subheader("Featured Items")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://placehold.co/200x150", caption="Dish 1")
    st.button("Add Dish 1 to Cart")

with col2:
    st.image("https://placehold.co/200x150", caption="Dish 2")
    st.button("Add Dish 2 to Cart")

with col3:
    st.image("https://placehold.co/200x150", caption="Dish 3")
    st.button("Add Dish 3 to Cart")

st.subheader("Full Menu")
menu_items = ["Burger", "Pasta", "Salad", "Soup", "Sandwich"]

for item in menu_items:
    with st.container():
        st.write(f"### {item}")
        st.write("Description: Placeholder description.")
        st.write("Price: $0.00")
        st.button(f"Add {item} to Cart")
        st.divider()
