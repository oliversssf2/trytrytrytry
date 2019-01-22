import pyrealsense2 as rs
import cv2
import numpy as np
from scripts.camutil import *
from scripts.robot import *
#import libraries

pipeline = rs.pipeline()
cfg = pipeline.start()
#save the configuration imformation of the realsense camera to access the camera later
profile = cfg.get_stream(rs.stream.depth)
#get stream profile
intr = profile.as_video_stream_profile().get_intrinsics()
#get the intrinsic values(size, fov, principle point of projection etc.) of the camera

depth_sensor: rs.sensor = cfg.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
#get the depth scale of the depth camera to calculate the distance in the real world

align_to = rs.stream.color
align = rs.align(align_to)
#align the depth stream to color stream

clipping_distance_in_meters = 1
#set the threshold of image clipping in meter
clipping_distance = clipping_distance_in_meters / depth_scale
#transform the distance according to the depth scale

current_CSV_direction = ''
coord = [0,0,0]

try:
    while True:
        frames = pipeline.wait_for_frames()
        #wait of a set of frame

        aligned_frames = align.process(frames)
        #align those frames

        color_frame = aligned_frames.get_color_frame()
        depth_frame: rs.depth_frame = aligned_frames.get_depth_frame()

        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        #transform the frames into arrays with numpy

        bg_removed = np.where((depth_image > clipping_distance) | (depth_image <= 0), 0, depth_image)
        #clip the object out of the depth image according to clipping distance

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(bg_removed, alpha = 0.3), cv2.COLORMAP_JET)
        #colorize the clipped depth image
        display_image = np.column_stack((color_image, depth_colormap))

        cv2.namedWindow('hhhh', cv2.WINDOW_AUTOSIZE)
        #create a opencv window
        cv2.imshow('hhhh', display_image)
        #show the colorized depth image

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q') or key == 27: #SHUT DOWN THE TERMINAL WHILE 'Q' OR ESC IS PRESSED
            cv2.destroyAllWindows()
            break
        if key == ord('h'):
            current_CSV_direction = generate_csv_from_image(depth_frame, intr)
        if key == ord('s'):
            if current_CSV_direction != '':
                start_simulation_with_file(current_CSV_direction)

finally:
    pipeline.stop() #stop the camera at last
