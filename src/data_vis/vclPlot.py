import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from .helperFunc import nd_crossplot


def vcl_plot(
    data,
    depth_start,
    depth_end,
    traject1: dict,
    traject2: dict,
    traject3: dict,
    clean_point1=[1, 1],
    clean_point2=[1, 1],
    clay_point=[1, 1],
    rhob_axis=[1.5, 2.8],
    nphi_axis=[0, 1],
):
    """
    Plot volume of clay from different methods with handling for missing data

    Parameters:
    -----------
    logs : pandas DataFrame
        Well log data containing depth and measurement curves
    depth_start, depth_end : float
        Depth range for plotting
    *_clean, *_clay : float, optional
        Clean and clay points for different methods
    """
    # filter the well depths:
    well_data = data[(data["DEPT"] >= depth_start) & (data["DEPT"] <= depth_end)]

    # Create figure and gridspec
    fig = plt.figure(figsize=(12, 10))
    fig.suptitle("Volume of clay from different methods", fontsize=14)
    fig.subplots_adjust(top=0.90, wspace=0.3, hspace=0.3)

    gs = gridspec.GridSpec(3, 3)

    # Initialize subplots
    ax1 = fig.add_subplot(gs[:, 0])  # All rows, column 1
    ax2 = fig.add_subplot(gs[0, 1])  # Row 1, column 2a
    ax3 = fig.add_subplot(gs[1, 1])  # Row 2, column 2b
    ax4 = fig.add_subplot(gs[2, 1])  # Row 3, column 2c
    ax5 = fig.add_subplot(gs[:, 2])  # Row all rows, column 3

    # Plot GR and SP (if available)
    ax1.set_ylim(depth_start, depth_end)
    ax1.invert_yaxis()
    ax1.set_ylabel("DEPTH")
    for i in range(len(traject1["data"])):
        ax1.plot(
            well_data[traject1["data"][i]], well_data.DEPT, color=traject1["colors"][i]
        )
        ax1.set_xlabel(traject1["labels"][i], color=traject1["colors"][i])
        ax1.set_xlim(traject1["intervals"][i])
        ax1.set_xscale(traject1["scales"][i])
        if i < len(traject1["data"]) - 1:
            ax1 = ax1.twiny()
    ax1.grid(True)

    # Histograms
    axes2 = [ax2, ax3]
    curves_to_plot = {}
    for i in range(len(traject2["data"])):
        curves_to_plot[traject2["data"][i]] = (
            traject2["colors"][i],
            axes2[i],
            traject2["scales"][i],
            traject2["labels"][i],
        )
    for curve, (color, ax, scale, xlabel) in curves_to_plot.items():
        ax.hist(well_data[curve].dropna(), bins=15, color=color)
        ax.set_xscale(scale)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Frequency")

    # N-D Crossplot (if both NPHI and RHOB are available)
    nd_crossplot(
        well_data, ax4, clean_point1, clean_point2, clay_point, nphi_axis, rhob_axis
    )

    # Plot VCL values
    ax5.set_ylim(depth_start, depth_end)
    ax5.invert_yaxis()
    ax5.grid(True)
    vcl_curves = {}
    for i in range(len(traject3["data"])):
        vcl_curves[traject3["data"][i]] = (traject3["labels"][i], traject3["colors"][i])
    for curve, (label, color) in vcl_curves.items():
        ax5.plot(well_data[curve], well_data.DEPT, label=label, color=color)

    ax5.set_xlim(0, 1)
    ax5.set_xlabel("VCL [v.v]")
    ax5.legend(loc="best", fontsize="x-small")

    return fig
