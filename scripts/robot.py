

# ---------------------------------------------------
# --------------- PROGRAM START ---------------------
from robolink import *  # API to communicate with RoboDK
from robodk import *  # basic library for robots operations
import csv

#file names:
# DE3CB2~1.CSV
#depth_215 - 複製.csv

#Import csv file(containning points) to array
POINTS = []
with open('D:\phoebe\Desktop\DE3CB2~1.CSV') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # each row is a list
        POINTS.append(row)

# Default parameters:
P_START = POINTS[0]   # Start point with respect to the robot base frame

# Initialize the RoboDK API
RDK = Robolink()

# turn off auto rendering (faster)
RDK.Render(False)

# Automatically delete previously generated items (Auto tag)
#list_names = RDK.ItemList()  # list all names
#for item_name in list_names:
   # if item_name.startswith('Auto'):
       # RDK.Item(item_name).Delete()

# Promt the user to select a robot (if only one robot is available it will select that robot automatically)
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)
# Set the initial joints of the robot
robot.setJoints([0,-90,-90,0,90,0])
#robot.setPose(TxyzRxyz_2_Pose([0, 0, 0, 0, 0, 180]))

# A reference frame of the object(already set)
frame = RDK.Item('Object')

# Turn rendering ON before starting the simulation
RDK.Render(True)

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

# a pose can also be defined as xyzwpr / xyzABC
# pose_ref = TxyzRxyz_2_Pose([100,200,300,0,0,pi])


# Create a follow curve project

# Create a new object given the list of points:
object = RDK.Item('Object', ITEM_TYPE_OBJECT)
object_curve = object.AddCurve(POINTS, PROJECTION_ALONG_NORMAL_RECALC)
#object_curve = RDK.AddCurve(POINTS)
#The object curve is relative to the frame "object" that has been set already
object_curve.setParent(frame)
#frame.setPose(TxyzRxyz_2_Pose([474.430,-109.000,607.850,-69.282,69.282,-69.282]))
#frame.setPose(transl(474.430,-109.000,607,850)*rotx(-69.282)*roty(69.282)*rotz(-69.282))


# Alternatively, we can project the points on the object surface
#object = RDK.Item('Object', ITEM_TYPE_OBJECT)
#object_curve = object.AddCurve(POINTS, PROJECTION_ALONG_NORMAL_RECALC)
# Place the curve at the same location as the reference frame of the object
#object_curve.setParent(object.Parent())

# Create a new "Curve follow project" to automatically follow the curve
path_settings = RDK.AddMillingProject("AutoCurveFollow settings")
prog, status = path_settings.setMillingParameters(part=object_curve)
# At this point, we may have to manually adjust the tool object or the reference frame

# Run the create program if success
prog.RunProgram()

# Done
quit()



