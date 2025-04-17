# Analysis Deliverable

## Analysis Question 1: Is there a statistically significant difference in the academic performance across race groups? 

### Why did you use this statistical test or ML algorithm? Which other tests did you consider or evaluate? What metric(s) did you use to measure success or failure, and why did you use it? What challenges did you face evaluating the model? Did you have to clean or restructure your data?

For this question, we used pairwise 2-sample t-tests to compare mean education scores across different racial groups (White, Asian, Black, Hispanic, Native American). The 2-sample t-test is appropriate here because we’re interested in determining whether the mean values of 2 independent groups (e.g., White vs. Black) are significantly different from each other. The t-test assumes that the samples are independent and drawn from populations with approximately normal distributions, which is reasonable given our large sample size (over 100,000 entries). A 1-sample t-test would not be appropriate here as we are comparing between each of the 2 groups pairwise.

We used the p-value from each t-test as our primary metric. A p-value less than 0.05 indicates that the difference in group means is statistically significant — meaning it's unlikely the difference is due to random chance. Also, the t-statistic also helped assess the magnitude of difference (larger values indicate more separation between groups). We ran this t-test pairwise across all race pairings (White vs Black, Asian vs Hispanic, etc) to view any potential differences. 

To clean the data, we did not have any major challenges. All we did was drop the rows with missing values in for each races' educational score column (gcs_mn_wht, gcs_mn_asn, etc.). This did, however, decrease our analysis sample size from 995,894 counties to 106,228 counties.

### What is your interpretation of the results? Do you accept or deny the hypothesis, or are you satisfied with your prediction accuracy? For prediction projects, we expect you to argue why you got the accuracy/success metric you have. Intuitively, how do you react to the results? Are you confident in the results?

Every single pairwise t-test resulted in statistically significant differences, with extremely small p-values (often reported as 0.0000e+00, meaning very close to zero). This means we can confidently reject the null hypothesis that these racial groups have the same mean education score. The t-statistics show both the direction and magnitude of differences. 

For example, the t-statistic of 364.736 between White and Black groups indicates a large difference, with White groups having significantly higher scores. On the other hand, a negative t-statistic, like for White vs. Asian (-41.321), suggests the Asian group had higher mean scores than the White group, both with statistically significant scores supported with a p-value < 0.05. These results to us make sense, but we found a couple statistics particularly surprising. For example, the t-statistic between Hispanic vs Native American being -31.568 and between Black vs Native American being -98.411, both insinuating that Native Americans are scoring statistically higher (supported by our p-values lower than 0.05) than Hispanic and Black populations. However, after comparing our results with existing research, we came to the conclusion that this might not be as surprising due to the inherently smaller sample size of the Native American population in our data compared to these other populations.

## Analysis Question 2: Is there statistical significance in academic performance between urban food deserts, rural food deserts, and non food deserts?

### Why did you use this statistical test or ML algorithm? Which other tests did you consider or evaluate? What metric(s) did you use to measure success or failure, and why did you use it? What challenges did you face evaluating the model? Did you have to clean or restructure your data?

### What is your interpretation of the results? Do you accept or deny the hypothesis, or are you satisfied with your prediction accuracy? For prediction projects, we expect you to argue why you got the accuracy/success metric you have. Intuitively, how do you react to the results? Are you confident in the results?

## Analysis Question 3: Is there statistical significance in sleep deprivation between urban food deserts, rural food deserts, and non food deserts?

### Why did you use this statistical test or ML algorithm? Which other tests did you consider or evaluate? What metric(s) did you use to measure success or failure, and why did you use it? What challenges did you face evaluating the model? Did you have to clean or restructure your data?

For this question, we used a 2-sample t-test to compare the mean prevalence of sleep deprivation across different area types: Urban Food Desert, Rural Food Desert, and Non–Food Desert counties. This test is appropriate because:

(1) We are comparing the means of a continuous variable (SLEEP_CrudePrev).

(2) The samples are independent.

(3) It is a standard method for testing whether two groups have significantly different means.

To measure success and failure, we used the p-value from the t-tests:
A p-value < 0.05 indicated statistically significant differences in means. The t-statistic also helped assess the magnitude of difference (larger values indicate more separation between groups).

To prepare the data, we did not have any major challenges. All we did was drop the rows with missing values in the SLEEP_CrudePrev column and (previously for analysis question 2) ensured that area_type was properly defined for each county.

### What is your interpretation of the results? Do you accept or deny the hypothesis, or are you satisfied with your prediction accuracy? For prediction projects, we expect you to argue why you got the accuracy/success metric you have. Intuitively, how do you react to the results? Are you confident in the results?

All pairwise comparisons (between Urban Food Deserts and Non-Food Deserts as well as Rural Food Deserts and Non-Food Deserts) produced extremely small p-values (effectively zero). At first, we were a bit surprised with how small these p-values are, as under the hood, the smallest number that can be represented is 5e-324. That is, our p-values must be even smaller than this number as they are coming out as effectively 0. This suggests a very strong statistical difference in sleep deprivation prevalence between urban food deserts, rural food deserts, and non–food desert areas. We also noticed that the t-statistic was particularly large for Urban vs Non-Food Desert, indicating a larger difference in means.

We reject the null hypothesis in all comparisons. That is, we found strong evidence that urban and rural food deserts do differ significantly from non–food deserts in terms of sleep deprivation prevalence.

According to these results, it does makes sense that urban food deserts, often associated with environmental stressors, limited access to healthcare, noise, and light pollution, would have higher sleep deprivation. In a similar manner, the rural difference was also significant, though smaller — possibly due to limited healthcare access and economic factors.

The high confidence is reinforced by our large sample sizes, very small p-values (effectively 0), and clear differences in group means (as shown in our t-statistics and visually on the bar graph).

## Analysis Question 4: Is there a statistical significance in education scores across racial groups when comparing communities with high versus low sleep deprivation prevalence?

### Why did you use this statistical test or ML algorithm? Which other tests did you consider or evaluate? What metric(s) did you use to measure success or failure, and why did you use it? What challenges did you face evaluating the model? Did you have to clean or restructure your data?

### What is your interpretation of the results? Do you accept or deny the hypothesis, or are you satisfied with your prediction accuracy? For prediction projects, we expect you to argue why you got the accuracy/success metric you have. Intuitively, how do you react to the results? Are you confident in the results?

## Overall Analysis
### Did you find the results corresponded with your initial belief in the data? If yes/no, why do you think this was the case?

### Do you believe the tools for analysis that you chose were appropriate? If yes/no, why or what method could have been used?

### Was the data adequate for your analysis? If not, what aspects of the data were problematic and how could you have remedied that?


