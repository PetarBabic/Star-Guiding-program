import gobject
import os
import time

gobject.threads_init()
 
from dbus import glib
glib.init_threads()
 
import dbus
bus = dbus.SessionBus()

# Create an object that will proxy for a particular remote object.
remote_object = bus.get_object("org.kde.kstars", # Connection name
                            "/KStars/INDI" # Object's path
                            )

iface = dbus.Interface(remote_object, 'org.kde.kstars.INDI')

iface.stop("7624")

mountDriver = "indi_eqmod_telescope"
mountName = "EQMod Mount"
ccdDriver = "indi_asi_ccd"
ccdName = "ZWO CCD ASI120MM Mini"

def connectDevices(deviceList):
    # Connectiong devices
    iface.start("7624", deviceList)

    print("Waiting for INDI devices...")

    devices = []

    while True:
        devices = iface.getDevices()

        if len(devices) < len(deviceList):
            time.sleep(1)
        else:
            break

        print(devices)
    

    print("We received the following devices: ")
    for device in devices:
        print(device)

        # Establishing connection
        # Set connect switch to ON to connect the devices
        iface.setSwitch(device, "CONNECTION", "CONNECT", "On")
        # Send the switch to INDI server so that it gets processed by the driver
        iface.sendProperty(device, "CONNECTION")
        
        # Wait until devices are connected
        while True:
            deviceState = iface.getPropertyState(device, "CONNECTION")
            if deviceState != "Ok":
                time.sleep(1)
            else:
                break

    print("Connection to selected devices succeded")

deviceList = [
    mountDriver,  #Mount        
    ccdDriver     #CCD
]

def guide(direction, lenght):
    if direction == "W" or direction == "E":
        if direction == "W":
            direction = "TIMED_GUIDE_W"
        elif direction == "E":
            direction = "TIMED_GUIDE_E"
        
        iface.setNumber(mountName, "TELESCOPE_TIMED_GUIDE_WE", direction, lenght)
        iface.sendProperty(mountName, "TELESCOPE_TIMED_GUIDE_WE")

        #deviceState(mountName, "TELESCOPE_TIMED_GUIDE_WE")

    if direction == "N" or direction == "S":
        if direction == "N":
            direction = "TIMED_GUIDE_S"
        elif direction == "S":
            direction = "TIMED_GUIDE_S"
    
        iface.setNumber(mountName, "TELESCOPE_TIMED_GUIDE_NS", direction, lenght)
        iface.sendProperty(mountName, "TELESCOPE_TIMED_GUIDE_NS")

        #deviceState(mountName, "TELESCOPE_TIMED_GUIDE_NS")
   
def park(park):
    if park:
        print("Mount is parking...")
        iface.setSwitch(mountName, "TELESCOPE_PARK", "PARK", "On")
        iface.sendProperty(mountName, "TELESCOPE_PARK")

        deviceState(mountName, "TELESCOPE_PARK")
        print("Mount is parked")

    else:
        print("Mount is unparked")
        iface.setSwitch(mountName, "TELESCOPE_PARK", "UNPARK", "On")
        iface.sendProperty(mountName, "TELESCOPE_PARK")

def deviceState(device, standardProperty):
    deviceState = "Busy"

    while True:
        deviceState = iface.getPropertyState(device, standardProperty)
        if deviceState != "Ok":
            time.sleep(1)
        else:
            break

def takeExpouser(expousreLenght):
    print('Taking a ' + str(expousreLenght) + ' second CCD expouser...')
    iface.setNumber(ccdName, "CCD_EXPOSURE", "CCD_EXPOSURE_VALUE", expousreLenght)
    iface.sendProperty(ccdName, "CCD_EXPOSURE")

    #deviceState(ccdName, "CCD_EXPOUSER")

def moveTelescope(ra, dec):
    print("\nTelescope is slewing to: \nRa: " + str(ra) + "\nDec: " + str(dec) + "\n")
    iface.setNumber(mountName, "EQUATORIAL_EOD_COORD", "RA", ra)
    iface.setNumber(mountName, "EQUATORIAL_EOD_COORD", "DEC", dec)
    iface.sendProperty(mountName, "EQUATORIAL_EOD_COORD")

guide("S", 5000)
time.sleep(6)

#iface.stop("7624")