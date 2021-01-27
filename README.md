# NCAA-Betting


This project is looking at historical NCAA basketball data in an attempt to create a model to predict 
whether a team will cover a spread.

Eventually these probabilities will be used in building a betting framework based on the kelly criterion.  



1/7
  - Cleanup Script has been significantly updated locally to turn individual games into useful data.  
  - Example of the structure of that data is provided in Repo
  - Other variables will likely be included in final model

1/8
  - 2017, 2018, 2019 data have been incoorporated.  
  - Favored team rank and underdog rank added into model.
  - My data has the favored team covering the spread 54% of the time. This will be the baseline model accuracy.  (Every Favorite Covers)
  - Initial model and predictions should be out tonight 
  - It will be interesting to compare the performance of model trained on historical data to one only using 2021 data.
  - Although the 2021 dataset will be small, since it is so different perhaps it will be significant. 
  - Initial Models:  Logistic Regression, Random Forest, Support Vector Machine 
 
 ~~ 
 
 ##  ~~  Model Adjusted to predict points by which favored team wins/loses by ~~

 

 ## I want to improve performance and then I will do this regularly
 
   Uploading Predictions To Google Sheet: https://docs.google.com/spreadsheets/d/1oiYz0PIL_gTicayJuRF_QtpKDnBN6EKMO6eXSXrzhR4/edit#gid=1948771975
   
   
 
 ## Vegas Spread is within 3 points of final score 25.7% of the time, that is what I aim to beat 
 

## 
  
 
 Eventually will begin streaming in every game, and having a running total of performance. 
 
 
 1/9 
 - Uploaded final data sample.  
 - Picks are being posted to twitter
 - Will upload the actual model this week, (no training data provided) 
 
 
 1/12
 - Uploaded the full cleanup script 
 - This takes the histroical efficiency metrics as well as a few other key values and turns them into individual data points
 - I use a weighted average 3 most recent games - using the previous games' stats as values for the current matchup in the data. 
 - 3 most recent games account for 60% everything else is 40%
 
 1/13
 - Uploaded initial modeling attempt
 - I used a bunch of different models and attempted to maximize adjusted r^2 as well as my custom scoring metric
 - Initial results are okay, seeing random forest regressor, gradient boosted regressor, and multiple linear regression all have similar performance
 - Next steps will be tuning the hyperparameters more
 - Initially I opted to only use the top 100 NCAA teams in the data set, to improve model performance I will likely expand this soon
 - Currently using 2015-2021 data (This will grow)
 
 
 
 
