from scripts.ROBODK.robodk import *
from scripts.ROBODK.robolink import *

RDK = Robolink()
item = RDK.AddFile(r'D:\Desktop\depth_115.sld')
item.setPose(transl(100, 40, 100))
