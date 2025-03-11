import streamlit as st

# Custom CSS for Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #d0f0ff; /* Light Sky Blue */
        }
        h1, h3 {
            font-size: 22px !important;
            text-align: center;
            font-weight: bold;
        }
        label {
            font-size: 18px !important;
            font-weight: bold;
            color: black !important;
        }
        .stRadio > div {
            flex-direction: column;
            align-items: center;
        }
        .stButton button {
            background-color: #d6d6d6 !important; /* Light Grey */
            color: black !important;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px;
            width: 100%;
        }
        .stButton button:hover {
            background-color: #bbbbbb !important;
        }
        .stNumberInput input, .stSlider {
            font-size: 18px;
            background: white;
            border-radius: 10px;
        }
        @media (max-width: 600px) {
            .stApp {
                padding: 10px !important;
            }
            h1, h3 {
                font-size: 18px !important;
            }
            label, .stButton button {
                font-size: 16px !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Function to calculate power
def calculate_power(phase, current_red=0, current_yellow=0, current_blue=0, power_factor=0.8):
    if phase == "Single Phase":
        voltage = 220  
        power = (voltage * current_red * power_factor) / 1000  
    else:
        voltage = 400  
        avg_current = (current_red + current_yellow + current_blue) / 3  
        power = (1.732 * voltage * avg_current * power_factor) / 1000  
    return round(power, 3)

# Function to convert HP ↔ kW
def convert_hp_kw(value, convert_to):
    if convert_to == "HP to kW":
        return round(value * 0.746, 3), "kW"
    else:
        return round(value / 0.746, 3), "HP"

# Streamlit UI
st.title("⚡ Electric Power Calculator & Converter")

# Mode selection
st.markdown("### **Select Calculation Mode**")
mode = st.radio("", ["Single Phase Power", "Three Phase Power", "HP ↔ kW Conversion"], horizontal=True)

if mode == "Single Phase Power":
    st.markdown("### **🔌 Enter Running Amp (A)**")
    current_red = st.number_input("", min_value=0.0, step=0.1, value=5.0)
    current_yellow = current_blue = 0  

elif mode == "Three Phase Power":
    st.markdown("### **Enter Running Amp for Each Phase**")
    current_red = st.number_input("🔴 **Red Phase Amp (A):**", min_value=0.0, step=0.1, value=5.0)
    current_yellow = st.number_input("🟡 **Yellow Phase Amp (A):**", min_value=0.0, step=0.1, value=5.0)
    current_blue = st.number_input("🔵 **Blue Phase Amp (A):**", min_value=0.0, step=0.1, value=5.0)

elif mode == "HP ↔ kW Conversion":
    st.markdown("### **Enter Value for Conversion**")
    value = st.number_input("Enter Value:", min_value=0.0, step=0.1, value=1.0)
    convert_to = st.radio("Select Conversion Type:", ["HP to kW", "kW to HP"], horizontal=True)

    # Auto conversion display
    converted_value, unit = convert_hp_kw(value, convert_to)
    st.markdown(f"#### ⚡ **{value} {convert_to.split()[0]} = {converted_value} {unit}**")

# Power Factor input (Only for Power Calculation)
if mode in ["Single Phase Power", "Three Phase Power"]:
    st.markdown("### **⚡ Enter Power Factor**")
    power_factor = st.number_input("", min_value=0.1, max_value=1.0, step=0.01, value=0.8)

# Calculate Button
if st.button("🔍 **Calculate**"):
    if mode in ["Single Phase Power", "Three Phase Power"]:
        result = calculate_power(mode, current_red, current_yellow, current_blue, power_factor)
        st.success(f"🔹 Power Consumption: {result} kW")
    elif mode == "HP ↔ kW Conversion":
        result, unit = convert_hp_kw(value, convert_to)
        st.success(f"🔹 Converted Value: {result} {unit}")

# Footer
st.markdown("<p style='text-align: center; color: black;'>⚡ Created by Noushad Akhter</p>", unsafe_allow_html=True)
