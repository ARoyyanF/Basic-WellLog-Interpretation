import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def boxplot(data, columns_to_plot, columns_unit):
    # Define the list of columns you want to create subplots for
    columns = (
        columns_to_plot  # ["GR", "CALI", "SP", "DR", "MR", "SR", "NPHI", "RHOB", "DT"]
    )
    units = columns_unit  # ["in", "API", "mV", "ohm/m", "ohm.m", "ohm.m", "v/v", "g/cm³", "us/ft"]

    # Get unique wells and assign colors
    wells = data["WELL"].unique()
    colors = sns.color_palette("viridis", n_colors=len(wells))

    # Set the figure size for the overall plot
    plt.figure(figsize=(16, 12))

    # Create subplots for each selected column
    for i, column in enumerate(columns, 1):
        plt.subplot(3, 3, i)  # Create a 3x3 grid of subplots

        # Plot boxplots for each well with different colors
        for well, color in zip(wells, colors):
            well_data = data[data["WELL"] == well]
            sns.boxplot(x=well_data[column], y=data["WELL"], color=color)

        plt.title(f"Boxplot for {column}", fontsize=12)  # Set the title for the subplot
        plt.xlabel(
            f"{column} [{units[i-1]}]", fontsize=10
        )  # Set the x-axis label with the corresponding unit
        plt.ylabel("Frequency", fontsize=10)  # Set the y-axis label as 'Frequency'

    # Add an overall title for the set of subplots
    plt.suptitle("DATA DISTRIBUTION (BOX PLOT)\n", fontsize=16, fontweight="bold")

    # Create a custom legend outside the subplots
    legend_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=well,
            markerfacecolor=color,
            markersize=10,
        )
        for well, color in zip(wells, colors)
    ]
    plt.legend(
        handles=legend_handles, title="WELL", bbox_to_anchor=(1.05, 1), loc="upper left"
    )

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()


def histplot(
    data,
    columns_to_plot,
    columns_unit,
    depth_start,
    depth_end,
    axes=(3, 3),
    fig_size=(12, 12),
):
    # Get unique wells and assign colors
    wells = data["WELL"].unique()
    colors = sns.color_palette("viridis", n_colors=len(wells))

    # Create subplots for histograms
    fig, axes = plt.subplots(axes[0], axes[1], figsize=fig_size)
    fig.suptitle(
        f"DATA DISTRIBUTION (HISTOGRAM PLOT) from {depth_start}ft to {depth_end}ft \n",
        fontsize=14,
        fontweight="bold",
    )
    fig.subplots_adjust(top=0.95, wspace=0.3, hspace=0.3)

    # List of columns and their corresponding units
    columns = columns_to_plot
    units = columns_unit

    for i, ax in enumerate(axes.flat):
        if i < len(columns):
            column_name = columns[i]
            column_unit = units[i]  # Specify the unit for the column
            ax.set_title(column_name)

            # Plot histograms for each well with different colors
            for well, color in zip(wells, colors):
                well_data = data[
                    (data["WELL"] == well)
                    & (data["DEPT"] >= depth_start)
                    & (data["DEPT"] <= depth_end)
                ]
                sns.histplot(
                    well_data[column_name].dropna(),
                    bins=50,
                    color=color,
                    ax=ax,
                    kde=True,
                    label=well,
                )

            ax.set_xlabel(
                f"{column_name} [{column_unit}]"
            )  # Include the specified unit in the x-axis label
            ax.legend(title="WELL")

    # Remove empty subplots if there are more plots than columns
    if len(columns) < len(axes.flat):
        for i in range(len(columns), len(axes.flat)):
            fig.delaxes(axes.flat[i])

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()


def densityplot(data, columns_to_plot, columns_unit):
    wells = data["WELL"].unique()
    colors = sns.color_palette("viridis", n_colors=len(wells))  # Add this line

    # Group the data by 'WELL' and create subplots
    fig, axes = plt.subplots(3, 3, figsize=(12, 10))
    fig.suptitle("DATA DISTRIBUTION (DENSITY PLOT)\n", fontsize=16)
    fig.subplots_adjust(top=0.95, wspace=0.3, hspace=0.3)

    # List of columns and their corresponding units
    columns = columns_to_plot
    units = columns_unit

    for i, ax in enumerate(axes.flat):
        if i < len(columns):
            column_name = columns[i]
            column_unit = units[i]  # Specify the unit for the column
            ax.set_title(column_name)

            # Plot density plots for each well with different colors
            for well, color in zip(wells, colors):
                well_data = data[data["WELL"] == well]
                well_data[column_name].plot(kind="kde", ax=ax, label=well, color=color)

            ax.set_xlabel(
                f"{column_name} [{column_unit}]"
            )  # Include the specified unit in the x-axis label
            ax.set_ylabel("Frequency")
            ax.legend(title="WELL")

    # Remove any remaining empty subplots
    if len(columns) < len(axes.flat):
        for i in range(len(columns), len(axes.flat)):
            fig.delaxes(axes.flat[i])

    plt.tight_layout()
    plt.show()


