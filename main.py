import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate


common_label_font_size = 16
common_legend_font_size = 12
common_annotation_font_size = 14


def lbft_to_Nm(val):
    return 1.3558179483 * val


def inv_hp_to_inv_kW(val):
    return 1.3596216173 * val


def plot_torque_curve():
    torque_curve = pd.read_csv(r"./data/C9TorqueCurve.csv",
                               sep=r'\s*,\s*', header=0, encoding='ascii',
                               engine='python')
    speed = torque_curve['Speed']
    torques_ftlb = torque_curve['Torque']
    torques_nm = 1.3558179483 * torques_ftlb

    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')

    torque_graph = sns.lineplot(x=speed, y=torques_nm, alpha=0, ax=ax)
    torque_graph.set_xlabel("Speed (rpm)", fontsize=common_label_font_size)
    torque_graph.set_ylabel("Torque (Nm)", fontsize=common_label_font_size)

    # Get the two lines from the axes to generate shading
    l1 = torque_graph.lines[0]
    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]
    torque_graph.fill_between(x1, y1, alpha=0.2)

    arrow_widths = 10
    arrow_head_lengths = 75
    arrow_head_widths = 35
    length_includes_head = True
    # Speed
    torque_graph.arrow(x=1200, y=1.3558179483 * 100, dx=0, dy=1.3558179483 * 400, width=arrow_widths,
                       head_width=arrow_head_widths, head_length=arrow_head_lengths,
                       length_includes_head=length_includes_head)
    torque_graph.annotate(text='Load', xy=(1000, 1.3558179483 * 280), fontsize=common_annotation_font_size)
    # Load
    torque_graph.arrow(x=1200, y=1.3558179483 * 500, dx=800, dy=0, width=arrow_widths,head_width=arrow_head_widths,
                       head_length=arrow_head_lengths,
                       length_includes_head=length_includes_head)
    torque_graph.annotate(text='Accel', xy=(1450, 1.3558179483 * 520), fontsize=common_annotation_font_size)
    # Speed and Load
    torque_graph.arrow(x=1200, y=1.3558179483 * 100, dx=800, dy=1.3558179483 * 400, width=arrow_widths,
                       head_width=arrow_head_widths, head_length=arrow_head_lengths,
                       length_includes_head=length_includes_head)
    torque_graph.annotate(text='Accel and Load', xy=(1500, 1.3558179483 * 200), fontsize=common_annotation_font_size)

    plt.ylim(0, 1400)
    plt.xlim(800, 2200)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/torque_curve_and_transients.png")
    plt.show(block=False)


def plot_optimal_vnt_and_egr_strategies_for_speed_transient(style):
    sns.set_style(style)

    speed_transient_egr_pos = pd.read_csv(r"./data/SpeedTransient_EGRPositions.csv",
                                         sep=r'\s*,\s*', header=0, encoding='ascii',
                                         engine='python')
    speed_transient_vnt_pos = pd.read_csv(r"./data/SpeedTransient_VNTPositions.csv",
                                         sep=r'\s*,\s*', header=0, encoding='ascii',
                                         engine='python')
    best_tests = [1, 5, 8, 9, 10]

    fig = plt.figure(figsize=(7.5, 9))
    ax = fig.add_subplot(211)

    for test_number in best_tests:
        sns.lineplot(x=speed_transient_vnt_pos['Time'], y=speed_transient_vnt_pos[str(test_number)]/100, ax=ax,
                     label="Test " + str(test_number))

    ax.legend(fontsize=common_legend_font_size)
    ax.set_xlabel(None)
    ax.set_ylabel("VNT Actuator Position (%)", fontsize=common_label_font_size)
    ax.set_ylim([0.0, 1.0])

    ax = fig.add_subplot(212)

    for test_number in [1, 5, 8, 9, 10]:
        sns.lineplot(x=speed_transient_egr_pos['Time'], y=speed_transient_egr_pos[str(test_number)]/100, ax=ax)

    ax.set_xlabel("Time (s)", fontsize=common_label_font_size)
    ax.set_ylabel("EGR Actuator Position (%)", fontsize=common_label_font_size)
    ax.set_ylim([0.0, 1.0])

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/speed_transient_ad_hoc_positions.png")
    plt.show(block=False)


