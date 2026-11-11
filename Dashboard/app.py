
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from pymongo import MongoClient
from dotenv import load_dotenv
import os


# -----------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="E-commerce Data Analysis",
    page_icon="🛒",
    layout="wide"
)

st.title("E-commerce Data Analysis Dashboard")
st.write("Analysis of products, inventory, customers, orders, payments and reviews.")


# -----------------------------------
# 2. MONGODB CONNECTION
# -----------------------------------

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    st.error("MongoDB connection string not found in .env file.")
    st.stop()

client = MongoClient(MONGODB_URI)

db = client["ecommerce_analysis"]


# -----------------------------------
# 3. SELECT COLLECTIONS
# -----------------------------------

products = db["products"]
product_inventories = db["product_inventories"]
warehouses = db["warehouses"]

users = db["users"]
orders = db["orders"]
order_items = db["order_items"]

payments = db["payments"]
addresses = db["addresses"]
product_reviews = db["product_reviews"]


# -----------------------------------
# 4. FETCH DATA FROM MONGODB
# -----------------------------------

products_data = list(
    products.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "name": 1,
            "price": 1,
            "category_id": 1,
            "brand_id": 1,
            "is_active": 1
        }
    )
)

inventory_data = list(
    product_inventories.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "product_id": 1,
            "warehouse_id": 1,
            "quantity_on_hand": 1,
            "quantity_reserved": 1,
            "reorder_level": 1
        }
    )
)

warehouses_data = list(
    warehouses.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "name": 1
        }
    )
)

users_data = list(
    users.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "email": 1,
            "first_name": 1,
            "last_name": 1
        }
    )
)

orders_data = list(
    orders.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "user_id": 1,
            "created_at": 1,
            "order_date": 1,
            "order_status_id": 1
        }
    )
)

order_items_data = list(
    order_items.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "order_id": 1,
            "product_id": 1,
            "quantity": 1,
            "unit_price": 1
        }
    )
)

payments_data = list(
    payments.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "order_id": 1,
            "payment_method_id": 1,
            "amount": 1,
            "payment_status": 1
        }
    )
)

addresses_data = list(
    addresses.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "user_id": 1,
            "city": 1,
            "state": 1,
            "country": 1
        }
    )
)

reviews_data = list(
    product_reviews.find(
        {},
        {
            "_id": 0,
            "id": 1,
            "user_id": 1,
            "product_id": 1,
            "rating": 1,
            "review": 1,
            "created_at": 1
        }
    )
)


# -----------------------------------
# 5. CONVERT DATA INTO DATAFRAMES
# -----------------------------------

products_df = pd.DataFrame(products_data)
inventory_df = pd.DataFrame(inventory_data)
warehouses_df = pd.DataFrame(warehouses_data)

users_df = pd.DataFrame(users_data)
orders_df = pd.DataFrame(orders_data)
order_items_df = pd.DataFrame(order_items_data)

payments_df = pd.DataFrame(payments_data)
addresses_df = pd.DataFrame(addresses_data)
reviews_df = pd.DataFrame(reviews_data)


# -----------------------------------
# 6. DATA PREPROCESSING
# -----------------------------------

if "price" in products_df.columns:
    products_df["price"] = pd.to_numeric(
        products_df["price"], errors="coerce"
    )

inventory_df["quantity_on_hand"] = pd.to_numeric(
    inventory_df["quantity_on_hand"], errors="coerce"
)

inventory_df["quantity_reserved"] = pd.to_numeric(
    inventory_df["quantity_reserved"], errors="coerce"
)

inventory_df["reorder_level"] = pd.to_numeric(
    inventory_df["reorder_level"], errors="coerce"
)

inventory_df["available_quantity"] = (
    inventory_df["quantity_on_hand"]
    - inventory_df["quantity_reserved"]
)

if "quantity" in order_items_df.columns:
    order_items_df["quantity"] = pd.to_numeric(
        order_items_df["quantity"], errors="coerce"
    )

if "unit_price" in order_items_df.columns:
    order_items_df["unit_price"] = pd.to_numeric(
        order_items_df["unit_price"], errors="coerce"
    )

if "amount" in payments_df.columns:
    payments_df["amount"] = pd.to_numeric(
        payments_df["amount"], errors="coerce"
    )

if "rating" in reviews_df.columns:
    reviews_df["rating"] = pd.to_numeric(
        reviews_df["rating"], errors="coerce"
    )


# -----------------------------------
# 7. CREATE REQUIRED DATAFRAMES
# -----------------------------------

# Connecting product inventory with products

if "product_id" in inventory_df.columns and "id" in products_df.columns:

    inventory_product_df = pd.merge(
        inventory_df,
        products_df[["id", "name", "price"]],
        left_on="product_id",
        right_on="id",
        how="left"
    )

else:
    inventory_product_df = inventory_df.copy()


# Connecting product inventory with warehouses

