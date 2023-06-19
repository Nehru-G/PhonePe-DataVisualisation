import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Your password",
        database="phonepe"
    )

# Function to retrieve transaction information
def get_transaction_info(db, year):
    # Create the SQL query to get overall transaction information
    query1 = f"""
    SELECT
        SUM(transaction_amount) AS total_amount,
        SUM(transaction_count) AS total_count,
        AVG(transaction_amount) AS average_amount
    FROM
        aggr_transaction
    WHERE
        year = {year}
    """

    # Execute the query to get overall transaction information
    cursor = db.cursor()
    cursor.execute(query1)
    result_all_transaction = cursor.fetchone()

    # Extract the results of overall transaction information
    total_amount = result_all_transaction[0]
    total_count = result_all_transaction[1]
    average_amount = result_all_transaction[2]

    # Create the SQL query to get transaction information by category
    query2 = f"""
    SELECT
        transaction_category,
        SUM(transaction_amount) AS total_amount
    FROM
        aggr_transaction
    WHERE
        year = {year}
    GROUP BY
        transaction_category
    """

    # Execute the query to get transaction information by category
    df = pd.read_sql_query(query2, db)

    query3 = f"""
    SELECT district, SUM(transaction_amount) AS total_amount
    FROM map_transaction
    WHERE
        year = {year} and district IS NOT NULL AND district != ''
    GROUP BY district
    ORDER BY total_amount DESC
    LIMIT 10
    """
    district = pd.read_sql_query(query3, db)

    query4 = f"""
        SELECT pincode, SUM(transaction_amount) AS total_amount
        FROM map_transaction
        WHERE
            year = {year} and pincode IS NOT NULL AND pincode != ''
        GROUP BY pincode
        ORDER BY total_amount DESC
        LIMIT 10
        """
    pincode = pd.read_sql_query(query4, db)

    query5 = f"""
        SELECT state, SUM(transaction_amount) AS total_amount
        FROM map_transaction
        WHERE
            year = {year} and state IS NOT NULL AND state != ''
        GROUP BY state
        ORDER BY total_amount DESC
        LIMIT 10
        """
    state = pd.read_sql_query(query5, db)
    query6 = """
        SELECT latitude, longitude, state, transaction_category, SUM(transaction_amount) AS total_amount
        FROM map
        GROUP BY latitude, longitude, state, transaction_category
        """
    map_query = pd.read_sql_query(query6, db)

    return total_amount, total_count, average_amount, df, district,pincode,state,map_query
def get_user_info(db,year):
    query1 = f"""
        SELECT
            SUM(registered_users) AS total_registered_users,
            SUM(app_opens) AS total_app_opens
        FROM
            aggr_user
        WHERE
            year = {year}
        """

    # Execute the query to get overall transaction information
    cursor = db.cursor()
    cursor.execute(query1)
    result_all_transaction = cursor.fetchone()

    # Extract the results of overall transaction information
    total_registered_users = result_all_transaction[0]
    total_app_opens = result_all_transaction[1]

    query2 = f"""
        SELECT state, Brand, SUM(count) AS Brand_count
        FROM aggr_user
        WHERE year = '{year}'
        GROUP BY state, Brand
        """
    heatmap_df = pd.read_sql_query(query2, db)

    return total_registered_users,total_app_opens,heatmap_df

# Main function
def main():
    # Connect to the database
    db = connect_to_database()

    st.title("PhonePe Data Visualisation")

    # Create dropdown options
    tab_transaction, tab_user= st.tabs(["Transaction", "User"])
    with tab_transaction:
        year_options = ["2018", "2019", "2020", "2021", "2022"]
        selected_year_option = st.selectbox("Select Year", year_options, index=0,key="transaction-year")

        # Retrieve transaction information
        total_amount, total_count, average_amount, df, district, pincode, state, map_query = get_transaction_info(db, selected_year_option)

        # Display overall transaction information
        st.title("Transactions")
        st.subheader(f"All PhonePe transactions (UPI + Cards + Wallets) till {selected_year_option}")
        total_amt_in_crores = total_amount / 10000000
        st.subheader(f"{round(total_amt_in_crores, 2)} cr")

        st.subheader(f"Total payment value till {selected_year_option}")
        st.subheader(total_count)

        st.subheader("Avg. transaction value")
        average_amt_in_crores = average_amount / 10000000
        st.subheader(f"{round(average_amt_in_crores, 2)} cr")
        st.divider()

        # Create pie chart
        fig, ax = plt.subplots()
        ax.pie(df['total_amount'], labels=df['transaction_category'], autopct='%1.2f%%')
        ax.set_title("Transaction Categories")
        # Create a custom legend with category and total amount
        legend_labels = [f'{cat}: {round(amt/10000000,2)}cr' for cat, amt in zip(df['transaction_category'],df['total_amount'])]
        legend = ax.legend(legend_labels, loc='lower left', bbox_to_anchor=(1, 0.5))
        legend.get_frame().set_alpha(None)  # Remove the legend box background
        legend.set_title('Legend')  # Set the legend title
        # Adjust the legend font size
        for text in legend.get_texts():
            text.set_fontsize('small')

        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        st.pyplot(fig)

        st.divider()

        tab1, tab2, tab3 = st.columns(3)

        with tab1:
            st.header("Top 10 States")
            st.table(state)
        with tab2:
            st.header("Top 10 Districts")
            st.table(district)
        with tab3:
            st.header("Top 10 Pincodes")
            st.table(pincode)
        st.divider()

        # Create a Streamlit app
        st.title("Live Geolocation Map of India")

        # Display the map using st.map
        st.map(map_query)

        # Display the sum of transaction amounts in crore for each state and transaction category
        st.subheader("Total Transaction Amounts (in Crore)")
        map_query['total_amount_cr'] = round(map_query['total_amount'] / 10000000, 2)
        grouped_df = map_query.groupby(['state', 'transaction_category'])['total_amount_cr'].sum().reset_index()
        st.dataframe(grouped_df)

    with tab_user:
        year_options = ["2018", "2019", "2020", "2021", "2022"]
        selected_year_option = st.selectbox("Select Year", year_options, index=0, key="user-year")

        # Retrieve user information
        total_registered_users, total_app_opens, heatmap_df = get_user_info(db, selected_year_option)

        st.subheader(f"Registered PhonePe users till {selected_year_option}")
        total_users_in_crores = total_registered_users / 10000000
        st.subheader(f"{round(total_users_in_crores, 2)} cr")

        st.subheader(f"PhonePe app opens till {selected_year_option}")
        total_open_apps_in_crores = total_app_opens / 10000000
        st.subheader(f"{round(total_open_apps_in_crores, 2)} cr")
        st.divider()

        # Create a pivot table for heatmap visualization
        pivot_table = heatmap_df.pivot(index="state", columns="Brand", values="Brand_count")

        # Create the heatmap using seaborn
        fig, ax = plt.subplots(figsize=(16, 10))
        sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt=".0f", cbar=True, ax=ax)
        plt.title("Brand Count Heatmap")
        plt.xlabel("Brand", fontsize=12)
        plt.ylabel("State", fontsize=12)
        st.pyplot(fig)

# Set page layout to wide mode
st.set_page_config(layout="wide")

# Run the main function
if __name__ == "__main__":
    main()