def plot_optimal_vnt_and_egr_strategies_for_load_transient(style):
    sns.set_style(style)

    transient_egr_pos = pd.read_csv(r"./data/LoadTransient_EGRPositions.csv",
                                    sep=r'\s*,\s*', header=0, encoding='ascii',
                                    engine='python')
    transient_vnt_pos = pd.read_csv(r"./data/LoadTransient_VNTPositions.csv",
                                    sep=r'\s*,\s*', header=0, encoding='ascii',
                                    engine='python')
    best_tests = [1, 5, 8, 9, 10]

    fig = plt.figure(figsize=(7.5, 9))
    ax = fig.add_subplot(211)

    for test_number in best_tests:
        sns.lineplot(x=transient_vnt_pos['Time'], y=transient_vnt_pos[str(test_number)]/100, ax=ax,
                     label="Test " + str(test_number))

    ax.legend(fontsize=common_legend_font_size)
    ax.set_xlabel(None)
    ax.set_ylabel("VNT Actuator Position (%)", fontsize=common_label_font_size)
    ax.set_ylim([0.0, 1.0])

    ax = fig.add_subplot(212)

    for test_number in [1, 5, 8, 9, 10]:
        sns.lineplot(x=transient_egr_pos['Time'], y=transient_egr_pos[str(test_number)]/100, ax=ax)

    ax.set_xlabel("Time (s)", fontsize=common_label_font_size)
    ax.set_ylabel("EGR Actuator Position (%)", fontsize=common_label_font_size)
    ax.set_ylim([0.0, 1.0])

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/load_transient_ad_hoc_positions.png")
    plt.show(block=False)


