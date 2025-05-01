import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

cleaned_data = pd.read_csv('cleaned_Illegal_Dumping_Incidents.csv')
cleaned_data["Completed Incident Date"] = pd.to_datetime(cleaned_data["Completed Incident Date"], errors='coerce')

st.sidebar.title("Filters")
selected_area = st.sidebar.multiselect("Select Area(s):", options=cleaned_data["Area"].unique())

cleaned_data["Completed Incident Date"] = pd.to_datetime(cleaned_data["Completed Incident Date"], errors='coerce')

min_date = cleaned_data["Completed Incident Date"].min().date()
max_date = cleaned_data["Completed Incident Date"].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date])

cleaned_data["Overall Environmental Impact"] = pd.to_numeric(cleaned_data["Overall Environmental Impact"], errors='coerce')
min_impact = int(cleaned_data["Overall Environmental Impact"].min())
max_impact = int(cleaned_data["Overall Environmental Impact"].max())
impact_range = st.sidebar.slider(
    "Overall Environmental Impact Range",
    min_value=min_impact,
    max_value=max_impact,
    value=(min_impact, max_impact)
)

filtered_data = cleaned_data.copy()
if selected_area:
    filtered_data = filtered_data[filtered_data["Area"].isin(selected_area)]

filtered_data = filtered_data[(filtered_data["Overall Environmental Impact"].between(*impact_range))]
filtered_data = filtered_data[
    (filtered_data["Completed Incident Date"] >= pd.to_datetime(date_range[0])) &
    (filtered_data["Completed Incident Date"] <= pd.to_datetime(date_range[1]))
]

st.title("Illegal Dumping Incidents Dashboard")
st.markdown("Explore incident trends, impact levels, and more.")
st.subheader("Top 10 Areas by Number of Incidents")
top_areas = filtered_data["Area"].value_counts().head(10)
fig1, ax1 = plt.subplots()
top_areas.plot(kind='bar', ax=ax1)
ax1.set_xlabel("Area")
ax1.set_ylabel("Number of Incidents")
ax1.set_title("Top 10 Areas")
st.pyplot(fig1)


st.subheader("Incidents Over Time")
monthly = filtered_data["Completed Incident Date"].dt.to_period("M").value_counts().sort_index()
fig2, ax2 = plt.subplots()
monthly.plot(marker='o', ax=ax2)
ax2.set_xlabel("Month")
ax2.set_ylabel("Number of Incidents")
ax2.set_title("Incidents Over Time")
st.pyplot(fig2)


st.subheader("Environmental Impact Distribution")
fig3, ax3 = plt.subplots()
filtered_data["Overall Environmental Impact"].astype(int).value_counts().sort_index().plot(kind='bar', ax=ax3)
ax3.set_xlabel("Impact Level")
ax3.set_ylabel("Number of Incidents")
ax3.set_title("Impact Ratings")
st.pyplot(fig3)


st.subheader("Most Common Incident Sizes")
fig4, ax4 = plt.subplots()
filtered_data["Incident Size"].value_counts().head(10).plot(kind='bar', ax=ax4)
ax4.set_xlabel("Incident Size")
ax4.set_ylabel("Number of Incidents")
ax4.set_title("Incident Size Distribution")
st.pyplot(fig4)

st.markdown("---")
st.markdown("Data Source: Illegal Dumping Incidents Dataset")
