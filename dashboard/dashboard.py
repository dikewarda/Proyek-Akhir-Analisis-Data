import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule="D", on="order_purchase_timestamp").agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })

    daily_orders_df.reset_index(inplace=True)
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)

    return daily_orders_df


def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule="M", on="order_purchase_timestamp").agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })

    monthly_orders_df.reset_index(inplace=True)
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)

    monthly_orders_df.sort_values(
        by="order_purchase_timestamp", ascending=True, inplace=True)

    return monthly_orders_df


def create_byproduct_df(df):
    byproduct_df = df.groupby(by="product_id").order_item_id.sum()\
        .sort_values(ascending=False).reset_index()
    byproduct_df.columns = ["product_id", "product_count"]

    return byproduct_df


def create_byproduct_category_df(df):
    byproduct_category_df = all_df.groupby(by="product_category_name_english").agg({
        "order_item_id": "sum",
        "seller_id": "nunique",
        "review_score": "mean"
    }).reset_index()
    byproduct_category_df.columns = ["product_category_name_english",
                                     "order_count", "seller_count", "review_score"]
    byproduct_category_df.sort_values(
        by="order_count", ascending=False)
    byproduct_category_df["review_score"] = byproduct_category_df[
        "review_score"].round(2)

    return byproduct_category_df


def create_bycustomer_city_df(df):
    bycustomer_city_df = df.groupby(by="customer_city").agg({
        "customer_id": "nunique"
    }).sort_values(by="customer_id", ascending=False).reset_index()
    bycustomer_city_df.columns = ["customer_city", "customer_count"]

    return bycustomer_city_df


def create_bycustomer_state_df(df):
    bycustomer_state_df = df.groupby(by="customer_state").agg({
        "customer_id": "nunique"
    }).sort_values(by="customer_id", ascending=False).reset_index()
    bycustomer_state_df.columns = ["customer_state", "customer_count"]

    return bycustomer_state_df


def create_byseller_city_df(df):
    byseller_city_df = df.groupby(by="seller_city").agg({
        "seller_id": "nunique"
    }).sort_values(by="seller_id", ascending=False).reset_index()
    byseller_city_df.columns = ["seller_city", "seller_count"]

    return byseller_city_df


def create_byseller_state_df(df):
    byseller_state_df = df.groupby(by="seller_state").agg({
        "seller_id": "nunique"
    }).sort_values(by="seller_id", ascending=False).reset_index()
    byseller_state_df.columns = ["seller_state", "seller_count"]

    return byseller_state_df


def create_byseller_order_df(df):
    byseller_order_df = df.groupby(by="seller_id").agg({
        "order_id": "nunique"
    }).sort_values(by="order_id", ascending=False).reset_index()

    byseller_order_df.columns = ["seller_id", "order_count"]

    return byseller_order_df


def create_bypayment_type_df(df):
    bypayment_type_df = df.groupby(by="payment_type").agg({
        "order_id": "nunique"
    }).reset_index()
    bypayment_type_df.columns = ["payment_type", "order_count"]

    return bypayment_type_df


def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_unique_id").agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()

    rfm_df.columns = [
        "customer_unique_id",
        "max_order_timestamp",
        "frequency",
        "monetary"
    ]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = all_df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(
        lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    return rfm_df


# import data
all_df = pd.read_csv("./dashboard/main_data.csv")

# datetime column for filter
all_df.sort_values(by="order_purchase_timestamp", ascending=True, inplace=True)
datetime_columns = [
    "order_purchase_timestamp", "order_approved_at",
    "order_delivered_customer_date", "order_delivered_carrier_date",
    "order_delivered_customer_date", "order_estimated_delivery_date",
    "shipping_limit_date", "review_creation_date", "review_answer_timestamp"]

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # mengambil start date and end date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) &
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)
byproduct_df = create_byproduct_df(main_df)
byproduct_category_df = create_byproduct_category_df(main_df)
bycustomer_city_df = create_bycustomer_city_df(main_df)
bycustomer_state_df = create_bycustomer_state_df(main_df)
byseller_city_df = create_byseller_city_df(main_df)
byseller_state_df = create_byseller_state_df(main_df)
byseller_order_df = create_byseller_order_df(main_df)
bypayment_type_df = create_bypayment_type_df(main_df)
rfm_df = create_rfm_df(main_df)


# header
st.header("Proyek Akhir Dicoding - E-Commerce Public Dataset")

