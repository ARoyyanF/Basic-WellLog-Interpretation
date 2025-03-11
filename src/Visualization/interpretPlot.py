import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from .helperFunc import add_trajectory
import pandas as pd
import altair as alt


def interpretation_plot(
    data,
    depth_start,
    depth_end,
    traject1: dict,
    traject2: dict,
    traject3: dict,
    traject4: dict,
    traject5: dict,
    traject6: dict,
    traject7: dict,
    fill=True,
):
    # filter the data
    data = data[(data.DEPT >= depth_start) & (data.DEPT <= depth_end)]

    fig, ax = plt.subplots(nrows=1, ncols=7, figsize=(12, 12), sharey=True)
    fig.suptitle("Interpretation Plot", fontsize=22)
    fig.subplots_adjust(top=0.85, wspace=0.4)

    # General setting for all axis
    for axes in ax:
        axes.set_ylim(depth_start, depth_end)
        axes.invert_yaxis()
        axes.yaxis.grid(True, which="minor", linestyle=":")
        axes.yaxis.grid(True, which="major", linestyle="-", linewidth="1")
        axes.yaxis.set_major_locator(ticker.AutoLocator())
        axes.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        axes.get_xaxis().set_visible(False)

    # 1st track: GR, SP, CALI track
    add_trajectory(ax[0], data, traject1)

    # 2nd track
    add_trajectory(ax[1], data, traject2)

    # 3rd track
    add_trajectory(ax[2], data, traject3)

    # 4th track
    add_trajectory(ax[3], data, traject4)

    # 5th track
    add_trajectory(ax[4], data, traject5)

    # 6th track
    add_trajectory(ax[5], data, traject6)

    # 7th track
    add_trajectory(ax[6], data, traject7)

    if fill:
        # BVW porosity fill plot
        ax[5].fill_betweenx(data.DEPT, 0, data.BVW, color="lightblue")
        ax[5].fill_betweenx(data.DEPT, data.PHIE, data.BVW, color="red")

        # Porosity vcl fill options
        ax[6].fill_betweenx(
            data.DEPT, 0, data.PHIE, color="lightgray", label="porosity"
        )
        ax[6].fill_betweenx(
            data.DEPT, data.PHIE, 1 - data.VCL, color="orange", label="matrix"
        )
        ax[6].fill_betweenx(
            data.DEPT, 1 - data.VCL, 1, color="lightgreen", label="Vclay"
        )
        ax[6].legend(loc="lower left")


# def pickett_plot(data, depth_start, depth_end, vcl_limit, a, rwa, m, n, z):
#     plt.figure(figsize=(7, 6))
#     plt.title("Pickett Plot" + "%" + " and Rw = " + str(rwa) + " ohm.m")
#     c = data[z][
#         (data.DEPT >= depth_start) & (data.DEPT <= depth_end) & (data.VCL < vcl_limit)
#     ]
#     plt.scatter(
#         data.DR[
#             (data.DEPT >= depth_start)
#             & (data.DEPT <= depth_end)
#             & (data.VCL < vcl_limit)
#         ],
#         data.PHIE[
#             (data.DEPT >= depth_start)
#             & (data.DEPT <= depth_end)
#             & (data.VCL < vcl_limit)
#         ],
#         c=c,
#         s=20,
#         cmap="plasma",
#     )
#     cbar = plt.colorbar()
#     cbar.set_label(f"{z}")
#     plt.xlim(0.1, 1000)
#     plt.ylim(0.01, 1)
#     plt.ylabel("PHIE [v/v]")
#     plt.xlabel("DR [m.ohm]")
#     plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
#     plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
#     plt.gca().set_xscale("log")
#     plt.gca().set_yscale("log")

#     # calculate the saturation lines
#     sw_plot = (1.0, 0.8, 0.6, 0.4, 0.2)
#     phie_plot = (0.01, 1)
#     rt_plot = np.zeros((len(sw_plot), len(phie_plot)))

#     for i in range(0, len(sw_plot)):
#         for j in range(0, len(phie_plot)):
#             rt_result = (a * rwa) / (sw_plot[i] ** n) / (phie_plot[j] ** m)
#             rt_plot[i, j] = rt_result
#     for i in range(0, len(sw_plot)):
#         plt.plot(rt_plot[i], phie_plot, label="SW " + str(int(sw_plot[i] * 100)) + "%")
#         plt.legend(loc="best")

#     plt.grid(True, which="both", ls="-", color="gray")

def pickett_plot(logs, depth_start, depth_end, x_range, y_range, vcl_limit, a, rwa, m, n, z):
    """
    Creates a Pickett Plot using Altair with tooltips and saturation lines.

    Args:
        logs (pd.DataFrame): DataFrame containing log data (DEPT, DR, PHIE, VCL, z).
        depth_start (float): Starting depth.
        depth_end (float): Ending depth.
        x_range (list): x axis plot range
        y_range (list): y axis plot range
        vcl_limit (float): Volume of clay limit.
        a (float): Tortuosity factor.
        rwa (float): Water resistivity.
        m (float): Cementation exponent.
        n (float): Saturation exponent.
        z (str): Column name for color encoding (e.g., 'VSH').

    Returns:
        alt.Chart: Altair chart object.
    """

    filtered_logs = logs[(logs.DEPT >= depth_start) & (logs.DEPT <= depth_end) & (logs.VCL < vcl_limit)].copy()

    scatter = alt.Chart(filtered_logs).mark_circle(size=60).encode(
        x=alt.X('DR:Q', scale=alt.Scale(type='log', domain=x_range), title='DR [m.ohm]'),
        y=alt.Y('PHIE:Q', scale=alt.Scale(type='log', domain=y_range), title='PHIE [v/v]'),
        color=alt.Color(f'{z}:Q', scale=alt.Scale(scheme='plasma'), title=z),
        tooltip=['DEPT', 'DR', 'PHIE', z]
    ).properties(
        title=f'Pickett Plot and Rw = {rwa} ohm.m',
        width=400,
        height=400  # Increase height
    )

    sw_plot = (1.0, 0.8, 0.6, 0.4, 0.2)
    phie_plot = (0.01, 1)
    rt_plot = {}

    for sw in sw_plot:
        rt_values = []
        for phie in phie_plot:
            rt_result = (a * rwa) / (sw ** n) / (phie ** m)
            rt_values.append(rt_result)
        rt_plot[f'SW {int(sw * 100)}%'] = rt_values

    lines = []
    for i, (label, rt_values) in enumerate(rt_plot.items()):
        line_data = pd.DataFrame({'DR': rt_values, 'PHIE': phie_plot, 'SW': label})
        line = alt.Chart(line_data).mark_line(opacity=0.4).encode(
            x='DR:Q',
            y='PHIE:Q',
            color=alt.value('grey'),
            strokeDash=alt.value([5, 5])
        ).transform_calculate(
            SW_label = f"'{label}'"
        ).properties(
            title = f"{label}"
        )
        dy_offset = -10 *(1 if i % 2 != 0 else -1) - 25 #adjust dy based on index
        text = alt.Chart(line_data.iloc[[0]]).mark_text(
            align='left',
            baseline='middle',
            dx=-20,
            dy = dy_offset
        ).encode(
            x='DR:Q',
            y='PHIE:Q',
            text = alt.value(label),
            color = alt.value("green")
        )

        lines.append(line + text)

    combined_lines = alt.layer(*lines)

    return scatter + combined_lines