import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
# from matplotlib.patches import FancyBboxPatch
# import matplotlib.patches as patches
import matplotlib.patches as mpatches
import matplotlib.font_manager as font_manager


all_datasets = [
    "Average",
    "Hadoop",
    "HDFS",
    "OpenStack",
    "Spark",
    "Zookeeper",
    "BGL",
    "HPC",
    "Thunderbird",
    "Linux",
    "Mac",
    "Apache",
    "OpenSSH",
    "HealthApp",
    "Proxifier",
]

methods = [
    "AEL",
    "Drain",
    "IPLoM",
    "LenMa",
    "LFA",
    "LogCluster",
    "LogMine",
    "Logram",
    "LogSig",
    "MoLFI",
    "SHISO",
    "SLCT",
    "Spell",
    "UniParser",
    "LogPPT",
]


def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


def process_result(data_type):
    results_dict = {}
    for method in methods:
        results_dict[method] = {}
        result_file = f"../../result/{method}_{data_type}_complex=0_frequent=0.csv"
        # print(result_file)
        output_file = f"temp/result_{data_type}_complex=0_frequent=0.json"
        if os.path.exists(result_file):
            df = pd.read_csv(result_file, header=1, index_col=0)
            for dataset in all_datasets:
                if dataset in df.columns and np.isnan(df.loc['GA', dataset]) == False:
                    results_dict[method][dataset] = {
                        'parse_time': "{:.3f}".format(df.loc['parse_time', dataset]),
                        'GA': "{:.3f}".format(df.loc['GA', dataset]),
                        'FGA': "{:.3f}".format(df.loc['FGA', dataset]),
                        'PA': "{:.3f}".format(df.loc['PA', dataset]),
                        'PTA': "{:.3f}".format(df.loc['PTA', dataset]),
                        'RTA': "{:.3f}".format(df.loc['RTA', dataset]),
                        'FTA': "{:.3f}".format(df.loc['FTA', dataset])
                    }
                else:
                    # print(method, dataset, "not found")
                    results_dict[method][dataset] = {
                    'parse_time': '-1',
                    'GA': '------',
                    'FGA': '------',
                    'PA': '------',
                    'PTA': '------',
                    'RTA': '------',
                    'FTA': '------'
                }
        else:
            # print(method, dataset, "all not found")
            for dataset in all_datasets:
                results_dict[method][dataset] = {
                    'parse_time': '-1',
                    'GA': '------',
                    'FGA': '------',
                    'PA': '------',
                    'PTA': '------',
                    'RTA': '------',
                    'FTA': '------'
                }
    write_json(results_dict, output_file)
    return output_file

