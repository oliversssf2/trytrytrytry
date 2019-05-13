# --------------- PROGRAM START ---------------------
from library.ROBODK.robolink import *  # API to communicate with RoboDK
from library.ROBODK.robodk import *  # basic library for robots operations

import csv

#file names:
# DE3CB2~1.CSV

#depth_109.csv
#depth_2486.csv

#Import csv file(containning points) to array
POINTS = []
NUM_POINTS = 0
with open('D:\phoebe\Desktop\cloud_2.csv') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # each row is a list
        POINTS.append(row)
        NUM_POINTS = NUM_POINTS + 1
# Default parameters:
P_START = POINTS[0]   # Start point with respect to the robot base frame

# Initialize the RoboDK API
RDK = Robolink()

# Automatically delete previously generated items (Auto tag)
#list_names = RDK.ItemList()  # list all names
#for item_name in list_names:
   # if item_name.startswith('Auto'):
       # RDK.Item(item_name).Delete()

# Promt the user to select a robot (if only one robot is available it will select that robot automatically)
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)
# Set the initial joints of the robot
#robot.setJoints([0.000000, -90.000000, 70.000000, 0.000000, 112.000000, 0.000000])
#robot.setPose(TxyzRxyz_2_Pose([0, 0, 0, 0, 0, 180]))

# A reference frame of the object(already set)
frame = RDK.Item('Object')


# Abort if the user hits Cancel
if not robot.Valid():
    quit()

# Retrieve the robot reference frame
reference = robot.Parent()

# Use the robot base frame as the active reference
robot.setPoseFrame(reference)
#tool.setPose(transl(474.430,-109.000,607.850)*rotx(-69.282)*roty(69.282)*rotz(-69.282))

# get the current orientation of the robot (with respect to the active reference frame and tool frame)
pose_ref = robot.Pose()

object_curve = RDK.AddCurve(POINTS)
object_curve.setParent(frame)

path_settings = RDK.AddMillingProject("AutoCurveFollow settings")
prog, status = path_settings.setMillingParameters(part=object_curve)

prog.RunProgram()

while True:
    # get the current robot joints
    joints = tr(robot.Joints())
    joints = joints.rows[0]
    print('Current robot joints:')
    print(joints)
