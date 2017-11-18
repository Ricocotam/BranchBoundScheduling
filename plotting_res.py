"""File used to plot tables.

Author
-------
Adrien Pouyet

"""

import subprocess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
from pandas.tools.plotting import table


if __name__ == '__main__':
    cases = []
    M = 26
    for i in range(3, M):
        with open("3_time_node/benchmark_" + str(i) + "_tasks_times.complex", "rb") as f:
            cases.append(pickle.load(f))

    times = {k: [] for k in cases[0]}
    for i, combos in enumerate(cases):
        for comb in combos:
            combos[comb] = np.array(combos[comb])
            times[comb].append([combos[comb][:, 0].min(), combos[comb][:, 0].mean(), combos[comb][:, 0].max()])

    for comb in times:
        times[comb] = np.array(times[comb])


    mean_times = {''.join(k): pd.Series(v[:, 1]) for k, v in times.items()}
    mean_times = pd.DataFrame(mean_times)

    rename = {i: j for i, j in zip(range(M-3), range(3, M))}
    mean_times = mean_times.rename(index=rename)

    mean_times.to_html('3_time_nodes.html')
    subprocess.call(
        '~/wkhtmltox/bin/wkhtmltoimage -f png --width 0 3_time_nodes.html 3_time_nodes.png', shell=True)

    M = 26
    cases = []
    for i in range(3, M):
        with open("3_time_node/benchmark_" + str(i) + "_tasks_times.complex", "rb") as f:
            cases.append(pickle.load(f))

    nodes = {k: [] for k in cases[0]}
    for i, combos in enumerate(cases):
        for comb in combos:
            combos[comb] = np.array(combos[comb])
            nodes[comb].append([combos[comb][:, 2].min(), combos[comb][:, 2].mean(), combos[comb][:, 2].max()])

    for comb in nodes:
        nodes[comb] = np.array(nodes[comb])


    mean_nodes = {''.join(k): pd.Series(v[:, 1]) for k, v in nodes.items()}
    mean_nodes = pd.DataFrame(mean_nodes)
    rename = {i: j for i, j in zip(range(M-3), range(3, M))}
    mean_nodes = mean_nodes.rename(index=rename)

    mean_nodes.to_html('3_node_nodes.html')
    subprocess.call(
        '~/wkhtmltox/bin/wkhtmltoimage -f png --width 0 3_node_nodes.html 3_node_nodes.png', shell=True)
