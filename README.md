# sqlalchemy-challenge
Module 10 Challenge

This challenge is a climate analysis about Honolulu, Hawaii.  I have been provided csv files with data to analyse

Using sqlalchemy, created a relational map across the 2 csv files provided.

We only wanted to look at the last 12 months precitpitation data so calculated the 12 month window using the measurement date and copied this into a new datafram called precipitaiton_df.

I was then able to create a bar graph.
Along with the bar graph, there are summary statistics proivded for revision.


Some analysis of weather stations was also done.  
A count of how many times a weather station has provided measurement data, and then for the station with highest number of active uses, a lower level investgaion of the lowest, highest and average temperature was calculated. 

A histogram was created to display the temperature range and the frequency of each.


After the first analysis completed and the 2 graphs created, a new Flask API app was used.

The following routes were created and data queried:
1./
•create the homepage and list all the routes

2./api/v1.0/precipitation
•a dictionary of precipitation by date (date as the key and prcp as the value).

3./api/v1.0/stations
•A list of all measurement stations

4./api/v1.0/tobs
•A list of temperature observations for the previous year for the most active station.

5./api/v1.0/<start> and /api/v1.0/<start>/<end>
•List of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
•For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
•For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
Note:  Dates to be entered at the end of the url using yyyy-mm-dd format