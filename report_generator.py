import streamlit as st
import pandas as pd
import base64
from datetime import datetime

def generate_olympic_report(df, country_flags):
    """Generate a comprehensive Olympic analysis report in simple English"""
    
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

def create_download_link(report_text, filename):
    """Create a download link for the report"""
    b64 = base64.b64encode(report_text.encode()).decode()
    href = f'<a href="data:text/markdown;base64,{b64}" download="{filename}">📄 Click Here to Download Report</a>'
    return href

def display_report_section(df, country_flags):
    """Display the report download section in Streamlit"""
    
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(90deg, #0085C3 0%, #00A651 100%); padding: 1rem; border-radius: 15px; color: white; text-align: center; margin: 1rem 0; font-size: 1.3rem; font-weight: bold;">
        📄 Download Olympic Analysis Report
    </div>
    """, unsafe_allow_html=True)
    
    # Download button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Download Olympic Analysis Report", key="download_report"):
            report_text = generate_olympic_report(df, country_flags)
            
            # Create download link
            download_link = create_download_link(report_text, "Olympic_Analysis_Report_Aryan_Gupta.md")
            st.markdown(download_link, unsafe_allow_html=True)
            st.success("✅ Report generated successfully! Click the link above to download.")
            
            # Show preview
            with st.expander("📖 Preview Report Content"):
                st.markdown(report_text)