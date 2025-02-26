import time
import threading
import itertools
from collections import deque

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pythonping import ping

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource, HoverTool, CheckboxGroup, CustomJS
from bokeh.layouts import column
from bokeh.palettes import Category20

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

# CSV must have columns: Short Name, Full Name, IP, Note, MapX, MapY
CSV_FILE = "pingtargets.csv"

# Default ping interval (seconds). 
# The user can override this via the Settings page.
PING_INTERVAL = 10

# Possible intervals in seconds + human labels
PING_INTERVAL_OPTIONS = [
    (3600,  "1 hour"),
    (1800,  "30 minutes"),
    (600,   "10 minutes"),
    (300,   "5 minutes"),
    (60,    "1 minute"),
    (30,    "30 seconds"),
    (10,    "10 seconds (default)"),
]

MAX_PING_HISTORY = 30
HIGH_PING_THRESHOLD = 50  # ms above which we consider "High Ping"

# -------------------------------------------------------------------
# Read CSV file
# -------------------------------------------------------------------
df_cols = ["Short Name", "Full Name", "IP", "Note", "MapX", "MapY"]
targets_df = pd.read_csv(CSV_FILE)

# If the CSV might not have MapX/MapY, make sure those columns exist:
for col in ["MapX", "MapY"]:
    if col not in targets_df.columns:
        targets_df[col] = 0  # default to 0 if missing

targets_df = targets_df[df_cols]  # Reorder or ensure columns

# Convert MapX/MapY to numeric, ignoring errors
targets_df["MapX"] = pd.to_numeric(targets_df["MapX"], errors="coerce").fillna(0)
targets_df["MapY"] = pd.to_numeric(targets_df["MapY"], errors="coerce").fillna(0)

# In-memory ping data structures
ping_data = {}
latest_status = {}

for idx, row in targets_df.iterrows():
    short_name = row["Short Name"]
    ping_data[short_name] = deque(maxlen=MAX_PING_HISTORY)
    latest_status[short_name] = {"ping": None, "status": "Unknown"}

# -------------------------------------------------------------------
# Background ping thread
# -------------------------------------------------------------------
def ping_devices():
    global PING_INTERVAL
    while True:
        for idx, row in targets_df.iterrows():
            short_name = row["Short Name"]
            ip = row["IP"]
            try:
                response_list = ping(ip, count=1, timeout=1)
                rtt_avg_ms = response_list.rtt_avg_ms
                if response_list.packets_lost > 0:
                    # Unreachable
                    ping_data[short_name].append(None)
                    latest_status[short_name]["ping"] = None
                    latest_status[short_name]["status"] = "Unreachable"
                else:
                    # Success
                    ping_data[short_name].append(rtt_avg_ms)
                    latest_status[short_name]["ping"] = rtt_avg_ms
                    if rtt_avg_ms > HIGH_PING_THRESHOLD:
                        latest_status[short_name]["status"] = "High Ping"
                    else:
                        latest_status[short_name]["status"] = "OK"
            except Exception:
                ping_data[short_name].append(None)
                latest_status[short_name]["ping"] = None
                latest_status[short_name]["status"] = "Unreachable"

        time.sleep(PING_INTERVAL)

thread = threading.Thread(target=ping_devices, daemon=True)
thread.start()

# -------------------------------------------------------------------
# Helper: update the CSV if positions change
# -------------------------------------------------------------------
def update_map_position(short_name, new_x, new_y):
    """
    Called when user drags a device label to new coords.
    We update the in-memory DataFrame and rewrite CSV.
    """
    global targets_df
    # Find the row for short_name
    mask = (targets_df["Short Name"] == short_name)
    if not mask.any():
        return False  # not found, do nothing

    targets_df.loc[mask, "MapX"] = new_x
    targets_df.loc[mask, "MapY"] = new_y
    targets_df.to_csv(CSV_FILE, index=False)
    return True

# -------------------------------------------------------------------
# Flask app
# -------------------------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.route("/")
def index():
    """
    Home page: side-by-side layout
    - Device status table (left)
    - Ping history (right)
    """
    # Build Bokeh plot
    p = figure(
        title="Recent Ping Times", 
        x_axis_label="Most Recent Pings (Oldest on left)",
        y_axis_label="Ping (ms)",
        width=600,
        height=400,
        toolbar_location="above"
    )
    p.add_tools(HoverTool(tooltips=[("Ping", "@y")]))

    # Distinct colors for each device
    color_cycle = itertools.cycle(Category20[20])
    lines = []
    labels = []
    for short_name, pings in ping_data.items():
        x_vals = list(range(-len(pings), 0))
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

    checkbox = CheckboxGroup(labels=labels, active=list(range(len(labels))))
    checkbox_callback = CustomJS(args=dict(lines=lines, checkbox=checkbox), code="""
        for (var i = 0; i < lines.length; i++) {
            lines[i].visible = false;
        }
        for (const idx of checkbox.active) {
            lines[idx].visible = true;
        }
    """)
    checkbox.js_on_change('active', checkbox_callback)

    layout = column(checkbox, p)
    script, div = components(layout)
    bokeh_resources = CDN.render()

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
    Page to choose a new PING_INTERVAL from a dropdown.
    """
    global PING_INTERVAL
    if request.method == "POST":
        new_interval_str = request.form.get("ping_interval")
        if new_interval_str:
            try:
                PING_INTERVAL = int(new_interval_str)
            except ValueError:
                pass
        return redirect(url_for("settings"))

    return render_template(
        "settings.html",
        current_interval=PING_INTERVAL,
        interval_options=PING_INTERVAL_OPTIONS
    )


@app.route("/map")
def school_map():
    """
    Shows the school map with devices overlaid. 
    We also have a button to toggle edit mode (JS-based).
    """
    return render_template(
        "map.html",
        targets_df=targets_df,
        latest_status=latest_status
    )


@app.route("/map/save_position", methods=["POST"])
def save_position():
    """
    AJAX endpoint: receives JSON { short_name, x, y } 
    and writes them to CSV via update_map_position().
    """
    data = request.get_json()
    short_name = data.get("short_name")
    new_x = data.get("x")
    new_y = data.get("y")
    if not short_name or new_x is None or new_y is None:
        return jsonify({"success": False, "message": "Missing data"}), 400
    
    ok = update_map_position(short_name, new_x, new_y)
    if not ok:
        return jsonify({"success": False, "message": "Device not found"}), 404
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
