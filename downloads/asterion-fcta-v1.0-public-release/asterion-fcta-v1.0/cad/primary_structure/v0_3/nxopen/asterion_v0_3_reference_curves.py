"""NXOpen Python journal starter for ASTERION v0.3 reference curves.

Run inside Siemens NX after creating or opening AST-1100-SPINE-TRUSS.prt.
The journal creates centreline curves only; inspect and adapt to the installed
NX release before saving production data.
"""
import math
import NXOpen

session = NXOpen.Session.GetSession()
work = session.Parts.Work
if work is None:
    raise RuntimeError("Open a work part before running this journal.")

truss_r = 1200.0
x_stations = [-21000,-18500,-16000,-13500,-11000,-8500,-6000,-3500,-2500,-1000,1500,2500,4000,6500,9000,11500,14000,15000,16500,19000,21000]
count = 8

# Create station polygons and longeron segments as associative-independent
# reference curves. Convert them into Tube features manually after audit.
points = {}
for i, x in enumerate(x_stations):
    for j in range(count):
        a = 2.0 * math.pi * j / count
        points[(i,j)] = NXOpen.Point3d(x, truss_r*math.cos(a), truss_r*math.sin(a))
    for j in range(count):
        work.Curves.CreateLine(points[(i,j)], points[(i,(j+1)%count)])

for i in range(len(x_stations)-1):
    step = 1 if i % 2 == 0 else -1
    for j in range(count):
        work.Curves.CreateLine(points[(i,j)], points[(i+1,j)])
        work.Curves.CreateLine(points[(i,j)], points[(i+1,(j+step)%count)])

session.ListingWindow.Open()
session.ListingWindow.WriteLine("ASTERION v0.3 spine reference curves created. Audit geometry before saving.")
