"""
Busca totes les cameres disponibles en Windows
"""

import cv2
from cv2_enumerate_cameras import enumerate_cameras

# MSMF backend
for camera_info in enumerate_cameras(cv2.CAP_MSMF):
    print(camera_info)
    print(camera_info.path)
