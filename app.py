# app.py
from flask import Flask, render_template_string, request
import pandas as pd
import scipy.stats as stats

app = Flask(__name__)

# Load and prepare your dataset
df = pd.read_csv("data/full_joined_table.csv")
df = df.dropna(subset=['gcs_mn_wht', 'gcs_mn_asn', 'gcs_mn_blk', 'gcs_mn_hsp', 'gcs_mn_nam'])

race_mapping = {
    'White': 'gcs_mn_wht',
    'Asian': 'gcs_mn_asn',
    'Black': 'gcs_mn_blk',
    'Hispanic': 'gcs_mn_hsp',
    'Native American': 'gcs_mn_nam'
}
race_labels = list(race_mapping.keys())

# The HTML page with two dropdowns and a submit button
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Race Comparison T-Test</title>
</head>
<body>
    <h1>Compare Academic Scores Between Race Groups</h1>
    <form method="POST">
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

    {% if result %}
    <h2>Result:</h2>
    <p>{{ result }}</p>
    {% endif %}
</body>
</html>
"""

# The function to compute t-test
def compare_races(race1, race2):
    # read from q2.csv to get row that contains column Race_1 = race1 and column Race_2 = race2
    ttest_df = pd.read_csv("data/q1.csv")

    row = ttest_df[((ttest_df['Race_1'] == race1) & (ttest_df['Race_2'] == race2))]
    if not row.empty:
        t_stat = row.iloc[0]['T-Statistic']
        p_val = row.iloc[0]['P-Value']
        return f"T-statistic: {t_stat:.4f}, P-value: {p_val:.4f}"
    else:
        return "No precomputed t-test result found for this pair."

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        race1 = request.form.get('race1')
        race2 = request.form.get('race2')
        if race1 and race2 and race1 != race2:
            result = compare_races(race1, race2)
        else:
            result = "Please select two different race groups."

    return render_template_string(html, races=race_labels, result=result)

if __name__ == "__main__":
    app.run(debug=True)
