import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

st.title('Hours of sunshine in US cities')

#DATE_COLUMN = 'date/time'
#DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows=None):
    df = pd.read_csv("sunshine.csv", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    df.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return df

data_load_state = st.text('Loading data...')
df = load_data()
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)

st.subheader('Annual sunshine data in US cities')
# hist_values = np.histogram(data["month"], bins=12, range=(0,12))[0]
# st.bar_chart(hist_values)

hov_data = {
    'sunshine': True,
    'city': False,
    'month': True
}
fig = px.scatter(df, x='month', y='sunshine', size='sunshine', 
                 color='city', 
                 hover_data=hov_data,#['sunshine'],
                 hover_name='city',
                 #title=' Annual sunshine data in US cities',
                 size_max=25)

# Create a horizontal line for the mean sunshine hours
mean_sunshine = df['sunshine'].mean()
mean_line = go.layout.Shape(type='line',
                            xref='paper', yref='y',
                            x0=0, x1=1, y0=mean_sunshine, y1=mean_sunshine,
                            line=dict(color='red', dash='dash'))

#fig.update_traces(mode="markers")

# Customize the chart layout
fig.update_layout(
    xaxis_title='Month',
    yaxis_title='Hours of sunshine',
    legend_title='City',
    hovermode='closest',
    hoverlabel=dict(
        bgcolor="white",
        font_size=17,
        font_family="Arial"
    ),
    font=dict(
        family="Arial",
        size=17
    ),
    shapes=[mean_line],
    xaxis=dict(
        showspikes=True,
        spikemode='across',
        spikedash='dot',
        spikethickness=1,
        spikecolor='grey',
        showline=True,
        linewidth=1,
        linecolor='grey',
        mirror=True
    ),
    yaxis=dict(
        showspikes=True,
        spikemode='across',
        spikedash='dot',
        spikethickness=1,
        spikecolor='grey',
        showline=True,
        linewidth=1,
        linecolor='grey',
        mirror=True
    ),
    height=500, width=800
)

# Show the chart in app
#fig.show()
st.plotly_chart(fig, theme=None)

#add histogram
##city to filter
city_to_filter = st.selectbox('city', df['city'].unique())
filtered_city = df[df['city'] == city_to_filter]
st.subheader('sunshine hours per city')
# Create the plot
fig_city = px.scatter(filtered_city, x="month", y="sunshine", 
                      color="city",
                      hover_data=hov_data,
                      size="sunshine")

# Define the layout
fig_city.update_layout(
    xaxis_title="Month",
    yaxis_title="Hours of Sunshine",
    font=dict(
        family="Arial",
        size=18,
        color="black"
        ),
    height=500, width=800
    )

# Show the chart in app
st.plotly_chart(fig_city, theme=None)

#hist_values = np.histogram(filtered_city["sunshine"], bins=12, range=(0,12))[0]
#st.bar_chart(hist_values)

# Some number in the range 0-12
# hour_to_filter = st.slider('month', 0, 12, 17)
# filtered_data = df[["lat", "lon", "sunshine"]]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)