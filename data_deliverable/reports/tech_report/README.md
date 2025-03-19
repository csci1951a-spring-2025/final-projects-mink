# Data Deliverable: Tech Report Questions

## [Food Access Research Atlas](https://www.ers.usda.gov/data-products/food-access-research-atlas)

Dataset: [https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data](https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data)  

For our main data analysis, we plan to filter the data into **3** categories: **Urban** **counties** that fit the food desert criteria, **Rural** **counties** that fit the food desert criteria, and all other counties (which we will call **non-food-deserts counties**). Then, we will cross reference these groups with their average standardized testing scores \+ health rates using our other 2 datasets.

### Data Attributes
Located in the Final Project Data Skim Markdown (./final-projects-mink/Final Project Data Skim.md)

### Tech Report Questions (Food Access Research Atlas)

* **How many data points are there in total?** How many are there in each group you care about (e.g. if you are dividing your data into positive/negative examples, are they split evenly)?   
  * Aim for a resource of reasonable size. **At least 700 records (at least 1000 records for capstone projects)** after cleaning and duplicate removal. Account that part of your data should be used for validation of your results only.   
    * 72,532 rows total, but 8,024 for California  
  * Do you think this is enough data to perform your analysis later on?  
    * Yes  
* What are the identifying attributes?  
  * CensusTract, which will be our Primary Key to join with our other datasets  
