import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

datasets = [
    "Proxifier",
    "Linux",
    "Apache",
    "Zookeeper",
    "Hadoop",
    "HealthApp",
    "OpenStack",
    "HPC",
    "Mac",
    "OpenSSH",
    "Spark",
    "Thunderbird",
    "BGL",
    "HDFS",
]

methods = [
    "AEL",
    "Drain",
    "IPLoM",
    # "LenMa",
    "LFA",
    # "LogCluster",
    # "LogMine",
    # "Logram",
    # "LogSig",
    # "MoLFI",
    # "SHISO",
    # "SLCT",
    # "Spell",
    # "UniParser",
    "LogPPT",
]

all_methods = [
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

def get_average(df, datasets, row):
    metrics = []
    for dataset in datasets:
        if dataset in df.columns and (not pd.isna(df.loc[row, dataset])):
            metrics.append(df.loc[row, dataset])
    return sum(metrics) / len(metrics)

def get_pattern_complex(tech):
    pattern_path = f"../../result/complex/"
    metrics = []
    file_path_1 = f"{pattern_path}/{tech}_full_complex=1_frequent=0.csv"
    file_path_2 = f"{pattern_path}/{tech}_full_complex=2_frequent=0.csv"
    file_path_3 = f"{pattern_path}/{tech}_full_complex=3_frequent=0.csv"
    if not os.path.exists(file_path_1) or not os.path.exists(file_path_2) or not os.path.exists(file_path_3):
        return metrics
    df_1 = pd.read_csv(file_path_1, skiprows=[0])
    df_2 = pd.read_csv(file_path_2, skiprows=[0])
    df_3 = pd.read_csv(file_path_3, skiprows=[0])
    metrics.append(get_average(df_1, datasets, 3))
    metrics.append(get_average(df_2, datasets, 3))
    metrics.append(get_average(df_3, datasets, 3))
    metrics.append(get_average(df_1, datasets, 5))
    metrics.append(get_average(df_2, datasets, 5))
    metrics.append(get_average(df_3, datasets, 5))
    metrics.append(get_average(df_1, datasets, 4))
    metrics.append(get_average(df_2, datasets, 4))
    metrics.append(get_average(df_3, datasets, 4))
    metrics.append(get_average(df_1, datasets, 8))
    metrics.append(get_average(df_2, datasets, 8))
    metrics.append(get_average(df_3, datasets, 8))
    return metrics


def get_pattern_frequent(tech, frequent=10):
    pattern_path = f"../../result/frequent/"
    metrics = []
    file_path_head = f"{pattern_path}/{tech}_full_complex=0_frequent={frequent}.csv"
    file_path_tail = f"{pattern_path}/{tech}_full_complex=0_frequent=-{frequent}.csv"
    if not os.path.exists(file_path_head) or not os.path.exists(file_path_tail):
        return metrics
    df_head = pd.read_csv(file_path_head, skiprows=[0])
    df_tail = pd.read_csv(file_path_tail, skiprows=[0])
    metrics.append(get_average(df_tail, datasets, 3))
    metrics.append(get_average(df_head, datasets, 3))
    metrics.append(get_average(df_tail, datasets, 5))
    metrics.append(get_average(df_head, datasets, 5))
    metrics.append(get_average(df_tail, datasets, 4))
    metrics.append(get_average(df_head, datasets, 4))
    metrics.append(get_average(df_tail, datasets, 8))
    metrics.append(get_average(df_head, datasets, 8))
    return metrics



def plot_data_complex(methods):
    print("plot data complex on ", methods)
    plt.rcParams.update({'font.size': 25, "font.family": 'Times New Roman'})
    col = 5
    row = int(len(methods) / col)
    scale = 2
    # scale = 2.5
    fig, axes = plt.subplots(nrows=row, ncols=col, figsize=(scale * 4 * (col + 0.04), 4 * row), dpi=300)
    fig.subplots_adjust(wspace=0.04, hspace=0.4)

    color1 = '#ADDB88'
    color2 = '#80A6E2'
    color3 = '#8481BA'
    for method_idx, method in enumerate(methods):
        fx, fy = method_idx // col, method_idx % col
        data = get_pattern_complex(method)
        if row == 1:
            axes[fy].set_title(method, fontsize=30)
        else:
            axes[fx][fy].set_title(method, fontsize=30)
        if len(data) < 8:
            continue
        if row == 1:
            if fy == 0:
                axes[fy].bar(0 * 4 + 0 * 1 + 1, data[0], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6, label="#Param. = 0")
                axes[fy].bar(0 * 4 + 1 * 1 + 1, data[1], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6, label="0 < #Param. < 5")
                axes[fy].bar(0 * 4 + 2 * 1 + 1, data[2], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6, label="#Param. >= 5")
            else:
                axes[fy].bar(0 * 4 + 0 * 1 + 1, data[0], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
                axes[fy].bar(0 * 4 + 1 * 1 + 1, data[1], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
                axes[fy].bar(0 * 4 + 2 * 1 + 1, data[2], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6)            
            axes[fy].bar(1 * 4 + 0 * 1 + 1, data[3], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fy].bar(1 * 4 + 1 * 1 + 1, data[4], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fy].bar(1 * 4 + 2 * 1 + 1, data[5], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6)
            axes[fy].bar(2 * 4 + 0 * 1 + 1, data[6], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fy].bar(2 * 4 + 1 * 1 + 1, data[7], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fy].bar(2 * 4 + 2 * 1 + 1, data[8], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6)
            axes[fy].bar(3 * 4 + 0 * 1 + 1, data[9], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fy].bar(3 * 4 + 1 * 1 + 1, data[10], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fy].bar(3 * 4 + 2 * 1 + 1, data[11], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6)
        else:
            if fx == 0 and fy == 0:
                axes[fx][fy].bar(0 * 4 + 0 * 1 + 1, data[0], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6, label="#Param = 0")
                axes[fx][fy].bar(0 * 4 + 1 * 1 + 1, data[1], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6, label="0 < #Param < 5")
                axes[fx][fy].bar(0 * 4 + 2 * 1 + 1, data[2], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6, label="#Param >= 5")
            else:
                axes[fx][fy].bar(0 * 4 + 0 * 1 + 1, data[0], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
                axes[fx][fy].bar(0 * 4 + 1 * 1 + 1, data[1], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
                axes[fx][fy].bar(0 * 4 + 2 * 1 + 1, data[2], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6)            
            axes[fx][fy].bar(1 * 4 + 0 * 1 + 1, data[3], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fx][fy].bar(1 * 4 + 1 * 1 + 1, data[4], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fx][fy].bar(1 * 4 + 2 * 1 + 1, data[5], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6)
            axes[fx][fy].bar(2 * 4 + 0 * 1 + 1, data[6], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fx][fy].bar(2 * 4 + 1 * 1 + 1, data[7], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fx][fy].bar(2 * 4 + 2 * 1 + 1, data[8], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6)
            axes[fx][fy].bar(3 * 4 + 0 * 1 + 1, data[9], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fx][fy].bar(3 * 4 + 1 * 1 + 1, data[10], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fx][fy].bar(3 * 4 + 2 * 1 + 1, data[11], width=0.8, edgecolor='black', color=color3, zorder=2, alpha=0.6)
    for fx in range(row):
        for fy in range(col):
            if row == 1:
                axes[fy].grid(color='lightgray', alpha=0.5)
                axes[fy].set_xlim(0, 3 * 4 + 2 * 1 + 1 + 1)
                axes[fy].set_xticks([2, 6, 10, 14])
                axes[fy].set_xticklabels(['GA', 'FGA', 'PA', 'FTA'], fontsize=25)
                axes[fy].set_ylim(0, 1.05)
                if fy == 0:
                    axes[fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                    axes[fy].set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'], fontsize=25)
                    axes[fy].set_ylabel('Average Score', fontsize=25)
                else:
                    axes[fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                    axes[fy].set_yticklabels([])
            else:
                axes[fx][fy].grid(color='lightgray', alpha=0.5)
                axes[fx][fy].set_xlim(0, 3 * 4 + 2 * 1 + 1 + 1)
                axes[fx][fy].set_xticks([2, 6, 10, 14])
                axes[fx][fy].set_xticklabels(['GA', 'FGA', 'PA', 'FTA'], fontsize=25)
                axes[fx][fy].set_ylim(0, 1.05)
                if fy == 0:
                    axes[fx][fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                    axes[fx][fy].set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'], fontsize=25)
                    axes[fx][fy].set_ylabel('Average Score', fontsize=25)
                else:
                    axes[fx][fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                    axes[fx][fy].set_yticklabels([])
    fig.legend(loc='upper center', prop={'size': 25}, ncol=3, bbox_to_anchor=(0.5, 1.25))
    if len(methods) != 15:
        plt.savefig(f"RQ3_complexity.pdf", bbox_inches='tight')
        plt.savefig(f"RQ3_complexity.png", bbox_inches='tight')
    else:
        plt.savefig(f"RQ3_complexity_all.pdf", bbox_inches='tight')
        plt.savefig(f"RQ3_complexity_all.png", bbox_inches='tight')


def plot_data_frequent(methods, frequent=10):
    print(f"Plotting frequent {frequent} on ", methods)
    plt.rcParams.update({'font.size': 25, "font.family": 'Times New Roman'})
    col = 5
    row = int(len(methods) / col)
    scale = 2
    # scale = 2.5
    fig, axes = plt.subplots(nrows=row, ncols=col, figsize=(scale * 4 * (col + 0.05), 4 * row), dpi=300)
    fig.subplots_adjust(wspace=0.04, hspace=0.4)

    color1 = '#ADDB88'
    color2 = '#80A6E2'
    for method_idx, method in enumerate(methods):
        fx, fy = method_idx // col, method_idx % col
        data = get_pattern_frequent(method, frequent)
        if row == 1:
            axes[fy].set_title(method, fontsize=30)
        else:
            axes[fx][fy].set_title(method, fontsize=30)
        if len(data) < 8:
            continue
        if row == 1:
            if fy == 0:
                axes[fy].bar(0 * 3 + 0 * 1 + 1, data[0], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6, label=f"Top {frequent}% frequencies")
                axes[fy].bar(0 * 3 + 1 * 1 + 1, data[1], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6, label=f"Bottom {frequent}% frequencies")
            else:
                axes[fy].bar(0 * 3 + 0 * 1 + 1, data[0], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
                axes[fy].bar(0 * 3 + 1 * 1 + 1, data[1], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fy].bar(1 * 3 + 0 * 1 + 1, data[2], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fy].bar(1 * 3 + 1 * 1 + 1, data[3], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fy].bar(2 * 3 + 0 * 1 + 1, data[4], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fy].bar(2 * 3 + 1 * 1 + 1, data[5], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fy].bar(3 * 3 + 0 * 1 + 1, data[6], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fy].bar(3 * 3 + 1 * 1 + 1, data[7], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
        else:
            if fx == 0 and fy == 0:
                axes[fx][fy].bar(0 * 3 + 0 * 1 + 1, data[0], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6, label=f"Top {frequent}% frequencies")
                axes[fx][fy].bar(0 * 3 + 1 * 1 + 1, data[1], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6, label=f"Bottom {frequent}% frequencies")
            else:
                axes[fx][fy].bar(0 * 3 + 0 * 1 + 1, data[0], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
                axes[fx][fy].bar(0 * 3 + 1 * 1 + 1, data[1], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fx][fy].bar(1 * 3 + 0 * 1 + 1, data[2], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fx][fy].bar(1 * 3 + 1 * 1 + 1, data[3], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fx][fy].bar(2 * 3 + 0 * 1 + 1, data[4], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fx][fy].bar(2 * 3 + 1 * 1 + 1, data[5], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
            axes[fx][fy].bar(3 * 3 + 0 * 1 + 1, data[6], width=0.8, edgecolor='black', color=color1, zorder=2, alpha=0.6)
            axes[fx][fy].bar(3 * 3 + 1 * 1 + 1, data[7], width=0.8, edgecolor='black', color=color2, zorder=2, alpha=0.6)
    for fx in range(row):
        for fy in range(col):
            if row == 1:
                axes[fy].grid(color='lightgray', alpha=0.5)
                axes[fy].set_xlim(0, 3 * 3 + 1 * 1 + 1 + 1)
                axes[fy].set_xticks([1.5, 4.5, 7.5, 10.5])
                axes[fy].set_xticklabels(['GA',  'FGA', 'PA', 'FTA'], fontsize=25)
                axes[fy].set_ylim(0, 1.05)
                if fy == 0:
                    axes[fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                    axes[fy].set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'], fontsize=25)
                    axes[fy].set_ylabel('Average Score', fontsize=25)

                else:
                    axes[fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                    axes[fy].set_yticklabels([])
            else:
                axes[fx][fy].grid(color='lightgray', alpha=0.5)
                axes[fx][fy].set_xlim(0, 3 * 3 + 1 * 1 + 1 + 1)
                axes[fx][fy].set_xticks([1.5, 4.5, 7.5, 10.5])
                axes[fx][fy].set_xticklabels(['GA',  'FGA', 'PA', 'FTA'], fontsize=25)
                axes[fx][fy].set_ylim(0, 1.05)
                if fy == 0:
                    axes[fx][fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                    axes[fx][fy].set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'], fontsize=25)
                    axes[fx][fy].set_ylabel('Average Score', fontsize=25)

                else:
                    axes[fx][fy].set_yticks([0, 0.25, 0.5, 0.75, 1.00])
                    axes[fx][fy].set_yticklabels([])
    fig.legend(loc='upper center', prop={'size': 25}, ncol=3, bbox_to_anchor=(0.5, 1.25))
    if len(methods) != 15:
        plt.savefig(f"RQ3_frequency.pdf", bbox_inches='tight')
        plt.savefig(f"RQ3_frequency.png", bbox_inches='tight')
    else:
        plt.savefig(f"RQ3_frequency_all.pdf", bbox_inches='tight')
        plt.savefig(f"RQ3_frequency_all.png", bbox_inches='tight')


if __name__ == '__main__':
    plot_data_complex(methods)
    plot_data_complex(all_methods)
    plot_data_frequent(methods)
    plot_data_frequent(all_methods)
