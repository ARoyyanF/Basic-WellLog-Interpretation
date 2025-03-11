# local module
from .options import curve_options, color_options, scale_options
from ..comboDashboard import combo_dashboard

import streamlit as st


def well_composite(well_data, depths):
    tracks = ["Track 1", "Track 2", "Track 3"]
    trajectory1 = {}
    trajectory2 = {}
    trajectory3 = {}
    trajectories = [trajectory1, trajectory2, trajectory3]

    with st.sidebar:
        for i in range(len(trajectories)):
            st.subheader(tracks[i])
            selected_curves = st.multiselect(
                label="curve", options=curve_options, key=f"curves_{i}"
            )
            trajectories[i]["data"] = selected_curves

            trajectories[i]["intervals"] = []
            trajectories[i]["scales"] = []
            for j, selected_curve in enumerate(selected_curves):
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    min_interval = st.number_input(label=f"Min {selected_curve}")
                with col2:
                    max_interval = st.number_input(label=f"Max {selected_curve}")
                with col3:
                    scales = st.selectbox(
                        label="scales", options=scale_options, key=f"scales_{i}_{j}"
                    )
                trajectories[i]["intervals"].append([min_interval, max_interval])
                trajectories[i]["scales"].append(scales)

            selected_labels = st.multiselect(
                label="label", options=curve_options, key=f"labels_{i}"
            )
            trajectories[i]["labels"] = selected_labels

            selected_positions = st.multiselect(
                label="Pos", options=[0, 40, 80], key=f"positions_{i}"
            )
            trajectories[i]["positions"] = selected_positions

            selected_colors = st.multiselect(
                label="color", options=color_options, key=f"colors_{i}"
            )
            trajectories[i]["colors"] = selected_colors

    tab1, tab2 = st.tabs(["Well Composites", "Custom Plot"])
    with tab1:
        combo_dashboard(well_data, depths, trajectory1, trajectory2, trajectory3)
    with tab2:
        st.write("hehe")