* Where is the data from?  
  * How did you collect your data?  
    * From the United States Department of Agriculture (USDA)  
  * Is the source reputable?  
    * Yes  
  * How did you generate the sample? Is it comparably small or large? Is it representative or is it likely to exhibit some kind of sampling bias?  
    * We should probably randomize a sample of census tracts in CA to avoid bias  
  * Are there any other considerations you took into account when collecting your data? This is open-ended based on your data; feel free to leave this blank. (Example: If it's user data, is it public/are they consenting to have their data used? Is the data potentially skewed in any direction?) No considerations needed  
* How clean is the data? Does this data contain what you need in order to complete the project you proposed to do? (Each team will have to go about answering this question differently but use the following questions as a guide. Graphs and tables are highly encouraged if they allow you to answer these questions more succinctly.)  
  * How did you check for the cleanliness of your data? What was your threshold reference?  
    * Checked min/max values for our desired attributes, any NULL values  
  * Did you implement any mechanism to clean your data? If so, what did you do?  
    * Filter data by state for California  
    * Since the census runs on smaller locations (tracts) for every county, we will have to do some aggregation to get the data in the per-county form. This is because even though our CDC data also uses per census tract, our education data works per county.   
      * We will average the poverty rates, housing units with vehicle shares, and housing units with SNAP benefits shares  
      * For the flag attributes, we will calculate some sort of “Food Desert Impact Score” for each county based on the number and proportion of census tracts marked as food deserts (or whatever flag applies) 
  * Are there missing values? Do these occur in fields that are important for your project's goals?  
    * Remove entries with NULL values for poverty rate, lahunvhalfshare, lahunv10share, lasnaphalfshare, and lasnap10share  
  * Are there duplicates? Do these occur in fields that are important for your project's goals?  
    * No  
  * How is the data distributed? Is it uniform or skewed? Are there outliers? What are the min/max values? (focus on the fields that are most relevant to your project goals)  
    * This is not relevant to this dataset  
  * Are there any data type issues (e.g. words in fields that were supposed to be numeric)? Where are these coming from? (E.g. a bug in your scraper? User input?) How will you fix them?  
    * No  
  * Do you need to throw any data away? What data? Why? Any reason this might affect the analyses you are able to run or the conclusions you are able to draw?  
    * NULL values for the attributes described above  
* Summarize any challenges or observations you have made since collecting your data. Then, discuss your next steps and how your data collection has impacted the type of analysis you will perform. (approximately 3-5 sentences)  
  * The observations we have made so far are that there are various datasets revolving around health that utilize the census tract as a primary key. This is beneficial because the data is public and published by reliable sources such as the CDC. This abundance of data allows us to analyze how food deserts affect the health of students and then examine their performance in schools. Still a challenge remains ensuring we take into account the missing data found in the educational opportunity dataset. Lastly we need to handle potential lost rows during joins to ensure we are not skewing are data

# [CDC PLACES: Census Tract Data](https://www.cdc.gov/places/index.html)

Dataset: [https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2021-/mb5y-ytti/about\_data](https://data.cdc.gov/500-Cities-Places/PLACES-Census-Tract-Data-GIS-Friendly-Format-2021-/mb5y-ytti/about_data)

The PLACES project provides local data on the health status of locations across the United States. Specifically the 2021 release publishes data on the state of 2019\. In addition the data is formatted with County Name and Census Tract. These columns provide flexibility and allow for a seamless join between the Food Desert, Educational, and CDC Health data. The dataset presents multiple health status to monitor, but for our case we are prioritizing sleep deprivation and mental health status.

### Data Attributes 
Located in the Final Project Data Skim Markdown (./final-projects-mink/Final Project Data Skim.md)

### Tech Report Questions
Total datapoints: 72335 across the U.S
- There is enough data to perform analysis especially since the Food Desert data has around the same total points. This allows for an easier join and a more complete data table after a join.

Identifying attributes: TractFIPS because there is only one row per tract id.

Where is the data from: Centers for Disease Control and Prevention (CDC) 
- How did you collect your data: Downloaded from their website
- Is the source reputable: yes federal public health agency under the U.S. Department of Health and Human Services
- How did you generate these sample: N/A  defined by the CDC
- Other considerations: N/A

 How clean is the data:
- The data is clean as there are no duplicates and the data comes from a trusted source. Additionally there are no null values for data regarding sleep deprivation and mental health status
- No mechanism to clean data as the data is alraedy clean
- No missing values or duplicates
- Data distribution
  - Ranges for sleep deprivation: 20.2 - 60.8
     - Slightly skewed with the most data being seen around 34-40%
  - Ranges for mental health score 5.5 38.6
     - Slightly right skewed with the most data being seen around 12-16%
- No data type issues
- No need to throw data away

Challenges:
There is no challenge in collecting this data. The data is formatted properly and joins well with the food desert data. Since we can join both Food Desert and Health outcomes per tract we plan on researching the relationship between food deserts/health and how they play a role in education outcomes. The next steps will be to join with the educational data set to construct an appropriate table containing educational results per region.

# [National Center for Education Statistics (NCES) School District Geographic Relationship](https://nces.ed.gov/programs/edge/geographic/relationshipfiles)

Dataset: [https://nces.ed.gov/programs/edge/geographic/relationshipfiles](https://nces.ed.gov/programs/edge/geographic/relationshipfiles)

This dataset provides a mapping from Local Education Agency Identification numbers to census tract numbers, allowing us to map standardized academic performance data from the SEDA dataset to the CDC and food desert data sets mentioned above.

### Data Attributes 
Located in the Final Project Data Skim Markdown (./final-projects-mink/Final Project Data Skim.md)

### Tech Report Questions (NCES)

Total datapoints: 113,520
- There is enough data to perform analysis as this dataset is being used to map one dataset to another. We may use the area of the different census tracts.

Identifying attributes: LEAID, NAME_LEA19, TRACT, LANDAREA

Where is the data from: NCES
- How did you collect your data: downloaded from their website
- Is the source reputable: yes
- How did you generate these sample: N/A - defined by government. this is being used for mapping purposes.
- Other considerations: N/A

How clean is the data:
- as clean as it can get; solely used for mapping datasets to each other
- no mechanism to clean data
- no missing values or duplicates
- data distribution is n/a
- no data type issues
- no need to throw data away

Challenges:
- no challenges with this dataset. this helps decrease the challenges of our other datasets as this helps us map the food, health, and education datasets to create one big dataset. this will be used to combine our datasets.


## [SEDA Dataset](https://edopportunity.org/opportunity/data/downloads/)

### Data Attributes 
Located in the Final Project Data Skim Markdown (./final-projects-mink/Final Project Data Skim.md)

### Tech Report Questions (SEDA)

Total datapoints: 354949
- While this dataset contains missing values, based on an initial analysis we should have enough for analysis when joining with the Food Atlas dataset

Identifying attributes: stateabb, sedacountyname, year, grade, subject

Where is the data from: Stanford Educational Opportunity Project Data Archive (SEDA)
- How did you collect your data: downloaded from their website
- Is the source reputable: yes
- How did you generate thes sample: N/A - we are just using the most recent version (5.0)
- Other considerations: there are lots of missing values so we will need to conduct our analysis on a subset. As such, we need to consider biases that might be introduced when filtering.

How clean is the data:
- When we have values, the data is pretty clean (checked via verifying datatypes). However, we do have relatively large amounts of missing data that is scattered in various feature columns of the dataset. The threshold reference was having unique identifying information which included state abbreviation, seda admin ID, subject, and grade information. Histogrms were also generated to ensure that there were no concerning outliers.
- No cleaning mechanisms were employed as the data was clean.
- There are missing values. These occur in fields that are important for the project's goals. (See the last bullet for our approach to this)
- There are no duplicates.
- The data is already standardized by SEDA to account for local and national variances in testing such that we can compare standarized scores directly. There were no outliers. The min/max is not relevant as everything is on a standardized scale.
- There are no data type issues.
- We will most likely need to throw away entire counties where we don't have enough data. This will most likely be on a case by case basis for specific analysis questions. For example, a given county might be included in out analysis when looking at scores across gender but not when looking at race due to missing data. One potential issue in this is that we could introduce biases where regions with better education infrastructre and performance reporting might be over represented in out analysis datasets.

Challenges:
- Joining with the Food Atlas dataset will be relatively easy but selecting the subsets of the data we will use for our analysis questions will be more involved and require careful stratified sampling techniques to avoid introducing biases. Another challenge is that the combined dataset is extremely large as everything school district in the dataset covers multiple census tracts so the join operations will yield a very deep and long table. The datasets are in a sql db and we will now begin to train machine learning models.

