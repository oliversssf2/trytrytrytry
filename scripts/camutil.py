import pyrealsense2 as rs

def generate_csv_from_image(depth_frame: rs.depth_frame, intr, clipping_distance, file_prefix = "depth_") :
    filename = file_prefix + str(depth_frame.get_frame_number()) + '.csv'
    filedir = '..\prefab\CSVs\\' + filename
    f = open(filedir, 'w+')
    # open the file to save pointcloud data
    width = depth_frame.get_width()
    # get the width of the depth image
    height = depth_frame.get_height()
# get the height of the depth image
    for i in range(0, height, 50):
        # iterate through each row of the depth image
        if i % 2 == 0:
            for j in range(0, width, 50):
                # iterate from left to right in the row if it is in a 2k(even number) row
                depth = depth_frame.get_distance(j, i)
                # get the exact distance of the pixel being iterated
                if depth > 0 and depth < (clipping_distance):
                    # if the distance of that pixel is in the clipping distance
                    coord = rs.rs2_deproject_pixel_to_point(intr, [j, i], depth)  # deproject the pixel
                    # transfer the pixel's 2D coordinate into a 3D coordinate according to camera
                    f.write(str(coord[0]*1000))
                    # save the 3d coodinate to a csv file
                    f.write(' ,')
                    f.write(str(coord[1]*1000))
                    f.write(' ,')
                    f.write(str(coord[2]*1000))
                    f.write(', 0, 0, -1')
                    # set the normal direction of each pixels
                    f.write('\n')
        else:
            for j in range(width - 1, -1, -50):
                # iterate from rijght to left in the row if it is in a 2k+1(odd number) row
                depth = depth_frame.get_distance(j, i)
                if depth > 0 and depth < (clipping_distance):
                    coord = rs.rs2_deproject_pixel_to_point(intr, [j, i], depth)
                    f.write(str(coord[0]*1000))
                    f.write(',')
                    f.write(str(coord[1]*1000))
                    f.write(',')
                    f.write(str(coord[2]*1000))
                    f.write(', 0,  0, -1')
                    f.write('\n')
        # iterate the image from left to right then to the left so the robotic arm will don't have to come back to the leftmost point after
        # scanning every single row
    return filedir