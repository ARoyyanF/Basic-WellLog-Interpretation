import streamlit as st
from ..Visualization.comboPlot import combo_plot


def combo_dashboard(well_data, values, tracks1, tracks2, tracks3):
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
        traject1=tracks1,
        traject2=tracks2,
        traject3=tracks3,
        # ticks_interval=[50, 10],
        with_title=False,
    )

    st.pyplot(fig)
