import matplotlib.pyplot as plt


def add_trajectory(ax, data, traject, use_xticks=False):
    for i in range(len(traject["data"])):
        twin_ax = ax.twiny()
        if use_xticks:
            twin_ax.set_xticks(
                range(
                    traject["intervals"][i][0],
                    traject["intervals"][i][1],
                    traject["intervals"][i][2],
                )
            )
        else:
            twin_ax.set_xlim(traject["intervals"][i])
        twin_ax.set_xscale(traject["scales"][i])
        twin_ax.set_xlabel(traject["labels"][i], color=traject["colors"][i])
        if "positions" in traject:
            twin_ax.spines["top"].set_position(("outward", traject["positions"][i]))
        twin_ax.plot(
            data[traject["data"][i]],
            data.DEPT,
            label=traject["labels"][i],
            color=traject["colors"][i],
        )
        if "positions" in traject:
            twin_ax.tick_params(axis="x", colors=traject["colors"][i])


def nd_crossplot(
    data, ax, clean_point1, clean_point2, clay_point, nphi_axis, rhob_axis, fontsize=6
):
    if all(curve in data.columns for curve in ["NPHI", "RHOB"]):
        points = ax.scatter(
            data.NPHI_corr,
            data.RHOB,
            c=data.GR if "GR" in data.columns else "blue",
            s=fontsize,
            cmap="viridis",
        )
        cbar = plt.colorbar(points)
        cbar.set_label("GR [API]", rotation=90, size=fontsize)
        ax.set_xlabel("NPHI [%]")
        ax.set_ylabel("RHOB [g/cc]")
        ax.invert_yaxis()
        ax.invert_xaxis()
        ax.grid(True)

        # Add axis limits (set constraints here)
        ax.set_xlim(nphi_axis)  # Example for NPHI, adjust based on your data
        ax.set_ylim(rhob_axis)

        # Plot clean and clay points if provided
        if all(
            clean_point is not None
            for clean_point in [
                clean_point1[0],
                clean_point1[1],
                clean_point2[0],
                clean_point2[1],
            ]
        ):
            ax.plot(
                [clean_point1[0], clean_point2[0]],
                [clean_point1[1], clean_point2[1]],
                marker="o",
                color="black",
                linewidth=1,
            )
            ax.text(
                clean_point1[0],
                clean_point1[1],
                "clean point 1",
                fontsize=fontsize,
                bbox=dict(boxstyle="round", fc="white", ec="0.5", alpha=0.8),
            )
            ax.text(
                clean_point2[0],
                clean_point2[1],
                "clean point 2",
                fontsize=fontsize,
                bbox=dict(boxstyle="round", fc="white", ec="0.5", alpha=0.8),
            )

        if clay_point[0] is not None and clay_point[1] is not None:
            ax.plot(clay_point[0], clay_point[1], marker="o", color="red", linewidth=1)
            ax.text(
                clay_point[0],
                clay_point[1],
                "clay point",
                fontsize=fontsize,
                bbox=dict(boxstyle="round", fc="white", ec="0.5", alpha=0.8),
            )
