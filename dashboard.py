# local module
from src.data_vis.comboPlot import combo_plot
from src.data_vis.vclPlot import vcl_plot
from src.data_calc.vclCalc import vclgr, vclnd, vclrt

# external libraries
import streamlit as st
import pandas as pd
import os

current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_path, "results/main.csv")

upload_file = st.file_uploader("Choose csv LAS files")


if upload_file:
    well_data = pd.read_csv(upload_file)
    min_depth = well_data.DEPT.min()
    max_depth = well_data.DEPT.max()
    with st.sidebar:
        st.text("sidebar")
        values = st.slider(
            label="Select Depth Range",
            min_value=min_depth,
            max_value=max_depth,
            value=(min_depth, max_depth),
        )
        st.write(f"Depth range: {values[0]} ft to {values[1]} ft")

        rhob_values = st.slider(
            label="Select Depth Range",
            min_value=0,
            max_value=3,
            value=(0, 3),
        )
        st.write(f"Rhob range: {rhob_values[0]} to {rhob_values[1]}")

    formations = (
        "Parigi",
        "Parigi 2nd",
        "Parigi 3rd",
        "Parigi 4th",
        "Preparigi",
        "Baturaja Onlap",
        "Baturaja Massive",
        "Deltaic TAF Top",
    )
    formation_depths = (2200, 2700, 2871, 2957, 3052, 7529, 7554, 9049)
    fig = combo_plot(
        well_data,
        values[0],
        values[1],
        formations,
        formation_depths,
        12,  # figure height in inch
        1.03,  # title position
        traject1={
            "data": ["GR", "CALI"],
            "intervals": [(0, 100), (0, 20)],
            "scales": ["linear", "linear"],
            "labels": ["GR [API]", "CALI [in]"],
            "positions": [0, 40],
            "colors": ["green", "orange"],
        },
        traject2={
            "data": ["SR", "DR"],
            "intervals": [(0, 2), (0, 2)],
            "scales": ["linear", "linear"],
            "labels": ["SR [OHM.M]", "DR [OHM.M]"],
            "positions": [0, 40],
            "colors": ["purple", "black"],
        },
        traject3={
            "data": ["NPHI", "NPHI_corr", "RHOB"],
            "intervals": [(1.0, -0.2), (1.0, -0.2), (0, 2.75)],
            "scales": ["linear", "linear", "linear"],
            "labels": ["NPHI [unknown]", "NPHI_corr", "RHOB [g/cc]"],
            "positions": [0, 40, 80],
            "colors": ["red", "brown", "blue"],
        },
        # ticks_interval=[50, 10],
        with_title=False,
    )

    # Clean point 1 (typical for a dense, clean rock like limestone)
    neut_clean1 = 0.1
    den_clean1 = 2.65

    # Clean point 2 (moderate porosity, consolidated formation)
    neut_clean2 = 0.35
    den_clean2 = 2.15

    # Clay point (high density, low porosity)
    neut_clay = 0.42
    den_clay = 2.57

    # sand and shale baseline
    gr_clean = 35
    gr_clay = 85
    rt_clean = 2
    rt_clay = 0.7

    well_data["VCLGR"] = vclgr(well_data.GR, gr_clean, gr_clay, correction="older")
    well_data["VCLRT"] = vclrt(well_data.DR, rt_clean, rt_clay)
    well_data["VCLND"] = vclnd(
        well_data.NPHI,
        well_data.RHOB,
        neut_clean1,
        den_clean1,
        neut_clean2,
        den_clean2,
        neut_clay,
        den_clay,
    )
    fig2 = vcl_plot(
        well_data,
        values[0],
        values[1],
        traject1={
            "data": ["GR", "DR"],
            "intervals": [(0, 100), (0, 2)],
            "scales": ["linear", "linear"],
            "labels": ["GR [API]", "DR [OHM.M]"],
            "colors": ["green", "purple"],
        },
        traject2={
            "data": ["GR", "DR"],
            "scales": ["linear", "linear"],
            "labels": ["GR [API]", "DR [OHM.M]"],
            "colors": ["green", "purple"],
        },
        traject3={
            "data": ["VCLGR", "VCLRT", "VCLND"],
            "labels": ["VCLGR [v/v]", "VCLRT [v/v]", "VCLND [v/v]"],
            "colors": ["green", "red", "blue"],
        },
        nphi_axis=[0, 1],
        rhob_axis=[rhob_values[1], rhob_values[0]],
    )

    (
        col1,
        col2,
    ) = st.columns(2)
    with col1:
        st.metric(label="Depth Start", value=f"{values[0]} ft")

    with col2:
        st.metric(label="Depth End", value=f"{values[1]} ft")

    tabs1, tabs2 = st.tabs(["Well Composite", "VCL plot"])

    with tabs1:
        st.pyplot(fig)

    with tabs2:
        st.pyplot(fig2)