if "warehouse_id" in inventory_df.columns and "id" in warehouses_df.columns:

    inventory_warehouse_df = pd.merge(
        inventory_df,
        warehouses_df,
        left_on="warehouse_id",
        right_on="id",
        how="left"
    )

else:
    inventory_warehouse_df = inventory_df.copy()


# Connecting users with orders

if "user_id" in orders_df.columns and "id" in users_df.columns:

    customer_orders_df = pd.merge(
        orders_df,
        users_df,
        left_on="user_id",
        right_on="id",
        how="left"
    )

else:
    customer_orders_df = orders_df.copy()


# Connecting order items with products

if "product_id" in order_items_df.columns and "id" in products_df.columns:

    order_product_df = pd.merge(
        order_items_df,
        products_df[["id", "name", "price"]],
        left_on="product_id",
        right_on="id",
        how="left"
    )

else:
    order_product_df = order_items_df.copy()


# -----------------------------------
# 8. SIDEBAR
# -----------------------------------

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Overview",
        "Product Analysis",
        "Inventory Analysis",
        "Order Analysis",
        "Customer Analysis",
        "Payment Analysis",
        "Review Analysis"
    ]
)


# -----------------------------------
# 9. OVERVIEW DASHBOARD
# -----------------------------------

if page == "Overview":

    st.header("E-commerce Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Products", len(products_df))
    col2.metric("Total Customers", len(users_df))
    col3.metric("Total Orders", len(orders_df))
    col4.metric("Total Payments", len(payments_df))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Product Price Distribution")

        if "price" in products_df.columns:

            fig = px.histogram(
                products_df,
                x="price",
                nbins=20,
                title="Distribution of Product Prices"
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Product Availability")

        if "is_active" in products_df.columns:

            active_data = products_df["is_active"].value_counts().reset_index()
            active_data.columns = ["Status", "Count"]

            active_data["Status"] = active_data["Status"].astype(str)

            fig = px.pie(
                active_data,
                names="Status",
                values="Count",
                title="Active vs Inactive Products"
            )

            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent Products")

    st.dataframe(products_df.head(10), use_container_width=True)


# -----------------------------------
# 10. PRODUCT ANALYSIS
# -----------------------------------

elif page == "Product Analysis":

    st.header("Product Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", len(products_df))

    if "price" in products_df.columns:

        col2.metric(
            "Average Price",
            round(products_df["price"].mean(), 2)
        )

        col3.metric(
            "Maximum Price",
            round(products_df["price"].max(), 2)
        )

    st.divider()

    if "price" in products_df.columns:

        st.subheader("Product Price Distribution")

        fig = px.histogram(
            products_df,
            x="price",
            nbins=20,
            title="Product Price Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top 10 Most Expensive Products")

        expensive_products = products_df.sort_values(
            by="price",
            ascending=False
        ).head(10)

        fig = px.bar(
            expensive_products,
            x="name",
            y="price",
            title="Top 10 Expensive Products"
        )

        st.plotly_chart(fig, use_container_width=True)

    if "is_active" in products_df.columns:

        st.subheader("Product Status")

        status_data = products_df["is_active"].value_counts().reset_index()
        status_data.columns = ["Status", "Count"]

        fig = px.bar(
            status_data,
            x="Status",
            y="Count",
            title="Active and Inactive Products"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Product Details")

    st.dataframe(products_df, use_container_width=True)


# -----------------------------------
# 11. INVENTORY ANALYSIS
# -----------------------------------

elif page == "Inventory Analysis":

    st.header("Inventory Analysis")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Inventory Records",
        len(inventory_df)
    )

    col2.metric(
        "Total Stock",
        int(inventory_df["quantity_on_hand"].sum())
    )

    col3.metric(
        "Reserved Stock",
        int(inventory_df["quantity_reserved"].sum())
    )

    col4.metric(
        "Available Stock",
        int(inventory_df["available_quantity"].sum())
    )

    st.divider()

    # Product-wise Stock

    st.subheader("Product-wise Stock")

    product_stock = inventory_product_df.groupby(
        "name"
    )["quantity_on_hand"].sum().reset_index()

    product_stock = product_stock.sort_values(
        by="quantity_on_hand",
        ascending=False
    ).head(10)

    fig = px.bar(
        product_stock,
        x="name",
        y="quantity_on_hand",
        title="Top 10 Products by Stock"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Warehouse-wise Stock

    st.subheader("Warehouse-wise Stock")

    warehouse_stock = inventory_warehouse_df.groupby(
        "name"
    )["quantity_on_hand"].sum().reset_index()

    fig = px.bar(
        warehouse_stock,
        x="name",
        y="quantity_on_hand",
        title="Stock Available in Each Warehouse"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Reorder Analysis

    st.subheader("Products Requiring Reorder")

    reorder_data = inventory_df[
        inventory_df["quantity_on_hand"] <= inventory_df["reorder_level"]
    ]

    st.metric(
        "Inventory Records Below Reorder Level",
        len(reorder_data)
    )

    st.dataframe(reorder_data, use_container_width=True)

    # Inventory Records

    st.subheader("Complete Inventory Records")

    st.dataframe(inventory_df, use_container_width=True)

# -----------------------------------
# 12. ORDER ANALYSIS
# -----------------------------------

elif page == "Order Analysis":

    st.header("Order Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", len(orders_df))
    col2.metric("Total Order Items", len(order_items_df))

    if "user_id" in orders_df.columns:

        col3.metric(
            "Unique Customers",
            orders_df["user_id"].nunique()
        )

    st.divider()

    if "quantity" in order_items_df.columns:

        st.subheader("Total Products Ordered")

        st.metric(
            "Total Quantity",
            int(order_items_df["quantity"].sum())
        )

    if "name" in order_product_df.columns:

        st.subheader("Most Ordered Products")

        most_ordered = order_product_df.groupby(
            "name"
        )["quantity"].sum().reset_index()

        most_ordered = most_ordered.sort_values(
            by="quantity",
            ascending=False
        ).head(10)

        fig = px.bar(
            most_ordered,
            x="name",
            y="quantity",
            title="Top 10 Most Ordered Products"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Order Records")

    st.dataframe(orders_df, use_container_width=True)

    st.subheader("Order Item Records")

    st.dataframe(order_items_df, use_container_width=True)


# -----------------------------------
# 13. CUSTOMER ANALYSIS
# -----------------------------------

elif page == "Customer Analysis":

    st.header("Customer Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Customers", len(users_df))

    if "user_id" in orders_df.columns:

        col2.metric(
            "Customers Who Placed Orders",
            orders_df["user_id"].nunique()
        )

        col3.metric(
            "Customers Without Orders",
            len(users_df) - orders_df["user_id"].nunique()
        )

    st.divider()

    if "user_id" in orders_df.columns:

        st.subheader("Top 10 Customers by Orders")

        customer_order_count = orders_df.groupby(
            "user_id"
        ).size().reset_index(name="total_orders")

        if "id" in users_df.columns:

            customer_order_count = pd.merge(
                customer_order_count,
                users_df,
                left_on="user_id",
                right_on="id",
                how="left"
            )

        if "first_name" in customer_order_count.columns:

            customer_order_count["customer_name"] = (
                customer_order_count["first_name"].fillna("")
                + " "
                + customer_order_count["last_name"].fillna("")
            )

            fig = px.bar(
                customer_order_count.sort_values(
                    by="total_orders",
                    ascending=False
                ).head(10),
                x="customer_name",
                y="total_orders",
                title="Top 10 Customers by Number of Orders"
            )

            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Details")

    st.dataframe(users_df, use_container_width=True)

    st.subheader("Customer Addresses")

    st.dataframe(addresses_df, use_container_width=True)


# -----------------------------------
# 14. PAYMENT ANALYSIS
# -----------------------------------

elif page == "Payment Analysis":

    st.header("Payment Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Payments", len(payments_df))

    if "amount" in payments_df.columns:

        col2.metric(
            "Total Payment Amount",
            round(payments_df["amount"].sum(), 2)
        )

        col3.metric(
            "Average Payment",
            round(payments_df["amount"].mean(), 2)
        )

    st.divider()

    if "payment_status" in payments_df.columns:

        st.subheader("Payment Status Distribution")

        payment_status = payments_df[
            "payment_status"
        ].value_counts().reset_index()

        payment_status.columns = ["Status", "Count"]

        fig = px.pie(
            payment_status,
            names="Status",
            values="Count",
            title="Payment Status"
        )

        st.plotly_chart(fig, use_container_width=True)

    if "amount" in payments_df.columns:

        st.subheader("Payment Amount Distribution")

        fig = px.histogram(
            payments_df,
            x="amount",
            nbins=20,
            title="Distribution of Payment Amounts"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Payment Records")

    st.dataframe(payments_df, use_container_width=True)


# -----------------------------------
# 15. PRODUCT REVIEW ANALYSIS
# -----------------------------------

elif page == "Review Analysis":

    st.header("Product Review Analysis")

    col1, col2 = st.columns(2)

    col1.metric("Total Reviews", len(reviews_df))

    if "rating" in reviews_df.columns:

        col2.metric(
            "Average Rating",
            round(reviews_df["rating"].mean(), 2)
        )

    st.divider()

    if "rating" in reviews_df.columns:

        st.subheader("Rating Distribution")

        rating_count = reviews_df["rating"].value_counts().reset_index()
        rating_count.columns = ["Rating", "Count"]

        fig = px.bar(
            rating_count.sort_values("Rating"),
            x="Rating",
            y="Count",
            title="Distribution of Product Ratings"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Product Reviews")

    st.dataframe(reviews_df, use_container_width=True)


# -----------------------------------
# 16. FOOTER
# -----------------------------------

st.divider()

st.caption("E-commerce Data Analysis Project | MongoDB, PyMongo, Pandas, NumPy, Plotly and Streamlit")
