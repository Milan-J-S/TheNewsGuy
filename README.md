# TheNewsGuy

A news recommender based on collaborative filtering

To run project pip install flask, flask_cors, time, datetime, json, requests, sklearn, numpy and pickle.

The latest solution server is in improvedSolutionForRareTopics.py
Run in python terminal and view from localhost:5000 on web browser with the following urls:
1.  http://localhost:5000/getNews?q=Real Madrid (to get data collected on Real Madrid)
2.  http://localhost:5000/getRec?q=Real Madrid (to get Recommendation for this topic based on similar previourly searched topics)

Please note atleast three searches must be made for appropriate recommendations
