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

v1.2.0
* *Average vaccinations graph* fixed so that zeros representing missing data are truncated in the last week.
* Data source attribution and link added to dashboard
* *European Union* added to graphs
* Documentation completed

v1.3.0
* Functionality so that graphs for specific country can be viewed by adding country name to '/country/'. e.g. '/country/denmark'. ('/' still generates the same charts as before)

v1.4.0
* Graph showing total vaccinations improved to seperate between people vaccinated once and people who are fully vaccinated
* Formatting of page improved (through use of Bootstrap framework)
* *European Union* removed due to data issues