import streamlit as st
from ..Visualization.vclPlot import vcl_plot
from ..Equations.vclCalc import vclgr, vclnd, vclrt


def vcl_dashboard(well_data, values, rhob_values):
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
    fig = vcl_plot(
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
        clean_point1=[neut_clean1, den_clean1],
        clean_point2=[neut_clean2, den_clean2],
        clay_point=[neut_clay, den_clay],
        nphi_axis=[0, 1],
        rhob_axis=[rhob_values[1], rhob_values[0]],
    )

    st.pyplot(fig)