st.subheader("Number of Orders")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        total_orders = daily_orders_df.order_count.sum()
        st.metric("Total Orders", value=total_orders)

    with col2:
        total_revenue = format_currency(
            daily_orders_df.revenue.sum(), "BRL", locale="en_US")
        st.metric("Total Revenue", value=total_revenue)

    tab_daily_orders, tab_monthly_orders = st.tabs(
        ["Daily Orders", "Monthly Orders"])

    with tab_daily_orders:
        fig, ax = plt.subplots(figsize=(16, 8))

        sns.lineplot(
            x="order_purchase_timestamp",
            y="order_count",
            data=daily_orders_df,
            marker="o",
            color="gray",
            linewidth=3
        )
        ax.set_xlabel(None)
        ax.set_ylabel("Order Count", fontsize=15)
        ax.tick_params("x", labelsize=12)
        ax.tick_params("y", labelsize=12)
        ax.set_title("Number of Orders Daily", loc="center", fontsize=20)
        st.pyplot(fig)

    with tab_monthly_orders:
        fig, ax = plt.subplots(figsize=(16, 8))

        sns.lineplot(
            x="order_purchase_timestamp",
            y="order_count",
            data=monthly_orders_df,
            marker="o",
            color="gray",
            linewidth=3
        )
        ax.set_xlabel(None)
        ax.set_ylabel("Order Count", fontsize=15)
        ax.tick_params("x", labelsize=12)
        ax.tick_params("y", labelsize=12)
        ax.set_title("Number of Orders Monthly", loc="center", fontsize=20)
        st.pyplot(fig)


st.subheader("Best Product By Number of Sales")

# Best Product by Number of Sales
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="product_id",
    y="product_count",
    data=byproduct_df.head(10),
    color="#72BCD4"
)
ax.patches[0].set_facecolor("#1f77b4")
ax.set_ylabel(None)
ax.set_xlabel("Product ID", fontsize=12)
ax.set_title("Best Product by Number of Sales", fontsize=22)
ax.tick_params(axis="x", labelsize=12, rotation=80)
ax.tick_params(axis="y", labelsize=12)
ax.bar_label(ax.containers[0], label_type="edge", fontsize=15)
ax.margins(0.05)
st.pyplot(fig)


st.subheader("Best Product Category Names")

with st.container():
    tab1, tab2, tab3 = st.tabs(
        ["By Number of Sales", "By Number of Seller", "By Review Score"])

    with tab1:
        st.write("Best Product Category Name by Number of Sales")
        # Best product category name by number of sales
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.barplot(
            y="product_category_name_english",
            x="order_count",
            data=byproduct_category_df.sort_values(
                by="order_count", ascending=False).head(10),
            color="#72BCD4"
        )
        ax.patches[0].set_facecolor("#1f77b4")
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.set_title(
            "Best Product Category Name by Number of Sales", fontsize=22)
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.bar_label(ax.containers[0], label_type="edge", fontsize=15)
        ax.margins(0.05)
        st.pyplot(fig)

    with tab2:
        st.write("The Most Sold Product Categories Based on Sellers")
        # The Most Sold Product Categories Based on Sellers
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.barplot(
            y="product_category_name_english",
            x="seller_count",
            data=byproduct_category_df.sort_values(
                by="seller_count", ascending=False).head(10),
            color="#72BCD4"
        )
        ax.patches[0].set_facecolor("#1f77b4")
        ax.set_ylabel(None)
        ax.set_xlabel("Number of Seller", fontsize=15)
        ax.set_title(
            "The Most Sold Product Categories Based on Sellers", fontsize=22)
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.bar_label(ax.containers[0],
                     label_type="edge", fontsize=15, padding=5)
        ax.margins(0.05)
        st.pyplot(fig)

    with tab3:
        st.write("Best Product Category Name Based on Reviews Score")
        # Best Product Category Name Based on Reviews Score
        fig, ax = plt.subplots(figsize=(9, 7))
        sns.barplot(
            x="review_score",
            y="product_category_name_english",
            data=byproduct_category_df.sort_values(
                by="review_score", ascending=False).head(10),
            color="#72BCD4"
        )
        ax.patches[0].set_facecolor("#1f77b4")
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.set_title(
            "Best Product Category Name Based on Reviews Score", fontsize=15)
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.bar_label(
            ax.containers[0], label_type="edge", fontsize=12, padding=3)
        ax.margins(0.08)
        st.pyplot(fig)


st.subheader("Customer and Seller Demographics")

