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

    # Inside the loop for calculating the loan schedule
for month in range(1, total_months + 1):
    # Calculate interest for the month
    monthly_interest = remaining_balance * monthly_interest_rate

    if month <= interest_only_months:
        moratorium_payment = moratorium_monthly_payment  # Fixed initial payment during the interest-only period
    elif monthly_payment == 0:
        # Use the standard EMI for the current month
        remaining_months = total_months - month + 1

        # Calculate principal payment
        principal_payment = calculate_standard_emi(remaining_balance, annual_interest_rate, remaining_months, 0, moratorium_monthly_payment)

        # Update the remaining balance
        remaining_balance -= principal_payment

        moratorium_payment = principal_payment  # Set moratorium payment to the principal payment for standard EMI
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
        "Moratorium Payment": round(moratorium_payment, 2),
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

    # Variable descriptions on the main page
    st.markdown("### Loan Amount (INR) [Mandatory]")
    st.write("The total amount of the loan.")

    st.markdown("### Annual Interest Rate (%) [Mandatory]")
    st.write("The annual interest rate for the loan.")

    st.markdown("### Loan Tenure (years) [Mandatory]")
    st.write("The duration of the loan in years.")

    st.markdown("### Interest-only Months [Optional]")
    st.write("Number of months with interest-only payments.")

    st.markdown("### Monthly Payment (INR) [Optional]")
    st.write("The fixed monthly payment towards the loan. If left as 0, standard EMI will be used.")

    st.markdown("### Moratorium Payment (INR) [Optional]")
    st.write("Fixed initial payment during the moratorium period.")

    st.sidebar.title("Loan Parameters")

    # Sidebar inputs
    loan_amount = st.sidebar.number_input("Loan Amount (INR) [Mandatory]", min_value=0)
    annual_interest_rate = st.sidebar.number_input("Annual Interest Rate (%) [Mandatory]", min_value=0.0, step=1e-3, format="%.2f")
    tenure_years = st.sidebar.number_input("Loan Tenure (years) [Mandatory]", min_value=0)
    interest_only_months = st.sidebar.number_input("Interest-only Months [Optional]", min_value=0)
    monthly_payment = st.sidebar.number_input("Monthly Payment (INR) [Optional]", min_value=0)
    moratorium_monthly_payment = st.sidebar.number_input("Moratorium Payment (INR) [Optional]", min_value=0)

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


if __name__ == "__main__":
    main()
