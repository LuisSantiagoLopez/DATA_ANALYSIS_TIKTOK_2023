
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
from matplotlib.ticker import ScalarFormatter
import matplotlib.ticker as ticker

# Function to get the IDs of the most viewed videos within the last three months
def get_most_viewed_recent_videos(file_path):
    df = pd.read_csv(file_path)
    df['createTimeISO'] = pd.to_datetime(df['createTimeISO'])
    last_three_months = df['createTimeISO'].max() - timedelta(days=90)
    recent_df = df[df['createTimeISO'] > last_three_months]
    sorted_recent_df = recent_df.sort_values(by='Plays', ascending=False)
    top_10_recent_videos = sorted_recent_df.head(10)
    return top_10_recent_videos['id'].tolist()

# Function to get the IDs of the most viral videos of all time
def get_most_viral_videos(file_path):
    df = pd.read_csv(file_path)
    df['createTimeISO'] = pd.to_datetime(df['createTimeISO'])
    sorted_df = df.sort_values(by='Plays', ascending=False)
    top_10_viral_videos = sorted_df.head(10)
    return top_10_viral_videos['id'].tolist()

# Function to create the scatter plot focusing on videos with over 1 million views
def create_scatter_plot(file_path):
    df = pd.read_csv(file_path)
    df['createTimeISO'] = pd.to_datetime(df['createTimeISO'])
    df_filtered = df[df['Plays'] > 1_000_000]
    plt.figure(figsize=(15, 10))
    distinct_colors = plt.cm.rainbow(np.linspace(0, 1, len(df_filtered['searchHashtag/name'].unique())))
    legend_labels = []
    for idx, (hashtag, group) in enumerate(df_filtered.groupby('searchHashtag/name')):
        plt.scatter(group['createTimeISO'], group['Plays'], 
                    s=group['Comments'] / 50, 
                    label=f"{hashtag} (#{len(group)} videos)", alpha=0.6, edgecolors='w', 
                    marker='o', c=[distinct_colors[idx]])
        legend_labels.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=distinct_colors[idx], markersize=10))
        for i, video_id in enumerate(group['id']):
            plt.annotate(str(video_id), (group['createTimeISO'].iloc[i], group['Plays'].iloc[i]))
    plt.xlabel('Time')
    plt.ylabel('Views')
    plt.title('TikTok Video Analysis by Views and Comments (1M+ Views)')
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.ylim(1_000_000, 50_000_000)
    y_ticks = [1_000_000, 10_000_000, 20_000_000, 30_000_000, 40_000_000, 50_000_000]
    plt.yticks(y_ticks, [f"{y:,}" for y in y_ticks])
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(legend_labels, df_filtered['searchHashtag/name'].unique(), title='Hashtags')
    plt.show()

# Example usage
if __name__ == '__main__':
    file_path = 'your_file_path_here.csv'
    print("Most viewed videos in the last three months:", get_most_viewed_recent_videos(file_path))
    print("Most viral videos of all time:", get_most_viral_videos(file_path))
    create_scatter_plot(file_path)
