
import streamlit as st

def calculate_old_regime_tax(income):
    if income <= 250000:
        return 0
    elif income <= 500000:
        return (income - 250000) * 0.05
    elif income <= 1000000:
        return 250000 * 0.05 + (income - 500000) * 0.2
    else:
        return 250000 * 0.05 + 500000 * 0.2 + (income - 1000000) * 0.3

def calculate_new_regime_tax(income):
    tax = 0
    slabs = [
        (400000, 0.00),
        (400000, 0.05),
        (400000, 0.10),
        (400000, 0.15),
        (400000, 0.20),
        (400000, 0.25),
        (float('inf'), 0.30)
    ]
    lower_limit = 0
    for slab_amount, rate in slabs:
        upper_limit = lower_limit + slab_amount
        if income > upper_limit:
            tax += slab_amount * rate
        else:
            tax += (income - lower_limit) * rate
            break
        lower_limit = upper_limit
    return tax

st.set_page_config(page_title="Trimmed Tax Calculator", layout="centered")
st.title("🧮 Income Tax Calculator (Trimmed Version)")

with st.form("tax_form"):
    st.subheader("Salary Inputs")
    basic_salary = st.number_input("Basic Salary", value=0, step=1000)
    da = st.number_input("DA", value=0, step=1000)
    hra = st.number_input("HRA Received", value=0, step=1000)
    special = st.number_input("Special Allowance", value=0, step=1000)
    bonus = st.number_input("Bonus", value=0, step=1000)
    pf = st.number_input("Employer PF", value=0, step=1000)
    variable = st.number_input("Variable Pay", value=0, step=1000)
    other = st.number_input("Other Allowance", value=0, step=1000)

    st.subheader("House Property Loss")
    sop = st.number_input("Interest on SOP Loan", value=0, step=1000)
    lop = st.number_input("Let-Out Property Loss (Net)", value=0, step=1000)
    house_property_loss = max(-(min(sop, 200000) + min(abs(lop), 200000)), -200000)

    st.subheader("Other Inputs")
    other_income = st.number_input("Other Income", value=0, step=1000)
    deduction_80c = st.number_input("80C Deduction", value=0, step=1000)
    deduction_80d = st.number_input("80D Deduction", value=0, step=1000)

    submitted = st.form_submit_button("Calculate Tax")

if submitted:
    gross_salary = basic_salary + da + hra + special + bonus + pf + variable + other
    std_old = 50000
    std_new = 75000
    total_ded_old = std_old + deduction_80c + deduction_80d
    total_ded_new = std_new

    taxable_old = gross_salary + other_income + house_property_loss - total_ded_old
    taxable_new = gross_salary + other_income - total_ded_new

    tax_old = calculate_old_regime_tax(taxable_old)
    tax_new = calculate_new_regime_tax(taxable_new)

    rebate_old = min(12500, tax_old) if taxable_old <= 500000 else 0
    rebate_new = min(25000, tax_new) if taxable_new <= 700000 else 0

    tax_old_final = tax_old - rebate_old
    tax_new_final = tax_new - rebate_new

    total_old = tax_old_final + tax_old_final * 0.04
    total_new = tax_new_final + tax_new_final * 0.04

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Old Regime")
        st.write(f"Taxable Income: ₹{taxable_old:,.2f}")
        st.write(f"Total Tax Payable: ₹{total_old:,.2f}")
    with col2:
        st.subheader("New Regime")
        st.write(f"Taxable Income: ₹{taxable_new:,.2f}")
        st.write(f"Total Tax Payable: ₹{total_new:,.2f}")
