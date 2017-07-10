# FireflyAstroPi
Sense Hat code 

Purpose: This project will manage Weather data given by the SENSE hat and use it to control the altitude of the Balloon.

-----Plan-----
modules:
- Data logger: Recieves and stores data into files marked by a time stamp. 
- data analyzer: analyzes data to find the the optimal height and calculates absolute humidity
- Tether Contol Master: take optimal height and turns it into tether legnth adjustment and sends it to tether microcontroller.

Algorithm:
start at ground level and elevates to the max altitude, while collecting data. Then it will adjust to the optimal starting point based
on data. Periodically it will move up/down and compare absolute humidity calculations of different adjustment. Will pick adjustment 
with highest absolute humidity. 

---current files---
weather-collector.py: script from first experiment
autoWeather.py: script for upcoming experiment. Will run autonomously on rpi that starts on boot. 
test1.csv: data from first experiment. 


helpful links: 
list of sense Hat functions and the kind of data they produce: https://pythonhosted.org/sense-hat/api/
