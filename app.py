import streamlit as st
import pickle
import numpy as np

# Load the pre-trained earthquake prediction model
try:
    earthquake_model_path = "MAG.pkl"  # Replace with the actual path
    earthquake_model = pickle.load(open(earthquake_model_path, 'rb'))
except FileNotFoundError as e:
    st.error(f"Error loading the earthquake prediction model: {e}")
    st.stop()

# Mock prediction function
import numpy as np
import streamlit as st

# Mock prediction function
def predict_earthquake_risk(params):
    # Ensure params is a list of scalars
    try:
        input_array = np.array([float(p) for p in params]).reshape(1, -1)  # Convert all to float
    except ValueError as e:
        raise ValueError(f"Invalid parameter in input_params: {params}. Error: {e}")
    
    # Mock model prediction (replace with your actual model prediction logic)
    mock_prediction = sum(input_array[0]) / len(input_array[0])  # Example: simple average
    return mock_prediction

# Function to predict alert level and display color-coded box
def alert_level():
    st.subheader("Enter the parameters for Alert Level Prediction:")
    col1, col2, col3 = st.columns(3)
    cid = float(col1.number_input("cid", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="cid"))
    longitude = float(col1.number_input("Longitude", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="longitude_alert"))
    mmi = float(col2.number_input("mmi", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="mmi"))
    sig = float(col2.number_input("sig", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="sig_alert"))
    tsunami = float(col3.number_input("Tsunami", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="tsunami"))
    
    # Alert Predict button
    if st.button("Predict Earthquake Alert", key="predict_alert"):
        # Fetch the predicted magnitude from session state
        if "mag" not in st.session_state:
            st.error("Magnitude is not available. Predict it first!")
            return

        input_params = [cid, longitude, st.session_state.mag, mmi, sig, tsunami]
        op = predict_earthquake_risk(input_params)

        # Display color-coded result
        if 0 < op < 0.5:
            #st.success(f"Predicted Earthquake Alert Level: {op}")
            st.markdown('<div style="background-color:green;padding:10px;border-radius:5px;text-align:center;color:white;">Green Alert</div>', unsafe_allow_html=True)
        elif 0.5 < op < 0.6:
            #st.success(f"Predicted Earthquake Alert Level: {op}")
            st.markdown('<div style="background-color:yellow;padding:10px;border-radius:5px;text-align:center;color:black;">Yellow Alert</div>', unsafe_allow_html=True)
        elif 0.6 < op < 0.7:
            #st.success(f"Predicted Earthquake Alert Level: {op}")
            st.markdown('<div style="background-color:orange;padding:10px;border-radius:5px;text-align:center;color:white;">Orange Alert</div>', unsafe_allow_html=True)
        elif 0.7< op < 1:
            #st.success(f"Predicted Earthquake Alert Level: {op}")
            st.markdown('<div style="background-color:red;padding:10px;border-radius:5px;text-align:center;color:white;">Red Alert</div>', unsafe_allow_html=True)
        else:
            st.error("Unexpected alert level.")

# Main Streamlit app
if __name__ == '__main__':
    st.title("Earthquake Prediction Model")

    # Create input fields for the earthquake model
    st.subheader("Enter the parameters for Magnitude Prediction:")
    col1, col2, col3 = st.columns(3)
    depth = float(col1.number_input("Depth", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="depth"))
    latitude = float(col1.number_input("Latitude", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="latitude"))
    longitude = float(col2.number_input("Longitude", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="longitude"))
    gap = float(col2.number_input("Gap", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="gap"))
    rms = float(col2.number_input("RMS", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="rms"))
    felt = float(col3.number_input("Felt", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="felt"))
    sig = float(col3.number_input("SIG", min_value=0.0, max_value=1.0, value=0.50, format="%.6f", key="sig"))
    
    # mag Predict button
    if st.button("Predict Earthquake Magnitude", key="predict_magnitude"):
        input_params = [depth, latitude, longitude, gap, rms, felt, sig]
        mag = predict_earthquake_risk(input_params)
        st.session_state.mag = mag  # Store magnitude in session state
        st.success(f"Predicted Earthquake Risk Magnitude: {mag}")
    
    # Check if magnitude is available before calling alert_level
    if "mag" in st.session_state:
        alert_level()
    else:
        st.info("Please predict the magnitude first.")
