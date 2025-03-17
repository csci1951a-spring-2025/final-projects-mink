# Data Deliverable

## [Food Access Research Atlas](https://www.ers.usda.gov/data-products/food-access-research-atlas)

Dataset: [https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data](https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data)  

For our main data analysis, we plan to filter the data into **3** categories: **Urban** **counties** that fit the food desert criteria, **Rural** **counties** that fit the food desert criteria, and all other counties (which we will call **non-food-deserts counties**). Then, we will cross reference these groups with their average standardized testing scores \+ health rates using our other 2 datasets.

Dataset: [https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data](https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data) 

For our main data analysis, we plan to filter the data into **3** categories: **Urban** **counties** that fit the food desert criteria, **Rural** **counties** that fit the food desert criteria, and all other counties (which we will call **non-food-deserts counties**). Then, we will cross reference these groups with their average standardized testing scores \+ health rates using our other 2 datasets.

### Data Attributes

- **CensusTract** :: Census tract number  
  - Type of data: Number  
  - Default value: None, all defined  
  - Range of value: 1001020100 \- 56045951300  
  - Simplified analysis of the distribution of values: An 11-digit number that identifies a specific census tract within a state and county. The number is made up of a state code, county code, and tract code.  
  - Are these values unique?: Yes  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No, there will be no duplicate records  
  - Is this a required value? Yes  
  - Do you plan to use this attribute/feature in the analysis? If so, how? As a PRIMARY KEY, in order to cross this dataset with our other 2  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- **State** :: State name  
  - Type of data: Text  
  - Default value: None, all defined  
  - Range of value: Alabama \- Wyoming  
  - Simplified analysis of the distribution of values: 50 states in USA  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? Yes  
  - Do you plan to use this attribute/feature in the analysis? If so, how? Likely for our map / interactive component  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- **County** :: County name  
  - Type of data: Text  
  - Default value: None, all defined  
  - Range of value: Abbeville County \- Ziebach County  
  - Simplified analysis of the distribution of values: All counties in USA  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? Yes  
  - Do you plan to use this attribute/feature in the analysis? If so, how? Likely for our map / interactive component  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- **Urban** :: Flag for urban area  
  - Type of data: Boolean flag  
  - Default value: 0  
  - Range of value: 0 or 1  
  - Simplified analysis of the distribution of values: 0 \= false, 1 \= true  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? Yes  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be needed in our 3 category food desert classification  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No

Attributes needed to define food deserts:

- **LATracts\_half** :: Flag (0 or 1\) for low access tract when considering 1/2 mile distance  
  - Type of data: Boolean flag  
  - Default value: 0  
  - Range of value: 0 or 1  
  - Simplified analysis of the distribution of values: 0 \= false, 1 \= true  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? Yes  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be needed in our 3 category food desert classification  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- **LATracts10** :: Flag (0 or 1\) for low access tract when considering 10 mile distance  
  - Type of data: Boolean flag  
  - Default value: 0  
  - Range of value: 0 or 1  
  - Simplified analysis of the distribution of values: 0 \= false, 1 \= true  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? Yes  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be needed in our 3 category food desert classification  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- **PovertyRate** :: Share (%) of the area population living with income at or below the Federal poverty thresholds for family size   
  - Type of data: Integer  
  - Default value: NULL  
  - Range of value: 0-100  
  - Simplified analysis of the distribution of values:  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? No, there are some NULL values we will clean out  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be needed in our 3 category food desert classification  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- **LowIncomeTracts** :: Flag (0 or 1\) for low income area  
  - Type of data: Boolean flag  
  - Default value: 0  
  - Range of value: 0 or 1  
  - Simplified analysis of the distribution of values: 0 \= false, 1 \= true  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? Yes  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be needed in our 3 category food desert classification  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No

With these attributes, we can now filter the data to organize our counties into the 3 categories mentioned above.

Other Attributes:

- **Lahunvhalfshare** :: Share (%) of tract housing units that are without vehicle and beyond 1/2 mile from supermarket  
  - Type of data: Integer  
  - Default value: NULL  
  - Range of value: 0-100  
  - Simplified analysis of the distribution of values: Percentage share  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? No, there are some NULL values we will clean out  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be used to analyze if vehicle access plays a part in whether the food desert populations change  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- **Lahunv10share** :: Share (%) of tract housing units that are without vehicle and beyond 10 miles from supermarket   
  - Type of data: Integer  
  - Default value: NULL  
  - Range of value: 0-100  
  - Simplified analysis of the distribution of values: Percentage share  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? No, there are some NULL values we will clean out  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be used to analyze if vehicle access plays a part in whether the food desert populations change  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- With these 2 attributes, we can make our own definition of whether the county is considered a low-vehicle population (ex. \< 30% of housing units)  
- (maybe) **lasnaphalfshare** :: Share (%) of tract housing units receiving SNAP benefits count beyond 1/2 mile from supermarket  
  - Type of data: Integer  
  - Default value: NULL  
  - Range of value: 0-100  
  - Simplified analysis of the distribution of values: Percentage share  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? No, there are some NULL values we will clean out  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be used to analyze if SNAP benefit access plays a part in whether the food desert populations change  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No  
- (maybe) **lasnap10share** :: Share (%) of tract housing units receiving SNAP benefits count beyond 10 miles from supermarket   
  - Type of data: Integer  
  - Default value: NULL  
  - Range of value: 0-100  
  - Simplified analysis of the distribution of values: Percentage share  
  - Are these values unique?: No  
  - Will you use this value (maybe in composition with others) to detect possible duplicate records? If so, how? No  
  - Is this a required value? No, there are some NULL values we will clean out  
  - Do you plan to use this attribute/feature in the analysis? If so, how? This attribute will be used to analyze if SNAP benefit access plays a part in whether the food desert populations change  
  - Does this feature include potentially sensitive information? If so, how do you suggest handling such issues? No

### Tech Report Questions

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


## [SEDA Dataset](https://edopportunity.org/opportunity/data/downloads/)

### Data Attributes 

### Tech Report Questions

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

