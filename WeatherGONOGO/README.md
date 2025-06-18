# GoNoGo

This Flask application helps water sport organisers decide if an activity can proceed based on guidance stored in two CSV files:

- **Conditions_and_Ratios.csv** – wind limits, distance limits and coach/leader ratios for different environments.
- **Locations_onshore_offshore.csv** – onshore wind directions for each location.

The form collects the planned location, environment, distance from shore, wind information and the number of participants and coaches. The app then checks the inputs against the CSV guidance and displays **GO** or **NO GO** along with the reasons.

## Usage
1. Install the dependency:
   ```bash
   pip install flask
   ```
2. Run the server:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser and complete the form.

