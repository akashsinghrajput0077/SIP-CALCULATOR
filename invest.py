import streamlit as st

st.set_page_config(page_title="SIP Calculator", layout="centered")

st.title("SIP Calculator")
st.write("Calculate the future value of a monthly SIP with a given annual return rate.")

monthly_investment = st.number_input(
    "Monthly investment amount (₹)",
    min_value=0.0,
    value=1000.0,
    step=100.0,
    format="%.2f",
)
annual_return = st.number_input(
    "Expected annual return rate (%)",
    min_value=0.0,
    value=12.0,
    step=0.1,
    format="%.2f",
)
investment_years = st.number_input(
    "Investment duration (years)",
    min_value=1,
    value=10,
    step=1,
)

if st.button("Calculate"):
    rate = annual_return / 100 / 12
    periods = int(investment_years * 12)

    if rate == 0:
        future_value = monthly_investment * periods
    else:
        future_value = monthly_investment * (((1 + rate) ** periods - 1) / rate) * (1 + rate)

    total_invested = monthly_investment * periods
    returns = future_value - total_invested

    st.success("SIP result")
    st.metric("Total investment", f"₹{total_invested:,.2f}")
    st.metric("Estimated future value", f"₹{future_value:,.2f}")
    st.metric("Estimated returns", f"₹{returns:,.2f}")

    st.write("### Details")
    st.write(f"- Monthly SIP: ₹{monthly_investment:,.2f}")
    st.write(f"- Annual return rate: {annual_return:.2f} %")
    st.write(f"- Duration: {investment_years} years ({periods} months)")
    st.write(f"- Total invested: ₹{total_invested:,.2f}")
    st.write(f"- Total estimated value: ₹{future_value:,.2f}")
    st.write(f"- Estimated returns: ₹{returns:,.2f}")

    if investment_years > 0 and total_invested > 0:
        cagr = ((future_value / total_invested) ** (1 / investment_years) - 1) * 100
        st.write(f"- Estimated CAGR: {cagr:.2f} %")
    else:
        st.write("- Estimated CAGR: 0.00 %")
