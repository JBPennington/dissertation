import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


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
    torque_graph.set_xlabel("Speed (rpm)", fontsize=18)
    torque_graph.set_ylabel("Torque (Nm)", fontsize=18)

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
    torque_graph.annotate(text='Load', xy=(1000, 1.3558179483 * 280), fontsize=15)
    # Load
    torque_graph.arrow(x=1200, y=1.3558179483 * 500, dx=800, dy=0, width=arrow_widths,head_width=arrow_head_widths,
                       head_length=arrow_head_lengths,
                       length_includes_head=length_includes_head)
    torque_graph.annotate(text='Accel', xy=(1450, 1.3558179483 * 520), fontsize=15)
    # Speed and Load
    torque_graph.arrow(x=1200, y=1.3558179483 * 100, dx=800, dy=1.3558179483 * 400, width=arrow_widths,
                       head_width=arrow_head_widths, head_length=arrow_head_lengths,
                       length_includes_head=length_includes_head)
    torque_graph.annotate(text='Accel and Load', xy=(1500, 1.3558179483 * 200), fontsize=15)

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

    ax.legend(loc='upper center', ncol=len(best_tests))
    ax.set_xlabel(None)
    ax.set_ylabel("VNT Actuator Position (%)", fontsize=18)
    ax.set_ylim([0.0, 1.0])

    ax = fig.add_subplot(212)

    for test_number in [1, 5, 8, 9, 10]:
        sns.lineplot(x=speed_transient_egr_pos['Time'], y=speed_transient_egr_pos[str(test_number)]/100, ax=ax)

    ax.set_xlabel("Time (s)", fontsize=18)
    ax.set_ylabel("EGR Actuator Position (%)", fontsize=18)
    ax.set_ylim([0.0, 1.0])

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/speed_transient_ad_hoc_positions.png")
    plt.show(block=False)


def plot_optimal_steady_state_vnt_and_egr_set_points_for_load_transient(style):
    sns.set_style(style)
    load_transient_steady_state = pd.read_csv(r"./data/LoadTransient_OptimalSteadyStateSetPoints.csv",
                                              sep=r'\s*,\s*', header=0, engine='python')

    fig, (subplot0, subplot1) = plt.subplots(2, 1, figsize=(7.5, 9))
    line_0 = sns.lineplot(x=1.3558179483 * load_transient_steady_state['Load'],
                          y=load_transient_steady_state["VGT_Position"]/100, color="red",
                          label="VNT Position", ax=subplot0, legend=False)
    line_0.set_ylabel("VNT Actuator Position (%)", fontsize=18)
    line_0.set_ylim([0.0, 1.0])
    line_0.set_xlabel(None)

    ax_01 = line_0.twinx()
    line_1 = sns.lineplot(x=1.3558179483 * load_transient_steady_state['Load'],
                          y=load_transient_steady_state["Boost"], ax=ax_01,
                          label="Boost", legend=False)
    ax_01.set_ylabel("Boost (kPa)", fontsize=18)
    ax_01.set_ylim([0, 50])

    h0, l0 = line_0.get_legend_handles_labels()
    h1, l1 = line_1.get_legend_handles_labels()
    ax_01.legend(h0 + h1, l0 + l1, loc=0, fontsize=16)

    line_2 = sns.lineplot(x=1.3558179483 * load_transient_steady_state['Load'],
                         y=load_transient_steady_state["EGR_Position"] / 100, ax=subplot1, color="red",
                         label="EGR Position", legend=False)
    subplot1.set_ylabel("EGR Actuator Position (%)", fontsize=18)
    subplot1.set_ylim([0.0, 1.0])
    subplot1.set_xlabel("Load (Nm)", fontsize=18)

    ax_11 = subplot1.twinx()
    line_3 = sns.lineplot(x=1.3558179483 * load_transient_steady_state['Load'],
                 y=load_transient_steady_state["EGR_Mass"] / 100, ax=ax_11,
                 label="EGR", legend=False)
    ax_11.set_ylabel("EGR (% Mass)", fontsize=18)
    ax_11.set_ylim([0.0, 1.0])

    h2, l2 = line_2.get_legend_handles_labels()
    h3, l3 = line_3.get_legend_handles_labels()
    ax_11.legend(h2 + h3, l2 + l3, loc=4, fontsize=16)

    plt.tight_layout()
    sns.despine()

    fig.savefig("figures/load_transient_steady_state_optimal_positions.png")
    plt.show(block=False)


if __name__ == '__main__':
    sns.set_theme()
    sns.set_palette(sns.color_palette("muted"))
    plt.rcParams["font.family"] = "Times New Roman"
    sns.set_style("white")

    plot_torque_curve()

    plot_optimal_vnt_and_egr_strategies_for_speed_transient("darkgrid")     # "ticks" is a good alternative

    plot_optimal_steady_state_vnt_and_egr_set_points_for_load_transient("darkgrid")

    plt.show(block=True)


