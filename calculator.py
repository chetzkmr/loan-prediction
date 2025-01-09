import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate monthly payment
def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12
    if monthly_interest_rate > 0:
        monthly_payment = (
            loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments
        ) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    else:
        monthly_payment = loan_amount / number_of_payments
    return monthly_payment

# Function to generate amortization schedule
def generate_amortization_schedule(loan_amount, annual_interest_rate, loan_term_years):
    monthly_payment = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)
    monthly_interest_rate = annual_interest_rate / 100 / 12
    balance = loan_amount
    schedule = []

    for payment_number in range(1, loan_term_years * 12 + 1):
        interest_payment = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        schedule.append({
            "Payment Number": payment_number,
            "Principal Payment": principal_payment,
            "Interest Payment": interest_payment,
            "Remaining Balance": max(balance, 0),
        })
        if balance <= 0:
            break

    return pd.DataFrame(schedule)

# Streamlit app title
st.title("Loan/Mortgage Calculator")

# User input
loan_amount = st.number_input("Loan Amount ($):", min_value=0.0, value=250000.0, step=1000.0)
annual_interest_rate = st.number_input("Annual Interest Rate (%):", min_value=0.0, value=5.0, step=0.1)
loan_term_years = st.number_input("Loan Term (Years):", min_value=1, value=30, step=1)

if st.button("Calculate"):
    # Calculate monthly payment
    monthly_payment = calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years)

    # Generate amortization schedule
    schedule = generate_amortization_schedule(loan_amount, annual_interest_rate, loan_term_years)

    # Display results
    st.subheader("Results")
    st.write(f"*Monthly Payment:* ${monthly_payment:,.2f}")

    # Display amortization schedule
    st.subheader("Amortization Schedule")
    st.dataframe(schedule)

    # Plot amortization schedule
    st.subheader("Amortization Chart")
    fig, ax = plt.subplots()
    ax.plot(schedule["Payment Number"], schedule["Remaining Balance"], label="Remaining Balance")
    ax.set_xlabel("Payment Number")
    ax.set_ylabel("Amount ($)")
    ax.set_title("Loan Amortization Schedule")
    ax.legend()
    st.pyplot(fig)