def plot_optimal_steady_state_vnt_and_egr_set_points_for_load_transient(style):
    sns.set_style(style)
    load_transient_steady_state = pd.read_csv(r"./data/LoadTransient_OptimalSteadyStateSetPoints.csv",
                                              sep=r'\s*,\s*', header=0, engine='python')

    fig, (subplot0, subplot1) = plt.subplots(2, 1, figsize=(7.5, 9))
    line_0 = sns.lineplot(x=1.3558179483 * load_transient_steady_state['Load'],
                          y=load_transient_steady_state["VGT_Position"]/100, color="red",
                          label="VNT Position", ax=subplot0, legend=False)
    line_0.set_ylabel("VNT Actuator Position (%)", fontsize=common_label_font_size)
    line_0.set_ylim([0.0, 1.0])
    line_0.set_xlabel(None)

    ax_01 = line_0.twinx()
    line_1 = sns.lineplot(x=1.3558179483 * load_transient_steady_state['Load'],
                          y=load_transient_steady_state["Boost"], ax=ax_01,
                          label="Boost", legend=False)
    ax_01.set_ylabel("Boost (kPa)", fontsize=common_label_font_size)
    ax_01.set_ylim([0, 50])

    h0, l0 = line_0.get_legend_handles_labels()
    h1, l1 = line_1.get_legend_handles_labels()
    ax_01.legend(h0 + h1, l0 + l1, loc=0, fontsize=common_legend_font_size)

    line_2 = sns.lineplot(x=1.3558179483 * load_transient_steady_state['Load'],
                         y=load_transient_steady_state["EGR_Position"] / 100, ax=subplot1, color="red",
                         label="EGR Position", legend=False)
    subplot1.set_ylabel("EGR Actuator Position (%)", fontsize=common_label_font_size)
    subplot1.set_ylim([0.0, 1.0])
    subplot1.set_xlabel("Load (Nm)", fontsize=common_label_font_size)

    ax_11 = subplot1.twinx()
    line_3 = sns.lineplot(x=1.3558179483 * load_transient_steady_state['Load'],
                 y=load_transient_steady_state["EGR_Mass"] / 100, ax=ax_11,
                 label="EGR", legend=False)
    ax_11.set_ylabel("EGR (% Mass)", fontsize=common_label_font_size)
    ax_11.set_ylim([0.0, 1.0])

    h2, l2 = line_2.get_legend_handles_labels()
    h3, l3 = line_3.get_legend_handles_labels()
    ax_11.legend(h2 + h3, l2 + l3, loc=4, fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/load_transient_steady_state_optimal_positions.png")
    plt.show(block=False)


def plot_speed_load_transient_time_comparison_of_boost_and_egr(style):
    sns.set_style(style)

    transient_times = [2, 4, 6, 8, 10]

    x_start = -2.0
    x_end = 12.0

    speed_load_time_data = []
    for time in transient_times:
        speed_load_time_data.append(pd.read_csv(r"./data/SpeedLoadComparison_" + str(time) +
                                                "SecondTransient_with_BaselineControl.csv",
                                                sep=r'\s*,\s*', header=0, engine='python'))

    fig, (subplot0, subplot1) = plt.subplots(2, 1, figsize=(7.5, 9))

    for idx in range(len(transient_times)):
        sns.lineplot(x=speed_load_time_data[idx]['TimeToEvent'], y=speed_load_time_data[idx]["Boost (kPa)"],
                     label=str(transient_times[idx]) + "s", ax=subplot0, legend=False)
    subplot0.set_xlabel(None)
    subplot0.set_xlim([x_start, x_end])
    subplot0.set_ylabel("Boost Pressure (kPa)", fontsize=common_label_font_size)
    subplot0.set_ylim([0, 120])

    for idx in range(len(transient_times)):
        sns.lineplot(x=speed_load_time_data[idx]['TimeToEvent'], y=speed_load_time_data[idx]["EGR Meter"],
                     label=str(transient_times[idx]) + "s", ax=subplot1, legend=False)
    subplot1.set_xlim([x_start, x_end])
    subplot1.set_ylabel("EGR Rate (% Mass)", fontsize=common_label_font_size)
    subplot1.set_ylim([5, 35])

    subplot0.legend(fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/speed_load_transient_time_comparison.png")
    plt.show(block=False)


def plot_transient_time_comparison_boost(transient_type, style):
    sns.set_style(style)

    transient_times = [2, 4, 6, 8, 10]

    time_data = []
    for time in transient_times:
        time_data.append(pd.read_csv(r"./data/" + transient_type + "Comparison_" + str(time) +
                                     "SecondTransient_with_BaselineControl.csv",
                                     sep=r'\s*,\s*', header=0, engine='python'))

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=steady_state_data['Boost'], label="Steady State",
                    ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(transient_times)):
        interp = interpolate.interp1d(time_data[idx]['TimeToEvent'], time_data[idx]['Boost (kPa)'])
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_times[idx] * percentage).item(0))

        sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label=str(transient_times[idx]) + "s",
                        ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    ax.set_ylabel("Boost Pressure (kPa)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_time_comparison_boost.png")
    plt.show(block=False)


def plot_transient_time_comparison_egr(transient_type, style, custom_y_limits=None):
    sns.set_style(style)

    transient_times = [2, 4, 6, 8, 10]

    time_data = []
    for time in transient_times:
        time_data.append(pd.read_csv(r"./data/" + transient_type + "Comparison_" + str(time) +
                                     "SecondTransient_with_BaselineControl.csv",
                                     sep=r'\s*,\s*', header=0, engine='python'))

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=steady_state_data['EGRMass'], label="Steady State",
                    ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(transient_times)):
        interp = interpolate.interp1d(time_data[idx]['TimeToEvent'], time_data[idx]['EGR Meter'])
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_times[idx] * percentage).item(0))

        sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label=str(transient_times[idx]) + "s",
                        ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    if custom_y_limits is not None:
        ax.set_ylim(custom_y_limits)
    ax.set_ylabel("EGR Rate (% mass)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_time_comparison_egr_rate.png")
    plt.show(block=False)


def plot_transient_time_comparison_bsfc(transient_type, style, custom_y_limits=None):
    sns.set_style(style)

    transient_times = [2, 4, 6, 8, 10]

    time_data = []
    for time in transient_times:
        time_data.append(pd.read_csv(r"./data/" + transient_type + "Comparison_" + str(time) +
                                     "SecondTransient_with_BaselineControl.csv",
                                     sep=r'\s*,\s*', header=0, engine='python'))

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=inv_hp_to_inv_kW(steady_state_data['BSFC']), label="Steady State",
                    ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(transient_times)):
        interp = interpolate.interp1d(time_data[idx]['TimeToEvent'], inv_hp_to_inv_kW(time_data[idx]['BSFC']))
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_times[idx] * percentage + 0.1).item(0))

        sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label=str(transient_times[idx]) + "s",
                        ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    if custom_y_limits is not None:
        ax.set_ylim(custom_y_limits)
    ax.set_ylabel("BSFC (g/kWh)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_time_comparison_bsfc.png")
    plt.show(block=False)


