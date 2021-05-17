Covid Web App
==============
Web app showing current data on covid cases, deaths and vaccinations.

Changelog
---------
v1.0.0
* Initial version
* Based on code migrated from [covid-analysis](https://github.com/easystef/covid-analysis) project.
* Basic Flask app gives a page with basic current statistics for Germany, Netherlands, Slovakia and the UK.
* Code for *bokeh* graphs still present in this version, but not yet used.

v1.1.0
* Main graphs reintroduced
* Set up with very basic HTML/CSS

v1.1.1
* *Average vaccinations graph* fixed so that zeros representing missing data are truncated in the last week.
* Data source attribution and link added to dashboard
* Documentation completed