import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title('Chat analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt user", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_message = helper.fetch_stats(selected_user,df)
        st.title("Chat statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Number of Words")
            st.title(words)
        with col3:
            st.header("Total Number of Media")
            st.title(num_media_message)

        # time line stats
        st.title('monthly timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        st.pyplot(fig)

        # finding busiest user
        if selected_user == 'Overall':
            st.title("Most busy user")
            x,new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Wordcloud
        st.title("Most frequent words")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig,ax = plt.subplot()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most common Words")
        st.pyplot(fig)


