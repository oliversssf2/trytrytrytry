from library.ROBODK.robolink import *
from library.ROBODK.robodk import *
import pyrealsense2 as rs
import cv2
import numpy as np
import array
import csv


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile: rs.pipeline_profile = pipeline.start(config)


depth_sensor: rs.sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

align_to = rs.stream.color
align = rs.align(align_to)

clipping_distance_in_meters = 1
clipping_distance = clipping_distance_in_meters / depth_scale

coord = array.array('f', [0,0,0])
intr = profile.as_video_stream_profile().get_intrinsics()

try:
    while True:
        frames = pipeline.wait_for_frames()

        aligned_frames = align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        depth_frame: rs.depth_frame = aligned_frames.get_depth_frame()

        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        bg_removed = np.where((depth_image > clipping_distance) | (depth_image <= 0), 0, depth_image)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(bg_removed, alpha = 0.3), cv2.COLORMAP_JET)

        cv2.namedWindow('hhhh', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('hhhh', depth_colormap)

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q') or key == 27: #SHUT DOWN THE TERMINAL WHILE 'Q' OR ESC IS PRESSED
            cv2.destroyAllWindows()
        if key == ord('h'):
            for i in (0, depth_frame.get_height(), 10):
                for j in (0, depth_frame.get_width(), 10):
                    depth = depth_frame.get_distance(i,j)
                    if depth > 0:
                        tem = array.array('f', [i,j])
                        rs.rs2_deproject_pixel_to_point(coord, intr , tem, depth_frame)
                        f = open("mycsv.csv", "x")
                        f.write(coord[0] + ', ' + coord[1] + ',' + coord[2] + ',' + "0, 0, 180")
            break

finally:
    pipeline.stop()
    #rs.rs2_deproject_pixel_to_point()
    #def save_pointcloud_to_disk(arg0: rs.intrinsics, )

