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
            "Month": tenure_months,
            "Opening Balance": round(remaining, 2),
            "Monthly Interest": round(monthly_interest, 2),
            "EMI": round(emi, 2),
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

        if monthly_amount > 0:
            principle = monthly_amount - monthly_interest
        else:
            principle = emi - monthly_interest

        remaining = remaining - principle
        total_interest_paid += monthly_interest
        tenure_months -= 1


        if remaining < 0:
            break
            
        schedule.append({
            "Month": tenure_months,
            "Opening Balance": round(remaining, 2) if remaining > 0 else 0,
            "Monthly Interest": round(monthly_interest, 2) if remaining > 0 else 0,
            "EMI": round(emi, 2) if remaining > 0 else 0,
            "Monthly Payment": round((monthly_amount if monthly_amount > 0 else emi) if remaining > 0 else 0, 2),
            "Closing Balance": round(remaining, 2) if remaining > 0 else 0
        })
    
    
    return schedule, f'Loan completed {tenure_months} months before tenure', total_interest_paid

# Streamlit app
def main():
    st.title("Amortization Schedule Calculator")

    # Input parameters
    loan_amount = st.number_input("Loan Amount (INR)", min_value=0)
    annual_interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.01, format="%.2f")
    loan_tenure = st.number_input("Loan Tenure (years)", min_value=0)
    monthly_payment = st.number_input("Monthly Payment (INR)", min_value=0)
    moratorium_months = st.number_input("Moratorium Months", min_value=0)
    moratorium_payment = st.number_input("Moratorium Payment (INR)", min_value=0)

    if st.button("Calculate"):
        schedule, completion_message, total_interest = amortization(loan_amount, annual_interest_rate, loan_tenure,
                                                                    monthly_payment, moratorium_months, moratorium_payment)
        st.subheader("Amortization Schedule")
        df_schedule = pd.DataFrame(schedule)
        st.dataframe(df_schedule,use_container_width=True,hide_index=True)

        st.subheader("Summary")
        st.write(completion_message)
        st.write(f"Total Interest Paid: {round(total_interest, 2)} INR")

if __name__ == "__main__":
    main()