def plot_transient_time_comparison_bspm(transient_type, style, custom_y_limits=None, number_legend_columns=1):
    sns.set_style(style)

    transient_times = [2, 4, 6, 8, 10]

    time_data = []
    for time in transient_times:
        time_data.append(pd.read_csv(r"./data/" + transient_type + "Comparison_" + str(time) +
                                     "SecondTransient_with_BaselineControl.csv",
                                     sep=r'\s*,\s*', header=0, engine='python'))

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=inv_hp_to_inv_kW(steady_state_data['BSPM']), label="Steady State",
                    ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(transient_times)):
        interp = interpolate.interp1d(time_data[idx]['TimeToEvent'], inv_hp_to_inv_kW(time_data[idx]['BSPM']))
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_times[idx] * percentage + 0.1).item(0))

        sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label=str(transient_times[idx]) + "s",
                        ax=ax, legend=False, s=sizes, marker=marker_styles[idx])
    if custom_y_limits is not None:
        ax.set_ylim(custom_y_limits)
    ax.set_yscale("log")
    ax.set_ylabel("BSPM (g/kWh)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size, ncol=number_legend_columns)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_time_comparison_bspm.png")
    plt.show(block=False)


def plot_transient_time_comparison_bsno(transient_type, style):
    sns.set_style(style)

    transient_times = [2, 4, 6, 8, 10]

    time_data = []
    for time in transient_times:
        time_data.append(pd.read_csv(r"./data/" + transient_type + "Comparison_" + str(time) +
                                     "SecondTransient_with_BaselineControl.csv",
                                     sep=r'\s*,\s*', header=0, engine='python'))

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=inv_hp_to_inv_kW(steady_state_data['BSNO']), label="Steady State",
                    ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(transient_times)):
        interp = interpolate.interp1d(time_data[idx]['TimeToEvent'], inv_hp_to_inv_kW(time_data[idx]['BSNO']))
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_times[idx] * percentage + 0.1).item(0))

        sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label=str(transient_times[idx]) + "s",
                        ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    ax.set_ylabel("BSNO (g/kWh)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_time_comparison_bsno.png")
    plt.show(block=False)


def plot_policy_comparison_boost(policies, transient_type, style):
    sns.set_style(style)

    transient_complete_time = []
    policy_data = []
    for policy in policies:
        data_set = pd.read_csv(r"./data/" + transient_type + "Comparison_2SecondTransient_with_Policy" +
                               str(policy) + ".csv", sep=r'\s*,\s*', header=0, engine='python')
        policy_data.append(data_set)
        transient_completion_idx = data_set[data_set['Torque'].gt(490)].index[0]
        transient_complete_time.append(data_set['TimeToEvent'][transient_completion_idx])

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=steady_state_data['Boost'], label="Steady State",
                    ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(policies)):
        interp = interpolate.interp1d(policy_data[idx]['TimeToEvent'], policy_data[idx]['Boost (kPa)'])
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_complete_time[idx] * percentage).item(0))
        if idx == 0:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Baseline",
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])
        else:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Policy " + str(policies[idx]),
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    ax.set_ylabel("Boost Pressure (kPa)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_policy_comparison_boost.png")
    plt.show(block=False)


