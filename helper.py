from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

# Fetch Statistics Function
def fetch_stats(selected_user, df):
    """
    Fetch statistics such as the number of messages, words, and media messages
    for a selected user or overall chat.

    Args:
        selected_user (str): The user for whom analysis is to be performed.
        df (DataFrame): The processed chat DataFrame.

    Returns:
        tuple: Number of messages, total word count, and number of media messages.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]

    # Total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>/n'].shape[0]

    return num_messages, len(words), num_media_messages


# Most Busy User Function
def most_busy_user(df):
    """
    Identify the most active users in the group chat.

    Args:
        df (DataFrame): The processed chat DataFrame.

    Returns:
        tuple: A Series of top users and a DataFrame with user activity percentages.
    """
    # Top users by message count
    x = df['user'].value_counts().head()

    # Percentage of activity per user
    new_df = (
        round((df['user'].value_counts() / df.shape[0]) * 100, 2)
        .reset_index()
        .rename(columns={'index': 'name', 'user': 'percent'})
    )

    return x, new_df


# Create WordCloud Function
def create_wordcloud(selected_user, df):
    """
    Generate a WordCloud based on the messages of the selected user or the overall chat.

    Args:
        selected_user (str): The user for whom the WordCloud is to be generated.
        df (DataFrame): The processed chat DataFrame.

    Returns:
        WordCloud: A WordCloud object.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Create WordCloud
    wc = WordCloud(
        width=500, height=500, min_font_size=10, background_color='white'
    )
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc
def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "," + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()





