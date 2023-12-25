# GLT-ADAM-Dash-control 

This is a dash app for GreenLand telescope(GLT) which using HTML interface to control the GLT ADAM module. 
In this app, the different py file (under the page dir)  if for control different ADAM module.  
There are also sample CSS style which can be changed by edit the ./asset/typography.css


###Module requiresement
* argparse             1.4.0
* dash                 2.6.1
* dash-core-components 2.0.0
* dash-html-components 2.0.0
* pymodbus             2.5.3
* time

### How to run:
python3 app.py 
or under  gltobscon 
cpy3 ~/sfyen/GLT-ADAM-Dash-control/app.py
than open brower open http://0.0.0.0:8052

### About the ReceiverADAM module
* This is a module for this project, in this ReceiverADAM.py there are functions for get(read infromation) and set the ADAM module. 
* We also list the IP of the ADAM and the unit information in the module.  
* The switch ture table and attentatur voltage will also list here in the future.



