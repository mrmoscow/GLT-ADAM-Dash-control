# GLT-ADAM-Dash-control 

This is a dash app for GreenLand telescope(GLT) which using HTML interface to control the GLT ADAM module. 
In this app, the different py file (under the page dir)  if for control different ADAM module.  
There is also CLI app which under the bin dir, which can be use under tht CLI. 
There are also sample CSS style which can be changed by edit the ./asset/typography.css


###Module requiresement
* argparse             1.4.0
* dash                 2.6.1
* dash-core-components 2.0.0
* dash-html-components 2.0.0
* pymodbus             2.5.3
* time

### How to run:
under gltobscon cpy3 ~/sfyen/GLT-ADAM-Dash-control/app.py   than open brower open http://0.0.0.0:8052  or http://192.168.1.11:8052
or python3 app.py

### About the ReceiverADAM module
* This is a module for this project, in this ReceiverADAM.py there are functions for get(read infromation) and set the ADAM module. 
* We also list the IP of the ADAM and the unit information in the module.  
* The switch ture table and attentatur voltage will also list here in the future.


### ToDo List
* link ADAM6224 with ASIC
* a way for get the SA data and make a png file.
* new bin app and dash page for control VVM and phase monitot
* a way for show the Allan Dev on dahs page.
* CSS(for updated) file for pages (C1 at lease)
* The new code stucture.(the ReceiverADAM is too big now.)



### Gold for testing day on 2024, Jan
* the SA image got
* the image shows


