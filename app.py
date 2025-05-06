# app.py
from flask import Flask, render_template_string, request
import pandas as pd
import scipy.stats as stats

app = Flask(__name__)

# The HTML page with two dropdowns and a submit button
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Race Comparison T-Test</title>
    <style>
    button {
        background-color: #007BFF;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        box-shadow: 0px 4px 8px rgba(0, 123, 255, 0.2);
    }

    button:hover {
        background-color: #0056b3;
    }

    button:active {
        transform: scale(0.98);
    }

    select {
        padding: 6px;
        border-radius: 5px;
        border: 1px solid #ccc;
        font-size: 14px;
    }
</style>

</head>
<body>
    <h1>Compare Academic Scores Between Race Groups</h1>
    <h3>Visualization:</h3>
    <img src="{{ url_for('static', filename='graphs/race_group_academic_scores.png') }}" alt="Graph 2" width="500">
    
    <form method="POST" action="/race">
        <label for="race1">Select first race:</label>
        <select id="race1" name="race1" required>
            {% for race in races %}
    <option value="{{ race }}" {% if race == selected_race1 %}selected{% endif %}>{{ race }}</option>
            {% endfor %}
        </select>

        <br><br>

        <label for="race2">Select second race:</label>
        <select id="race2" name="race2" required>
            {% for race in races %}
    <option value="{{ race }}" {% if race == selected_race2 %}selected{% endif %}>{{ race }}</option>
            {% endfor %}
        </select>

        <br><br>

        <button type="submit">Compare</button>
    </form>

    {% if race_result %}
    <h2>Academic Scores Comparison Result:</h2>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Race 1</th>
            <th>Race 2</th>
            <th>T-Statistic</th>
            <th>P-Value</th>
            <th>Significance</th>
        </tr>
        <tr>
            <td>{{ race_result['Race_1'] }}</td>
            <td>{{ race_result['Race_2'] }}</td>
            <td>{{ race_result['T-Statistic'] }}</td>
            <td>{{ race_result['P-Value'] }}</td>
            <td>{{ race_result['Significance'] }}</td>
        </tr>
    </table>
    {% endif %}

    <h1>Compare Academic Scores across Food Deserts and Non-Food Deserts</h1>
    <h3>Visualization:</h3>
    <img src="{{ url_for('static', filename='graphs/area_type_academic_scores.png') }}" alt="Graph 1" width="500">

    <form method="POST" action="/area">
        <label for="area">Select Area Type:</label>
        <select id="area" name="area" required>
            {% for area in areas %}
    <option value="{{ area }}" {% if area == selected_area %}selected{% endif %}>{{ area }}</option>
            {% endfor %}
        </select>

        <br><br>

        <button type="submit">Show Academic Scores Result</button>
    </form>

    {% if area_result %}
    <h3>Academic Scores Comparison Result:</h3>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Area Type</th>
            <th>Baseline Mean</th>
            <th>T-Statistic</th>
            <th>P-Value</th>
            <th>Significance</th>
        </tr>
        <tr>
            <td>{{ area_result['Area_Type'] }}</td>
            <td>{{ area_result['Baseline_Mean'] }}</td>
            <td>{{ area_result['T-Statistic'] }}</td>
            <td>{{ area_result['P-Value'] }}</td>
            <td>{{ area_result['Significance'] }}</td>
        </tr>
    </table>
    {% endif %}
    
    <h1>Compare Sleep Deprivation across Food Deserts and Non-Food Deserts</h1>
    <h3>Visualization:</h3>
    <img src="{{ url_for('static', filename='graphs/area_type_sleep_deprivation.png') }}" alt="Graph 2" width="500">
    <form method="POST" action="/food">
        <label for="area">Select Area Type:</label>
        <select id="area" name="area" required>
            {% for area in areas %}
    <option value="{{ area }}" {% if area == selected_food_area %}selected{% endif %}>{{ area }}</option>
            {% endfor %}
        </select>

        <br><br>

        <button type="submit">Show Sleep Deprivation Result</button>
    </form>

    {% if food_result %}
    <h3>Sleep Deprivation Comparison Result:</h3>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Group 1</th>
            <th>Group 2</th>
            <th>T-Statistic</th>
            <th>P-Value</th>
            <th>Significance</th>
        </tr>
        <tr>
            <td>{{ food_result['Group_1'] }}</td>
            <td>{{ food_result['Group_2'] }}</td>
            <td>{{ food_result['T-Statistic'] }}</td>
            <td>{{ food_result['P-Value'] }}</td>
            <td>{{ food_result['Significance'] }}</td>
        </tr>
    </table>
    {% endif %}

    
    <h1>Compare Academic Scores Between Race Groups Depending on Sleep Deprivation</h1>
    <form method="POST" action="/sleep">
        <label for="sleepRace1">Select first race:</label>
        <select id="sleepRace1" name="sleepRace1" required>
            {% for race in races %}
    <option value="{{ race }}" {% if race == selected_sleepRace1 %}selected{% endif %}>{{ race }}</option>
            {% endfor %}
        </select>

        <br><br>

        <label for="sleepRace2">Select second race:</label>
        <select id="sleepRace2" name="sleepRace2" required>
            {% for race in races %}
    <option value="{{ race }}" {% if race == selected_sleepRace2 %}selected{% endif %}>{{ race }}</option>
            {% endfor %}
        </select>

        <br><br>

    <label for="sleep_status">Select Sleep Deprivation Level:</label>
    <select id="sleep_status" name="sleep_status" required>
    <option value="High" {% if selected_sleep_status == "High" %}selected{% endif %}>High</option>
    <option value="Low" {% if selected_sleep_status == "Low" %}selected{% endif %}>Low</option>
    </select>

    <br><br>

    <button type="submit">Compare Sleep Deprivation</button>
    </form>

    {% if sleep_result %}
    <h3>Sleep Deprivation Comparison Result:</h3>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Race 1</th>
            <th>Race 2</th>
            <th>Sleep Deprivation Level</th>
            <th>T-Statistic</th>
            <th>P-Value</th>
            <th>Significance</th>
        </tr>
        <tr>
            <td>{{ sleep_result['Race_1'] }}</td>
            <td>{{ sleep_result['Race_2'] }}</td>
            <td>{{ sleep_result['Sleep_Deprivation_Level'] }}</td>
            <td>{{ sleep_result['T-Statistic'] }}</td>
            <td>{{ sleep_result['P-Value'] }}</td>
            <td>{{ sleep_result['Significance'] }}</td>
        </tr>
    </table>
    {% endif %}

