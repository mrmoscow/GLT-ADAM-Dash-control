import socket
import vvmbase as vvm
#sys.path.append('/var/www/cgi-bin/GLT')

vvm.set_device()

# Take Measurements
vvm.sendVVM("DAN OFF")
vvm.sendVVM("SENSE AVOL")
vvm.sendVVM("FORM LIN")
avol = vvm.queryVVM("MEAS? AVOL")
vvm.sendVVM("SENSE BVOL")
vvm.sendVVM("FORM LIN")
bvol = vvm.queryVVM("MEAS? BVOL")
vvm.sendVVM("SENSE PHASE")
vvm.sendVVM("FORM POL")
phase = vvm.queryVVM("MEAS? PHASE")
vvm.sendVVM("DAN ON")
vvm.sendVVM("SYST:KEY 2")

print('A volts: ',str(avol),' B Volts: ',str(bvol),' B-A Phase: ',str(phase))
