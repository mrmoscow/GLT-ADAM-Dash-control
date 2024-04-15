

**How to colleect the vvm data. 
# need Vector
# run cpy3 ../bin/AllanVVM.py 100000 2 345 -30
# first paremeter is the time (in second) to run, 2 mesn run 2 loops. 
# 345 is the LO frequency (must be correct!), -30 is the power for RF (just for note)

**Move the vvm data to from bin to this dir. 
# cp ../bin/Phase*.txt ./

** How to deal with the vvm data.
cpy3 ./plotVVM.py Phase_020224_143049_1_1_RF648.txt
# it will need AmpPhaseToolsRanjani.py and computeAVRanjani
# computeAVRanjani is a bin code just work in x86 (or x86_64) linux. 
