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
CSV_FILE = "pingtargets.csv"

PING_INTERVAL = 10
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
HIGH_PING_THRESHOLD = 50

# Known device types (or gather them from CSV)
ALL_DEVICE_TYPES = [
    "AP",
    "Wired_PC",
    "Media_Device",
    "Wireless_Device",
    "Network_Switch",
    "Server",
    "Firewall",
    "Juniper",
    "Gateway_to_ISP",
    "Printer",
    "Other"
]

# By default, show all device types
VISIBLE_DEVICE_TYPES = set(ALL_DEVICE_TYPES)

# -------------------------------------------------------------------
# Read CSV, ensure columns
# -------------------------------------------------------------------
EXPECTED_COLS = [
    "Short Name","Full Name","IP","Note",
    "MapX","MapY","FantX","FantY","Device Type","FantName"
]
df = pd.read_csv(CSV_FILE)

for col in EXPECTED_COLS:
    if col not in df.columns:
        if col == "Device Type":
            df[col] = "Other"
        elif col in ["MapX","MapY","FantX","FantY"]:
            df[col] = 0
        else:
            df[col] = ""

df["MapX"]   = pd.to_numeric(df["MapX"],   errors="coerce").fillna(0)
df["MapY"]   = pd.to_numeric(df["MapY"],   errors="coerce").fillna(0)
df["FantX"]  = pd.to_numeric(df["FantX"],  errors="coerce").fillna(0)
df["FantY"]  = pd.to_numeric(df["FantY"],  errors="coerce").fillna(0)

df = df[EXPECTED_COLS]
df.to_csv(CSV_FILE, index=False)

targets_df = df.copy()

# -------------------------------------------------------------------
# In-memory ping data
# -------------------------------------------------------------------
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
                    ping_data[short_name].append(None)
                    latest_status[short_name]["ping"] = None
                    latest_status[short_name]["status"] = "Unreachable"
                else:
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
# Helpers to update positions
# -------------------------------------------------------------------
def update_map_position(short_name, x, y):
    mask = (targets_df["Short Name"] == short_name)
    if not mask.any():
        return False
    targets_df.loc[mask, "MapX"] = x
    targets_df.loc[mask, "MapY"] = y
    targets_df.to_csv(CSV_FILE, index=False)
    return True

def update_fantasy_position(short_name, x, y):
    mask = (targets_df["Short Name"] == short_name)
    if not mask.any():
        return False
    targets_df.loc[mask, "FantX"] = x
    targets_df.loc[mask, "FantY"] = y
    targets_df.to_csv(CSV_FILE, index=False)
    return True

# -------------------------------------------------------------------
# Flask App
# -------------------------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.route("/")
def index():
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


@app.route("/settings", methods=["GET","POST"])
def settings():
    """
    Settings page: 
      - Adjust ping interval
      - Check/uncheck device types to display
    """
    global PING_INTERVAL, VISIBLE_DEVICE_TYPES

    if request.method == "POST":
        # 1) Handle ping interval
        new_interval_str = request.form.get("ping_interval")
        if new_interval_str:
            try:
                PING_INTERVAL = int(new_interval_str)
            except ValueError:
                pass

        # 2) Handle device type checkboxes
        # 'device_types' is the name attribute in the checkboxes
        selected_types = request.form.getlist("device_types")
        # Convert to set
        VISIBLE_DEVICE_TYPES = set(selected_types)

        return redirect(url_for("settings"))

    return render_template(
        "settings.html",
        current_interval=PING_INTERVAL,
        interval_options=PING_INTERVAL_OPTIONS,
        all_device_types=ALL_DEVICE_TYPES,
        visible_device_types=VISIBLE_DEVICE_TYPES
    )


@app.route("/map")
def school_map():
    """
    Original map page. 
    Only show rows whose device type is in VISIBLE_DEVICE_TYPES
    """
    return render_template(
        "map.html",
        targets_df=targets_df,
        latest_status=latest_status,
        visible_device_types=VISIBLE_DEVICE_TYPES
    )


@app.route("/map/save_position", methods=["POST"])
def save_position():
    data = request.get_json()
    short_name = data.get("short_name")
    x = data.get("x")
    y = data.get("y")

    if not short_name or x is None or y is None:
        return jsonify({"success": False, "message": "Missing data"}), 400

    ok = update_map_position(short_name, x, y)
    if not ok:
        return jsonify({"success": False, "message": "Device not found"}), 404
    return jsonify({"success": True})


@app.route("/fantasymap")
def fantasy_map():
    """
    Fantasy map page. 
    Only show device types in VISIBLE_DEVICE_TYPES
    """
    return render_template(
        "fantasymap.html",
        targets_df=targets_df,
        latest_status=latest_status,
        visible_device_types=VISIBLE_DEVICE_TYPES
    )


@app.route("/fantasymap/save_position", methods=["POST"])
def save_fantasy_position():
    data = request.get_json()
    short_name = data.get("short_name")
    x = data.get("x")
    y = data.get("y")

    if not short_name or x is None or y is None:
        return jsonify({"success": False, "message": "Missing data"}), 400

    ok = update_fantasy_position(short_name, x, y)
    if not ok:
        return jsonify({"success": False, "message": "Device not found"}), 404
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
