import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("Olympics Data Visualization (Beginner Level)")

# Load dataset
df = pd.read_csv("Olympic_Games_Medal_Tally.csv")

st.subheader("Dataset Preview")
st.write(df.head())

# ==============================
# Chart 1: Top 10 Countries by Total Medals
# ==============================

st.subheader("Top 10 Countries by Total Medals")

grouped = df.groupby("country")
totals = grouped["total"]
totals = totals.sum()
totals = totals.sort_values(ascending = False)
top10 = totals.head(10)

fig1, ax1 = plt.subplots(figsize=(10,6))
ax1.barh(top10.index, top10.values, color="skyblue")
ax1.set_xlabel("Total Medals")
ax1.set_ylabel("Country")
ax1.set_title("Top 10 Countries by Total Olympic Medals")
st.pyplot(fig1)

# ==============================
# Chart 2: Medals Over Time (Top 5 + India)
# ==============================

st.subheader("Medals Over Time: Top 5 Countries + India")

country_total = df.groupby("country")["total"].sum().sort_values(ascending=False)
top5 = country_total.head(5)
top5_countries = list(top5.index)
if "India" not in top5_countries:
    top5_countries.append("India")

df_top = df[df["country"].isin(top5_countries)]
df_grouped = df_top.groupby(["year", "country"])["total"].sum().reset_index()

fig2, ax2 = plt.subplots(figsize=(14,8))
for country in top5_countries:
    country_data = df_grouped[df_grouped["country"] == country]
    ax2.plot(country_data["year"], country_data["total"], marker="o", label=country)
ax2.set_xlabel("Year")
ax2.set_ylabel("Total Medals")
ax2.set_title("Medals Over Time: Top 5 Countries + India")
ax2.legend()
st.pyplot(fig2)

# ==============================
# Chart 3: India’s Medal Breakdown
# ==============================

st.subheader("India’s Olympic Medal Breakdown (Gold, Silver, Bronze)")

india = df[df["country"] == "India"]
india_group = india.groupby("year")[["gold", "silver", "bronze"]].sum().reset_index()

fig3, ax3 = plt.subplots(figsize=(14,8))
ax3.bar(india_group["year"], india_group["gold"], color="gold", label="Gold")
ax3.bar(india_group["year"], india_group["silver"], bottom=india_group["gold"], color="silver", label="Silver")
ax3.bar(india_group["year"], india_group["bronze"], bottom=india_group["gold"] + india_group["silver"], color="brown", label="Bronze")
ax3.set_xlabel("Year")
ax3.set_ylabel("Number of Medals")
ax3.set_title("India's Olympic Medal Breakdown")
ax3.legend()
st.pyplot(fig3)

# ==============================
# Chart 4: Misleading Pie Chart
# ==============================

st.subheader("Misleading Visualization: Pie Chart")

grouped = df.groupby("country")["total"].sum().sort_values(ascending=False)
top15 = grouped.head(15)

fig4, ax4 = plt.subplots(figsize=(10,10))
ax4.pie(top15, labels=top15.index, autopct="%1.1f%%", startangle=140)
ax4.set_title("Medal Distribution (Misleading Pie Chart)")
st.pyplot(fig4)

# ==============================
# Chart 5: Corrected Bar Chart
# ==============================

st.subheader("Corrected Visualization: Bar Chart")

fig5, ax5 = plt.subplots(figsize=(12,8))
ax5.barh(top15.index, top15.values, color="skyblue")
ax5.set_xlabel("Total Medals")
ax5.set_ylabel("Country")
ax5.set_title("Top 15 Countries by Total Medals (Corrected View)")
st.pyplot(fig5)

# ==============================
# Chart 6: USA vs India Medal Growth
# ==============================

st.subheader("USA vs India Medal Growth Over Time")

story_df = df[df["country"].isin(["United States", "India"])]
story_grouped = story_df.groupby(["year", "country"])["total"].sum().reset_index()

fig6, ax6 = plt.subplots(figsize=(14,8))
india_data = story_grouped[story_grouped["country"] == "India"]
usa_data = story_grouped[story_grouped["country"] == "United States"]

ax6.plot(india_data["year"], india_data["total"], marker="o", label="India")
ax6.plot(usa_data["year"], usa_data["total"], marker="o", label="United States")

ax6.set_xlabel("Year")
ax6.set_ylabel("Total Medals")
ax6.set_title("USA vs India: Medal Growth Over Time")
ax6.legend()
st.pyplot(fig6)

# ==============================
# Chart 7: India’s Medals Since 2000
# ==============================

st.subheader("India’s Olympic Medals Since 2000")

india_recent = df[(df["country"]=="India") & (df["year"]>=2000)]
india_recent_group = india_recent.groupby("year")["total"].sum().reset_index()

fig7, ax7 = plt.subplots(figsize=(12,6))
ax7.bar(india_recent_group["year"], india_recent_group["total"], color="royalblue")
ax7.set_xlabel("Year")
ax7.set_ylabel("Total Medals")
ax7.set_title("India’s Olympic Medals Since 2000")
st.pyplot(fig7)

# ==============================
# Chart 8: USA Medal Breakdown
# ==============================

st.subheader("USA Olympic Medal Breakdown (Gold, Silver, Bronze)")

usa_df = df[df["country"]=="United States"]
usa_grouped = usa_df.groupby("year")[["gold","silver","bronze"]].sum().reset_index()

fig8, ax8 = plt.subplots(figsize=(12,6))
ax8.stackplot(usa_grouped["year"],
              usa_grouped["gold"],
              usa_grouped["silver"],
              usa_grouped["bronze"],
              labels=["Gold","Silver","Bronze"],
              colors=["gold","silver","brown"])
ax8.set_xlabel("Year")
ax8.set_ylabel("Number of Medals")
ax8.set_title("USA Olympic Medal Breakdown Over Time")
ax8.legend()
st.pyplot(fig8)
