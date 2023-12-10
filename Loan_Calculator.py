import streamlit as st

def ammortization(loan, interest_rate, tenure, monthly_amount, moro_months, moro_pay):
    monthly_interest_rate = (interest_rate / 12) / 100
    tenure_months = tenure * 12

    emi = loan * monthly_interest_rate * ((1 + monthly_interest_rate) ** tenure_months) / (
            (1 + monthly_interest_rate) ** tenure_months - 1
    )

    remaining = loan
    counter = 0

    # Precompute components that don't change in the loop
    monthly_interest = remaining * monthly_interest_rate
    emi_minus_interest = emi - monthly_interest

    schedule = []

    while moro_months > 0:
        added_principle = emi_minus_interest - moro_pay

        remaining += added_principle

        tenure_months -= counter
        counter += 1
        moro_months -= 1

    total_interest_paid = 0

    while tenure_months > 0:
        monthly_interest = remaining * monthly_interest_rate
        emi_minus_interest = emi - monthly_interest

        if monthly_amount > 0:
            principle = monthly_amount - monthly_interest
        else:
            principle = emi_minus_interest

        remaining -= principle

        total_interest_paid += monthly_interest

        tenure_months -= 1

        # Append to the schedule
        schedule.append({
            "Month": tenure_months,
            "Opening Balance": remaining + principle,
            "Monthly Interest": monthly_interest,
            "Monthly Payment": monthly_amount if monthly_amount > 0 else emi,
            "Principal Payment": principle,
            "Closing Balance": remaining
        })

        if remaining < 0:
            break

    return schedule, total_interest_paid, tenure_months

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
        schedule, total_interest_paid, months_before_completion = ammortization(
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
