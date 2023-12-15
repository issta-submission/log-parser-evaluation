import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import regex as re
import calendar
from collections import Counter
from tqdm import tqdm

all_datasets = [
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

def get_occurencies(dataset):
    df_2k = pd.read_csv(f'../../2k_dataset/{dataset}/{dataset}_2k.log_templates.csv')
    df_full = pd.read_csv(f'../../full_dataset/{dataset}/{dataset}_full.log_templates.csv')
    frequencies_2k = list(df_2k['Occurrences'])
    frequencies_full = list(df_full['Occurrences'])

    max_values = max(frequencies_full)
    x_ticks = []
    x = 1
    while x < max_values:
        x_ticks.append(x)
        x *= 10
    if max_values > 5 * (x / 10):
        x_ticks.append(x)
    num_bins = x
    hist1, bins1 = np.histogram(frequencies_2k, bins=num_bins)
    hist2, bins2 = np.histogram(frequencies_full, bins=num_bins)
    cumulative1 = np.cumsum(hist1) / len(frequencies_2k)
    cumulative2 = np.cumsum(hist2) / len(frequencies_full)
    return (cumulative1, cumulative2, bins1, bins2, x_ticks)

def get_variables(dataset):
    df_2k = pd.read_csv(f'../../2k_dataset/{dataset}/{dataset}_2k.log_templates_corrected.csv')
    df_full = pd.read_csv(f'../../full_dataset/{dataset}/{dataset}_full.log_templates.csv')
    templates_2k = list(df_2k['EventTemplate'])
    templates_full = list(df_full['EventTemplate'])
    variables_2k = [template.count("<*>") for template in templates_2k]
    variables_full = [template.count("<*>") for template in templates_full]

    hist1, bins1 = np.histogram(variables_2k, bins=max(variables_2k))
    hist2, bins2 = np.histogram(variables_full, bins=max(variables_full))
    cumulative1 = np.cumsum(hist1) / len(variables_2k)
    cumulative2 = np.cumsum(hist2) / len(variables_full)
    return (cumulative1, cumulative2, bins1, bins2)

def get_data(datasets):
    occurencies, variables = [], []
    for dataset in datasets:
        occurencies.append(get_occurencies(dataset))
        variables.append(get_variables(dataset))
    return occurencies, variables

def plot_all(datasets, occurencies, variables, plot_type=''):
    print("Plotting on datasets: ", datasets)
    length = len(datasets)
    plt.rcParams.update({'font.size': 30, "font.family": 'Times New Roman'})
    row, col = length, 2
    fig, axes = plt.subplots(nrows=row, ncols=col, figsize=(2.4 * 4 * (col + 0.1 * col), 4 * (row + 0.5 * row)), dpi=300)
    fig.subplots_adjust(wspace=0.04, hspace=0.5)

    for i, dataset in enumerate(datasets):
        cumulative1, cumulative2, bins1, bins2, x_ticks = occurencies[i]
        axes[i][0].plot(bins1[:-1], cumulative1, label='Loghub-2k', color=(0.863, 0.078, 0.235), linewidth=3, linestyle="-")
        axes[i][0].plot(bins2[:-1], cumulative2, label='LogPub', color="#2878B5", linewidth=3, linestyle="-")

        axes[i][0].set_xscale('log')
        # axes[i][0].set_xlim([-0.05, 1.05])
        axes[i][0].set_xticks(x_ticks)
        # axes[i][0].set_xticklabels()

        axes[i][0].set_yticks([0, 0.25, 0.5, 0.75, 1])
        axes[i][0].set_yticklabels([0, 0.25, 0.5, 0.75, 1])
        axes[i][0].set_ylim([0, 1.05])
        # Add legend and labels
        #axes[i][0].legend(loc='lower right')
        axes[i][0].set_xlabel('Frequencies of templates', fontsize=30)
        axes[i][0].set_ylabel('Cumulative Probability', fontsize=30)
        axes[i][0].grid(color='lightgray', alpha=0.5)
        axes[i][0].legend(loc='lower right', prop={'size': 25}, handlelength=0.5)
        axes[i][0].set_title(dataset, fontsize=35)

        cumulative1, cumulative2, bins1, bins2 = variables[i]
        axes[i][1].plot(bins1[:-1], cumulative1, label='Loghub-2k', color=(0.863, 0.078, 0.235), linewidth=3, linestyle="-")
        axes[i][1].plot(bins2[:-1], cumulative2, label='LogPub', color="#2878B5", linewidth=3, linestyle="-")

        axes[i][1].set_yticks([0, 0.25, 0.5, 0.75, 1])
        axes[i][1].set_yticklabels([])
        axes[i][1].set_ylim([0, 1.05])

        axes[i][1].set_xlabel('Parameter counts of templates', fontsize=30)
        axes[i][1].grid(color='lightgray', alpha=0.5)
        axes[i][1].legend(loc='lower right', prop={'size': 25}, handlelength=0.5)
        axes[i][1].set_title(dataset, fontsize=35)

    plt.savefig(f"RQ1{plot_type}.pdf", bbox_inches='tight')
    plt.savefig(f"RQ1{plot_type}.png", bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    occurrencies, variables = get_data(['Spark', 'Linux', 'OpenSSH'])
    plot_all(['Spark', 'Linux', 'OpenSSH'], occurrencies, variables)
    occurrencies, variables = get_data(all_datasets)
    plot_all(all_datasets, occurrencies, variables, "_all")
