"""
module for creating graphs
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from adjustText import adjust_text


def average_color_bubble():
    """
    Generates colored bubble chart, with x- and y- axis as the first two
    variables, color as the third variable, and the size of bubble as fourth
    point.

    Args:
        None.

    Returns
    """
    average_data = pd.read_csv("artists_average.csv")
    average_df = pd.DataFrame(average_data)

    averages_scatter = plt.scatter(
        average_df["valence"],
        average_df["acousticness"],
        c=average_df["instrumentalness"],
        s=average_df["speechiness"] * 3000,
    )
    plt.xlabel("Valence")
    plt.ylabel("Acousticness")
    plt.title("Average of Song Features for All Artists")

    plt.xlim(0, 1)
    plt.ylim(0, 1)

    # create legend for 'Instrumentalness' color values
    plt.colorbar(averages_scatter, label="Instrumentalness")

    # create legend for 'Speechiness' size values
    plt.scatter([], [], s=0, label="Speechiness")
    size_labels = [0.2, 0.15, 0.1, 0.05]
    for size in size_labels:
        plt.scatter([], [], s=size * 3000, label=f"{size}", alpha=0.5)
    plt.legend()

    # label each point with artist name
    texts = []
    for i, artist_name in enumerate(average_df["artist_name"]):
        texts.append(
            plt.text(
                average_df["valence"][i],
                average_df["acousticness"][i],
                artist_name,
            )
        )
    adjust_text(texts)

    plt.show()


def artist_sums_bar():
    """
    Generates bar charts, measuring artist's total value for each feature.
    The x-axis is artists, and y-axis is the sum of their songs' values for
    the feature of the chart.

    Args:
        None.

    Returns:
        None.
    """
    all_data = pd.read_csv("all_tracks.csv")
    all_df = pd.DataFrame(all_data)

    grouped = all_df.groupby("artist_name").sum()

    # finds sum for each feature, new values placed in own dataframe
    summed_df = grouped[
        ["valence", "acousticness", "instrumentalness", "speechiness"]
    ]

    _, axes = plt.subplots(1, 4, figsize=(15, 5))

    for i, feature in enumerate(summed_df.columns):
        ax = axes[i]
        ax.bar(summed_df.index, summed_df[feature])
        ax.set_title(feature)
        ax.set_xlabel("Artist")
        ax.set_ylabel("Sum of " + feature)
        ax.tick_params(axis="x", rotation=90)
    plt.tight_layout()
    plt.show()


def correlation_matrix():
    """
    Generates correlation_matrix for all of the features.

    Args:
        None.

    Returns:
        None.
    """
    all_data = pd.read_csv("all_tracks.csv")
    all_df = pd.DataFrame(all_data)

    columns_to_include = [
        "valence",
        "acousticness",
        "instrumentalness",
        "speechiness",
    ]
    numeric_df = all_df[columns_to_include]

    corr_matrix = numeric_df.corr()

    plt.figure(figsize=(8, 6))
    plt.imshow(corr_matrix, cmap="coolwarm", interpolation="nearest")
    plt.colorbar(label="Correlation coefficient")
    plt.title("Correlation Matrix")
    plt.xticks(np.arange(len(corr_matrix)), corr_matrix.columns, rotation=45)
    plt.yticks(np.arange(len(corr_matrix)), corr_matrix.columns)
    plt.xlabel("Features")
    plt.ylabel("Features")
    plt.show()


def track_scatterplot_matrix():
    """
    Create a scatteplot matrix for all songs.

    Args:
        None.

    Returns
        None.
    """
    all_data = pd.read_csv("all_tracks.csv")
    all_df = pd.DataFrame(all_data)

    matrix = pd.plotting.scatter_matrix(
        all_df[["valence", "acousticness", "instrumentalness", "speechiness"]],
        figsize=(10, 10),
        marker="o",
        alpha=0.7,
    )
    for ax in matrix.ravel():
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    plt.show()


def feature_box_plot():
    """
    Generates box plots using all tracks for each feature.

    Args:
        None.

    Returns:
        None.
    """
    all_data = pd.read_csv("all_tracks.csv")
    all_df = pd.DataFrame(all_data)

    columns_to_keep = [
        "valence",
        "acousticness",
        "instrumentalness",
        "speechiness",
    ]
    subset_df = all_df[columns_to_keep]
    feature_columns = subset_df

    plt.figure(figsize=(10, 5))

    for i, feature in enumerate(feature_columns, 1):
        plt.subplot(1, 4, i)
        plt.boxplot(all_df[feature])
        plt.title(feature + " of all songs")

    plt.tight_layout()
    plt.show()


def single_artist_box():
    """
    Generates box plots for all artists for each feature.

    Args:
        None.

    Returns:
        None.
    """
    all_data = pd.read_csv("all_tracks.csv")
    all_df = pd.DataFrame(all_data)

    df = all_df[
        [
            "artist_name",
            "valence",
            "acousticness",
            "instrumentalness",
            "speechiness",
        ]
    ]
    unique_artists = df["artist_name"].unique()

    _, axes = plt.subplots(4, 9, figsize=(15, 9), sharex=True)

    min_value = (
        df[["valence", "acousticness", "instrumentalness", "speechiness"]]
        .min()
        .min()
    )
    max_value = (
        df[["valence", "acousticness", "instrumentalness", "speechiness"]]
        .max()
        .max()
    )

    # iterate for each artist
    for i, artist in enumerate(unique_artists):
        artist_df = df[df["artist_name"] == artist]
        if pd.isnull(artist):
            continue
        # iterate over each feature
        for j, feature in enumerate(
            ["valence", "acousticness", "instrumentalness", "speechiness"]
        ):
            sns.boxplot(y=artist_df[feature], ax=axes[j, i])
            axes[j, i].set_ylim(min_value, max_value)

            if i == 0:
                axes[j, i].set_ylabel(feature)
            if j == 0:
                axes[j, i].set_title(artist)

    plt.tight_layout()
    plt.show()
