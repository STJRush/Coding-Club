import time
import threading
import itertools
from collections import deque
import csv
import speedtest
from datetime import datetime

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json   # <-- Added import for json
from pythonping import ping

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource, HoverTool, CheckboxGroup, CustomJS
from bokeh.layouts import column
from bokeh.palettes import Category20

import plotly.graph_objects as go

# NEW: Imports for Google Tasks API
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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
VISIBLE_DEVICE_TYPES = set(ALL_DEVICE_TYPES)

# Google Tasks Config
SCOPES_TASKS = ["https://www.googleapis.com/auth/tasks.readonly"]
TASKLIST_NAME = "Current Issues"  # same as before

# -------------------------------------------------------------------
# Create Flask App
# -------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "my_super_secret_key_123"

# -------------------------------------------------------------------
# Read pingtargets.csv
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
df["MapX"]   = pd.to_numeric(df["MapX"], errors="coerce").fillna(0)
df["MapY"]   = pd.to_numeric(df["MapY"], errors="coerce").fillna(0)
df["FantX"]  = pd.to_numeric(df["FantX"], errors="coerce").fillna(0)
df["FantY"]  = pd.to_numeric(df["FantY"], errors="coerce").fillna(0)
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
# Background Ping Thread
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
# Map Position Helpers
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
# Speedtest Scheduling
# -------------------------------------------------------------------
def measure_speed():
    s = speedtest.Speedtest(secure=True)
    download = s.download() / 1e6
    upload = s.upload() / 1e6

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    day_of_week = now.strftime("%A")
    hour = now.hour

    file_empty = False
    try:
        with open("externalSpeeds.csv", "r") as f:
            if not f.read().strip():
                file_empty = True
    except FileNotFoundError:
        file_empty = True

    with open("externalSpeeds.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if file_empty:
            writer.writerow(["Date","Time","Download","Upload","DayOfWeek","Hour"])
        writer.writerow([date_str, time_str, f"{download:.2f}", f"{upload:.2f}", day_of_week, hour])
    return (download, upload)

def speedtest_loop():
    while True:
        now = datetime.now()
        wd = now.weekday()  # Mon=0
        hr = now.hour
        if wd < 5 and 8 <= hr < 16:
            measure_speed()
            time.sleep(1200)
        else:
            time.sleep(300)

threading.Thread(target=speedtest_loop, daemon=True).start()

# -------------------------------------------------------------------
# Compute Typical Averages
# -------------------------------------------------------------------
def get_typical_averages(df):
    if "DayOfWeek" not in df.columns or df["DayOfWeek"].isna().any():
        df["ParsedDate"] = pd.to_datetime(df["Date"], errors="coerce")
        df["DayOfWeek"] = df["ParsedDate"].dt.day_name()
    if "Hour" not in df.columns or df["Hour"].isna().any():
        df["ParsedTime"] = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")
        df["Hour"] = df["ParsedTime"].dt.hour
    grouped = df.groupby(["DayOfWeek","Hour"])["Download"].mean()
    return grouped.to_dict()

# -------------------------------------------------------------------
# New: Google Tasks (Read-Only) Helper Functions
# -------------------------------------------------------------------
def tasks_authenticate():
    creds = None
    if "tasks_credentials" in session:
        try:
            creds = Credentials.from_authorized_user_info(session["tasks_credentials"], SCOPES_TASKS)
            if creds.valid and creds.refresh_token:
                return creds
        except Exception as e:
            session.pop("tasks_credentials", None)
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES_TASKS)
    creds = flow.run_local_server(port=5001, access_type="offline", prompt="consent")
    session["tasks_credentials"] = json.loads(creds.to_json())
    return creds

def get_tasks_readonly():
    """
    Fetches active (non-completed) tasks from the 'Current Issues' task list.
    Returns a list of dictionaries with keys: title and due.
    """
    creds = tasks_authenticate()
    service = build("tasks", "v1", credentials=creds)
    tasklists = service.tasklists().list().execute().get("items", [])
    tasklist_id = None
    for tl in tasklists:
        if tl["title"] == TASKLIST_NAME:
            tasklist_id = tl["id"]
            break
    if not tasklist_id:
        return []
    tasks = service.tasks().list(tasklist=tasklist_id, showCompleted=False, showHidden=False).execute().get("items", [])
    formatted_tasks = []
    for task in tasks:
        formatted_tasks.append({
            "title": task.get("title", "Untitled Task"),
            "due": task.get("due", "No Due Date")
        })
    return formatted_tasks

