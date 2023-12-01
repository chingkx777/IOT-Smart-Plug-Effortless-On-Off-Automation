import socket
import network
import camera
import time

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to the network...')
    wlan.connect('HUAWEI nova 7', 'nova7140720')

    while not wlan.isconnected():
        pass
print('Network configuration:', wlan.ifconfig())

# Initialize the camera
try:
    camera.init(0, format=camera.JPEG)
except Exception as e:
    camera.deinit()
    camera.init(0, format=camera.JPEG)

# Other settings:
# Flip up and down
camera.flip(1)
# Mirror left/right
camera.mirror(1)

# Resolution
camera.framesize(camera.FRAME_HVGA)
# Options:
# FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
# FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
# FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
# FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
# FRAME_P_FHD FRAME_QSXGA
# For more details, see this link: https://bit.ly/2YOzizz

# Special effects
camera.speffect(camera.EFFECT_NONE)
# Options:
# EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO

# White balance
# camera.whitebalance(camera.WB_HOME)
# Options:
# WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

# Saturation
camera.saturation(0)
# -2 to 2 (default 0). -2 for grayscale, 2 for high saturation

# Brightness
camera.brightness(0)
# -2 to 2 (default 0). 2 for high brightness

# Contrast
camera.contrast(0)
# -2 to 2 (default 0). 2 for high contrast

# Quality
camera.quality(10)
# 10-63, with a lower number indicating higher quality

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

try:
    while True:
        buf = camera.capture()  # Get image data
        s.sendto(buf, ("192.168.43.140", 9090))  # Send image data to the server
        time.sleep(0.1)
except:
    pass
finally:
    camera.deinit()
