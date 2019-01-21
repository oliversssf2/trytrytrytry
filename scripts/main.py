from library.ROBODK.robolink import *
from library.ROBODK.robodk import *
import pyrealsense2 as rs
import cv2
import numpy as np
import array
import csv

pipeline = rs.pipeline()
profile = pipeline.start()

#