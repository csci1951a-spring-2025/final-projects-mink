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
</head>
<body>
    <h1>Compare Academic Scores Between Race Groups</h1>
    <form method="POST" action="/race">
        <label for="race1">Select first race:</label>
        <select id="race1" name="race1" required>
            {% for race in races %}
            <option value="{{ race }}">{{ race }}</option>
            {% endfor %}
        </select>

        <br><br>

        <label for="race2">Select second race:</label>
        <select id="race2" name="race2" required>
            {% for race in races %}
            <option value="{{ race }}">{{ race }}</option>
            {% endfor %}
        </select>

        <br><br>

        <button type="submit">Compare</button>
    </form>

    {% if race_result %}
    <h2>Result:</h2>
    <p>{{ race_result }}</p>
    {% endif %}
    
    <h2>View Area Type Results</h2>
    <form method="POST" action="/area">
        <label for="area">Select Area Type:</label>
        <select id="area" name="area" required>
            {% for area in areas %}
            <option value="{{ area }}">{{ area }}</option>
            {% endfor %}
        </select>

        <br><br>

        <button type="submit">Show Area Type Result</button>
    </form>

    {% if area_result %}
    <h3>Area Type Comparison Result:</h3>
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
        t_stat = row.iloc[0]['T-Statistic']
        p_val = row.iloc[0]['P-Value']
        Significance = row.iloc[0]['Significance']
        return f"T-statistic: {t_stat:.4f}, P-value: {p_val:.4f}, Statistically {Significance}"
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

# Home route
@app.route('/', methods=['GET'])
def home():
    return render_template_string(html, races=race_labels, areas=area_labels, race_result=None, area_result=None)

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
    return render_template_string(html, races=race_labels, areas=area_labels, race_result=result, area_result=None)

# Area comparison route
@app.route('/area', methods=['POST'])
def area_compare():
    area = request.form.get('area')
    result = None
    if area:
        result = get_area_result(area)
    return render_template_string(html, races=race_labels, areas=area_labels, race_result=None, area_result=result)

if __name__ == "__main__":
    app.run(debug=True)
