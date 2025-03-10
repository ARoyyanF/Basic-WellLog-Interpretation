import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .helperFunc import add_trajectory


# Create the figure and subplots
def combo_plot(
    data,
    top_depth: float,
    bottom_depth: float,
    formations,
    formation_depths,
    figure_height: float,
    suptitleadjust: float,
    traject1: dict,
    traject2: dict,
    traject3: dict,
    ticks_interval="auto",
    with_title=True,
):

    selected_data = data[(data.DEPT >= top_depth) & (data.DEPT <= bottom_depth)]
    fig, ax = plt.subplots(
        nrows=1, ncols=3, figsize=(12, figure_height), sharey=True
    )  # pembuatan format 1 baris 3 kolom, width 12 height 10, dan sumbu y yang sama (sharey)

    if with_title:
        fig.suptitle(
            f"WELL COMPOSITE {top_depth}ft to {bottom_depth}ft".upper(),
            y=suptitleadjust,
            va="bottom",
        )
    fig.subplots_adjust(wspace=0.1)

    # General setting for all axis
    for axes in ax:
        axes.set_ylim(top_depth, bottom_depth)
        axes.invert_yaxis()
        axes.yaxis.grid(True)
        axes.yaxis.grid(True, which="minor", linestyle=":")
        axes.yaxis.grid(True, which="major", linestyle="-", linewidth="1")
        for i, j in zip(formation_depths, formations):
            if (i >= top_depth) and (i <= bottom_depth):
                axes.axhline(y=i, linewidth=0.5, color="black")
                axes.text(
                    0.1, i, j, horizontalalignment="center", verticalalignment="center"
                )

        if ticks_interval == "auto":
            axes.yaxis.set_major_locator(ticker.AutoLocator())
            axes.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        else:
            axes.yaxis.set_major_locator(ticker.MultipleLocator(ticks_interval[0]))
            axes.yaxis.set_minor_locator(ticker.MultipleLocator(ticks_interval[1]))

        axes.get_xaxis().set_visible(False)

    # 1st Trajectory: typically for GR, CALI, SP
    add_trajectory(ax[0], selected_data, traject1)

    # 2nd Trajectory: typically for Resistivity
    if traject2:
        add_trajectory(ax[1], selected_data, traject2)

    # 3rd Trajectory: typically for NPHI, RHOB, etc
    if traject3:
        add_trajectory(ax[2], selected_data, traject3)

    plt.show()

    return fig


def custom_plot(
    data,
    depth_start,
    depth_end,
    custom_data,
    units,
    res_range=[0.1, 10],
    res_scale="log",
):
    selected_data = data[(data.DEPT >= depth_start) & (data.DEPT <= depth_end)]
    num_tracks = len(custom_data)
    fig, ax = plt.subplots(nrows=1, ncols=num_tracks, figsize=(15, 10), sharey=True)
    fig.suptitle("Custom Interpretation Plot", fontsize=22)

    # Calculate top value with less free space based on the number of tracks
    top_value = 1 - 0.015 * 7

    # Adjust top parameter to leave less free space at the top
    fig.subplots_adjust(top=top_value, wspace=0.2)

    units = units  # in list

    # General setting for all axes
    for axes in ax:
        axes.set_ylim(depth_start, depth_end)
        axes.invert_yaxis()
        axes.yaxis.grid(True, which="minor", linestyle=":")
        axes.yaxis.grid(True, which="major", linestyle="-", linewidth="1")
        axes.yaxis.set_major_locator(ticker.AutoLocator())
        axes.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        axes.get_xaxis().set_visible(False)

    # Customizing each track with unit and color
    for i, data_name in enumerate(custom_data):
        current_ax = ax[i].twiny()
        current_ax.plot(
            selected_data[data_name],
            selected_data.DEPT,
            label=f"{data_name} [{units[i]}]",
            color="C" + str(i),
        )
        if data_name == "DR" or data_name == "MR" or data_name == "SR":
            current_ax.set_xlim(res_range)
            current_ax.set_xscale(res_scale)
        elif data_name == "RW":
            current_ax.set_xlim(0.01, 1)
            current_ax.set_xscale("log")
        current_ax.set_xlabel(f"{data_name} [{units[i]}]", color="C" + str(i))
        current_ax.tick_params(axis="x", colors="C" + str(i))
        current_ax.spines["top"].set_position(("outward", 0))
        current_ax.legend(
            loc="lower right", facecolor="white", framealpha=1, fontsize=7
        )
    plt.show()

    return fig
