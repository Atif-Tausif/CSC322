import streamlit as st

st.set_page_config(page_title="EBA Express", layout="wide")

st.title("🍔 EBA Express")
st.markdown("**AI-Enabled Online Restaurant – Delicious Food, Delivered Fast!**")
st.image("https://placehold.co/1200x350?text=EBA+Express+Hero+Image", width='stretch')
st.markdown("---")  # Optional separator line

# ----------------- SESSION STATE -----------------
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {item_name: {"price": float, "qty": int}}


# ----------------- DATA MODEL (SIMPLE MOCK) -----------------
menu_items = [
    {
        "name": "Classic Burger",
        "description": "Juicy beef patty, cheddar, lettuce, tomato, and house sauce.",
        "price": 11.99,
        "category": "Main",
        "image": "https://blog-content.omahasteaks.com/wp-content/uploads/2022/06/blogwp_classic-american-burger-scaled-1.jpg",
        "featured": True,
    },
    {
        "name": "Creamy Alfredo Pasta",
        "description": "Fettuccine tossed in rich parmesan cream sauce.",
        "price": 13.50,
        "category": "Main",
        "image": "https://www.vanillabeancuisine.com/wp-content/uploads/2024/12/Spaghetti-Alfredo-2nd-Set-7.jpg",
        "featured": True,
    },
    {
        "name": "Garden Salad",
        "description": "Mixed greens, cherry tomatoes, cucumber, light vinaigrette.",
        "price": 8.25,
        "category": "Side",
        "image": "https://feelgoodfoodie.net/wp-content/uploads/2023/03/Everyday-Garden-Salad-07-500x500.jpg",
        "featured": True,
    },
    {
        "name": "Tomato Basil Soup",
        "description": "Slow-cooked tomato soup with fresh basil and cream.",
        "price": 6.75,
        "category": "Side",
        "image": "https://sugarspunrun.com/wp-content/uploads/2024/08/Fresh-Roasted-Tomato-Basil-Soup-1-of-1-2.jpg",
        "featured": False,
    },
    {
        "name": "Chicken Sandwich",
        "description": "Grilled chicken, lettuce, tomato, mayo on brioche bun.",
        "price": 10.50,
        "category": "Main",
        "image": "https://www.cucinabyelena.com/wp-content/uploads/2024/03/Ultimate-Grilled-Chicken-Sandwich-Recipe-16-scaled.jpg",
        "featured": False,
    },
]

# ----------------- HELPERS -----------------
def add_to_cart(item_name: str, price: float):
    cart = st.session_state.cart
    if item_name not in cart:
        cart[item_name] = {"price": price, "qty": 0}
    cart[item_name]["qty"] += 1

def clear_cart():
    st.session_state.cart = {}

def cart_total():
    return sum(v["price"] * v["qty"] for v in st.session_state.cart.values())

# ----------------- SIDEBAR: ASSISTANT -----------------
st.sidebar.title("Assistant")

ai_tab = st.sidebar.radio("Mode", ["Info", "Ask AI"], label_visibility="collapsed")

if ai_tab == "Ask AI":
    st.sidebar.subheader("Ask EBA Assistant")
    user_question = st.sidebar.text_area(
        "Question",
        height=80,
        placeholder="Ask about dishes, delivery, hours..."
    )
    if st.sidebar.button("Send", width='stretch'):
        # Placeholder: integrate with LLM later
        st.sidebar.info("AI response placeholder. (Connect to ChatService/LLM in backend.)")
else:
    st.sidebar.markdown(
        "- Browse menu and add items to your cart.\n"
        "- Track cart total in real time.\n"
        "- Use *Ask AI* to hook into your future chatbot."
    )

# ----------------- MAIN LAYOUT -----------------
left_col, right_col = st.columns([3, 1])

# -------- LEFT: FEATURED + MENU --------
with left_col:
    st.subheader("Featured Items")

    featured = [m for m in menu_items if m["featured"]]
    if featured:
        cols = st.columns(len(featured))
        for col, item in zip(cols, featured):
            with col:
                st.image(item["image"], caption=item["name"], width='stretch')
                st.caption(item["description"])
                st.markdown(f"**${item['price']:.2f}**")
                if st.button("Add to Cart", key=f"feat_{item['name']}"):
                    add_to_cart(item["name"], item["price"])
    else:
        st.write("No featured items available.")

    st.markdown("---")

    # Search + filters
    st.subheader("Full Menu")
    top_filter_col1, top_filter_col2 = st.columns([3, 1])

    with top_filter_col1:
        search_query = st.text_input(
            "Search menu",
            value="",
            placeholder="Type a dish name or keyword...",
        )

    with top_filter_col2:
        categories = sorted(set(m["category"] for m in menu_items))
        selected_category = st.selectbox(
            "Category",
            options=["All"] + categories,
            index=0,
        )

    # Filtered items
    filtered_items = menu_items
    if search_query:
        sq = search_query.lower()
        filtered_items = [
            m for m in filtered_items
            if sq in m["name"].lower() or sq in m["description"].lower()
        ]
    if selected_category != "All":
        filtered_items = [m for m in filtered_items if m["category"] == selected_category]

    if not filtered_items:
        st.info("No menu items match your search/filter.")
    else:
        for item in filtered_items:
            with st.container(border=True):
                cols = st.columns([1, 2, 1])
                with cols[0]:
                    st.image(item["image"], width='stretch')
                with cols[1]:
                    st.markdown(f"### {item['name']}")
                    st.markdown(item["description"])
                    st.markdown(f"**Category:** {item['category']}")
                with cols[2]:
                    st.markdown(f"### ${item['price']:.2f}")
                    if st.button(
                        "Add to Cart",
                        key=f"add_{item['name']}",
                        width='stretch',
                    ):
                        add_to_cart(item["name"], item["price"])

# -------- RIGHT: CART SUMMARY --------
with right_col:
    st.subheader("Your Cart")
    if not st.session_state.cart:
        st.write("Cart is empty.")
    else:
        for name, info in st.session_state.cart.items():
            qty = info["qty"]
            price = info["price"]
            st.markdown(
                f"**{name}**  \n"
                f"Qty: {qty} | Unit: ${price:.2f} | Subtotal: ${price * qty:.2f}"
            )
            st.divider()

        total = cart_total()
        st.markdown(f"### Total: ${total:.2f}")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Clear Cart", width='stretch'):
                clear_cart()
                st.experimental_rerun()
        with col_b:
            st.button("Checkout (Mock)", width='stretch')
