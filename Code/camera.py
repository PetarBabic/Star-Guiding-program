import zwoasi as asi
import time

global binning
binning = 1

asi.init('/home/astroberry/Desktop/zavrsni/1.18/linux_sdk/lib/armv7/libASICamera2.so.1.18')

num_cameras = asi.get_num_cameras()
if num_cameras == 0:
    raise ValueError('No cameras found')

camera_id = 0  # use first camera from list
cameras_found = asi.list_cameras()
print(cameras_found)
camera = asi.Camera(camera_id)

# Use minimum USB bandwidth permitted
camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MinValue'])

camera.set_control_value(asi.ASI_MONO_BIN, binning)
camera.set_roi(bins=binning)

# Set some sensible defaults. They will need adjusting depending upon
# the sensitivity, lens and lighting conditions used.
camera.disable_dark_subtract()


def capture(expouser, gain):
    while(True):
        camera.set_control_value(asi.ASI_GAIN, gain)
        camera.set_control_value(asi.ASI_EXPOSURE, expouser * 1000000) # microseconds

        filename = 'image_mono.tif'
        camera.set_image_type(asi.ASI_IMG_RAW8)
        if(camera.capture(filename=filename)):
            break

    time.sleep(expouser + 0.1)

    return "./image_mono.tif"

def guide(direction, duration):
    if direction == "N":
        camera.pulse_guide_on(asi.ASI_GUIDE_NORTH)
    elif direction == "S":
        camera.pulse_guide_on(asi.ASI_GUIDE_SOUTH)
    elif direction == "E":
        camera.pulse_guide_on(asi.ASI_GUIDE_EAST)
    elif direction == "W":
        camera.pulse_guide_on(asi.ASI_GUIDE_WEST)

    time.sleep(duration)

    camera.pulse_guide_off(asi.ASI_GUIDE_NORTH)
    camera.pulse_guide_off(asi.ASI_GUIDE_SOUTH)
    camera.pulse_guide_off(asi.ASI_GUIDE_EAST)
    camera.pulse_guide_off(asi.ASI_GUIDE_WEST)
    
    time.sleep(duration)

def StartGuide(direction):
    if direction == "N":
        camera.pulse_guide_on(asi.ASI_GUIDE_NORTH)
    elif direction == "S":
        camera.pulse_guide_on(asi.ASI_GUIDE_SOUTH)
    elif direction == "E":
        camera.pulse_guide_on(asi.ASI_GUIDE_EAST)
    elif direction == "W":
        camera.pulse_guide_on(asi.ASI_GUIDE_WEST)

def StopGuide(direction):
    if direction == "N":
        camera.pulse_guide_off(asi.ASI_GUIDE_NORTH)
    elif direction == "S":
        camera.pulse_guide_off(asi.ASI_GUIDE_SOUTH)
    elif direction == "E":
        camera.pulse_guide_off(asi.ASI_GUIDE_EAST)
    elif direction == "W":
        camera.pulse_guide_off(asi.ASI_GUIDE_WEST)