@app.route("/tasks_login")
def tasks_login():
    # Route to trigger Google Tasks authentication.
    tasks_authenticate()
    return redirect(url_for("settings"))

# -------------------------------------------------------------------
# Flask App Routes
# -------------------------------------------------------------------
@app.route("/")
def index():
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

@app.route("/settings", methods=["GET", "POST"])
def settings():
    global PING_INTERVAL, VISIBLE_DEVICE_TYPES
    if request.method == "POST":
        new_interval_str = request.form.get("ping_interval")
        if new_interval_str:
            try:
                PING_INTERVAL = int(new_interval_str)
            except ValueError:
                pass
        selected_types = request.form.getlist("device_types")
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
    speed_df = pd.read_csv("externalSpeeds.csv")
    speed_df["Date"] = pd.to_datetime(speed_df["Date"], errors="coerce")
    typical_dict = get_typical_averages(speed_df)
    last_row = speed_df.tail(1).iloc[0]
    last_download = last_row["Download"]
    last_upload = last_row["Upload"]
    last_speed_str = f"Down: {last_download:.1f} Mbps / Up: {last_upload:.1f} Mbps"
    last_day = last_row.get("DayOfWeek", None)
    last_hour = last_row.get("Hour", None)
    feedback_msg = ""
    if last_day is not None and last_hour is not None:
        key = (last_day, last_hour)
        typical_val = typical_dict.get(key, None)
        if typical_val is not None:
            if last_download < typical_val * 0.8:
                feedback_msg = (f"Current speed ({last_download:.1f} Mbps) is <strong>SLOWER</strong> "
                                f"than typical ({typical_val:.1f} Mbps) for {last_day} at {last_hour}:00.")
            elif last_download > typical_val * 1.2:
                feedback_msg = (f"Current speed ({last_download:.1f} Mbps) is <strong>FASTER</strong> "
                                f"than typical ({typical_val:.1f} Mbps) for {last_day} at {last_hour}:00!")
            else:
                feedback_msg = (f"Current speed ({last_download:.1f} Mbps) is within the normal range "
                                f"(typical ~{typical_val:.1f} Mbps) for {last_day} at {last_hour}:00.")
        else:
            feedback_msg = f"No historical data found for {last_day} at {last_hour}:00."
    else:
        feedback_msg = "Cannot determine day/hour from the last row. CSV might be missing DayOfWeek/Hour."
    today_str = pd.Timestamp.now().strftime("%Y-%m-%d")
    if "DayOfWeek" not in speed_df.columns:
        speed_df["DayOfWeek"] = speed_df["Date"].dt.day_name()
    if "Hour" not in speed_df.columns:
        speed_df["ParsedTime"] = pd.to_datetime(speed_df["Time"], format="%H:%M:%S", errors="coerce")
        speed_df["Hour"] = speed_df["ParsedTime"].dt.hour
    today_mask = (speed_df["Date"].dt.strftime("%Y-%m-%d") == today_str)
    today_data = speed_df.loc[today_mask].copy()
    typical_vals = []
    for idx, row in today_data.iterrows():
        day = row.get("DayOfWeek", None)
        hr = row.get("Hour", None)
        key = (day, hr)
        typical_vals.append(typical_dict.get(key, None))
    today_data["TypicalAvg"] = typical_vals
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=today_data["Time"],
        y=today_data["Download"],
        mode="lines+markers",
        name="Today",
        line=dict(color="blue", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=today_data["Time"],
        y=today_data["TypicalAvg"],
        mode="lines",
        name="Historical Avg",
        line=dict(color="grey", width=2, dash="dot"),
        opacity=0.4
    ))
    fig.update_layout(
        title="External Download Speed (Today)",
        xaxis_title="Time",
        yaxis_title="Download (Mbps)",
        font=dict(family="Arial", size=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        height=300
    )
    graph_html = fig.to_html(full_html=False)
    return render_template(
        "map.html",
        targets_df=targets_df,
        latest_status=latest_status,
        visible_device_types=VISIBLE_DEVICE_TYPES,
        last_speed_str=last_speed_str,
        graph_html=graph_html,
        feedback_msg=feedback_msg
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
    speed_df = pd.read_csv("externalSpeeds.csv")
    speed_df["Date"] = pd.to_datetime(speed_df["Date"], errors="coerce")
    typical_dict = get_typical_averages(speed_df)
    last_row = speed_df.tail(1).iloc[0]
    last_speed_str = f"Down: {last_row['Download']:.1f} / Up: {last_row['Upload']:.1f} Mbps"
    fantasy_feedback_msg = ""
    last_day = last_row.get("DayOfWeek", None)
    last_hour = last_row.get("Hour", None)
    if last_day is not None and last_hour is not None:
        key = (last_day, last_hour)
        typical_val = typical_dict.get(key, None)
        if typical_val is not None:
            if last_row["Download"] < typical_val * 0.8:
                fantasy_feedback_msg = (f"<strong>Dark Age Speed!</strong><br>"
                                        f"At {last_hour}:00 on {last_day}, we normally see ~{typical_val:.1f} Mbps, "
                                        f"but now it’s only {last_row['Download']:.1f}. Even the donkey is faster!")
            elif last_row["Download"] > typical_val * 1.2:
                fantasy_feedback_msg = (f"<strong>Lightning-Fast!</strong><br>"
                                        f"At {last_hour}:00 on {last_day}, typical is {typical_val:.1f} Mbps, "
                                        f"but we have {last_row['Download']:.1f} – the knights rejoice!")
            else:
                fantasy_feedback_msg = (f"<strong>Within Normal Castle Bounds</strong><br>"
                                        f"At {last_hour}:00 on {last_day}, typical ~{typical_val:.1f} Mbps. "
                                        f"Today is {last_row['Download']:.1f} Mbps – stable enough for the realm.")
        else:
            fantasy_feedback_msg = (f"No scroll records for {last_day} at {last_hour}:00. "
                                    f"This speed is a mystery to our wizards!")
    else:
        fantasy_feedback_msg = "Alas, the day/hour remain unknown – we cannot compare speeds to history."
    if "DayOfWeek" not in speed_df.columns:
        speed_df["DayOfWeek"] = speed_df["Date"].dt.day_name()
    if "Hour" not in speed_df.columns:
        speed_df["ParsedTime"] = pd.to_datetime(speed_df["Time"], format="%H:%M:%S", errors="coerce")
        speed_df["Hour"] = speed_df["ParsedTime"].dt.hour
    today_str = pd.Timestamp.now().strftime("%Y-%m-%d")
    today_mask = (speed_df["Date"].dt.strftime("%Y-%m-%d") == today_str)
    today_data = speed_df.loc[today_mask].copy()
    typical_vals = []
    for idx, row in today_data.iterrows():
        day = row.get("DayOfWeek", None)
        hr = row.get("Hour", None)
        key = (day, hr)
        typical_vals.append(typical_dict.get(key, None))
    today_data["TypicalAvg"] = typical_vals
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=today_data["Time"],
        y=today_data["Download"],
        mode="lines+markers",
        name="Today",
        line=dict(color="yellow", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=today_data["Time"],
        y=today_data["TypicalAvg"],
        mode="lines",
        name="Historical Avg",
        line=dict(color="white", dash="dot"),
        opacity=0.4
    ))
    fig.update_layout(
        title="External Download Speed (Today)",
        xaxis_title="Time",
        yaxis_title="Download (Mbps)",
        font=dict(family="Uncial Antiqua", size=14, color="white"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        height=300
    )
    graph_html = fig.to_html(full_html=False)
    
    # NEW: Get read-only Google Tasks (active tasks only)
    google_tasks = get_tasks_readonly()
    
    return render_template(
        "fantasymap.html",
        targets_df=targets_df,
        latest_status=latest_status,
        visible_device_types=VISIBLE_DEVICE_TYPES,
        last_speed_str=last_speed_str,
        graph_html=graph_html,
        fantasy_feedback_msg=fantasy_feedback_msg,
        google_tasks=google_tasks
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

@app.route("/speedtest/manual", methods=["GET"])
def run_speed_test():
    download, upload = measure_speed()
    download_str = f"{download:.2f}"
    upload_str = f"{upload:.2f}"
    return render_template(
        "speedtest_now.html",
        finished=True,
        download_str=download_str,
        upload_str=upload_str
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
