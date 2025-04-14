
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

st.set_page_config(page_title="Tax Calculator with House Property", layout="centered")
st.title("🧮 Income Tax Calculator with House Property (FY 2025-26)")

with st.form("tax_form"):
    st.subheader("💼 Salary Components")
    basic_salary = st.number_input("Basic Salary", value=0, step=1000)
    da = st.number_input("Dearness Allowance (DA)", value=0, step=1000)
    hra_received = st.number_input("HRA Received", value=0, step=1000)
    special_allowance = st.number_input("Special Allowance", value=0, step=1000)
    lta = st.number_input("Leave Travel Allowance (LTA)", value=0, step=1000)
    transport_allowance = st.number_input("Transport Allowance", value=0, step=1000)
    bonus = st.number_input("Bonus", value=0, step=1000)
    pf = st.number_input("Employer Provident Fund Contribution", value=0, step=1000)
    variable_pay = st.number_input("Variable Pay", value=0, step=1000)
    other_allowance = st.number_input("Other Allowance", value=0, step=1000)

    st.subheader("📥 Other Inputs")
    other_income = st.number_input("Other Income (e.g. Interest)", value=0, step=1000)
    deductions_80C = st.number_input("Deduction under 80C", value=0, step=1000)
    deductions_80D = st.number_input("Deduction under 80D", value=0, step=1000)

    st.subheader("🏠 Income from House Property")

    st.markdown("### Self-Occupied Property")
    col1, col2 = st.columns([2, 1])
    col1.write("Interest on Housing Loan (max ₹2,00,000 allowed)")
    sop_interest = col2.number_input(" ", key="sop_int")
    sop_loss = -min(sop_interest, 200000)

    st.markdown("### Let-Out Property")
    col1, col2 = st.columns([2, 1])
    col1.write("Gross Rental Income (GTI)")
    gti = col2.number_input(" ", key="gti")

    col1, col2 = st.columns([2, 1])
    col1.write("Less: Property Tax Paid (PTP)")
    ptp = col2.number_input(" ", key="ptp")

    nti = gti - ptp
    std_ded = 0.30 * nti if nti > 0 else 0

    col1, col2 = st.columns([2, 1])
    col1.write("Less: Interest on Housing Loan (24b)")
    lop_interest = col2.number_input(" ", key="lop_int")

    lop_loss = nti - std_ded - lop_interest
    lop_loss_capped = -min(abs(lop_loss), 200000)
    total_hp_loss = sop_loss + lop_loss_capped

    st.write(f"**Total Income/Loss from House Property (adjusted): ₹{total_hp_loss:,.2f}**")

    claim_hra = st.checkbox("Claim HRA Exemption (Old Regime Only)?")
    hra_exemption = 0
    if claim_hra:
        rent_paid = st.number_input("Rent Paid (Annual)", value=0, step=1000)
        is_metro = st.checkbox("Do you live in a Metro City?")
        percent_salary = 0.5 if is_metro else 0.4
        hra_exemption = min(hra_received, rent_paid - 0.1 * (basic_salary + da), percent_salary * (basic_salary + da))
        if hra_exemption < 0:
            hra_exemption = 0

    submitted = st.form_submit_button("Calculate Tax")

if submitted:
    gross_salary = basic_salary + da + hra_received + special_allowance + lta + transport_allowance + bonus + pf + variable_pay + other_allowance
    standard_deduction_old = 50000
    standard_deduction_new = 75000

    total_deductions_old = standard_deduction_old + deductions_80C + deductions_80D + hra_exemption
    total_deductions_new = standard_deduction_new

    taxable_income_old = gross_salary + other_income + total_hp_loss - total_deductions_old
    taxable_income_new = gross_salary + other_income - total_deductions_new  # No HP loss allowed in new regime

    tax_old = calculate_old_regime_tax(taxable_income_old)
    tax_new = calculate_new_regime_tax(taxable_income_new)

    rebate_old = min(12500, tax_old) if taxable_income_old <= 500000 else 0
    rebate_new = min(25000, tax_new) if taxable_income_new <= 700000 else 0

    tax_after_rebate_old = tax_old - rebate_old
    tax_after_rebate_new = tax_new - rebate_new

    cess_old = tax_after_rebate_old * 0.04
    cess_new = tax_after_rebate_new * 0.04

    total_tax_old = tax_after_rebate_old + cess_old
    total_tax_new = tax_after_rebate_new + cess_new

    st.markdown("## 🧾 Tax Computation Summary")
    st.write(f"**Gross Salary (Annual):** ₹{gross_salary:,.2f}")
    st.write(f"**Other Income:** ₹{other_income:,.2f}")
    st.write(f"**HRA Exemption (Old Regime):** ₹{hra_exemption:,.2f}")
    if claim_hra:
        hra_1 = hra_received
        hra_2 = rent_paid - 0.1 * (basic_salary + da)
        hra_3 = percent_salary * (basic_salary + da)
        hra_2 = hra_2 if hra_2 > 0 else 0
        st.markdown("**📘 HRA Exemption Calculation:**")
        st.write(f"1. Actual HRA Received: ₹{hra_1:,.2f}")
        st.write(f"2. Rent Paid – 10% of Salary (Basic + DA): ₹{hra_2:,.2f}")
        st.write(f"3. {'50%' if is_metro else '40%'} of Salary (Basic + DA): ₹{hra_3:,.2f}")
        st.write(f"✅ **Exemption Allowed (least of above): ₹{hra_exemption:,.2f}**")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Old Regime")
        st.write(f"**Taxable Income:** ₹{taxable_income_old:,.2f}")
        st.write(f"**87A Rebate:** ₹{rebate_old:,.2f}")
        st.write(f"**Total Tax Payable:** ₹{total_tax_old:,.2f}")
    with col2:
        st.subheader("New Regime")
        st.write(f"**Taxable Income:** ₹{taxable_income_new:,.2f}")
        st.write(f"**87A Rebate:** ₹{rebate_new:,.2f}")
        st.write(f"**Total Tax Payable:** ₹{total_tax_new:,.2f}")
