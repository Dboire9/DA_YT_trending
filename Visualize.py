import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import isodate



yt_file = 'youtube_top_1000_videos_FR.csv'
df = pd.read_csv(yt_file)


# Checking if there are any null values in the dataset
nulls = pd.DataFrame(df.isnull().sum().sort_values(ascending=False))
nulls.columns = ['Null Count']
nulls.index.name = 'Feature'
# print(nulls)

# Views vs. Likes scatter plot
plt.figure(figsize=(8, 5))
sns.scatterplot(x='LikeCount', y='viewCount', data=df)
plt.title('View Count vs. Like Count')
plt.xlabel('Like Count')
plt.ylabel('View Count')


plt.figure(figsize=(8, 5))
sns.scatterplot(x='subscriberCount', y='viewCount', data=df)
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.title('View Count vs. Subscriber Count')
plt.xlabel('Subscriber Count')
plt.ylabel('View Count')


df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
# Extract hour
df['publishedHour'] = df['publishedAt'].dt.hour

plt.figure(figsize=(8, 5))
ax1 = plt.gca()
sns.countplot(x='publishedHour', data=df, palette='Set3', ax=ax1)
ax1.set_title('Number of Videos and Total Views per Hour')
ax1.set_xlabel('Hour of Publication')
ax1.set_ylabel('Number of Videos')

# Calculate total views per hour
hourly_views = df.groupby('publishedHour')['viewCount'].sum().reset_index()

# Plot total views as a line on a secondary y-axis
ax2 = ax1.twinx()
sns.lineplot(x='publishedHour', y='viewCount', data=hourly_views, color='red', marker='o', ax=ax2)
ax2.set_ylabel('Total Views', color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# plt.show()


# Extract day of the week (0=Monday, 6=Sunday)
df['publishedDay'] = df['publishedAt'].dt.dayofweek
# Map numbers to weekday names
weekday_map = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
df['publishedDayName'] = df['publishedDay'].map(weekday_map)

daily_views = df.groupby('publishedDayName').agg(
    video_count=('videoId', 'count'),
    total_views=('viewCount', 'sum')
).reindex(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']).reset_index()


# Bar plot: number of videos per day
fig, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(x='publishedDayName', y='video_count', data=daily_views, palette='Set2', ax=ax1)
ax1.set_title('Number of Videos and Total Views per Day of Week')
ax1.set_xlabel('Day of Week')
ax1.set_ylabel('Number of Videos', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Line plot: total views per day (secondary y-axis)
ax2 = ax1.twinx()
sns.lineplot(x='publishedDayName', y='total_views', data=daily_views, color='red', marker='o', ax=ax2)
ax2.set_ylabel('Total Views', color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
# plt.show()


#Live Broadcast Content ? 
df['isLive'] = df['liveBroadcastContent'].apply(lambda x: 'Yes' if x == 'live' else 'No')

plt.figure(figsize=(8, 5))
sns.countplot(x='isLive', data=df, palette='Set2')
plt.title('Number of Live vs. Non-Live Videos')
plt.xlabel('Was Live Broadcast?')
plt.ylabel('Number of Videos')
plt.show()