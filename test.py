import streamlit as st

st.set_page_config(page_title="EBA Express", layout="wide")

# ----------------- GLOBAL SESSION STATE -----------------
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {item_name: {"price": float, "qty": int}}

# ----------------- DATA MODEL (MOCK MENU) -----------------
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

# ----------------- HELPERS (BACKEND-LIKE FUNCTIONS) -----------------
def add_to_cart(item_name: str, price: float):
    cart = st.session_state.cart
    if item_name not in cart:
        cart[item_name] = {"price": price, "qty": 0}
    cart[item_name]["qty"] += 1

def clear_cart():
    st.session_state.cart = {}

def cart_total():
    return sum(v["price"] * v["qty"] for v in st.session_state.cart.values())

# ----------------- PAGE FUNCTIONS -----------------
def page_home():
    st.title("🍔 EBA Express")
    st.subheader("AI-Enabled Online Restaurant – Delicious Food, Delivered Fast!")
    st.image("https://placehold.co/1200x350?text=EBA+Express+Hero+Image", use_container_width=True)

    st.markdown("### Why EBA Express?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Personalized Menu**")
        st.caption("See dishes recommended for you based on past orders and ratings.")
    with col2:
        st.markdown("**Smart Delivery**")
        st.caption("Delivery bidding ensures fair pricing and fast arrival.")
    with col3:
        st.markdown("**AI Assistant**")
        st.caption("Ask our chatbot anything about orders, dishes, or policies.")

    st.markdown("---")
    st.markdown("### Quick Links")
    st.markdown("- Go to the **Menu** page to place an order.")
    st.markdown("- Visit **About Us** to see how the system works.")
    st.markdown("- Use **Contact** if you want to send feedback or complaints.")


def page_menu():
    st.title("Menu")
    st.markdown("Choose from our curated selection of dishes.")

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
                # later: call backend OrderService.create_order(...)
                st.button("Checkout (Mock)", use_container_width=True)

        st.markdown("---")
        st.caption("Later, this page will connect to your backend order, deposit, and VIP logic.")


def page_about():
    st.title("About Us")
    st.markdown("### What is EBA Express?")
    st.write(
        "EBA Express is an AI-enabled online restaurant platform that lets customers "
        "browse a personalized menu, place orders, and get smart delivery. "
        "Managers use the system to monitor staff performance, handle complaints, and "
        "maintain a knowledge base that powers the AI assistant."
    )

    st.markdown("### Key Features")
    st.markdown("""
    - Deposit-based payment and VIP customer logic  
    - Delivery bidding system for fair and transparent delivery fees  
    - Reputation and HR rules for chefs, delivery people, and customers  
    - AI chatbot backed by a local knowledge base + LLM fallback
    """)

    st.markdown("### Technology Stack")
    st.markdown("""
    - **Frontend:** Streamlit, HTML/CSS  
    - **Backend / Logic:** Python services (OrderService, FinanceService, HRService, ChatService, etc.)  
    - **Database:** PostgreSQL (or similar relational DB)  
    - **AI:** LLM API + local knowledge base for restaurant-specific questions
    """)


def page_contact():
    st.title("Contact Us")

    st.markdown("Use this form to send feedback, complaints, or general questions.")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        topic = st.selectbox("Topic", ["General Question", "Complaint", "Compliment", "Technical Issue"])
        message = st.text_area("Message")

        submitted = st.form_submit_button("Submit")
        if submitted:
            # backend: save to DB or send email; for now, just acknowledge
            st.success("Thank you for contacting EBA Express. We have received your message.")

    st.markdown("---")
    st.caption("In the full system, this will create a record for the manager or trigger a complaint workflow.")


def page_location():
    st.title("Our Location")

    st.markdown("### Find EBA Express")
    st.write("123 AI Avenue, New York, NY 10001")

    st.markdown("#### Map (placeholder)")
    st.image("https://placehold.co/800x400?text=Map+Placeholder", use_container_width=True)

    st.markdown("#### Hours")
    st.markdown("""
    - Monday–Friday: 11:00 AM – 10:00 PM  
    - Saturday–Sunday: 12:00 PM – 11:00 PM
    """)

    st.markdown("#### Delivery Coverage")
    st.write(
        "We deliver within a 5-mile radius of our main location. "
        "In Phase 2/3, this page can connect to backend logic to show delivery eligibility based on the user’s address."
    )

# ----------------- SIDEBAR NAVIGATION + ASSISTANT -----------------
st.sidebar.title("EBA Express")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Menu", "About Us", "Contact", "Location"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Assistant")

ai_tab = st.sidebar.radio("Mode", ["Info", "Ask AI"], label_visibility="collapsed", key="ai_mode_radio")

if ai_tab == "Ask AI":
    st.sidebar.write("Ask EBA Assistant")
    question = st.sidebar.text_area("Question", height=80, placeholder="Ask about dishes, delivery, hours...")
    if st.sidebar.button("Send", use_container_width=True):
        # later: call ChatService.answer_question(...)
        st.sidebar.info("AI response placeholder.")
else:
    st.sidebar.markdown(
        "- Use the **Menu** page to browse and order.\n"
        "- The **Assistant** will later connect to your AI backend."
    )

# ----------------- PAGE ROUTER -----------------
if page == "Home":
    page_home()
elif page == "Menu":
    page_menu()
elif page == "About Us":
    page_about()
elif page == "Contact":
    page_contact()
elif page == "Location":
    page_location()
