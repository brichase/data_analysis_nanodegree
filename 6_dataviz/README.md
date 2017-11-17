# Udacity DAND Project: Prosper Loan Rating Scores Visualization

## Summary
This visualization shows how Prosper's rating system of individual loans
changed from being almost solely based on the individual's credit rating to
having much less correlation after July of 2009---when they moved from
CreditGrade to ProsperRating.

As background, Prosper is a peer-to-peer lending platform that allows people
to invest directly into personal loans.

Loans are rated from AA (best -- most credit worthy) to HR (worst -- least
credit worthy).

## Design
#### Initial design:  
My first thought is to convey the information that CreditGrade was highly
correlated with CreditScore and ProsperRating is correlated not as much with CreditScore than BorrowerAPR.

To show this, my plan was two scatter plots---side by side---showing both CreditScore and BorrowerAPR colored by CreditScore and the other ProsperRating.

The color scheme used highlights the sequential ordered nature of the ratings.
B is a better rating than A and so on.

There was a bug in dimplejs where some datapoints would cause the chart to not
appear. So I cleaned the first 200 datapoints and used that.

#### Iterations:
The viewers had issues picking out my main findings in the charts. So I pivoted
to using histograms and only kept CreditScore bins as categories to highlight this effect.

Using histograms allowed me to use the full data. (Quite large--could do some extra processing to make it load quickly)

Another reason that I removed the BorrowerAPR data from the charts is when it
occurred to me that ProsperScore was the main determinant of the APR
(one of the main reasons!).

I also changed the accompanying text/titles to highlight the change of credit score---before and after.

#### Iteration after Udacity Review
* Changed data to be more friendly with spaces (so axis and tooltips do not need to be defined)
* Processed data for improved load time
* Modified color scheme from sequential to qualitative

## Feedback
Reviewer #1 (initial iteration):
* What is APR?
* The key is backwards and not completely ordered
* Not sure what she was supposed to be looking for---but she saw the pattern after a few moments. Also some other patterns.

Reviewer #2: (initial iteration)
* Titles are confusing
* What am I supposed to be looking for?

Reviewer #3: (One iteration before first submission)  
* What is CreditGradeCat?
* What are the loan grades? (I had the text missing in the introduction)
* She explored the number of loans---the distribution.
* What DOES affect the prosperRating?

Reviewer #4: (Udacity Reviewer)
* add some more comments to the dimple section of your code
* remove the lines of redundant code and consider adding more white space
* address the three issues highlighted relating to reader/graphic communication
* I'd also highly recommend processing your data so the load time is quicker - 45 seconds is definitely very long!
Communication improvements:
* colour scheme - in your README file you mention that a sequential colour scheme is most suitable but I think in this particular case you would be better off with a qualitative colour scheme such as this. The key aim of your story is to point out the difference in distribution between the loan ratings and a qualitative color scheme will allow the reader to see these differences more clearly.
* Axis and tooltip labels - one of your feedback reviewers asked "What is CreditGradeCat?". It really helps with reader/graphic communication if all labels are accessible and consistent. "Credit Score Group" or something similar would be clearer. Also, NumberOfLoans should have spaces in between the words. This may seem a small point but it makes a bit difference to how your visualisation is perceived. Here is a link to help with tooltips, Here is a link to help with axis labels.
* Credit Score Bins - it would seem to me more logical since you have sorted the bins from max score (900) to min score (0) that the labels should be in the same order - i.e. (900,760) instead of (760,900)?

## Resources
http://stackoverflow.com/questions/31150764/how-to-create-a-new-column-of-data-in-r-with-if-statements

https://stackoverflow.com/questions/6104836/splitting-a-continuous-variable-into-equal-sized-groups

https://stackoverflow.com/questions/31869328/sort-a-list-alphabetically-with-characters-at-the-end

https://www.quora.com/How-do-I-get-a-frequency-count-based-on-two-columns-variables-in-an-R-dataframe
