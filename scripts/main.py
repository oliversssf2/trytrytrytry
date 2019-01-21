import pyrealsense2 as rs
import cv2
import numpy as np

pipeline = rs.pipeline()
cfg = pipeline.start()
profile = cfg.get_stream(rs.stream.depth)
intr = profile.as_video_stream_profile().get_intrinsics()

depth_sensor: rs.sensor = cfg.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

align_to = rs.stream.color
align = rs.align(align_to)

clipping_distance_in_meters = 1
clipping_distance = clipping_distance_in_meters / depth_scale

coord = [0,0,0]

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
            break
        if key == ord('h'):
            f = open("mycsv.csv", 'w')
            i = 0
            j = 0
            tem = [0, 0]
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            for i in range(0, height, 5):
                if i%2 == 0:
                    for j in range(0, width, 5):
                        depth = depth_frame.get_distance(j,i)
                        if depth > 0 and depth < 1:
                            coord = rs.rs2_deproject_pixel_to_point(intr, [j,i], depth)
                            f.write(str(coord[0] * 1000))
                            f.write(',')
                            f.write(str(coord[1] * 1000))
                            f.write(',')
                            f.write(str(coord[2] * 1000))
                            f.write('\n')
                else:
                    for j in range(width - 1, -1, -5):
                        depth = depth_frame.get_distance(j, i)
                        if depth > 0 and depth < 1:
                            coord = rs.rs2_deproject_pixel_to_point(intr, [j, i], depth)
                            f.write(str(coord[0] * 1000))
                            f.write(',')
                            f.write(str(coord[1] * 1000))
                            f.write(',')
                            f.write(str(coord[2] * 1000))
                            f.write('\n')
finally:
    pipeline.stop()
    #rs.rs2_deproject_pixel_to_point()
    #def save_pointcloud_to_disk(arg0: rs.intrinsics, )


