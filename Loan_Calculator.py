import streamlit as st
import pandas as pd

def amortization(loan, interest_rate, tenure, monthly_amount, moro_months, moro_pay):
    monthly_interest_rate = (interest_rate / 12) / 100
    tenure_months = tenure * 12
    remaining = loan
    schedule = []

    while moro_months > 0:
        monthly_interest = remaining * monthly_interest_rate
        emi = remaining * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure_months) / (
                    (1 + monthly_interest_rate) ** tenure_months - 1)
        monthly_remain = emi - monthly_interest
        added_principle = monthly_remain - moro_pay + monthly_interest
        remaining += added_principle

        schedule.append({
            "Opening Balance": round(remaining, 2),
            "Monthly Interest": round(monthly_interest, 2),
            "Monthly Remaining": round(monthly_remain, 2),
            "Added Principle": round(added_principle, 2),
            "Closing Balance": round(remaining, 2) if remaining > 0 else 0
        })

        tenure_months -= 1
        moro_months -= 1
        
    total_interest_paid = 0

    while tenure_months > 0:
        monthly_interest = remaining * monthly_interest_rate
        emi = remaining * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure_months) / (
                    (1 + monthly_interest_rate) ** tenure_months - 1)
        schedule.append({
            "Opening Balance": round(remaining, 2),
            "Monthly Interest": round(monthly_interest, 2),
        })

        if monthly_amount > 0:
            principle = monthly_amount - monthly_interest
        else:
            principle = emi - monthly_interest

        remaining = remaining - principle
        total_interest_paid += monthly_interest
        tenure_months -= 1

        schedule.append({
            "Monthly Payment": round(monthly_amount if monthly_amount > 0 else emi, 2),
            "Principal/EMI Payment": round(principle, 2) if remaining > 0 else 'Balance Adjusted',
            "Closing Balance": round(remaining, 2) if remaining > 0 else 0
        })

        if remaining < 0:
            break

    return schedule, "Loan completed {} months before tenure".format(tenure_months),total_interest_paid


def main():
    st.title("Loan Amortization Calculator")

    # Sidebar inputs
    loan_amount = st.sidebar.number_input("Loan Amount (INR) [Mandatory]", min_value=0)
    annual_interest_rate = st.sidebar.number_input("Annual Interest Rate (%) [Mandatory]", min_value=0.0, step=1e-3, format="%.2f")
    tenure_years = st.sidebar.number_input("Loan Tenure (years) [Mandatory]", min_value=0)
    monthly_payment = st.sidebar.number_input("Monthly Payment (INR) [Optional]", min_value=0)
    moratorium_months = st.sidebar.number_input("Moratorium Months [Optional]", min_value=0)
    moratorium_payment = st.sidebar.number_input("Moratorium Payment (INR) [Optional]", min_value=0)

    if st.sidebar.button("Calculate"):
        schedule, total_interest_paid, months_before_completion = amortization(
            loan_amount, annual_interest_rate, tenure_years, monthly_payment, moratorium_months, moratorium_payment
        )

        # Display total interest paid and months before completion
        st.subheader("Summary")
        st.write(f"Total Interest Paid: {round(total_interest_paid, 2)} INR")
        st.write(f"Loan Completed {months_before_completion} months before the tenure.")

        # Display the loan schedule
        st.subheader("Loan Repayment Schedule")
        df_schedule = pd.DataFrame(schedule)
        st.dataframe(df_schedule)

if __name__ == "__main__":
    main()