with st.container():
    tab_customer, tab_seller = st.tabs(["Customer", "Seller"])

    with tab_customer:
        st.write("Customer Demographics")

        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

        # by city
        sns.barplot(
            x="customer_count",
            y="customer_city",
            data=bycustomer_city_df.head(5),
            ax=ax[0],
            orient="h",
            color="#72BCD4"
        )
        ax[0].patches[0].set_facecolor("#1f77b4")
        ax[0].bar_label(ax[0].containers[0], label_type="edge", fontsize=15)
        ax[0].set_ylabel(None)
        ax[0].set_xlabel(None)
        ax[0].set_title("Number of Customer by City", fontsize=22)
        ax[0].tick_params(axis="y", labelsize=12)
        ax[0].tick_params(axis="x", labelsize=12)
        ax[0].margins(0.1)

        # by state
        sns.barplot(
            x="customer_count",
            y="customer_state",
            data=bycustomer_state_df.head(5),
            ax=ax[1],
            orient="h",
            color="#72BCD4"
        )
        ax[1].patches[0].set_facecolor("#1f77b4")
        ax[1].bar_label(
            ax[1].containers[0], label_type="edge", fontsize=15, padding=3)
        ax[1].set_ylabel(None)
        ax[1].set_xlabel(None)
        ax[1].set_title("Number of Customer by State", fontsize=22)
        ax[1].invert_xaxis()
        ax[1].tick_params(axis="y", labelsize=12,
                          labelleft=False, labelright=True)
        ax[1].tick_params(axis="x", labelsize=12)
        ax[1].margins(0.1)
        st.pyplot(fig)

    with tab_seller:
        st.write("Seller Demographics")

        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

        # by city
        sns.barplot(
            x="seller_count",
            y="seller_city",
            data=byseller_city_df.head(5),
            ax=ax[0],
            orient="h",
            color="#72BCD4"
        )
        ax[0].patches[0].set_facecolor("#1f77b4")
        ax[0].set_ylabel(None)
        ax[0].set_xlabel(None)
        ax[0].set_title("Number of Seller by City", fontsize=22)
        ax[0].tick_params(axis="y", labelsize=12)
        ax[0].tick_params(axis="x", labelsize=12)
        ax[0].bar_label(ax[0].containers[0], label_type="edge",
                        fontsize=15, padding=3)
        ax[0].margins(0.1)

        # by state
        sns.barplot(
            x="seller_count",
            y="seller_state",
            data=byseller_state_df.head(5),
            ax=ax[1],
            orient="h",
            color="#72BCD4"
        )
        ax[1].patches[0].set_facecolor("#1f77b4")
        ax[1].set_ylabel(None)
        ax[1].set_xlabel(None)
        ax[1].set_title("Number of Seller by State", fontsize=22)
        ax[1].invert_xaxis()
        ax[1].tick_params(axis="y", labelsize=12,
                          labelleft=False, labelright=True)
        ax[1].tick_params(axis="x", labelsize=12)
        ax[1].bar_label(ax[1].containers[0], label_type="edge",
                        fontsize=15, padding=3)
        ax[1].margins(0.1)
        st.pyplot(fig)


st.subheader("Best Seller by Number of Order")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    x="seller_id",
    y="order_count",
    data=byseller_order_df.head(10),
    ax=ax,
    color="#72BCD4"
)
ax.patches[0].set_facecolor("#1f77b4")
ax.set_ylabel(None)
ax.set_xlabel("Seller ID", fontsize=15)
ax.set_title("Best Seller Based on Number of Order", fontsize=22)
ax.tick_params(axis="x", labelsize=12, rotation=75)
ax.tick_params(axis="y", labelsize=12)
ax.bar_label(ax.containers[0], label_type="edge", fontsize=15, padding=3)
ax.margins(0.05)
st.pyplot(fig)


# The Most Used Payment Method
with st.expander("The Most Used Payment Method"):
    colors = sns.color_palette("bright")[0:len(bypayment_type_df)]
    fig, ax = plt.subplots()
    ax.pie(bypayment_type_df.order_count, labels=bypayment_type_df.payment_type,
           colors=colors, autopct="%.1f%%", pctdistance=0.8, shadow=True)
    ax.set_title("Payment Type Based on Number of Order")
    st.pyplot(fig)


# Best customer based on RFM parameters
st.subheader("Best Customer Based on RFM Parameters")

with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_recency = rfm_df.recency.mean().round(1)
        st.metric("Average Recency (days)", value=avg_recency)

    with col2:
        avg_frequency = rfm_df.frequency.mean().round(2)
        st.metric("Average Frequency", value=avg_frequency)

    with col3:
        avg_monetary = format_currency(
            rfm_df.monetary.mean(), "AUD", locale="es_CO")
        st.metric("Average Monetary", value=avg_monetary)

    # plot RFM
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 8))

    sns.barplot(
        y="recency",
        x="customer_unique_id",
        data=rfm_df.sort_values(by="recency", ascending=True).head(5),
        color="#72BCD4",
        ax=ax[0]
    )
    ax[0].set_ylabel("Days")
    ax[0].set_xlabel("Customer Unique ID")
    ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
    ax[0].tick_params(axis='x', labelsize=15, rotation=75)

    sns.barplot(
        x="customer_unique_id",
        y="frequency",
        data=rfm_df.sort_values(by="frequency", ascending=False).head(5),
        color="#72BCD4",
        ax=ax[1]
    )
    ax[1].set_xlabel("Customer Unique ID")
    ax[1].set_ylabel("Frequency")
    ax[1].set_title("By Frequency", loc="center", fontsize=18)
    ax[1].tick_params(axis='x', labelsize=15, rotation=75)

    sns.barplot(
        x="customer_unique_id",
        y="monetary",
        data=rfm_df.sort_values(by="monetary", ascending=False).head(5),
        color="#72BCD4",
        ax=ax[2]
    )
    ax[2].set_xlabel("Customer Unique ID")
    ax[2].set_ylabel("Monetary")
    ax[2].set_title("By Monetary", loc="center", fontsize=18)
    ax[2].tick_params(axis='x', labelsize=15, rotation=75)
    ax[2].bar_label(ax[2].containers[0], label_type="edge", fontsize=15)

    plt.suptitle(
        "Best Customer Based on RFM Parameters (customer_unique_id)", fontsize=20)

    st.pyplot(fig)
