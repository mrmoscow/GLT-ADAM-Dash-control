# GLT-ADAM-Dash-control 

This app controls the Greenland telescope(GLT) Receiver and the GLT ADAM module by 2 ways. 
1. CLI interface: several Python scripts under the bin dir. ex: cpy3./rxSelect.py -r 1 
2. HTML interface:  control the GLT-RX by browser, 


### Module requirement
* argparse             1.4.0
* dash                 2.6.1
* dash-core-components 2.0.0
* dash-html-components 2.0.0
* pymodbus             2.5.3
* time


### How to run:
#under gltobscon cpy3 ~/sfyen/GLT-ADAM-Dash-control/app.py   than open browser open http://0.0.0.0:8052  or http://192.168.1.11:8052
#editing the ./asset/typography.css for the page CSS style. 

### About the ReceiverADAM module
* This is a module for this project, in this ReceiverADAM.py there are functions for getting (read status) and setting up the ADAM module. 
* We also list the IP of the ADAM and the unit information in the module.  
* The switch ture table and attenuator voltage will also list here in the future.


### ToDo List
* fix bug in CAB-A3 (for reaging: last two dig, for set re-check)
* new branch for more functions and code structure. 
* a way to show Allan Dev on dahs page.   
* CSS (for updated) file for pages.
* the r page and the baseic.

### Thing finished.
* link ADAM6224 with ASIC  (Done, no need, using the old method)
* a way to get the SA data and make a PNG file. (Done, the SpecAnalyzer.py)
* Test the check of the IP of VVM.  (Done 204)
* This is for test2 

