## Final report
The purpose of this document is to summarize and present our findings related to question 17 of the third exercise in Data Oriented Programming Paradigms. The analysis discussed below aims to explain potential trends in modal split across multiple countries, i.e. with which means of transport people tend to move, and how this tendency has changed over time. 

In order to allow for better comparisons among countries, we chose to focus on European countries only, because transportation related data is recorded on a regular basis as part of the continuous monitoring efforts of the European Union. The Eurostat statistical office offers such data on their official website, from which we have analyzed and studied several transport-related datasets in the time period ranging from 1994 up until 2020. 

The benefit of using these datasets is that the information extracted can be studied on a yearly basis and grouped together on the country level. Nevertheless, it was necessary to develop a standardized way of preprocessing all data, which included transforming data columns, dealing with missing data or special data formats, and aggregating information per country and year.

The biggest challenge in the preprocessing step was the missing data that several European countries have for the earlier years of this analysis (1990-2009). Unfortunately, not all countries have had the appropriate infrastructure to record transport related data in the past, which is why many of them have missing information up until 1994 (Bulgaria, Hungary), 1998 (Estonia, North Macedonia), 2000 (Lithuania, Netherlands), or even 2009 (Montenegro, Serbia). Therefore, for certain questions – such as the change of modal split over time – we decided to restrict the analysis only to countries that had data available for the full time period studied. 

We considered to extrapolate over the missing years using SPLINE extrapolation or linear models, but we concluded that it will be difficult to predict estimates for such long time periods, because for those countries, there is no data available for 4, 10, or even 15 consecutive years.  Additionally, the relatively large number of 17+ remaining European countries - that don’t have any missing information - still allows us to extensively analyze the modal split even when removing missing data.

We were able to distinguish different kinds of modal split tendencies that differ in transportation type usage. Firstly, countries mainly located in Western Europe – such as the United Kingdom, Norway, Netherlands, France, Austria, or Germany – heavily rely on and consistently use car transportation as their main form of transport, where transportation by car makes up around 80% of usage, and bus and train transport usually revolve around 10% in proportions. This trend remains steady over the course of the last 30 years. Secondly, countries located in Eastern Europe – such as Bulgaria, Czech Republic, North Macedonia, Poland, or Slovenia – tend to have a considerably lower car transportation usage, with bus transport proportions consistently reaching up to ~30% in the majority of years studied. Lastly, there are group of countries that exhibit very strong changes in modal split tendencies – such as Slovakia, Romania, and Turkey. Over the course of 25 years, Slovakia went from a bus-transportation proportion of more than 40% in 1993-1998, to predominantly using cars for transportation from 2000-2019. Romania’s transport usage, on the other hand, is by car over the whole study period (1995-2019), but has experienced a consistent decrease in train transport usage from almost 30% in 1995 to less than 5% in 2019. Similarly, Turkey’s most extensively used form of transportation was bus-transport from 1990-2001 with more than 50% usage over the whole time period, but this tendency has changed to bus transportation decreasing down to 30% and car transportation continuously increasing from ~28% in 1990 to over 70% in 2019. 