def crossplot(logs, x, y, c, x_label, y_label, c_label):
    def scatter_hist(
        x,
        y,
        c,
        ax,
        ax_histx,
        ax_histy,
        ax_cbar,
        x_name,
        y_name,
        c_name,
        x_label,
        y_label,
        c_label,
    ):
        ax_histx.tick_params(axis="x")
        ax_histy.tick_params(axis="y")

        # Remove NaN values from the data
        valid_data_mask = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(c)
        x = x[valid_data_mask]
        y = y[valid_data_mask]
        c = c[valid_data_mask]

        points = ax.scatter(
            x, y, c=c, s=50, cmap="viridis", alpha=0.8, edgecolors="none"
        )
        cbar = plt.colorbar(points, cax=ax_cbar)

        bins = 100

        # Create a histogram for x and set the color based on values in column C
        hist_x, edges_x = np.histogram(x, bins=bins)

        # Create a colormap for gradient colors based on column C
        norm_x = plt.Normalize(c.min(), c.max())
        cmap_x = plt.get_cmap("viridis")

        for i in range(len(edges_x) - 1):
            mask = (x >= edges_x[i]) & (x < edges_x[i + 1])
            ax_histx.bar(
                [edges_x[i]],
                [np.sum(mask)],
                width=np.diff(edges_x)[i],
                color=cmap_x(norm_x(c[mask])),
            )

        # Create a histogram for y and set the color based on values in column C
        hist_y, edges_y = np.histogram(y, bins=bins)

        # Create a colormap for gradient colors based on column C
        norm_y = plt.Normalize(c.min(), c.max())
        cmap_y = plt.get_cmap("viridis")

        for i in range(len(edges_y) - 1):
            mask = (y >= edges_y[i]) & (y < edges_y[i + 1])
            ax_histy.barh(
                [edges_y[i]],
                [np.sum(mask)],
                height=np.diff(edges_y)[i],
                color=cmap_y(norm_y(c[mask])),
            )

        ax.invert_yaxis()
        ax_histy.invert_yaxis()

        ax.set_xlabel(f"{x_name} [{x_label}]")
        ax.set_ylabel(f"{y_name} [{y_label}]")

        ax_histx.set_xlabel(f"{x_name} [{x_label}]")
        ax_histx.set_ylabel(f"{c_name} [{c_label}]")
        ax_histx.set_yticks([])

        ax_histy.set_ylabel(f"{y_name} [{y_label}]")
        ax_histy.set_xlabel(f"{c_name} [{c_label}]")
        ax_histy.set_xticks([])

        ax_cbar.set_title(f"{c_name} [{c_label}]", fontsize=10)

    fig = plt.figure(figsize=(10, 10))
    fig.suptitle(f"{x} - {y} Crossplot".upper(), fontsize=14, fontweight="bold")
    fig.subplots_adjust(top=0.95, wspace=0.01, hspace=0.01)

    gs = fig.add_gridspec(2, 3, width_ratios=(0.1, 9, 0.9), height_ratios=(1, 9))

    # Create the axes
    ax = fig.add_subplot(gs[1, 1])
    ax_histx = fig.add_subplot(gs[0, 1], xticklabels=[])
    ax_histy = fig.add_subplot(gs[1, 2], yticklabels=[])
    ax_cbar = fig.add_subplot(gs[1, 0])

    # Replace 'logs.NPHI' and 'logs.RHOB' with 'x' and 'y' as you pass these as function arguments
    scatter_hist(
        logs[x],
        logs[y],
        logs[c],
        ax,
        ax_histx,
        ax_histy,
        ax_cbar,
        x,
        y,
        c,
        x_label,
        y_label,
        c_label,
    )

    # Finally, show the plot
    plt.tight_layout()
    plt.show()
