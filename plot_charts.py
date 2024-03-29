"""
module for creating graphs
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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

    #create legend for 'Instrumentalness' color values
    plt.colorbar(averages_scatter, label="Instrumentalness")

    #create legend for 'Speechiness' size values
    plt.scatter([], [], s=0, label="Speechiness")
    size_labels = [0.2, 0.15, 0.1, 0.05]
    for size in size_labels:
        plt.scatter([], [], s=size * 3000, label=f"{size}", alpha=0.5)
    plt.legend()

    #label each point with artist name
    texts = []
    for i, artist_name in enumerate(average_df['artist_name']):
        texts.append(plt.text(average_df['valence'][i],
                              average_df['acousticness'][i], artist_name))
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

    grouped = all_df.groupby('artist_name').sum()

    #finds sum for each feature, new values placed in own dataframe
    summed_df = grouped[['valence', 'acousticness', 'instrumentalness', 'speechiness']]

    #plot
    fig, axes = plt.subplots(1, 4, figsize=(40, 8))  # 1 row, 4 columns for 4 features

    for i, feature in enumerate(summed_df.columns):
        ax = axes[i]
        ax.bar(summed_df.index, summed_df[feature])
        ax.set_title(feature)
        ax.set_xlabel('Artist')
        ax.set_ylabel('Sum of ' + feature)
    plt.tight_layout()
    plt.show()
def correlation_matrix():
    all_data = pd.read_csv("all_tracks.csv")
    all_df = pd.DataFrame(all_data)

    columns_to_include = ['valence', 'acousticness', 'instrumentalness', 'speechiness']
    numeric_df = all_df[columns_to_include]

    corr_matrix = numeric_df.corr()

    plt.figure(figsize=(8, 6))
    plt.imshow(corr_matrix, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(label='Correlation coefficient')
    plt.title('Correlation Matrix')
    plt.xticks(np.arange(len(corr_matrix)), corr_matrix.columns, rotation=45)
    plt.yticks(np.arange(len(corr_matrix)), corr_matrix.columns)
    plt.xlabel('Features')
    plt.ylabel('Features')
    plt.show()
    return
def tracks_color_bubble():
    """
    Generates colored bubble chart, with x- and y- axis as the first two
    variables, color as the third variable, and the size of bubble as fourth
    point.

    Args:
        None.

    Returns
    """
    all_data = pd.read_csv("all_tracks.csv")
    all_df = pd.DataFrame(all_data)

    color_map = plt.cm.get_cmap('tab10')

    # Extract unique artist names
    artists = all_df['artist_name'].unique()

    # Assign a unique color to each artist
    colors = {artist: color_map(i) for i, artist in enumerate(artists)}

    # Scatterplot matrix
    pd.plotting.scatter_matrix(all_df[['valence', 'acousticness', 'instrumentalness', 'speechiness']], figsize=(10, 10), c=all_df['artist_name'].apply(lambda x: colors[x]), marker='o', alpha=0.7)

    # Add legend
    legend_entries = [plt.Line2D([0], [0], marker='o', color='w', label=artist, markersize=8, markerfacecolor=colors[artist]) for artist in artists]
    plt.legend(handles=legend_entries, loc='upper left')

    plt.show()
def feature_box_plot():
    all_data = pd.read_csv("all_tracks.csv")
    all_df = pd.DataFrame(all_data)

    columns_to_keep = ['valence', 'acousticness', 'instrumentalness', 'speechiness']    
    subset_df = all_df[columns_to_keep]

    # Extracting only the columns relevant for features
    feature_columns = subset_df  # Assuming features start from the 3rd column

    # Plotting boxplots for each feature
    plt.figure(figsize=(5, 10))  # Adjust the figure size if necessary

    for i, feature in enumerate(feature_columns, 1):
        plt.subplot(2, 2, i)  # Adjust subplot layout according to the number of features
        plt.boxplot(all_df[feature])
        plt.title(feature + " of all songs")

    plt.tight_layout()  # Adjust subplot layout to prevent overlapping
    plt.show()

average_color_bubble()
artist_sums_bar()
correlation_matrix()
tracks_color_bubble()
feature_box_plot()