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
            # Use the standard EMI for the current month
            remaining_months = total_months - month + 1
            standard_emi = calculate_standard_emi(remaining_balance, annual_interest_rate, remaining_months, 0, moratorium_monthly_payment)
            moratorium_payment = standard_emi
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
            "Moratorium Payment": round(moratorium_payment, 2),  # Round the EMI to 2 decimal places
            "Principal Payment": round(principal_payment, 2),
            "Closing Balance": round(remaining_balance, 2)
        })

        if remaining_balance <= 0:
            break

    return pd.DataFrame(schedule)

# Function to calculate the standard EMI for a given remaining balance
def calculate_standard_emi(remaining_balance, annual_interest_rate, remaining_tenure_months, remaining_interest_only_months, moratorium_monthly_payment):
    # Convert annual interest rate to monthly rate
    monthly_interest_rate = (annual_interest_rate / 12) / 100

    # Calculate the EMI using the standard formula for the remaining balance
    emi = (remaining_balance * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -remaining_tenure_months)

    return emi
    
# Streamlit app
def main():
    st.title("Loan Repayment Schedule Calculator")
    st.sidebar.title("Loan Parameters")

    # Sidebar inputs
    loan_amount = st.sidebar.number_input("Loan Amount (INR)", min_value=0)
    annual_interest_rate = st.sidebar.number_input("Annual Interest Rate (%)", min_value=0.0, step=1e-3, format="%.2f")
    tenure_years = st.sidebar.number_input("Loan Tenure (years)", min_value=0)
    interest_only_months = st.sidebar.number_input("Interest-only Months", min_value=0)
    monthly_payment = st.sidebar.number_input("Monthly Payment (INR)", min_value=0)
    moratorium_monthly_payment = st.sidebar.number_input("Moratorium Payment (INR)", min_value=0)
    
    # Add input for bulk payment
    bulk_payment_option = st.sidebar.checkbox("Make Bulk Payment")
    if bulk_payment_option:
        bulk_payment_amount = st.sidebar.number_input("Bulk Payment Amount (INR)", min_value=0)
        bulk_payment_month = st.sidebar.number_input("Month for Bulk Payment", min_value=1, max_value=tenure_years * 12)

    if st.sidebar.button("Calculate"):
        if monthly_payment == 0:
            # Display a message indicating the standard EMI will be used
            st.warning("Using standard EMI for the current month.")
            # Calculate the loan schedule with standard EMI for the current month
            standard_emi = calculate_standard_emi(loan_amount, annual_interest_rate, tenure_years, interest_only_months, moratorium_monthly_payment)
            schedule_result = calculate_loan_schedule(loan_amount, annual_interest_rate, tenure_years, interest_only_months, moratorium_monthly_payment, standard_emi)
        else:
            # Calculate the loan schedule with the user-provided monthly payment
            schedule_result = calculate_loan_schedule(loan_amount, annual_interest_rate, tenure_years, interest_only_months, moratorium_monthly_payment, monthly_payment)

        # Check if a bulk payment is specified and calculate the loan schedule with it
        if bulk_payment_option and bulk_payment_amount > 0:
            schedule_result = apply_bulk_payment(schedule_result, bulk_payment_month, bulk_payment_amount)

        # Check if it's a string message indicating loan won't be settled
        if isinstance(schedule_result, str):
            st.error(schedule_result)  # Display the error message
        else:
            # Calculate total interest paid and total loan taken
            total_interest_paid = schedule_result['Monthly Interest'].sum()

            # Display total interest paid and total loan taken
            st.subheader("Summary")
            st.write(f"Total Interest Paid: {round(total_interest_paid, 2)} INR")
            st.write(f"Total Loan Taken: {round(loan_amount, 2)} INR")

            # Display the loan schedule
            st.subheader("Loan Repayment Schedule")
            st.dataframe(schedule_result)

# Function to apply bulk payment to the loan schedule
def apply_bulk_payment(schedule, bulk_payment_month, bulk_payment_amount):
    if bulk_payment_month <= len(schedule):
        # Deduct the bulk payment from the closing balance of the specified month
        schedule.loc[bulk_payment_month - 1, "Closing Balance"] -= bulk_payment_amount
        return schedule
    else:
        return "Invalid bulk payment month. Please select a valid month."

if __name__ == "__main__":
    main()
