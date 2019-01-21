import pyrealsense2 as rs
import cv2
import numpy as np
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
        display_image = np.hstack((color_image, depth_colormap))

        cv2.namedWindow('hhhh', cv2.WINDOW_AUTOSIZE)
        #create a opencv window
        cv2.imshow('hhhh', display_image)
        #show the colorized depth image

        key = cv2.waitKey(1)

        if key & 0xFF == ord('q') or key == 27: #SHUT DOWN THE TERMINAL WHILE 'Q' OR ESC IS PRESSED
            cv2.destroyAllWindows()
            break
        if key == ord('h'):
            f = open("mycsv.csv", 'w')
            #open the file to save pointcloud data
            width = depth_frame.get_width()
            #get the width of the depth image
            height = depth_frame.get_height()
            #get the height of the depth image
            for i in range(0, height, 5):
                #iterate through each row of the depth image
                if i % 2 == 0:
                    for j in range(0, width, 5):
                        #iterate from left to right in the row if it is in a 2k(even number) row
                        depth = depth_frame.get_distance(j, i)
                        #get the exact distance of the pixel being iterated
                        if depth > 0 and depth < 1:
                            #if the distance of that pixel is in the clipping distance
                            coord = rs.rs2_deproject_pixel_to_point(intr, [j,i], depth) #deproject the pixel
                            #transfer the pixel's 2D coordinate into a 3D coordinate according to camera
                            f.write(str(coord[0] * 1000))
                            #save the 3d coodinate to a csv file
                            f.write(' ,')
                            f.write(str(coord[1] * 1000))
                            f.write(' ,')
                            f.write(str(coord[2] * 1000))
                            f.write(', 0, 0, 180')
                            #set the normal direction of each pixels
                            f.write('\n')
                else:
                    for j in range(width - 1, -1, -5):
                        #iterate from rijght to left in the row if it is in a 2k+1(odd number) row
                        depth = depth_frame.get_distance(j, i)
                        if depth > 0 and depth < 1:
                            coord = rs.rs2_deproject_pixel_to_point(intr, [j, i], depth)
                            f.write(str(coord[0] * 1000))
                            f.write(',')
                            f.write(str(coord[1] * 1000))
                            f.write(',')
                            f.write(str(coord[2] * 1000))
                            f.write(', 0,  0, 180')
                            f.write('\n')
                #iterate the image from left to right then to the left so the robotic arm will don't have to come back to the leftmost point after
                #scanning every single row
finally:
    pipeline.stop() #stop the camera at last
