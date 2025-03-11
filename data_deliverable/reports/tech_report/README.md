**SEDA Dataset**

Total datapoints: 354949
- While this dataset contains missing values, based on an initial analysis we should have enough for analysis when joining with the Food Atlas dataset

Identifying attributes: stateabb, sedacountyname, year, grade, subject

Where is the data from: Stanford Educational Opportunity Project Data Archive (SEDA)
- How did you collect your data: downloaded from their website
- Is the source reputable: yes
- How did you generate thes sample: N/A - we are just using the most recent version (5.0)
- Other considerations: there are lots of missing values so we will need to conduct our analysis on a subset. As such, we need to consider biases that might be introduced when filtering.

How clean is the data:
- When we have values, the data is pretty clean. However, we do have relatively large amounts of missing data that is scattered in various feature columns of the dataset.
- The data is already standardized by SEDA to account for local and national variances in testing such that we can compare standarized scores directly.
- We will most likely need to throw away entire counties where we don't have enough data. This will most likely be on a case by case basis for specific analysis questions. For example, a given county might be included in out analysis when looking at scores across gender but not when looking at race due to missing data. One potential issue in this is that we could introduce biases where regions with better education infrastructre and performance reporting might be over represented in out analysis datasets.

Challenges:
- Joining with the Food Atlas dataset will be relatively easy but selecting the subsets of the data we will use for our analysis questions will be more involved and require careful stratified sampling techniques to avoid introducing biases.

