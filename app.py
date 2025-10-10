import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page config
st.set_page_config(
    page_title="Olympics Data Storytelling",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #FF6B35;
    text-align: center;
    font-weight: bold;
    margin-bottom: 2rem;
}
.student-info {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 2rem;
}
.insight-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-left: 5px solid #FFD700;
    margin: 1rem 0;
    border-radius: 5px;
    color: white;
}
.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏅 Olympic Games: A Data Storytelling Journey</h1>', unsafe_allow_html=True)

# Student Information
st.markdown("""
<div class="student-info">
    <h3>📚 Assignment Details</h3>
    <p><strong>Name:</strong> Aryan Gupta</p>
    <p><strong>Roll No:</strong> 2415800019</p>
    <p><strong>Assignment:</strong> Data Visualization & Storytelling with Olympics Dataset</p>
    <p><strong>Submitted to:</strong> Dr. Saurabh Tewari</p>
    <p><strong>Tools Used:</strong> Python, Streamlit, Matplotlib, Seaborn, Plotly</p>
</div>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv("Olympic_Games_Medal_Tally.csv")
    return df

df = load_data()

# Sidebar for navigation
st.sidebar.title("📊 Navigation")
analysis_type = st.sidebar.selectbox(
    "Choose Analysis Type:",
    ["📈 Overview & Key Metrics", "🌍 Global Medal Analysis", "🇮🇳 India's Olympic Journey", 
     "⚠️ Misleading vs Corrected Visualizations", "📖 Data Storytelling"]
)

# Overview Section
if analysis_type == "📈 Overview & Key Metrics":
    st.header("📈 Dataset Overview & Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Countries", df['country'].nunique(), "Participating Nations")
    with col2:
        st.metric("Years Covered", f"{df['year'].min()}-{df['year'].max()}", "Time Span")
    with col3:
        st.metric("Total Medals", f"{df['total'].sum():,}", "All Time")
    with col4:
        st.metric("Olympic Games", df['year'].nunique(), "Editions")
    
    st.markdown("""
    <div class="insight-box">
    <h4 style="color: #FFD700;">🔍 Key Insights:</h4>
    <ul style="color: white;">
    <li>The dataset spans multiple Olympic Games from 1896 to recent years</li>
    <li>Covers both Summer and Winter Olympics medal tallies</li>
    <li>Includes comprehensive medal breakdown (Gold, Silver, Bronze)</li>
    <li>Represents the global nature of Olympic competition</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive dataset preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Basic statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Medal Distribution Statistics")
        stats_df = df[['gold', 'silver', 'bronze', 'total']].describe()
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Top Medal Winners")
        top_countries = df.groupby('country')['total'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(x=top_countries.values, y=top_countries.index, orientation='h',
                    title="Top 10 Countries by Total Medals",
                    color=top_countries.values,
                    color_continuous_scale='Viridis')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# Global Analysis Section
elif analysis_type == "🌍 Global Medal Analysis":
    st.header("🌍 Global Olympic Medal Analysis")
    
    # Medal distribution over time
    st.subheader("📈 Global Medal Trends Over Time")
    
    yearly_medals = df.groupby('year')[['gold', 'silver', 'bronze']].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=yearly_medals['year'], y=yearly_medals['gold'], 
                            mode='lines+markers', name='Gold', line=dict(color='gold', width=3)))
    fig.add_trace(go.Scatter(x=yearly_medals['year'], y=yearly_medals['silver'], 
                            mode='lines+markers', name='Silver', line=dict(color='silver', width=3)))
    fig.add_trace(go.Scatter(x=yearly_medals['year'], y=yearly_medals['bronze'], 
                            mode='lines+markers', name='Bronze', line=dict(color='#CD7F32', width=3)))
    
    fig.update_layout(title="Global Medal Distribution Trends", xaxis_title="Year", 
                     yaxis_title="Number of Medals", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <h4 style="color: #FFD700;">🔍 Insights:</h4>
    <ul style="color: white;">
    <li>Medal counts show significant variations across different Olympic years</li>
    <li>Some years show spikes due to expanded events or participation</li>
    <li>The trend reflects the growth of Olympic Games over time</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Top performing countries analysis
    st.subheader("🏆 Elite Olympic Nations Analysis")
    
    country_totals = df.groupby('country')['total'].sum().sort_values(ascending=False)
    top_10_countries = country_totals.head(10)
    
    # Create detailed breakdown for top countries
    top_countries_detailed = df[df['country'].isin(top_10_countries.index)].groupby('country')[['gold', 'silver', 'bronze']].sum()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Gold', x=top_countries_detailed.index, y=top_countries_detailed['gold'], marker_color='gold'))
    fig.add_trace(go.Bar(name='Silver', x=top_countries_detailed.index, y=top_countries_detailed['silver'], marker_color='silver'))
    fig.add_trace(go.Bar(name='Bronze', x=top_countries_detailed.index, y=top_countries_detailed['bronze'], marker_color='#CD7F32'))
    
    fig.update_layout(barmode='stack', title="Medal Composition of Top 10 Olympic Nations",
                     xaxis_title="Country", yaxis_title="Number of Medals", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance consistency analysis
    st.subheader("📊 Performance Consistency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Medal efficiency (Gold/Total ratio)
        top_countries_efficiency = df[df['country'].isin(top_10_countries.index)].groupby('country').agg({
            'gold': 'sum', 'total': 'sum'
        })
        top_countries_efficiency['efficiency'] = (top_countries_efficiency['gold'] / top_countries_efficiency['total'] * 100).round(2)
        
        fig = px.bar(x=top_countries_efficiency.index, y=top_countries_efficiency['efficiency'],
                    title="Gold Medal Efficiency (Gold/Total %)",
                    color=top_countries_efficiency['efficiency'],
                    color_continuous_scale='RdYlGn')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Participation span
        participation_span = df[df['country'].isin(top_10_countries.index)].groupby('country')['year'].agg(['min', 'max', 'count'])
        participation_span['span'] = participation_span['max'] - participation_span['min']
        
        fig = px.scatter(x=participation_span['span'], y=participation_span['count'],
                        hover_name=participation_span.index,
                        title="Olympic Participation: Years Span vs Games Count",
                        labels={'x': 'Years Span', 'y': 'Games Participated'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# India Analysis Section
elif analysis_type == "🇮🇳 India's Olympic Journey":
    st.header("🇮🇳 India's Olympic Journey: A Detailed Analysis")
    
    india_data = df[df['country'] == 'India']
    
    if len(india_data) > 0:
        # India's medal timeline
        st.subheader("🏅 India's Medal Timeline")
        
        india_yearly = india_data.groupby('year')[['gold', 'silver', 'bronze', 'total']].sum().reset_index()
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Bar(x=india_yearly['year'], y=india_yearly['gold'], name='Gold', marker_color='gold'))
        fig.add_trace(go.Bar(x=india_yearly['year'], y=india_yearly['silver'], name='Silver', marker_color='silver'))
        fig.add_trace(go.Bar(x=india_yearly['year'], y=india_yearly['bronze'], name='Bronze', marker_color='#CD7F32'))
        
        fig.add_trace(go.Scatter(x=india_yearly['year'], y=india_yearly['total'], 
                                mode='lines+markers', name='Total Medals', 
                                line=dict(color='red', width=3)), secondary_y=True)
        
        fig.update_layout(title="India's Olympic Medal Journey", barmode='stack', height=500)
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Individual Medals", secondary_y=False)
        fig.update_yaxes(title_text="Total Medals", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # India's performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Medals", india_data['total'].sum())
        with col2:
            st.metric("Gold Medals", india_data['gold'].sum())
        with col3:
            st.metric("Best Year", india_yearly.loc[india_yearly['total'].idxmax(), 'year'])
        with col4:
            st.metric("Games Participated", len(india_yearly))
        
        st.markdown("""
        <div class="insight-box">
        <h4 style="color: #FFD700;">🔍 India's Olympic Insights:</h4>
        <ul style="color: white;">
        <li>India's Olympic journey shows gradual improvement over the decades</li>
        <li>Recent years have seen better medal tallies compared to earlier participation</li>
        <li>The country has shown consistent participation in Olympic Games</li>
        <li>Performance peaks align with increased investment in sports infrastructure</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Comparison with other nations
        st.subheader("🌏 India vs Other Asian Nations")
        
        available_countries = sorted([c for c in df['country'].unique() if c != 'India'])
        
        selected_asian_countries = st.multiselect(
            "Select countries to compare with India:",
            options=available_countries,
            default=['Japan'] if 'Japan' in available_countries else []
        )
        
        comparison_countries = ['India'] + selected_asian_countries
        asian_data = df[df['country'].isin(comparison_countries)]
        
        if len(asian_data) > 0:
            asian_comparison = asian_data.groupby(['year', 'country'])['total'].sum().reset_index()
            
            fig = px.line(asian_comparison, x='year', y='total', color='country',
                         title=f"Medal Performance: India vs {', '.join(selected_asian_countries)}",
                         markers=True, line_shape='spline')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("No data found for India in the dataset.")

# Misleading vs Corrected Visualizations
elif analysis_type == "⚠️ Misleading vs Corrected Visualizations":
    st.header("⚠️ Misleading Visualizations vs Corrected Versions")
    
    st.markdown("""
    <div class="insight-box">
    <h4 style="color: #FFD700;">📚 Learning Objective:</h4>
    <p style="color: white;">Understanding how visualizations can be misleading and learning to create more accurate representations of data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Misleading Pie Chart
    st.subheader("❌ Misleading Visualization: Pie Chart for Medal Distribution")
    
    top_15_countries = df.groupby('country')['total'].sum().sort_values(ascending=False).head(15)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**❌ Problematic: Pie Chart**")
        fig = go.Figure(data=[go.Pie(
            labels=top_15_countries.index,
            values=top_15_countries.values,
            hole=0.3,
            marker_colors=px.colors.qualitative.Set3,
            textinfo='label+percent',
            textfont_size=10,
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )])
        fig.update_layout(
            title="Medal Distribution (Misleading Pie Chart)",
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **🚫 Problems with this visualization:**
        - Hard to compare values accurately
        - Too many categories make it cluttered
        - Percentages don't show actual medal counts
        - Difficult to read labels
        - Not suitable for ranking comparison
        """)
    
    with col2:
        st.markdown("**✅ Corrected: Horizontal Bar Chart**")
        
        fig = px.bar(x=top_15_countries.values, y=top_15_countries.index, 
                    orientation='h', title="Medal Distribution Among Top 15 Countries\n(Corrected Visualization)",
                    color=top_15_countries.values, color_continuous_scale='viridis')
        fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
        fig.update_traces(texttemplate='%{x}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **✅ Improvements in this visualization:**
        - Easy to compare exact values
        - Clear ranking from top to bottom
        - Shows actual medal counts
        - Clean and readable labels
        - Better for quantitative comparison
        """)
    
    # Misleading 3D Chart
    st.subheader("❌ Misleading Visualization: Truncated Y-Axis")
    
    col1, col2 = st.columns(2)
    
    recent_years = df[df['year'] >= 2000].groupby('year')['total'].sum().reset_index()
    
    with col1:
        st.markdown("**❌ Problematic: Truncated Y-Axis**")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(recent_years['year'], recent_years['total'], color='lightcoral')
        ax.set_ylim(recent_years['total'].min() - 50, recent_years['total'].max() + 50)  # Truncated
        ax.set_title("Total Medals by Year (Misleading - Truncated Y-Axis)")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Medals")
        st.pyplot(fig)
        
        st.markdown("""
        **🚫 Problems:**
        - Exaggerates small differences
        - Misleading visual proportions
        - Y-axis doesn't start from zero
        """)
    
    with col2:
        st.markdown("**✅ Corrected: Full Y-Axis Scale**")
        
        fig = px.bar(recent_years, x='year', y='total', 
                    title="Total Medals by Year (Corrected - Full Scale)",
                    color='total', color_continuous_scale='blues')
        fig.update_layout(yaxis=dict(range=[0, recent_years['total'].max() * 1.1]))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **✅ Improvements:**
        - Y-axis starts from zero
        - True proportional representation
        - Honest visualization of differences
        """)

# Data Storytelling Section
else:  # "📖 Data Storytelling"
    st.header("📖 Olympic Games: A Data-Driven Story")
    
    st.markdown("""
    <div class="insight-box">
    <h4 style="color: #FFD700;">🎯 Story Narrative:</h4>
    <p style="color: white;">"From Ancient Greece to Modern Glory: How Olympic Medal Patterns Reveal the Evolution of Global Sports Dominance"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Story Chapter 1: The Rise of Olympic Powers
    st.subheader("📚 Chapter 1: The Rise of Olympic Superpowers")
    
    # Interactive timeline
    country_yearly = df.groupby(['year', 'country'])['total'].sum().reset_index()
    top_countries = df.groupby('country')['total'].sum().sort_values(ascending=False).head(8).index
    
    story_data = country_yearly[country_yearly['country'].isin(top_countries)]
    
    fig = px.line(story_data, x='year', y='total', color='country',
                 title="The Evolution of Olympic Dominance (1896-Present)",
                 markers=True, line_shape='spline')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **📊 Story Insights:**
    - The United States has maintained consistent Olympic dominance across decades
    - Soviet Union showed remarkable performance during its existence (1952-1988)
    - Germany's performance reflects historical changes (East/West division and reunification)
    - Emerging nations like China have dramatically increased their medal tallies in recent decades
    """)
    
    # Story Chapter 2: The Medal Efficiency Story
    st.subheader("📚 Chapter 2: Quality vs Quantity - The Medal Efficiency Tale")
    
    # Calculate medal efficiency metrics
    country_stats = df.groupby('country').agg({
        'total': 'sum',
        'gold': 'sum',
        'year': 'nunique'
    }).reset_index()
    
    country_stats['medals_per_game'] = (country_stats['total'] / country_stats['year']).round(2)
    country_stats['gold_ratio'] = (country_stats['gold'] / country_stats['total'] * 100).round(2)
    
    # Filter for countries with significant participation
    significant_countries = country_stats[country_stats['total'] >= 50]
    
    fig = px.scatter(significant_countries, x='medals_per_game', y='gold_ratio',
                    size='total', hover_name='country',
                    title="Olympic Efficiency: Medals per Game vs Gold Medal Ratio",
                    labels={'medals_per_game': 'Average Medals per Olympic Game',
                           'gold_ratio': 'Gold Medal Percentage (%)'})
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Story Chapter 3: The Underdog Stories
    st.subheader("📚 Chapter 3: Underdog Nations and Breakthrough Moments")
    
    # Find countries with significant improvement
    recent_performance = df[df['year'] >= 2000].groupby('country')['total'].sum()
    historical_performance = df[df['year'] < 2000].groupby('country')['total'].sum()
    
    improvement_countries = []
    for country in recent_performance.index:
        if country in historical_performance.index:
            recent_avg = recent_performance[country] / len(df[df['year'] >= 2000]['year'].unique())
            historical_avg = historical_performance[country] / len(df[df['year'] < 2000]['year'].unique())
            if recent_avg > historical_avg * 2:  # Significant improvement
                improvement_countries.append(country)
    
    if improvement_countries:
        improvement_data = df[df['country'].isin(improvement_countries[:5])]
        improvement_yearly = improvement_data.groupby(['year', 'country'])['total'].sum().reset_index()
        
        fig = px.bar(improvement_yearly, x='year', y='total', color='country',
                    title="Breakthrough Nations: Dramatic Olympic Improvements",
                    barmode='group')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Final Story Summary
    st.subheader("🎯 Story Conclusion: Key Takeaways")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🏆 Dominance Patterns**
        - Consistent performers maintain long-term success
        - Political changes significantly impact performance
        - Investment in sports infrastructure shows clear results
        """)
    
    with col2:
        st.markdown("""
        **📈 Emerging Trends**
        - Asian nations showing remarkable growth
        - Smaller nations finding niche specializations
        - Technology and training methods leveling the field
        """)
    
    with col3:
        st.markdown("""
        **🔮 Future Implications**
        - Medal distribution becoming more global
        - Traditional powers facing new competition
        - Olympic Games reflecting global power shifts
        """)
    
    # Interactive conclusion
    st.subheader("🎪 Interactive Exploration")
    
    all_countries = sorted(df['country'].unique())
    default_countries = [c for c in ['United States', 'China', 'Germany', 'India'] if c in all_countries]
    
    selected_countries = st.multiselect(
        "Select countries to compare their Olympic journey:",
        options=all_countries,
        default=default_countries
    )
    
    if selected_countries:
        comparison_data = df[df['country'].isin(selected_countries)]
        comparison_yearly = comparison_data.groupby(['year', 'country'])['total'].sum().reset_index()
        
        fig = px.area(comparison_yearly, x='year', y='total', color='country',
                     title=f"Olympic Medal Journey: {', '.join(selected_countries)}")
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

# Download Report Section
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(90deg, #0085C3 0%, #00A651 100%); padding: 1rem; border-radius: 15px; color: white; text-align: center; margin: 1rem 0; font-size: 1.3rem; font-weight: bold;">
    📄 Download Olympic Analysis Report
</div>
""", unsafe_allow_html=True)

# Generate report function
def generate_report():
    from datetime import datetime
    
    # Country flags mapping
    country_flags = {
        'United States': '🇺🇸', 'China': '🇨🇳', 'Germany': '🇩🇪', 'India': '🇮🇳',
        'Japan': '🇯🇵', 'Great Britain': '🇬🇧', 'France': '🇫🇷', 'Italy': '🇮🇹',
        'Australia': '🇦🇺', 'South Korea': '🇰🇷', 'Russia': '🇷🇺', 'Canada': '🇨🇦'
    }
    
    report_content = f"""
# 🏅 Olympic Games Data Analysis Report

**Student Name:** Aryan Gupta  
**Roll Number:** 2415800019  
**Subject:** Data Visualization and Storytelling  
**Teacher:** Dr. Saurabh Tewari  
**Date:** {datetime.now().strftime('%B %d, %Y')}

---

## 📊 Executive Summary

This report shows the analysis of Olympic Games medal data. We have studied how different countries perform in Olympics and what patterns we can see over the years.

### Key Numbers:
- **Total Countries:** {df['country'].nunique()} countries have participated
- **Total Medals:** {df['total'].sum():,} medals given in all Olympics
- **Time Period:** From {df['year'].min()} to {df['year'].max()}
- **Olympic Games:** {df['year'].nunique()} different Olympic games

---

## 🏆 Top Performing Countries

These are the countries that won most medals in Olympics:

"""
    
    # Add top 10 countries
    top_10 = df.groupby('country')['total'].sum().sort_values(ascending=False).head(10)
    for i, (country, medals) in enumerate(top_10.items(), 1):
        flag = country_flags.get(country, '🏳️')
        report_content += f"{i}. {flag} **{country}** - {medals:,} medals\n"
    
    report_content += f"""

### What This Tells Us:
- USA is the clear winner with most medals
- Big countries like China, Germany, and Russia also perform very well
- These countries invest a lot of money in sports training
- They have good facilities and coaches for athletes

---

## 🇮🇳 India's Olympic Performance

"""
    
    india_data = df[df['country'] == 'India']
    if len(india_data) > 0:
        india_total = india_data['total'].sum()
        india_gold = india_data['gold'].sum()
        india_games = len(india_data)
        
        report_content += f"""
### India's Numbers:
- **Total Medals:** {india_total} medals
- **Gold Medals:** {india_gold} gold medals  
- **Games Played:** {india_games} Olympic games
- **Average per Game:** {india_total/india_games:.1f} medals per Olympics

### India's Story:
- India has been participating in Olympics for many years
- Our performance is slowly getting better
- We need more investment in sports to compete with top countries
- Recent Olympics show improvement in India's medal count
"""
    else:
        report_content += "No data available for India in this dataset.\n"
    
    report_content += f"""

---

## 📈 Important Trends We Found

### 1. Medal Distribution Over Time
- Number of medals given has increased over years
- This is because more sports and events are added to Olympics
- More countries participate now than before

### 2. Country Performance Patterns
- **Consistent Winners:** USA, Germany, and Great Britain always perform well
- **Rising Powers:** China has improved a lot in recent Olympics
- **Political Impact:** When Soviet Union broke up, it affected their medal count

### 3. Medal Types
- Gold, Silver, and Bronze medals are almost equally distributed
- This shows fair competition in Olympics
- No single country dominates all medal types

---

## ⚠️ Common Mistakes in Data Visualization

We also learned about wrong ways to show data:

### Pie Charts Problems:
- **Bad:** Using pie charts with too many countries
- **Why Bad:** Hard to compare small slices
- **Better:** Use bar charts to show rankings clearly

### Y-Axis Tricks:
- **Bad:** Starting Y-axis from middle instead of zero
- **Why Bad:** Makes small differences look very big
- **Better:** Always start from zero to show true picture

---

## 🎯 Key Learnings

### For Countries:
1. **Investment Matters:** Countries that spend more on sports get more medals
2. **Long-term Planning:** Success comes from years of preparation
3. **Infrastructure:** Good training facilities are very important

### For Data Analysis:
1. **Choose Right Charts:** Bar charts are better than pie charts for rankings
2. **Be Honest:** Don't manipulate scales to mislead people
3. **Tell Stories:** Data should tell a clear story that everyone can understand

---

## 🔮 Future Predictions

Based on current trends:
- **Asian Countries** will likely win more medals in future Olympics
- **India** has potential to improve if we invest more in sports
- **Medal Distribution** will become more spread across countries
- **New Sports** will be added, giving more opportunities to different countries

---

## 📝 Conclusion

This analysis of Olympic data teaches us many things:

1. **Sports Success Needs Investment:** Countries that spend money on sports training get better results

2. **Consistency Wins:** Countries like USA succeed because they consistently support their athletes

3. **Data Tells Stories:** When we analyze data properly, we can understand patterns and make predictions

4. **Visualization Matters:** How we show data is very important - it should be clear and honest

5. **India's Opportunity:** Our country has potential to do much better in Olympics with proper planning

### Final Thoughts:
Olympics is not just about winning medals. It brings countries together and shows the power of human achievement. Through data analysis, we can understand these patterns and help our country perform better in future Olympics.

---

**Report Prepared By:** Aryan Gupta (Roll No: 2415800019)  
**Course:** Data Visualization and Storytelling  
**Instructor:** Dr. Saurabh Tewari  
**Tools Used:** Python, Streamlit, Plotly, Matplotlib, Seaborn

*This report uses simple English to explain complex data patterns so everyone can understand the Olympic Games analysis.*
"""
    
    return report_content

# Download button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📥 Download Olympic Analysis Report", key="download_report"):
        report_text = generate_report()
        
        # Create PDF download
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from io import BytesIO
        import base64
        
        # Create PDF with enhanced styling
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle('CustomTitle', 
                                   parent=styles['Heading1'], 
                                   fontSize=20, 
                                   spaceAfter=30, 
                                   alignment=1,  # Center alignment
                                   textColor='darkblue')
        
        heading_style = ParagraphStyle('CustomHeading', 
                                     parent=styles['Heading2'], 
                                     fontSize=14, 
                                     spaceAfter=12, 
                                     spaceBefore=12,
                                     textColor='darkgreen')
        
        normal_style = ParagraphStyle('CustomNormal', 
                                    parent=styles['Normal'], 
                                    fontSize=11, 
                                    spaceAfter=6,
                                    leftIndent=0.2*inch)
        
        story = []
        
        # Title with Olympic theme
        story.append(Paragraph("🏅 OLYMPIC GAMES DATA ANALYSIS REPORT 🏅", title_style))
        story.append(Spacer(1, 20))
        
        # Student info box
        from reportlab.lib.colors import lightblue, darkblue
        info_style = ParagraphStyle('InfoStyle', 
                                  parent=styles['Normal'], 
                                  fontSize=12, 
                                  spaceAfter=4,
                                  leftIndent=0.5*inch,
                                  textColor=darkblue)
        
        story.append(Paragraph("📚 <b>ASSIGNMENT DETAILS</b>", heading_style))
        story.append(Paragraph("👤 <b>Student Name:</b> Aryan Gupta", info_style))
        story.append(Paragraph("🎓 <b>Roll Number:</b> 2415800019", info_style))
        story.append(Paragraph("📖 <b>Subject:</b> Data Visualization and Storytelling", info_style))
        story.append(Paragraph("👨🏫 <b>Teacher:</b> Dr. Saurabh Tewari", info_style))
        from datetime import datetime
        story.append(Paragraph(f"📅 <b>Date:</b> {datetime.now().strftime('%B %d, %Y')}", info_style))
        story.append(Spacer(1, 25))
        
        # Executive Summary with enhanced formatting
        story.append(Paragraph("📊 EXECUTIVE SUMMARY", heading_style))
        story.append(Paragraph("This report shows the analysis of Olympic Games medal data. We have studied how different countries perform in Olympics and what patterns we can see over the years.", normal_style))
        
        # Key numbers in a formatted box
        key_numbers = f"""<b>🔢 KEY NUMBERS:</b><br/>
        • Total Countries: <b>{df['country'].nunique()}</b> countries have participated<br/>
        • Total Medals: <b>{df['total'].sum():,}</b> medals given in all Olympics<br/>
        • Time Period: From <b>{df['year'].min()}</b> to <b>{df['year'].max()}</b><br/>
        • Olympic Games: <b>{df['year'].nunique()}</b> different Olympic games"""
        
        story.append(Paragraph(key_numbers, normal_style))
        story.append(Spacer(1, 15))
        
        # Top countries with better formatting
        story.append(Paragraph("🏆 TOP PERFORMING COUNTRIES", heading_style))
        story.append(Paragraph("These are the countries that won most medals in Olympics:", normal_style))
        
        top_10 = df.groupby('country')['total'].sum().sort_values(ascending=False).head(10)
        countries_list = ""
        for i, (country, medals) in enumerate(top_10.items(), 1):
            if i <= 3:
                medal_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            else:
                medal_emoji = "🏅"
            countries_list += f"{medal_emoji} <b>{i}. {country}</b> - {medals:,} medals<br/>"
        
        story.append(Paragraph(countries_list, normal_style))
        story.append(Paragraph("<b>💡 What This Tells Us:</b> USA is the clear winner with most medals. Big countries like China, Germany, and Russia also perform very well. These countries invest a lot of money in sports training and have good facilities and coaches for athletes.", normal_style))
        story.append(Spacer(1, 15))
        
        # India's performance with enhanced formatting
        story.append(Paragraph("🇮🇳 INDIA'S OLYMPIC PERFORMANCE", heading_style))
        india_data = df[df['country'] == 'India']
        if len(india_data) > 0:
            india_total = india_data['total'].sum()
            india_gold = india_data['gold'].sum()
            india_games = len(india_data)
            
            india_stats = f"""<b>🏅 INDIA'S NUMBERS:</b><br/>
            • Total Medals: <b>{india_total}</b> medals<br/>
            • Gold Medals: <b>{india_gold}</b> gold medals<br/>
            • Games Played: <b>{india_games}</b> Olympic games<br/>
            • Average per Game: <b>{india_total/india_games:.1f}</b> medals per Olympics"""
            
            story.append(Paragraph(india_stats, normal_style))
            story.append(Paragraph("<b>🇮🇳 India's Story:</b> India has been participating in Olympics for many years. Our performance is slowly getting better. We need more investment in sports to compete with top countries. Recent Olympics show improvement in India's medal count.", normal_style))
        else:
            story.append(Paragraph("No data available for India in this dataset.", normal_style))
        story.append(Spacer(1, 15))
        
        # Trends with better formatting
        story.append(Paragraph("📈 IMPORTANT TRENDS WE FOUND", heading_style))
        
        trends_text = """<b>1. 📊 Medal Distribution Over Time:</b><br/>
        Number of medals given has increased over years. This is because more sports and events are added to Olympics. More countries participate now than before.<br/><br/>
        
        <b>2. 🌍 Country Performance Patterns:</b><br/>
        • <b>Consistent Winners:</b> USA, Germany, and Great Britain always perform well<br/>
        • <b>Rising Powers:</b> China has improved a lot in recent Olympics<br/>
        • <b>Political Impact:</b> When Soviet Union broke up, it affected their medal count<br/><br/>
        
        <b>3. 🏅 Medal Types:</b><br/>
        Gold, Silver, and Bronze medals are almost equally distributed. This shows fair competition in Olympics."""
        
        story.append(Paragraph(trends_text, normal_style))
        story.append(Spacer(1, 15))
        
        # Visualization mistakes with enhanced formatting
        story.append(Paragraph("⚠️ COMMON MISTAKES IN DATA VISUALIZATION", heading_style))
        
        mistakes_text = """We also learned about wrong ways to show data:<br/><br/>
        
        <b>🥧 Pie Charts Problems:</b><br/>
        • <b>❌ Bad:</b> Using pie charts with too many countries<br/>
        • <b>🚫 Why Bad:</b> Hard to compare small slices<br/>
        • <b>✅ Better:</b> Use bar charts to show rankings clearly<br/><br/>
        
        <b>📊 Y-Axis Tricks:</b><br/>
        • <b>❌ Bad:</b> Starting Y-axis from middle instead of zero<br/>
        • <b>🚫 Why Bad:</b> Makes small differences look very big<br/>
        • <b>✅ Better:</b> Always start from zero to show true picture"""
        
        story.append(Paragraph(mistakes_text, normal_style))
        story.append(Spacer(1, 15))
        
        # Key learnings with enhanced formatting
        story.append(Paragraph("🎯 KEY LEARNINGS", heading_style))
        
        learnings_text = """<b>🏆 For Countries:</b><br/>
        • <b>💰 Investment Matters:</b> Countries that spend more on sports get more medals<br/>
        • <b>📅 Long-term Planning:</b> Success comes from years of preparation<br/>
        • <b>🏟️ Infrastructure:</b> Good training facilities are very important<br/><br/>
        
        <b>📊 For Data Analysis:</b><br/>
        • <b>📈 Choose Right Charts:</b> Bar charts are better than pie charts for rankings<br/>
        • <b>💯 Be Honest:</b> Don't manipulate scales to mislead people<br/>
        • <b>📖 Tell Stories:</b> Data should tell a clear story that everyone can understand"""
        
        story.append(Paragraph(learnings_text, normal_style))
        story.append(Spacer(1, 15))
        
        # Future predictions
        story.append(Paragraph("🔮 FUTURE PREDICTIONS", heading_style))
        
        predictions_text = """Based on current trends:<br/>
        • <b>🌏 Asian Countries</b> will likely win more medals in future Olympics<br/>
        • <b>🇮🇳 India</b> has potential to improve if we invest more in sports<br/>
        • <b>🌍 Medal Distribution</b> will become more spread across countries<br/>
        • <b>🆕 New Sports</b> will be added, giving more opportunities to different countries"""
        
        story.append(Paragraph(predictions_text, normal_style))
        story.append(Spacer(1, 15))
        
        # Conclusion
        story.append(Paragraph("📝 CONCLUSION", heading_style))
        
        conclusion_text = """This analysis of Olympic data teaches us many things:<br/><br/>
        
        <b>1. 💰 Sports Success Needs Investment:</b> Countries that spend money on sports training get better results<br/><br/>
        
        <b>2. 🏆 Consistency Wins:</b> Countries like USA succeed because they consistently support their athletes<br/><br/>
        
        <b>3. 📊 Data Tells Stories:</b> When we analyze data properly, we can understand patterns and make predictions<br/><br/>
        
        <b>4. 📈 Visualization Matters:</b> How we show data is very important - it should be clear and honest<br/><br/>
        
        <b>5. 🇮🇳 India's Opportunity:</b> Our country has potential to do much better in Olympics with proper planning<br/><br/>
        
        <b>💭 Final Thoughts:</b> Olympics is not just about winning medals. It brings countries together and shows the power of human achievement. Through data analysis, we can understand these patterns and help our country perform better in future Olympics."""
        
        story.append(Paragraph(conclusion_text, normal_style))
        story.append(Spacer(1, 20))
        
        # Footer with enhanced styling
        footer_style = ParagraphStyle('FooterStyle', 
                                    parent=styles['Normal'], 
                                    fontSize=10, 
                                    spaceAfter=4,
                                    textColor='darkblue')
        
        story.append(Paragraph("📋 <b>REPORT DETAILS</b>", heading_style))
        story.append(Paragraph("👤 <b>Report Prepared By:</b> Aryan Gupta (Roll No: 2415800019)", footer_style))
        story.append(Paragraph("📚 <b>Course:</b> Data Visualization and Storytelling", footer_style))
        story.append(Paragraph("👨🏫 <b>Instructor:</b> Dr. Saurabh Tewari", footer_style))
        story.append(Paragraph("🛠️ <b>Tools Used:</b> Python, Streamlit, Plotly, Matplotlib, Seaborn", footer_style))
        story.append(Spacer(1, 12))
        
        italic_style = ParagraphStyle('ItalicStyle', 
                                    parent=styles['Italic'], 
                                    fontSize=9, 
                                    textColor='gray')
        story.append(Paragraph("<i>💡 This report uses simple English to explain complex data patterns so everyone can understand the Olympic Games analysis.</i>", italic_style))

        
        doc.build(story)
        buffer.seek(0)
        
        # Create download link
        b64 = base64.b64encode(buffer.read()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="Olympic_Analysis_Report_Aryan_Gupta.pdf">📄 Click Here to Download PDF Report</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.success("✅ PDF Report generated successfully! Click the link above to download.")
        
        # Show preview
        with st.expander("📖 Preview Report Content"):
            st.markdown(report_text)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>📊 Created with ❤️ using Streamlit, Matplotlib, Seaborn & Plotly</p>
    <p>🏅 Olympic Data Visualization Project | Data Storytelling Assignment</p>
</div>
""", unsafe_allow_html=True)