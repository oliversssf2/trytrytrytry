from library.ROBODK.robolink import *
from library.ROBODK.robodk import *

RDK = Robolink()
item = RDK.AddFile(r'D:\Desktop\depth_115.sld')
item.setPose(transl(100, 40, 100))
#kjkkjk

