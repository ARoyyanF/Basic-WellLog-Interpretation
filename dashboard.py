# local module
from numpy import integer
from src.Components.vclDashboard import vcl_dashboard
from src.Components.Pages.wellComposite import well_composite

# external libraries
import streamlit as st
import pandas as pd
import os

current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_path, "results/main.csv")

st.title("Log Interpretation Dashboard")
upload_file = st.file_uploader("Choose csv LAS files")

curve_options = [
    "GR",
    "CALI",
    "SP",
    "SR",
    "MR",
    "DR",
    "DT",
    "RHOB",
    "NPHI",
    "NPHI_corr",
]

scale_options = ["linear", "log", "symlog", "logit", "function"]
color_options = [
    "#FFD700",  # Gold (Lithology shading)
    "#90EE90",  # LightGreen (Lithology fill)
    "#006400",  # DarkGreen (Permeability indicator)
    "#FFB6C1",  # LightPink (Resistivity background)
    "#DC143C",  # Crimson (Resistivity curve)
    "#87CEEB",  # SkyBlue (Pore space)
    "#4682B4",  # SteelBlue (Pore space data points)
    "#FFA500",  # Orange (SP curve)
    "#800080",  # Purple (Water saturation curves)
    "#A52A2A",  # Brown (Shale indicator)
    "#D8BFD8",  # Thistle (Background shading)
]
if upload_file:
    well_data = pd.read_csv(upload_file)
    min_depth = well_data.DEPT.min()
    max_depth = well_data.DEPT.max()

    with st.sidebar:
        st.title("Control Panel")

        depth1, depth2 = st.columns(2)
        with depth1:
            depth_start = st.number_input(label="Start Depth")
        with depth2:
            depth_end = st.number_input(label="End Depth")
        depths = [depth_start, depth_end]
        st.write(f"Depth range: {depths[0]} ft to {depths[1]} ft")

    # create columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Depth Start", value=f"{depth_start} ft")

    with col2:
        st.metric(label="Depth End", value=f"{depth_end} ft")

    def page1():
        well_composite(well_data, depths)

    def page2():
        with st.sidebar:
            rhob_values = st.slider(
                label="Select Depth Range",
                min_value=0,
                max_value=3,
                value=(0, 3),
            )
        st.write(f"Rhob range: {rhob_values[0]} to {rhob_values[1]}")

        vcl_dashboard(well_data, depths, rhob_values)

    def page3():
        st.title("Hello World")

    def page4():
        st.title("Hello World")

    def page0():
        st.title("Hello World")

    pg = st.navigation(
        [
            st.Page(page0, title="Main Page"),
            st.Page(page1, title="Well Composites"),
            st.Page(page2, title="VCL Plot"),
            st.Page(page3, title="Porosity"),
            st.Page(page4, title="Water Saturation"),
        ]
    )
    pg.run()
