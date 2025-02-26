import time
import threading
from collections import deque

import pandas as pd
from flask import Flask, render_template
from pythonping import ping

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, CheckboxGroup, CustomJS
from bokeh.layouts import column

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
CSV_FILE = "pingtargets.csv"   # The CSV file path
PING_INTERVAL = 10             # Seconds between each ping cycle
MAX_PING_HISTORY = 30          # How many recent pings to keep for graphing
HIGH_PING_THRESHOLD = 50       # ms above which we consider "high ping"

# -------------------------------------------------------------------
# Read CSV file into a DataFrame
#    NOTE: Since your CSV uses commas (as shown in your snippet),
#    we use sep=",". If your headers have extra spaces, you may need
#    something like: df.columns = df.columns.str.strip()
# -------------------------------------------------------------------
targets_df = pd.read_csv(CSV_FILE, sep=",")

# Create a structure to store ping history (rolling) and latest status.
ping_data = {}
latest_status = {}

# Initialize structures for each row in the CSV
for idx, row in targets_df.iterrows():
    short_name = row["Short Name"]
    ping_data[short_name] = deque(maxlen=MAX_PING_HISTORY)
    latest_status[short_name] = {"ping": None, "status": "Unknown"}

# -------------------------------------------------------------------
# Background thread for pinging
# -------------------------------------------------------------------
def ping_devices():
    while True:
        for idx, row in targets_df.iterrows():
            short_name = row["Short Name"]
            ip = row["IP"]
            
            try:
                response_list = ping(ip, count=1, timeout=1)
                rtt_avg_ms = response_list.rtt_avg_ms
                if response_list.packets_lost > 0:
                    # Mark as unreachable
                    ping_data[short_name].append(None)
                    latest_status[short_name]["ping"] = None
                    latest_status[short_name]["status"] = "Unreachable"
                else:
                    # Successful ping
                    ping_data[short_name].append(rtt_avg_ms)
                    latest_status[short_name]["ping"] = rtt_avg_ms
                    if rtt_avg_ms > HIGH_PING_THRESHOLD:
                        latest_status[short_name]["status"] = "High Ping"
                    else:
                        latest_status[short_name]["status"] = "OK"
            except:
                # On any error, mark unreachable
                ping_data[short_name].append(None)
                latest_status[short_name]["ping"] = None
                latest_status[short_name]["status"] = "Unreachable"

        time.sleep(PING_INTERVAL)

# Start background thread
thread = threading.Thread(target=ping_devices, daemon=True)
thread.start()

# -------------------------------------------------------------------
# Flask App
# -------------------------------------------------------------------
app = Flask(__name__)

@app.route("/")
def index():
    # Build the Bokeh plot from the current ping data
    p = figure(
        title="Recent Ping Times", 
        x_axis_label="Most Recent Pings (Oldest on left)",
        y_axis_label="Ping (ms)",
        width=900,
        height=400,
        toolbar_location="above"
    )
    p.add_tools(HoverTool(tooltips=[("Ping", "@y")]))

    # Create a line on the plot for each short_name
    lines = []
    for short_name, pings in ping_data.items():
        # x-values are range(-len(pings), 0)
        x_vals = list(range(-len(pings), 0))
        # Convert None to 0 for the plot
        y_vals_plot = [val if val is not None else 0 for val in pings]

        source = ColumnDataSource(data={"x": x_vals, "y": y_vals_plot})
        line_renderer = p.line(
            x="x", 
            y="y", 
            source=source, 
            line_width=2,
            line_color="blue",
            legend_label=short_name
        )
        lines.append(line_renderer)

    # Let users click legend to hide lines
    p.legend.click_policy = "hide"

    # Alternatively: a CheckboxGroup so user can selectively show lines
    checkbox = CheckboxGroup(labels=list(ping_data.keys()), 
                             active=list(range(len(ping_data))))
    checkbox_callback = CustomJS(args=dict(lines=lines, checkbox=checkbox), code="""
        // Make all lines invisible
        for (var i = 0; i < lines.length; i++) {
            lines[i].visible = false;
        }
        // Activate only the selected ones
        for (const idx of checkbox.active) {
            lines[idx].visible = true;
        }
    """)
    checkbox.js_on_change('active', checkbox_callback)

    layout = column(checkbox, p)
    script, div = components(layout)

    return render_template("index.html",
                           script=script,
                           div=div,
                           targets_df=targets_df,
                           latest_status=latest_status)

if __name__ == "__main__":
    # Run Flask in debug mode on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
