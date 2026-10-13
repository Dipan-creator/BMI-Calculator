import streamlit as st
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Personal BMI Calculator", page_icon="⚖️", layout="centered")

st.title("⚖️ Personal BMI Calculator")
st.write("Enter your weight and height below to calculate your Body Mass Index (BMI).")

# --- INITIALISE SESSION STATE FOR BMI ---
if 'calculated_bmi' not in st.session_state:
    st.session_state.calculated_bmi = 21.0  # Default normal value on first load

# --- 1. BMI METER AT THE TOP WITH LABELS ---
# Define colors for the arcs
step_underweight = dict(range=[10, 18.5], color='#ff4d4d')
step_normal = dict(range=[18.5, 25.0], color='#2ecc71')
step_overweight = dict(range=[25.0, 30.0], color='#f1c40f')
step_obese = dict(range=[30.0, 40.0], color='#e74c3c')

# Custom positioning variables to put text labels nicely inside the scale arc
# We place each word at the mathematical center point of its range
tick_values = [14.25, 21.75, 27.5, 35.0]
tick_labels = ["Underweight", "Normal", "Overweight", "Obese"]

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = st.session_state.calculated_bmi,
    title = {'text': "Current BMI Score", 'font': {'size': 22}},
    gauge = {
        'axis': {
            'range': [10, 40],
            'tickvals': tick_values,
            'ticktext': tick_labels,
            'tickfont': {'size': 14, 'color': 'black', 'weight': 'bold'}
        },
        'bar': {'color': "black", 'thickness': 0.2},
        'bgcolor': "white",
        'steps': [step_underweight, step_normal, step_overweight, step_obese]
    }
))

fig.update_layout(height=280, margin=dict(l=30, r=30, t=20, b=10))
st.plotly_chart(fig, use_container_width=True)

# Display text banners directly below the meter based on the current score
if st.session_state.calculated_bmi < 18.5:
    st.info("Category: **Underweight** 🔵\n\nYou are below a healthy weight range. Consider consulting a health professional.")
elif 18.5 <= st.session_state.calculated_bmi < 25.0:
    st.success("Category: **Normal / Healthy Weight** 🟢\n\nGreat job! You are in a healthy weight range.")
elif 25.0 <= st.session_state.calculated_bmi < 30.0:
    st.warning("Category: **Overweight** 🟡\n\nYou are in the overweight range. Regular exercise and a balanced diet can help to reduce your BMI.")
else:
    st.error("Category: **Obese** 🔴\n\nYou are in the obese range. Consider consulting a health professional.")

st.write("---")

# --- 2. INPUT FIELDS AND CONTROLS BELOW THE METER ---
weight = st.number_input("**Weight(in kilograms)**", min_value=1.0, max_value=300.0, value=65.0, step=0.1)

st.write("**Height(Feet & Inches)**")
col1, col2 = st.columns(2)

with col1:
    feet = st.number_input("Feet", min_value=1, max_value=8, value=5, step=1)

with col2:
    inches = st.number_input("Inches", min_value=0, max_value=11, value=11, step=1)

if st.button("Submit", type="primary"):
    # Mathematical Conversions
    total_inches = (feet * 12) + inches
    height_m = total_inches * 0.0254
    
    # Update Session State and rerun page to show new meter value
    st.session_state.calculated_bmi = weight / (height_m ** 2)
    st.rerun()
