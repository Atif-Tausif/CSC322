import streamlit as st

st.set_page_config(page_title="EBA Express", layout="wide")

# Sidebar – AI Assistant Button/Section
st.sidebar.title("Assistant")
ai_mode = st.sidebar.button("Ask AI")

if ai_mode:
    st.sidebar.write("AI mode activated (placeholder).")
    user_question = st.sidebar.text_input("Ask a question:")
    if user_question:
        st.sidebar.write("AI response will appear here...")
else:
    st.sidebar.write("Press the button to ask the AI.")


# Main Page – Menu
st.title("EBA Express Menu")

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
