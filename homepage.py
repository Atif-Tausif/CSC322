import streamlit as st

st.set_page_config(page_title="EBA Express Home", layout="wide")

# ----------------- SIDEBAR -----------------
st.sidebar.title("Navigation")

if st.sidebar.button("Home"):
    st.experimental_set_query_params(page="home")
    st.experimental_rerun()

if st.sidebar.button("Menu"):
    st.experimental_set_query_params(page="menu")
    st.experimental_rerun()

if st.sidebar.button("Cart"):
    st.experimental_set_query_params(page="cart")
    st.experimental_rerun()

if st.sidebar.button("AI Assistant"):
    st.experimental_set_query_params(page="ai")
    st.experimental_rerun()

if st.sidebar.button("About Us"):
    st.experimental_set_query_params(page="about")
    st.experimental_rerun()

# ----------------- HERO / TITLE -----------------
st.title("🍔 EBA Express")
st.markdown("**AI-Enabled Online Restaurant – Delicious Food, Delivered Fast!**")
st.image("https://placehold.co/1200x350?text=EBA+Express+Hero+Image", width='stretch')

# ----------------- BRIEF DESCRIPTION -----------------
st.markdown(
    """
    Welcome to **EBA Express**! We bring you the tastiest dishes, made fresh every day,
    and delivered right to your door. Whether you are craving a hearty burger, 
    creamy pasta, or fresh salads, we have something for everyone.
    """
)

# ----------------- GALLERY / IMAGES -----------------
st.subheader("Our Specialties")
cols = st.columns(3)
special_images = [
    "https://placehold.co/400x250?text=Burger",
    "https://placehold.co/400x250?text=Pasta",
    "https://placehold.co/400x250?text=Salad"
]
special_captions = ["Classic Burger", "Creamy Alfredo Pasta", "Garden Salad"]

for col, img, cap in zip(cols, special_images, special_captions):
    with col:
        st.image(img, caption=cap, width='stretch')

# ----------------- HOURS & CONTACT -----------------
st.markdown("---")
st.subheader("Hours & Contact Info")

st.markdown(
    """
    **Hours of Operation:**  
    Monday - Friday: 10:00 AM - 9:00 PM  
    Saturday: 11:00 AM - 10:00 PM  
    Sunday: Closed

    **Address:** 123 Main Street, Anytown, USA  
    **Phone:** (123) 456-7890  
    **Email:** contact@ebaexpress.com
    """
)

# ----------------- FOOTER -----------------
st.markdown("---")
st.caption("© 2025 EBA Express | All rights reserved")
