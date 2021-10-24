# raspi-backboiler
back boiler monitoring app in python

This is a scratchpad, as with most projects, it will be messy. This repo serves as a way to move code between a Rasberry Pi 4 and my desktop to make editing and so on easier. Sensors include a set of MAX6675's and DS18B20's on SPI and 1WD.

#Dependencies
Dependencies are on the adafruit boards libraries https://pypi.org/project/Adafruit-Blinka/
* todo: add links to hardware diagrams and tutorials i used
* todo: the pinout printable template
* todo: add python modules
* todo: add matplotlib into this
* todo: add flask web server to the app

#H/W&S/W Components
```
+--------------+  +--------------+  +--------------+     
|              |  |              |  |              |     
| Temperature  |  |  SQLLITE     |  |  Datalogger  |     
|   Sensors    |  |              |  |   history    |     
|              |  |              |  |              |     
+--------------+  +--------------+  +--------------+     
                                                         
+--------------+  +--------------+                       
|              |  |              |                       
|  Pollution   |  |  Arduino     |                       
|  Sensors     |  |   ADC        |                       
|              |  | conversion   |                       
+--------------+  +--------------+                       
```
##Sensors 1WD:
* 4* DS18B20 sensors (boiler hot side) 
* 1* DS18B20 sensors (pump line)
##Sensors SPI:
* 1* MAX6675 thermocouple (flue)

##Planned sensors:
Will connect to a second raspi in loft space 
* 1* Arduino ADC into SPI port (pollution sensor MX1)
* 1* Arduino ADC into SPI port (pollution sensor MX2)
* Serial data acquisition from solar system : 
  todo link blog post for details
  
# Software
Multiple data acquisition and data logging and rendering apps.
todo: configuration notes

* Acquisition app: Read DS81B20's and the MAX6675's and write into sqlilite write each to 1 row of database at 5 second intervals for live data values. 
  Data will also get piped via a filter into a rotating data-logger table. 
* Data-logger routine runs in the acquisition app, will run every 1 minute and filter and deadband the data to save space, into a second table.
  Deadband threshold and timer to ensure a value is written every hour, but no more than every minute. Logger will also use a second filter to write a row into a google docs sheet at least once per 24 hours. Each sensor will have it's own deadband configuration.
* Flask Web server, very basic phase1. Read just the last valid values and display, allow changing of sensor names.
* Flask Web server phase2. Read history sql table and render matplotlib static graphic.
* Acquisition phase2 : Acquisition app to integrate Arduino ADC inputs to read 2 analog values
* Acquisition phase3 : Adds a second raspberry pi. Separate serial data Acquisition app with ethernet TCP "chat socket" conversion and a new "chat protocol". "chat socket acessible from the main acquisition app and added up to 5 new solar panel datas to log with the temperatures. Adapt the logger accordingly with the new datas. 
  Move arduino atmosphere sensors to also use the ethernet "chat socket" protocol instead of directly to host.
* Connect main Raspberry pi to public internet

#Installation steps
 enable 1WD in sudo raspi-config
 enable spi driver in sudo raspi-config
```
 sudo apt-get install python3-pip
 sudo pip3 install --upgrade setuptools
 
 pip3 install adafruit_blinka
 :: Required to install since numpy wants some c library called 
 ::  libf77blas.so.3
 sudo apt-get install libatlas-base-dev
 pip3 install pandas
 pip3 install matplotlib
 pip3 install seaborn
```
## Google docs Integration
(todo)
* setup auth token https://developers.google.com/sheets/api/quickstart/python
* pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
