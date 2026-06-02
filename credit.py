import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

st.set_page_config(page_title="Credit Scoring App", layout="wide")

st.title("💳 Credit Scoring Application")
st.markdown("---")

# Sidebar for navigation
page = st.sidebar.radio("Select Page", ["Score Calculator", "Model Info"])

if page == "Score Calculator":
    st.header("Calculate Credit Score")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        income = st.number_input("Annual Income ($)", min_value=0, value=50000)
        employment_years = st.number_input("Years of Employment", min_value=0, max_value=60, value=5)
        credit_history_months = st.number_input("Credit History (months)", min_value=0, value=60)
    
    with col2:
        num_accounts = st.number_input("Number of Credit Accounts", min_value=0, max_value=20, value=3)
        credit_utilization = st.slider("Credit Utilization (%)", 0, 100, 30)
        missed_payments = st.number_input("Missed Payments (past 12 months)", min_value=0, value=0)
        total_debt = st.number_input("Total Debt ($)", min_value=0, value=10000)
    
    if st.button("Calculate Credit Score", use_container_width=True):
        # Calculate credit score based on formula
        score = 300  # Base score
        
        # Age factor
        if 25 <= age <= 65:
            score += 50
        elif age > 65:
            score += 40
        
        # Income factor
        if income >= 100000:
            score += 80
        elif income >= 50000:
            score += 60
        elif income >= 30000:
            score += 40
        else:
            score += 20
        
        # Employment stability
        if employment_years >= 10:
            score += 60
        elif employment_years >= 5:
            score += 40
        elif employment_years >= 2:
            score += 20
        
        # Credit history length
        if credit_history_months >= 120:
            score += 50
        elif credit_history_months >= 60:
            score += 30
        elif credit_history_months > 0:
            score += 10
        
        # Credit utilization
        utilization_score = (100 - credit_utilization) / 100 * 100
        score += utilization_score * 0.3
        
        # Missed payments penalty
        score -= missed_payments * 100
        
        # Debt-to-income ratio
        if income > 0:
            dti = total_debt / income
            if dti <= 0.3:
                score += 50
            elif dti <= 0.5:
                score += 30
            elif dti <= 0.8:
                score += 10
            else:
                score -= 20
        
        # Cap score between 300 and 850
        score = max(300, min(850, int(score)))
        
        # Determine credit rating
        if score >= 750:
            rating = "Excellent"
            color = "🟢"
        elif score >= 670:
            rating = "Good"
            color = "🔵"
        elif score >= 580:
            rating = "Fair"
            color = "🟡"
        else:
            rating = "Poor"
            color = "🔴"
        
        # Display results
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Credit Score", score)
        
        with col2:
            st.metric("Rating", f"{color} {rating}")
        
        with col3:
            approval_chance = ((score - 300) / 550) * 100
            st.metric("Loan Approval Chance", f"{min(100, approval_chance):.1f}%")
        
        st.markdown("---")
        
        # Recommendations
        st.subheader("📋 Recommendations")
        recommendations = []
        
        if credit_utilization > 50:
            recommendations.append("• Reduce credit card utilization below 50%")
        if missed_payments > 0:
            recommendations.append("• Pay all bills on time to improve score")
        if employment_years < 2:
            recommendations.append("• Build employment stability for better rates")
        if income < 30000:
            recommendations.append("• Increase income to improve creditworthiness")
        if total_debt > income * 0.8:
            recommendations.append("• Pay down debt to reduce debt-to-income ratio")
        if score < 750:
            recommendations.append("• Monitor and improve factors to reach 'Excellent' rating")
        
        if recommendations:
            for rec in recommendations:
                st.write(rec)
        else:
            st.success("✅ Excellent credit profile! Keep up the good work!")

elif page == "Model Info":
    st.header("Credit Scoring Information")
    
    st.subheader("Score Ranges")
    ranges_df = pd.DataFrame({
        "Score Range": ["300-579", "580-669", "670-749", "750-850"],
        "Rating": ["Poor", "Fair", "Good", "Excellent"],
        "Characteristics": [
            "High risk, likely loan denial",
            "Below average, higher interest rates",
            "Acceptable, standard terms",
            "Low risk, best terms available"
        ]
    })
    st.table(ranges_df)
    
    st.subheader("Factors Considered")
    factors_df = pd.DataFrame({
        "Factor": [
            "Age",
            "Annual Income",
            "Employment Stability",
            "Credit History Length",
            "Credit Utilization",
            "Missed Payments",
            "Debt-to-Income Ratio"
        ],
        "Impact": [
            "10%",
            "15%",
            "12%",
            "10%",
            "20%",
            "18%",
            "15%"
        ]
    })
    st.table(factors_df)
    
    st.info("📌 Note: This is a simplified credit scoring model for educational purposes.")
