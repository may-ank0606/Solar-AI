import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.title("Solar Industry AI Assistant ☀️")
st.write("Upload a satellite image of a rooftop and enter a prompt to analyze solar potential.")

uploaded_file = st.file_uploader("Upload Satellite Image", type=["png", "jpg", "jpeg"])
user_prompt = st.text_area("Enter your analysis prompt", value="Analyze this rooftop for solar panel suitability and give panel placement area, estimated power output (kWh/year), and shading issues.")

def segment_rooftop_area(image: Image.Image) -> float:
    # Convert to grayscale and use thresholding to simulate segmentation
    image_np = np.array(image.convert("L"))  # Convert to grayscale
    _, thresh = cv2.threshold(image_np, 180, 255, cv2.THRESH_BINARY)
    area_pixels = np.sum(thresh == 255)
    total_pixels = image_np.shape[0] * image_np.shape[1]
    usable_ratio = area_pixels / total_pixels
    return usable_ratio * total_pixels / 10000  # return m²

def mock_image_analysis(image: Image.Image, prompt: str) -> str:
    area_estimate = segment_rooftop_area(image)
    return f"**Prompt**: {prompt}\n\n**Estimated Rooftop Area**: {area_estimate:.2f} m²\n- Suitable for ~{int(area_estimate // 1.6)} panels\n- Estimated Power Output: ~{area_estimate * 15:.0f} kWh/year\n- Shading Issues: Minor near corners."

def estimate_roi(area_m2, cost_per_watt=50, efficiency=0.18):
    kw_installed = area_m2 * efficiency
    annual_output_kwh = kw_installed * 1500
    savings_per_year = annual_output_kwh * 6  # ₹6/kWh
    cost = kw_installed * 1000 * cost_per_watt / 100
    payback_years = cost / savings_per_year
    return annual_output_kwh, savings_per_year, cost, payback_years

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Rooftop Image", use_column_width=True)

    if user_prompt:
        with st.spinner("Analyzing rooftop..."):
            analysis = mock_image_analysis(image, user_prompt)
            st.success("Analysis Complete!")
            st.markdown(analysis)

    area_m2 = st.number_input("Estimated Suitable Area (m²)", min_value=10, max_value=500, value=100)
    if st.button("Estimate ROI"):
        output_kwh, savings, cost, payback = estimate_roi(area_m2)
        st.write(f"📊 **Estimated Output**: {output_kwh:.2f} kWh/year")
        st.write(f"💰 **Annual Savings**: ₹{savings:.2f}")
        st.write(f"🛠️ **Installation Cost**: ₹{cost:.2f}")
        st.write(f"📉 **Payback Period**: {payback:.1f} years")

