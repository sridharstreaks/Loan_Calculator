import streamlit as st
import pandas as pd

# Function to calculate loan schedule
def calculate_loan_schedule(loan_amount, annual_interest_rate, tenure_years, interest_only_months, moratorium_monthly_payment, monthly_payment):
    # Convert annual interest rate to monthly rate
    monthly_interest_rate = (annual_interest_rate / 12) / 100

    # Convert tenure in years to months
    total_months = tenure_years * 12

    # Initialize variables
    remaining_balance = loan_amount
    schedule = []

    for month in range(1, total_months + 1):
        # Calculate interest for the month
        monthly_interest = remaining_balance * monthly_interest_rate

        # Determine the moratorium payment for the month
        if month <= interest_only_months:
            moratorium_payment = moratorium_monthly_payment  # Fixed initial payment during the interest-only period
        elif monthly_payment == 0:
            return "Loan won't be settled"
        else:
            moratorium_payment = monthly_payment

        # Calculate principal payment
        principal_payment = moratorium_payment - monthly_interest

        # Update the remaining balance
        remaining_balance -= principal_payment

        # Create a table entry
        schedule.append({
            "Month": month,
            "Opening Balance": round(remaining_balance + principal_payment, 2),
            "Monthly Interest": round(monthly_interest, 2),
            "Moratorium Payment": moratorium_payment,
            "Principal Payment": round(principal_payment, 2),
            "Closing Balance": round(remaining_balance, 2)
        })

        if remaining_balance <= 0:
            break

    return pd.DataFrame(schedule)

# Streamlit app
def main():
    st.title("Loan Repayment Schedule Calculator")
    st.sidebar.title("Loan Parameters")

    # Sidebar inputs
    loan_amount = st.sidebar.number_input("Loan Amount (INR)", min_value=0)
    annual_interest_rate = st.sidebar.number_input("Annual Interest Rate (%)", min_value=0,step=1e-4,format="%.3f")
    tenure_years = st.sidebar.number_input("Loan Tenure (years)", min_value=0)
    interest_only_months = st.sidebar.number_input("Interest-only Months", min_value=0)
    monthly_payment = st.sidebar.number_input("Monthly Payment (INR)", min_value=0)
    moratorium_monthly_payment = st.sidebar.number_input("Moratorium Payment (INR)", min_value=0)

    if st.sidebar.button("Calculate"):
        # Calculate the loan schedule
        schedule_result = calculate_loan_schedule(loan_amount, annual_interest_rate, tenure_years, interest_only_months, moratorium_monthly_payment, monthly_payment)

        # Display the loan schedule
        st.subheader("Loan Repayment Schedule")
        st.dataframe(schedule_result)

if __name__ == "__main__":
    main()