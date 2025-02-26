import time
import threading
import itertools
from collections import deque

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from pythonping import ping

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource, HoverTool, CheckboxGroup, CustomJS
from bokeh.layouts import column, row
from bokeh.palettes import Category20

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

# Ping interval (seconds). We initialize a default. 
# This will be updated via the Settings page if the user changes it.
PING_INTERVAL = 10

# We define multiple possible intervals (seconds). You could expand these if desired.
PING_INTERVAL_OPTIONS = [
    (3600,  "1 hour"),
    (1800,  "30 minutes"),
    (600,   "10 minutes"),
    (300,   "5 minutes"),
    (60,    "1 minute"),
    (30,    "30 seconds"),
    (10,    "10 seconds (default)"),
]

MAX_PING_HISTORY = 30    # How many recent pings to keep for graphing
HIGH_PING_THRESHOLD = 50 # ms above which we consider "high ping"
CSV_FILE = "pingtargets.csv"  # The CSV file path

# -------------------------------------------------------------------
# Read CSV file into a DataFrame (comma-separated)
# -------------------------------------------------------------------
targets_df = pd.read_csv(CSV_FILE, sep=",")

# Create structures for storing ping history and status
ping_data = {}
latest_status = {}

# Initialize for each row in the CSV
for idx, row in targets_df.iterrows():
    short_name = row["Short Name"]
    ping_data[short_name] = deque(maxlen=MAX_PING_HISTORY)
    latest_status[short_name] = {"ping": None, "status": "Unknown"}

# -------------------------------------------------------------------
# Background thread for pinging
# -------------------------------------------------------------------
def ping_devices():
    global PING_INTERVAL
    while True:
        # Ping each device in the CSV once
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
            except Exception:
                # On any error, mark unreachable
                ping_data[short_name].append(None)
                latest_status[short_name]["ping"] = None
                latest_status[short_name]["status"] = "Unreachable"

        # After all pings, sleep for the configured interval
        time.sleep(PING_INTERVAL)

# Start the background ping thread
thread = threading.Thread(target=ping_devices, daemon=True)
thread.start()

# -------------------------------------------------------------------
# Flask App
# -------------------------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.route("/")
def index():
    """
    Main page showing:
    - Device Status table on the left
    - Ping History chart and checkboxes on the right
    """
    # Build the Bokeh plot from the current ping data
    p = figure(
        title="Recent Ping Times", 
        x_axis_label="Most Recent Pings (Oldest on left)",
        y_axis_label="Ping (ms)",
        width=600,
        height=400,
        toolbar_location="above"
    )
    p.add_tools(HoverTool(tooltips=[("Ping", "@y")]))

    # We'll cycle through a color palette so each device gets a distinct color
    color_cycle = itertools.cycle(Category20[20])  # 20 distinct colors

    # Create a line on the plot for each short_name
    lines = []
    labels = []
    for short_name, pings in ping_data.items():
        x_vals = list(range(-len(pings), 0))  # e.g. -30..-1
        # Convert None to 0 for the plot
        y_vals_plot = [val if val is not None else 0 for val in pings]
        
        source = ColumnDataSource(data={"x": x_vals, "y": y_vals_plot})
        color = next(color_cycle)

        line_renderer = p.line(
            x="x", 
            y="y", 
            source=source, 
            line_width=2,
            line_color=color,
            legend_label=short_name
        )
        lines.append(line_renderer)
        labels.append(short_name)

    p.legend.click_policy = "hide"

    # A CheckboxGroup so user can selectively show/hide lines
    checkbox = CheckboxGroup(labels=labels, active=list(range(len(lines))))
    checkbox_callback = CustomJS(args=dict(lines=lines, checkbox=checkbox), code="""
        for (var i = 0; i < lines.length; i++) {
            lines[i].visible = false;
        }
        for (const idx of checkbox.active) {
            lines[idx].visible = true;
        }
    """)
    checkbox.js_on_change('active', checkbox_callback)

    # If you prefer the checkboxes to appear above the plot, use column(...).
    # If you want them side by side, use row(...). 
    # For demonstration, we'll keep them stacked:
    bokeh_layout = column(checkbox, p)

    script, div = components(bokeh_layout)
    bokeh_resources = CDN.render()  # ensure Bokeh JS/CSS is included

    return render_template(
        "index.html",
        bokeh_resources=bokeh_resources,
        script=script,
        div=div,
        targets_df=targets_df,
        latest_status=latest_status
    )


@app.route("/settings", methods=["GET", "POST"])
def settings():
    """
    A simple page with a dropdown to set the ping interval (in seconds).
    """
    global PING_INTERVAL

    if request.method == "POST":
        # The form field is named 'ping_interval' 
        new_interval_str = request.form.get("ping_interval")
        if new_interval_str is not None:
            try:
                new_val = int(new_interval_str)
                PING_INTERVAL = new_val
            except ValueError:
                pass
        # After saving, redirect so a refresh doesn't resubmit the form
        return redirect(url_for("settings"))

    return render_template(
        "settings.html",
        current_interval=PING_INTERVAL,
        interval_options=PING_INTERVAL_OPTIONS
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
