import os
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def styled_print(text, header=False):
    """Custom Print Function"""
    class style:
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

    if header:
        print(f'{style.BOLD}› {style.UNDERLINE}{text}{style.END}')
    else:
        print(f'    {text}')


def download_data(url, path_to_download="./data"):
    file_name = url.split('/')[-1]
    response = requests.get(url, stream=True)
    with open(os.path.join(path_to_download, file_name), 'wb') as handle:
        for chunk in response.iter_content(chunk_size=2048):
            if chunk:
                handle.write(chunk)
    return os.path.join(path_to_download, file_name)


def read_and_clean_data(file_path, header=None, na_values=["?"]):
    df = pd.read_csv(file_path, header=None, names=header, na_values=na_values)
    return df


def plot_box_plot_hist_plot(df, column, title="Distribution Plot", figsize=(16, 16),
                            dpi=300, save_flag=False, file_path=None):
    fig, (ax_box, ax_hist) = plt.subplots(
        nrows=2,
        sharex=True,
        figsize=figsize,
        gridspec_kw={"height_ratios": (.20, .80)},
        dpi=dpi,
        constrained_layout=False
    )
    sns.boxplot(data=df, x=column, ax=ax_box)
    sns.histplot(data=df, x=column, ax=ax_hist, kde=True, bins='sqrt')
    ax_box.set(xlabel='')
    ax_box.set_facecolor('white')
    ax_hist.set_facecolor('white')
    plt.title(title)
    if save_flag:
        fig.savefig(file_path, dpi=dpi, facecolor='white')
        plt.close()


def plot_count_plot(df, column, hue=None, title="Count Plot", figsize=(24, 24), dpi=300,
                    save_flag=False, file_path=None):
    fig, axs = plt.subplots(1, 1, figsize=figsize,
                            dpi=dpi, constrained_layout=False)
    pt = sns.countplot(data=df, x=column, hue=hue,
                       palette=sns.color_palette("Set2"))
    pt.set_xticklabels(pt.get_xticklabels(), rotation=30)
    if hue is not None:
        axs.legend(loc="upper right", title=hue)
    axs.set_facecolor('white')
    plt.title(title)
    if save_flag:
        fig.savefig(file_path, dpi=dpi, facecolor='white')
        plt.close()


def discrete_to_target_plot(df, discrete_column, target_column, title="Plot", figsize=(24, 24), dpi=300,
                            save_flag=False, file_path=None):
    fig, axs = plt.subplots(1, 1, figsize=figsize,
                            dpi=dpi, constrained_layout=False)

    (pd.crosstab(df[discrete_column], df[target_column], normalize='index')
     * 100).plot(kind='bar', figsize=(8, 4), stacked=True, ax=axs)
    plt.ylabel(f'Percentage {target_column} %')

    axs.set_facecolor('white')
    plt.title(title)
    if save_flag:
        fig.savefig(file_path, dpi=dpi, facecolor='white')
        plt.close()


def continuous_to_target_plot(df, continuous_column, target_column, hue=None, title="Plot", figsize=(24, 24), dpi=300,
                              save_flag=False, file_path=None):
    fig, axs = plt.subplots(1, 1, figsize=figsize,
                            dpi=dpi, constrained_layout=False)

    sns.boxplot(
        x=target_column,
        y=continuous_column,
        hue=hue,
        palette=sns.color_palette("Set2"),
        data=df
    )
    plt.ylabel(f'Distribution of {continuous_column}')
    plt.xlabel(f'Categories of {target_column}')
    axs.set_facecolor('white')
    plt.title(title)
    if save_flag:
        fig.savefig(file_path, dpi=dpi, facecolor='white')
        plt.close()


def plot_correlation(corr, mask, title="Correlation Heatmap", figsize=(16, 16),
                     save_flag=False, file_path=None):
    fig = plt.figure(figsize=figsize)
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, annot=True, cmap=cmap,
                fmt=".2f", vmin=-1.0, vmax=1.0)
    plt.title(title)
    if save_flag:
        fig.savefig(file_path)
        plt.close()


def correlation_analysis(df, method='pearson',
                         save_flag=False,
                         plot_dir="plots",
                         title=None,
                         prefix="Correlation_Matrix",
                         postfix="", figsize=(24, 24)):
    # Calculate correlation matrix.
    corr = df.corr(method=method)
    plot_correlation(
        corr=corr,
        mask=np.triu(np.ones_like(corr, dtype=bool)),
        title=f"{prefix}{title}{postfix}",
        figsize=figsize,
        save_flag=save_flag
    )
    return corr


def traditional_feature_importance(model, df, apply_ln=False, title="Plot", figsize=(24, 24), dpi=300,
                                   save_flag=False, file_path=None):
    importance = model.coef_
    if len(importance.shape) > 1:
        importance = importance[0]
        
    if apply_ln:
        importance = np.exp(importance)
    feature_importance = {
        key: importance[i] for i, key in enumerate(list(df.keys()))
    }
    feature_importance = pd.DataFrame(feature_importance.items(), columns=[
                                      'Features', 'Importance'])
    fig, axs = plt.subplots(1, 1, figsize=figsize,
                            dpi=dpi, constrained_layout=False)
    pt = sns.barplot(data=feature_importance, x='Features', y='Importance')
    pt.set_xticklabels(pt.get_xticklabels(), rotation=30)
    plt.ylabel(f'Coeeficient as Importance of Feature')
    plt.xlabel(f'Features')
    axs.set_facecolor('white')
    plt.title(title)
    if save_flag:
        fig.savefig(file_path, dpi=dpi, facecolor='white')
        plt.close()
    return feature_importance
