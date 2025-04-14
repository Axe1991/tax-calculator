
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

st.set_page_config(page_title="Tax Calculator - Old vs New Regime", layout="centered")

st.title("🧮 Income Tax Calculator (India)")
st.subheader("Compare Tax Payable under Old and New Regime (FY 2025-26)")

with st.form("tax_form"):
    st.markdown("### 👤 Enter Your Details")
    basic_salary = st.number_input("Basic Salary", value=0, step=1000)
    hra = st.number_input("HRA Received", value=0, step=1000)
    other_allowances = st.number_input("Other Allowances", value=0, step=1000)
    other_income = st.number_input("Other Income (e.g. Interest)", value=0, step=1000)
    deductions_80C = st.number_input("Deduction under 80C", value=0, step=1000)
    deductions_80D = st.number_input("Deduction under 80D", value=0, step=1000)

    submitted = st.form_submit_button("Calculate Tax")

if submitted:
    # Standard deductions
    standard_deduction_old = 50000
    standard_deduction_new = 75000

    gross_salary = basic_salary + hra + other_allowances
    total_deductions_old = standard_deduction_old + deductions_80C + deductions_80D
    total_deductions_new = standard_deduction_new

    taxable_income_old = gross_salary + other_income - total_deductions_old
    taxable_income_new = gross_salary + other_income - total_deductions_new

    tax_old = calculate_old_regime_tax(taxable_income_old)
    tax_new = calculate_new_regime_tax(taxable_income_new)

    # 87A rebate
    rebate_old = min(12500, tax_old) if taxable_income_old <= 500000 else 0
    rebate_new = min(25000, tax_new) if taxable_income_new <= 700000 else 0

    tax_after_rebate_old = tax_old - rebate_old
    tax_after_rebate_new = tax_new - rebate_new

    cess_old = tax_after_rebate_old * 0.04
    cess_new = tax_after_rebate_new * 0.04

    total_tax_old = tax_after_rebate_old + cess_old
    total_tax_new = tax_after_rebate_new + cess_new

    st.markdown("## 🧾 Tax Computation Summary")
    st.write(f"**Gross Salary:** ₹{gross_salary:,.2f}")
    st.write(f"**Other Income:** ₹{other_income:,.2f}")
    st.divider()
    st.write("### Old Regime")
    st.write(f"**Taxable Income:** ₹{taxable_income_old:,.2f}")
    st.write(f"**87A Rebate:** ₹{rebate_old:,.2f}")
    st.write(f"**Total Tax Payable:** ₹{total_tax_old:,.2f}")
    st.write("### New Regime")
    st.write(f"**Taxable Income:** ₹{taxable_income_new:,.2f}")
    st.write(f"**87A Rebate:** ₹{rebate_new:,.2f}")
    st.write(f"**Total Tax Payable:** ₹{total_tax_new:,.2f}")
