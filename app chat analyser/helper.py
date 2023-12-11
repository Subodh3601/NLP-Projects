from wordcloud import WordCloud
import pandas as pd
from collections import Counter


def fetch_stats(selected_user, df):

    if selected_user == 'overall':
        # 1.fetch number og messages
        num_messages = df.shape[0]
        # 2. fetch number of words
        words = []
        for word in df['message']:
            words.extend(word.split())

        # 3. fetch number of media messages
        num_media_message = df[df['message'] == '<Media omitted>/n'].shape[0]
        return num_messages, len(words), num_media_message
    else:
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]
        words = []
        for word in new_df['message']:
            words.extend(word.split())

        # 3. fetch number of media messages
        num_media_message = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]

        return num_messages, len(words), num_media_message

def most_busy_user(df):
    x = x=df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percentage'})
    return x,df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'black')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for word in temp['message']:
        words.extend(word.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline