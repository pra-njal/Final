import pandas as pd
import streamlit as st
import plotly.express as px

#loading spotify data
spotify_data = pd.read_csv("songs_normalize.csv")

#set the page title
st.set_page_config(page_title="Spotify Dashboard", page_icon=":musical_note:")

# Define custom CSS for the dashboard background with the image
background = """
<style>
body {
    background-image: url('C:/Users/hp/Downloads/GoOnlineTools-image-downloader.jpg');
    background-size: cover;
}
</style>
"""

st.markdown(background, unsafe_allow_html=True)

# Display Spotify logo and title horizontally
col1, col2 = st.columns([2, 3])

# Displaying dashboard title
with col1:
    spotify_logo_url = "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg"
    st.image(spotify_logo_url, width=100) 

# Displaying logo
with col2:
    st.title("Spotify Dashboard")

#sidebar dropdowns
selected_feature = st.sidebar.selectbox("select Feature", spotify_data.columns)

# Subsetting data to a smaller sample
subset_data = spotify_data.sample(n=1000, random_state=1)

# Summary statistics for the selected feature
summary_stats = subset_data[selected_feature].describe()

# Display summary statistics
st.write(f"Summary Statistics for {selected_feature.capitalize()}:")
st.write(summary_stats)
# Sidebar for selecting page
page = st.sidebar.selectbox("Select type of Chart", ["Histogram", "Bar Chart", "Scatter Plot,Box Plot, Pie&Line Chart"])

# Sidebar description
st.sidebar.write(
    """
    This dashboard provides insights into Spotify songs data. You can explore different features of the songs dataset using the options on the sidebar. 
    You can select a feature to view its summary statistics, choose a page to visualize different aspects of the data such as histograms, bar charts, scatter plots, pie charts, and line charts.
    """
)

if page == "Histogram":
    # Plot the histogram based on the selected feature
    fig = px.histogram(spotify_data, x=selected_feature, template='plotly_dark', marginal='box', title=f'Distribution of {selected_feature}')
    st.plotly_chart(fig)

    # Visualizing total songs based on genres
    fig_genre_count = px.histogram(spotify_data.groupby('genre', as_index=False).count().sort_values(by='song', ascending=False),
                                   x='genre', y='song', color_discrete_sequence=['green'],
                                   template='plotly_dark', marginal='box', title='Total songs based on genres',width=800,height=600)
    fig_genre_count.update_layout(title_x=0.5)
    st.plotly_chart(fig_genre_count)

    # Visualizing popular genres based on popularity
    fig_genre_popularity = px.histogram(spotify_data.groupby('genre', as_index=False).sum().sort_values(by='popularity', ascending=False),
                                        x='genre', y='popularity', color_discrete_sequence=['lightgreen'],
                                        template='plotly_dark', marginal='box', title='Popular genres based on popularity',width=800,height=600)
    fig_genre_popularity.update_layout(title_x=0.5)
    st.plotly_chart(fig_genre_popularity)

elif page == "Bar Chart":
    # Bar chart for list of songs recorded by each singer
    fig_total_songs = px.bar(spotify_data.groupby('artist', as_index=False).count().sort_values(by='song', ascending=False).head(50),
                             x='artist', y='song', labels={'song': 'Total Songs'}, width=1000,
                             color_discrete_sequence=['green'], text='song', title='<b>List of Songs Recorded by Each Singer')
    st.plotly_chart(fig_total_songs)

    # Bar chart for top 30 popular singers
    fig_popular_singers = px.bar(spotify_data.groupby('artist', as_index=False).sum().sort_values(by='popularity', ascending=False).head(30),
                                  x='artist', y='popularity', color_discrete_sequence=['lightgreen'],
                                  template='plotly_dark', text='popularity', title='<b>Top 30 Popular Singers')
    st.plotly_chart(fig_popular_singers)

elif page == "Scatter Plot,Box Plot, Pie&Line Chart":
    # Create the scatter plot
    scatter_options = {
        "Tempo vs Popularity": ["tempo", "popularity"],
        "Speechiness vs Popularity": ["speechiness", "popularity"],
        "Energy vs Danceability": ["energy", "danceability"]
    }
    selected_scatter = st.sidebar.selectbox("Select a scatter plot", list(scatter_options.keys()))

    # Get selected scatter plot parameters
    x_feature, y_feature = scatter_options[selected_scatter]

    # Create the scatter plot
    fig_scatter = px.scatter(spotify_data, x=x_feature, y=y_feature, color=y_feature, color_continuous_scale='Plasma',
                             template='plotly_dark', title=f'<b>{selected_scatter}')
    st.plotly_chart(fig_scatter)

    # Create the pie chart
    fig_pie = px.pie(spotify_data.groupby('explicit', as_index=False).count().sort_values(by='song', ascending=False),
                      names='explicit', values='song', labels={'song': 'Total songs'}, hole=.6,
                      color_discrete_sequence=['green', 'crimson'], template='plotly_dark',
                      title='<b>Songs having explicit content')
    fig_pie.update_layout(title_x=0.5)
    st.plotly_chart(fig_pie)

    # Create the box plot
    fig_box = px.box(spotify_data, x='explicit', y='popularity', color='explicit',
                     template='plotly_dark', color_discrete_sequence=['cyan', 'magenta'],
                     title='<b>Popularity based on explicit content')
    st.plotly_chart(fig_box)

    # Create the line plot
    fig_line = px.line(spotify_data.sort_values(by='popularity', ascending=False).head(25),
                       x='song', y='popularity', hover_data=['artist'],
                       color_discrete_sequence=['green'], markers=True,
                       title='<b>Top 25 songs in Spotify')
    st.plotly_chart(fig_line)