def plot_policy_comparison_egr(policies, transient_type, style, custom_y_limits=None, number_legend_columns=1):
    sns.set_style(style)

    transient_complete_time = []
    policy_data = []
    for policy in policies:
        data_set = pd.read_csv(r"./data/" + transient_type + "Comparison_2SecondTransient_with_Policy" +
                               str(policy) + ".csv", sep=r'\s*,\s*', header=0, engine='python')
        policy_data.append(data_set)
        transient_completion_idx = data_set[data_set['Torque'].gt(490)].index[0]
        transient_complete_time.append(data_set['TimeToEvent'][transient_completion_idx])

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=steady_state_data['EGRMass'], label="Steady State",
                    ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(policies)):
        interp = interpolate.interp1d(policy_data[idx]['TimeToEvent'], policy_data[idx]['EGR Meter'])
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_complete_time[idx] * percentage).item(0))
        if idx == 0:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Baseline",
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])
        else:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Policy " + str(policies[idx]),
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    if custom_y_limits is not None:
        ax.set_ylim(custom_y_limits)
    ax.set_ylabel("EGR Rate (% mass)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size, ncol=number_legend_columns)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_policy_comparison_egr_rate.png")
    plt.show(block=False)


def plot_policy_comparison_bsfc(policies, transient_type, style, custom_y_limits=None, number_legend_columns=1):
    sns.set_style(style)

    transient_complete_time = []
    policy_data = []
    for policy in policies:
        data_set = pd.read_csv(r"./data/" + transient_type + "Comparison_2SecondTransient_with_Policy" +
                               str(policy) + ".csv", sep=r'\s*,\s*', header=0, engine='python')
        policy_data.append(data_set)
        transient_completion_idx = data_set[data_set['Torque'].gt(490)].index[0]
        transient_complete_time.append(data_set['TimeToEvent'][transient_completion_idx])

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=inv_hp_to_inv_kW(steady_state_data['BSFC']),
                    label="Steady State", ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(policies)):
        interp = interpolate.interp1d(policy_data[idx]['TimeToEvent'], inv_hp_to_inv_kW(policy_data[idx]['BSFC']))
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_complete_time[idx] * percentage).item(0))
        if idx == 0:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Baseline",
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])
        else:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Policy " + str(policies[idx]),
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    if custom_y_limits is not None:
        ax.set_ylim(custom_y_limits)
    ax.set_ylabel("BSFC (g/kWh)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size, ncol=number_legend_columns)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_policy_comparison_bsfc.png")
    plt.show(block=False)


def plot_policy_comparison_bspm(policies, transient_type, style):
    sns.set_style(style)

    transient_complete_time = []
    policy_data = []
    for policy in policies:
        data_set = pd.read_csv(r"./data/" + transient_type + "Comparison_2SecondTransient_with_Policy" +
                               str(policy) + ".csv", sep=r'\s*,\s*', header=0, engine='python')
        policy_data.append(data_set)
        transient_completion_idx = data_set[data_set['Torque'].gt(490)].index[0]
        transient_complete_time.append(data_set['TimeToEvent'][transient_completion_idx])

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=inv_hp_to_inv_kW(steady_state_data['BSPM']),
                    label="Steady State", ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(policies)):
        interp = interpolate.interp1d(policy_data[idx]['TimeToEvent'], inv_hp_to_inv_kW(policy_data[idx]['BSPM']))
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_complete_time[idx] * percentage).item(0))
        if idx == 0:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Baseline",
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])
        else:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Policy " + str(policies[idx]),
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    ax.set_yscale("log")
    ax.set_ylabel("BSPM (g/kWh)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_policy_comparison_bspm.png")
    plt.show(block=False)