</body>
</html>
"""

# Load data for area type comparison (Question 1)
q1_df = pd.read_csv("results/q1.csv")
race_mapping = {
    'White': 'gcs_mn_wht',
    'Asian': 'gcs_mn_asn',
    'Black': 'gcs_mn_blk',
    'Hispanic': 'gcs_mn_hsp',
    'Native American': 'gcs_mn_nam'
}
race_labels = list(race_mapping.keys())

# Function to get race comparison for education data
def compare_races(race1, race2):
    # Read from q2.csv to get row that contains column Race_1 = race1 and column Race_2 = race2
    row = q1_df[((q1_df['Race_1'] == race1) & (q1_df['Race_2'] == race2))]
    if not row.empty:
        return {
            "Race_1": row.iloc[0]['Race_1'],
            "Race_2": row.iloc[0]['Race_2'],
            "T-Statistic": f"{row.iloc[0]['T-Statistic']:.4f}",
            "P-Value": f"{row.iloc[0]['P-Value']:.2e}",
            "Significance": row.iloc[0]['Significance']
        }
    else:
        return "No precomputed t-test result found for this pair."

# Load data for area type comparison (Question 2)
q2_df = pd.read_csv("results/q2.csv")
area_labels = q2_df['Area_Type'].tolist()

# Function to get area type results for education data
def get_area_result(area):
    row = q2_df[q2_df['Area_Type'] == area]
    if not row.empty:
        return {
            "Area_Type": row.iloc[0]['Area_Type'],
            "Baseline_Mean": f"{row.iloc[0]['Baseline_Mean']:.3f}",
            "T-Statistic": f"{row.iloc[0]['T-Statistic']:.3f}",
            "P-Value": f"{row.iloc[0]['P-Value']:.2e}",
            "Significance": row.iloc[0]['Significance']
        }
    else:
        return None

# Load data for food desert comparison (Question 3)
q3_df = pd.read_csv("results/q3.csv")

def get_food_desert_result(group):
    row = q3_df[q3_df['Group_1'] == group] 
    if not row.empty:
        return {
            "Group_1": row.iloc[0]['Group_1'],
            "Group_2": row.iloc[0]['Group_2'],
            "T-Statistic": f"{row.iloc[0]['T-Statistic']:.3f}",
            "P-Value": f"{row.iloc[0]['P-Value']:.2e}",
            "Significance": row.iloc[0]['Significance']
        }
    else:
        return None

def get_sleep_result(race1, race2, sleep_status):
    sleep_df = pd.read_csv("results/q4.csv")
    row = sleep_df[
        (sleep_df['Sleep_Deprivation_Level'] == sleep_status) &
        (sleep_df['Race_1'] == race1) &
        (sleep_df['Race_2'] == race2) 
    ]
    row_opposite = sleep_df[
        (sleep_df['Sleep_Deprivation_Level'] == sleep_status) &
        (sleep_df['Race_1'] == race2) &
        (sleep_df['Race_2'] == race1) 
    ]
    if not row.empty:
        return {
            "Race_1": race1,
            "Race_2": race2,
            "Sleep_Deprivation_Level": sleep_status,
            "T-Statistic": f"{row.iloc[0]['T-Statistic']:.4f}",
            "P-Value": f"{row.iloc[0]['P-Value']:.4f}",
            "Significance": row.iloc[0]['Significance']
        }
    if not row_opposite.empty:
        t_stat_flipped = -1 * row_opposite.iloc[0]['T-Statistic']
        return {
            "Race_1": race1,
            "Race_2": race2,
            "Sleep_Deprivation_Level": sleep_status,
            "T-Statistic": f"{t_stat_flipped:.4f}",
            "P-Value": f"{row_opposite.iloc[0]['P-Value']:.4f}",
            "Significance": row_opposite.iloc[0]['Significance']
        }
    else:
        return {'Error': "No precomputed sleep deprivation result found for this combination."}

# Home route
@app.route('/', methods=['GET'])
def home():
    return render_template_string(html, races=race_labels, areas=area_labels)

# Race comparison route
@app.route('/race', methods=['POST'])
def race_compare():
    race1 = request.form.get('race1')
    race2 = request.form.get('race2')
    result = None
    if race1 and race2 and race1 != race2:
        result = compare_races(race1, race2)
    else:
        result = "Please select two different race groups."
    return render_template_string(html, races=race_labels, areas=area_labels, race_result=result, selected_rac1e = race1, selected_race2 = race2)

# Area comparison route
@app.route('/area', methods=['POST'])
def area_compare():
    area = request.form.get('area')
    result = None
    if area:
        result = get_area_result(area)
    return render_template_string(html, races=race_labels, areas=area_labels, area_result=result, selected_area=area)

@app.route('/food', methods=['POST'])
def food_compare():
    area = request.form.get('area')
    result = None
    if area:
        result = get_food_desert_result(area)
    return render_template_string(html, races=race_labels, areas=area_labels, food_result=result, selected_food_area=area)


@app.route('/sleep', methods=['POST'])
def sleep_depr_compare():
    race1 = request.form.get('sleepRace1')
    race2 = request.form.get('sleepRace2')
    sleep_status = request.form.get('sleep_status')
    result = None
    if race1 and race2 and sleep_status and race1 != race2:
        result = get_sleep_result(race1, race2, sleep_status)
    else:
        result = "Please select two different races and a sleep deprivation status."
    return render_template_string(
        html,
        areas=area_labels, 
        races=race_labels,
        # food_result=result,
        sleep_result=result,
        selected_sleepRace1=race1,
        selected_sleepRace2=race2,
        selected_sleep_status=sleep_status
    )

if __name__ == "__main__":
    app.run(debug=True)