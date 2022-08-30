###  To load optimization data###

import sklearn as skl
import sklearn.feature_selection as featsel
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import skopt
import sys
import os
from typing import List, Tuple, Dict


def load_opt_dataset(
    file_path: str,
    ) -> pd.DataFrame:
    """
    Load an optimization dataset into a pandas DataFrame.

    Parameters
    ----------
    file_path : str
        File path to the optimization data.

    Returns
    -------
    optimization_dataframe : pandas.DataFrame
        DataFrame containing the optimization data.
    """
    data: np.ndarray = np.loadtxt(file_path, dtype=np.float64, skiprows=1,)
    with open(file_path, "r") as in_file:
        first_line: str = in_file.readline()
    first_line_split: List[str] = first_line.strip().split()
    data_frame: pd.DataFrame = pd.DataFrame(data, columns=first_line_split,)
    return data_frame


full_lasse_df: pd.DataFrame = load_opt_dataset(
    os.path.join(
        os.path.abspath(""),
        #os.pardir,
        "opt-data",
        "opt_data_GPE_random.txt",
    ),
)


def feature_selection(
    random_data,
    fitness="SMAPE",
    sort=True,
    length=None,
    resamples=1,
):
    columns: Tuple[str] = tuple(random_data.columns)
    parameters: List[str] = [
        column for column in columns if column not in (
            "MSE", "RMSE", "MAE", "MAPE", "R2", "SMAPE",
        )
    ]

    full_L = len(random_data[fitness].values)
    if length is not None and length < full_L:
        L = length
    else:
        L = full_L
    design_matrix = np.zeros(shape=(L, len(parameters)))
    # ind = np.random.choice(range(full_L), size=L, replace=False)

    # order = ('N,P', 'N,G', 'N,C', 'N,W', 'P,G', 'P,C', 'P,W', 'G,C',  'G,W', 'C,W')
    order = ("L,G", "L,C", "G,P", "C,W", "P,C", "P,W", "N,P", "N,C", "G,C", "G,W")
    #order = ("C,W", "G,C", "G,W")
    F_array = np.zeros(shape=(resamples, len(parameters)))
    MI_array = np.zeros(shape=(resamples, len(parameters)))

    for metric, array in zip(('F', 'MI'),  (F_array, MI_array)):
        for iteration in range(resamples):
            # resample_ind = np.random.choice(ind, size=L, replace=True)
            r_ind = np.random.choice(range(full_L), size=L, replace=False)
            for i, parameter in enumerate(order):
                design_matrix[:, i] = random_data[parameter].values[r_ind]
            target = random_data[fitness].values[r_ind]

            if metric == 'F':
                F, _ = featsel.f_regression(design_matrix, target)
                array[iteration, :] = F
            else:
                MI = featsel.mutual_info_regression(design_matrix, target,
                                                    discrete_features=False)
                array[iteration, :] = MI

        print(f"{'':>10} {metric:>20} {'std':>20} {'relative':>20}", end="")
        print("\n====================================================")

        for p, m, s in zip(order,
                           np.mean(array, axis=0),
                           np.std(array, axis=0)):
            print(f"{p:10} {m:20.15f} {s:20.15f} {m/np.max(np.mean(array, axis=0)):20.15f}")
        print()

    return (order,
            np.mean(F_array, axis=0), np.std(F_array, axis=0),
            np.mean(MI_array, axis=0), np.std(MI_array, axis=0))

order, F_mean, F_std, MI_mean, MI_std = feature_selection(
    # dppc_allrandom_types_df,
    full_lasse_df,
    length=200,
    resamples=1000,
)


############            Plot feature importance            ###############
def plot_feature_importance(chi, F, F_std, MI, MI_std, length, save=False):
    for name, metric, stddev in zip(('F', 'MI'), (F, MI), (F_std, MI_std)):
        plt.rc('text', usetex=True)
        _font_opts = {'fontsize': 10}
        plt.figure(figsize=(3.3, 2.5))
        # rect : [left, bottom, width, height]
        ax = plt.axes([0.2, 0.25, 0.75, 0.7])
        ind = np.argsort(metric)[::-1]
        print(ind)
        print(metric / np.max(metric))
        print(stddev / np.max(metric))
        fmt = 'b.' if name == 'F' else 'r.'
        sorted_chi = [chi[i] for i in ind]
        plt.errorbar(sorted_chi,
                     metric[ind] / np.max(metric),
                     yerr=(stddev[ind] / np.max(metric)),
                     fmt=fmt,
                     capsize=1,
                     elinewidth=1)
        # ax.set_yscale("log", nonposy='clip')
        plt.xlabel('Interaction parameter', **_font_opts)
        plt.ylabel('Normalised F-value', **_font_opts)
        if name == 'MI':
            plt.ylabel('Normalised MI', **_font_opts)
        # ax.yaxis.set_major_formatter(
        #     ticker.FuncFormatter(
        #         lambda y, pos: (
        #             '{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y), 0)))
        #         ).format(y)
        #     )
        # )
        xticks = [c for c in sorted_chi[::2]]
        # xticks_minor = [f" \n{c}" for c in chi_F[1::2]]
        xticks_minor = [f"{c}" for c in sorted_chi[1::2]]

        print(list(range(10)), xticks)
        print(plt.xticks())
        #ax.set_xticks(list(range(0, 10, 2)), minor=False)
        #ax.set_xticks(list(range(1, 10, 2)), minor=True)
        #ax.set_xticklabels(xticks)
        #ax.set_xticklabels(xticks_minor, minor=True)
        #ax.tick_params(which='minor', length=8, axis='x')
        if name == 'F' and length == 1000:
            ax.set_ylim(bottom=0.001)
        else:
            ax.set_ylim(bottom=0.01)
        if save:
            file_name = f"{name}-all-{L}.eps"
            plt.savefig(file_name, format='eps', dpi=1200)
        plt.show()

plot_feature_importance(order, F_mean, F_std, MI_mean, MI_std, length=100, save=False)


order = ["L,G", "L,C", "G,P", "C,W", "P,C", "P,W", "N,P", "N,C", "G,C", "G,W"]
#order = ["C,W", "G,C", "G,W"]
# Correlation matrices - pair plot
def plot_pairs(df_data,order):
    data = df_data[order]
    g = sns.pairplot(data, diag_kind = 'kde', plot_kws={"s": 5}, height = 0.8)
    plt.show()

# Plot pairs
#plot_pairs(full_lasse_df, order)