def plot_policy_comparison_bsno(policies, transient_type, style):
    sns.set_style(style)

    transient_complete_time = []
    policy_data = []
    for policy in policies:
        data_set = pd.read_csv(r"./data/" + transient_type + "Comparison_2SecondTransient_with_Policy" +
                               str(policy) + ".csv", sep=r'\s*,\s*', header=0, engine='python')
        policy_data.append(data_set)
        transient_completion_idx = data_set[data_set['Torque'].gt(490)].index[0]
        transient_complete_time.append(data_set['TimeToEvent'][transient_completion_idx])

    steady_state_data = pd.read_csv(r"./data/" + transient_type + "Comparison_SteadyStates.csv",
                                    sep=r'\s*,\s*', header=0, engine='python')

    fig, ax = plt.subplots()
    marker_styles = ["s", "^", "X", "*", "o"]
    sizes = 100

    percent_complete = [0.0, 0.25, 0.5, 0.75, 1.0]

    sns.scatterplot(x=[100 * x for x in percent_complete], y=inv_hp_to_inv_kW(steady_state_data['BSNO']),
                    label="Steady State", ax=ax, legend=False, s=sizes, marker="D")

    for idx in range(len(policies)):
        interp = interpolate.interp1d(policy_data[idx]['TimeToEvent'], inv_hp_to_inv_kW(policy_data[idx]['BSNO']))
        values = []
        for percentage in percent_complete:
            values.append(interp(transient_complete_time[idx] * percentage).item(0))
        if idx == 0:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Baseline",
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])
        else:
            sns.scatterplot(x=[100 * x for x in percent_complete], y=values, label="Policy " + str(policies[idx]),
                            ax=ax, legend=False, s=sizes, marker=marker_styles[idx])

    ax.set_yscale("log")
    ax.set_ylabel("BSNO (g/kWh)", fontsize=common_label_font_size)
    ax.set_xlabel("Transient Percent Complete (%)", fontsize=common_label_font_size)
    ax.set_xticks([100 * x for x in percent_complete])  # <--- set the ticks first
    ax.set_xticklabels([100 * x for x in percent_complete])
    ax.legend(fontsize=common_legend_font_size)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/" + transient_type + "_transient_policy_comparison_bsno.png")
    plt.show(block=False)


if __name__ == '__main__':
    sns.set_theme()
    sns.set_palette(sns.color_palette("muted"))
    plt.rcParams["font.family"] = "Times New Roman"
    sns.set_style("white")

    plot_style = "darkgrid"     # "ticks" is a good alternative

    # plot_torque_curve()
    #
    # plot_optimal_vnt_and_egr_strategies_for_speed_transient(plot_style)
    #
    # plot_optimal_vnt_and_egr_strategies_for_load_transient(plot_style)
    #
    # plot_optimal_steady_state_vnt_and_egr_set_points_for_load_transient(plot_style)
    #
    # plot_speed_load_transient_time_comparison_of_boost_and_egr(plot_style)
    #
    # plot_transient_time_comparison_boost("Load", plot_style)
    #
    # plot_transient_time_comparison_egr("Load", plot_style, custom_y_limits=[26, 42])
    #
    # plot_transient_time_comparison_bsfc("Load", plot_style, custom_y_limits=[160, 340])
    #
    # plot_transient_time_comparison_bspm("Load", plot_style, custom_y_limits=[0.01, 10])
    #
    # plot_transient_time_comparison_bsno("Load", plot_style)
    #
    # plot_transient_time_comparison_boost("Speed", plot_style)
    #
    # plot_transient_time_comparison_egr("Speed", plot_style)
    #
    # plot_transient_time_comparison_bsfc("Speed", plot_style, custom_y_limits=[250, 550])
    #
    # plot_transient_time_comparison_bspm("Speed", plot_style, custom_y_limits=[0.01, 10], number_legend_columns=3)
    #
    # plot_transient_time_comparison_bsno("Speed", plot_style)
    #
    # plot_transient_time_comparison_boost("SpeedLoad", plot_style)
    #
    # plot_transient_time_comparison_egr("SpeedLoad", plot_style, custom_y_limits=[10, 34])
    #
    # plot_transient_time_comparison_bsfc("SpeedLoad", plot_style, custom_y_limits=[250, 1000])
    #
    # plot_transient_time_comparison_bspm("SpeedLoad", plot_style, custom_y_limits=[0.01, 100], number_legend_columns=3)
    #
    # plot_transient_time_comparison_bsno("SpeedLoad", plot_style)

    best_load_policies = [1, 5, 8, 9, 10]
    # plot_policy_comparison_boost(best_load_policies, "Load", plot_style)
    #
    # plot_policy_comparison_egr(best_load_policies, "Load", plot_style, custom_y_limits=[25, 42], number_legend_columns=3)
    #
    plot_policy_comparison_bsfc(best_load_policies, "Load", plot_style, custom_y_limits=[100, 500], number_legend_columns=3)
    #
    # plot_policy_comparison_bspm(best_load_policies, "Load", plot_style)
    #
    # plot_policy_comparison_bsno(best_load_policies, "Load", plot_style)

    plt.show(block=True)


