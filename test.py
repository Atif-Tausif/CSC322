import streamlit as st

st.set_page_config(page_title="EBA Express", layout="wide")

# ----------------- SESSION STATE -----------------
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {item_name: {"price": float, "qty": int}}

# ----------------- NAVBAR HTML -----------------
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

        /* Make Streamlit content start lower so it doesn't hide under navbar */
        .main > div {
            padding-top: 80px;
        }
    </style>

    <div id="custom-navbar">
        <div class="navbar-left">
            <div class="hamburger">☰</div>
            <div class="navbar-title">EBA Express</div>
        </div>

        <div class="navbar-center">
            <input type="text" placeholder="Search menu (UI only)...">
        </div>

        <div class="navbar-right">
            <div class="icon-btn" onclick="window.alert('Cart clicked!')">🛒</div>
            <img src="https://placehold.co/40x40" class="profile-pic" onclick="window.alert('Profile clicked!')">
        </div>
    </div>
""")

# ----------------- DATA MODEL (SIMPLE MOCK) -----------------
menu_items = [
    {
        "name": "Classic Burger",
        "description": "Juicy beef patty, cheddar, lettuce, tomato, and house sauce.",
        "price": 11.99,
        "category": "Main",
        "image": "https://placehold.co/400x250?text=Burger",
        "featured": True,
    },
    {
        "name": "Creamy Alfredo Pasta",
        "description": "Fettuccine tossed in rich parmesan cream sauce.",
        "price": 13.50,
        "category": "Main",
        "image": "https://placehold.co/400x250?text=Pasta",
        "featured": True,
    },
    {
        "name": "Garden Salad",
        "description": "Mixed greens, cherry tomatoes, cucumber, light vinaigrette.",
        "price": 8.25,
        "category": "Side",
        "image": "https://placehold.co/400x250?text=Salad",
        "featured": True,
    },
    {
        "name": "Tomato Basil Soup",
        "description": "Slow-cooked tomato soup with fresh basil and cream.",
        "price": 6.75,
        "category": "Side",
        "image": "https://placehold.co/400x250?text=Soup",
        "featured": False,
    },
    {
        "name": "Chicken Sandwich",
        "description": "Grilled chicken, lettuce, tomato, mayo on brioche bun.",
        "price": 10.50,
        "category": "Main",
        "image": "https://placehold.co/400x250?text=Sandwich",
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
    user_question = st.sidebar.text_area("Question", height=80, placeholder="Ask about dishes, delivery, hours...")
    if st.sidebar.button("Send", use_container_width=True):
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
                st.image(item["image"], caption=item["name"], use_container_width=True)
                st.caption(item["description"])
                st.markdown(f"**${item['price']:.2f}**")
                if st.button(f"Add to Cart", key=f"feat_{item['name']}"):
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
                    st.image(item["image"], use_container_width=True)
                with cols[1]:
                    st.markdown(f"### {item['name']}")
                    st.markdown(item["description"])
                    st.markdown(f"**Category:** {item['category']}")
                with cols[2]:
                    st.markdown(f"### ${item['price']:.2f}")
                    if st.button(
                        "Add to Cart",
                        key=f"add_{item['name']}",
                        use_container_width=True,
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
            if st.button("Clear Cart", use_container_width=True):
                clear_cart()
                st.experimental_rerun()
        with col_b:
            st.button("Checkout (Mock)", use_container_width=True)

    st.markdown("---")
    st.caption(
        "In Phase 2/3, this cart will connect to your `OrderService.create_order` "
        "and enforce deposit / VIP logic from the design report."
    )
