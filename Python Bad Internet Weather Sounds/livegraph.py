from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10
import pandas as pd

# Initialize an empty dictionary to hold data sources for each switch
sources = {}
lines = {}
colors = Category10[10]  # Color palette for up to 10 switches

# Create the figure (replace plot_height and plot_width with height and width)
p = figure(x_axis_type='datetime', title='Ping over Time', height=350, width=800)
p.legend.location = "top_left"
p.legend.click_policy = "hide"
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Ping (ms)'

def update():
    # Read data from the CSV file
    df = pd.read_csv('pings.csv', names=['timestamp', 'switch', 'ping'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Get the latest 1000 data points
    df = df.tail(1000)
    
    # Group the data by switch
    groups = df.groupby('switch')
    
    for i, (switch, group) in enumerate(groups):
        if switch not in sources:
            # Initialize a new data source for the switch
            sources[switch] = ColumnDataSource(data=dict(x=[], y=[]))
            color = colors[i % len(colors)]
            # Add a new line to the plot for the switch
            line = p.line('x', 'y', source=sources[switch], color=color, legend_label=switch)
            lines[switch] = line
        # Update the data source with the latest data
        sources[switch].data = dict(x=group['timestamp'], y=group['ping'])

# Add the periodic callback
curdoc().add_periodic_callback(update, 1000)  # Update every 1000 milliseconds

# Add the figure to the current document
curdoc().add_root(p)
