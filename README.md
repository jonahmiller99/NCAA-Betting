# NCAA-Betting


This project is looking at historical NCAA basketball data in an attempt to create a model to predict 
whether a team will cover a spread.

Eventually these probabilities will be used in building a betting framework based on the kelly criterion.  

Update:  Out of nowhere this repo got a lot of traffic. In an effort to not overload the site I am scraping data from I have decided to remove the script that 
I wrote to scrape.  Instead I have uploaded the pickles which are used in the cleanup file in order to show that the scraping and cleanup work. 


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

 
 
 