def plot_data(file_path_2k, file_path_full):
    print("Plot file: ", file_path_2k, file_path_full)
    plt.rcParams.update({'font.size': 25, "font.family": 'Times New Roman'})
    row, col = 3, 5
    scale = 2
    # scale = 2.5
    fig, axes = plt.subplots(nrows=row, ncols=col, figsize=(scale * 4 * (col + 0.04), 4 * (row + 0.32)), dpi=300)
    fig.subplots_adjust(wspace=0.04, hspace=0.4)

    data_2k = load_json(file_path_2k)
    data_full = load_json(file_path_full)
    print(len(data_2k), len(data_full))
    flierprops = {'marker': 'o', 'markerfacecolor': 'black', 'markersize': 6, 'markeredgecolor': 'black'}
    width, left, space, group = 1, 0.5, 1.2, 3.5
    color1 = '#FBDD85'
    # color2 = '#80A6E2'
    # color1 = '#ADDB88'
    color2 = '#80A6E2'
    for method_idx, method in enumerate(methods):
        fx, fy = method_idx // col, method_idx % col
        metrics_2k = [[] for _ in range(4)]
        metrics_full = [[] for _ in range(4)]
        for dataset in all_datasets[1:]:
            for i, metric in enumerate(['GA',  'FGA', 'PA', 'FTA']):
                if data_2k[method][dataset][metric] != '------' and data_full[method][dataset][metric] != '------':
                    metrics_2k[i].append(float(data_2k[method][dataset][metric]))
                    metrics_full[i].append(float(data_full[method][dataset][metric]))
        vaild_num = len(metrics_full[0])
        positions = []
        for i in range(4):
            boxprops1 = {'facecolor': color1, 'linewidth': 1.1, 'alpha': 0.6}
            boxprops2 = {'facecolor': color2, 'linewidth': 1.1, 'alpha': 0.6}
            boxplot_2k = axes[fx][fy].boxplot(metrics_2k[i], labels=['Loghub-2k'], patch_artist=True, showmeans=True, positions=[i * group + left + width / 2], widths=width, boxprops=boxprops1, flierprops=flierprops, medianprops={'color': 'black', 'linewidth': 1.2})
            boxplot_full = axes[fx][fy].boxplot(metrics_full[i], labels=['LogPub'], patch_artist=True, showmeans=True, positions=[i * group + left + width / 2 + space], boxprops=boxprops2 ,widths=width, flierprops=flierprops, medianprops={'color': 'black', 'linewidth': 1.2})
            positions.append(i * group + left + width / 2 + space / 2)
            # mean = sum(metrics_2k[i]) / len(metrics_2k[i])  # 计算平均值
            # print(boxplot_2k['boxes'][0])
            # x = boxplot_2k['boxes'][0].get_xdata()  # 获取箱线图的x坐标
            # line = Line2D([x[0], x[2]], [mean, mean], color='green')  # 创建一个线段
            # axes[fx][fy].add_line(line)  # 将线段添加到图上
            # mean = sum(metrics_full[i]) / len(metrics_full[i])  # 计算平均值
            # x = boxplot_full['boxes'][0].get_xdata()  # 获取箱线图的x坐标
            # line = Line2D([x[0], x[2]], [mean, mean], color='green')  # 创建一个线段
            # axes[fx][fy].add_line(line)  # 将线段添加到图上
            title = axes[fx][fy].set_title(method + " (" + str(vaild_num) + ")", color="black", fontsize=30)

    for fx in range(row):
        for fy in range(col):
            axes[fx][fy].grid(color='lightgray', alpha=0.7)
            axes[fx][fy].set_xlim(0, 3 * group + left + space + width + left)
            axes[fx][fy].set_xticks(positions)
            axes[fx][fy].set_xticklabels(['GA',  'FGA', 'PA', 'FTA'], fontsize=25)
            axes[fx][fy].set_ylim(-0.05, 1.05)
            if fy == 0:
                axes[fx][fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                axes[fx][fy].set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'], fontsize=25)
            else:
                axes[fx][fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                axes[fx][fy].set_yticklabels([])
    patch1 = mpatches.Patch(color=color1, label='Loghub-2k')
    patch2 = mpatches.Patch(color=color2, label='LogPub')
    font_prop = font_manager.FontProperties(size=25)

    fig.legend(handles=[patch1, patch2], loc='upper center', prop=font_prop, ncol=2)
    # axes[0][0].legend(loc='upper right')
    plt.savefig(f"RQ2.pdf", bbox_inches='tight')
    plt.savefig(f"RQ2.png", bbox_inches='tight')

def generate_table(datasets, file_2k, file_full, effectiveness, efficiency):
    results_2k = load_json(file_2k)
    results_full = load_json(file_full)
    with open(effectiveness, 'w') as f:
        f.write('dataset+metrics,')
        for method in methods:
            delimiter = ',' if method != methods[-1] else '\n'
            f.write(method + delimiter)
        for dataset in datasets:
            for metric in ['GA',  'FGA', 'PA', 'FTA']:
                f.write(f"{dataset} {metric}" + ',')
                for method in methods:
                    delimiter = ',' if method != methods[-1] else '\n'
                    f.write(
                        results_2k[method][dataset][metric] + ' / ' +  results_full[method][dataset][metric] + delimiter
                    )
    with open(efficiency, 'w') as f:
        f.write('Dataset,')
        for method in methods:
            delimiter = ',' if method != methods[-1] else '\n'
            f.write(method + delimiter)
        for dataset in datasets:
            f.write(dataset + ',')
            for method in methods:
                delimiter = ',' if method != methods[-1] else '\n'
                f.write(
                    results_2k[method][dataset]['parse_time'] + ' / ' +  results_full[method][dataset]['parse_time'] + delimiter
                )

if __name__ == '__main__':
    file_2k = process_result("2k")
    file_full = process_result("full")
    plot_data(file_2k, file_full)
    generate_table(all_datasets, file_2k, file_full, "effectiveness_results.csv", "efficiency_results.csv")
