"""ASTERION FCTA-1 Version 0.2 NXOpen journal starter.

Run inside Siemens NX using Tools > Journal > Play. It creates named wireframe
reference geometry only: centreline, station ticks, ring polygons, solar
rectangles, pod axes and the Skimmer envelope. Rebuild datums and expressions
according to nx_build_tutorial.md after reviewing the geometry.

NXOpen interfaces can differ by NX release. Test in a copy of the part first.
"""
from __future__ import annotations

import math
import NXOpen

MM = 1.0

STATIONS = [
    ("STA_00", -21000.0), ("STA_10", -16000.0), ("STA_20", -8000.0),
    ("STA_30", -2500.0), ("STA_40", 2500.0), ("STA_50", 9000.0),
    ("STA_60", 15000.0), ("STA_70", 21000.0),
]


def add_line(work_part, p1, p2, name, layer):
    line = work_part.Curves.CreateLine(NXOpen.Point3d(*p1), NXOpen.Point3d(*p2))
    line.SetName(name)
    line.Layer = layer
    return line


def polygon_yz(work_part, x, radius, count, prefix, layer):
    pts = []
    for i in range(count):
        a = 2.0 * math.pi * i / count
        pts.append((x, radius * math.cos(a), radius * math.sin(a)))
    for i in range(count):
        add_line(work_part, pts[i], pts[(i + 1) % count], f"{prefix}_{i+1:02d}", layer)


def rectangle_xy(work_part, x1, x2, y1, y2, z, prefix, layer):
    pts = [(x1,y1,z),(x2,y1,z),(x2,y2,z),(x1,y2,z)]
    for i in range(4):
        add_line(work_part, pts[i], pts[(i+1)%4], f"{prefix}_{i+1}", layer)


def rectangle_xz(work_part, x1, x2, z1, z2, y, prefix, layer):
    pts = [(x1,y,z1),(x2,y,z1),(x2,y,z2),(x1,y,z2)]
    for i in range(4):
        add_line(work_part, pts[i], pts[(i+1)%4], f"{prefix}_{i+1}", layer)


def main():
    session = NXOpen.Session.GetSession()
    work_part = session.Parts.Work
    if work_part is None:
        raise RuntimeError("Open or create a metric NX part before playing this journal.")

    mark = session.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "ASTERION V0.2 skeleton")

    # Layer 10: global centreline and station references
    add_line(work_part, (-21000,0,0), (21000,0,0), "CL_VEHICLE_X", 10)
    for sid, x in STATIONS:
        add_line(work_part, (x,-1500,0), (x,1500,0), f"TICK_{sid}_Y", 10)
        add_line(work_part, (x,0,-1500), (x,0,1500), f"TICK_{sid}_Z", 10)

    # Layer 20: 72-sided ring outer and inner envelopes
    for prefix, x in (("RING_A",-2500.0),("RING_B",2500.0)):
        polygon_yz(work_part, x, 13000.0, 72, prefix + "_OUTER", 20)
        polygon_yz(work_part, x, 11000.0, 72, prefix + "_INNER", 20)

    # Layer 30: solar deployed rectangles, 58 m tip-to-tip
    x1, x2 = 6900.0, 11100.0
    rectangle_xy(work_part, x1, x2, 1200.0, 29000.0, 0.0, "SOLAR_PY", 30)
    rectangle_xy(work_part, x1, x2, -29000.0, -1200.0, 0.0, "SOLAR_NY", 30)
    rectangle_xz(work_part, x1, x2, 1200.0, 29000.0, 0.0, "SOLAR_PZ", 30)
    rectangle_xz(work_part, x1, x2, -29000.0, -1200.0, 0.0, "SOLAR_NZ", 30)

    # Layer 40: propulsion pod axes
    for i in range(6):
        a = math.radians(i*60.0)
        y, z = 3000.0*math.cos(a), 3000.0*math.sin(a)
        add_line(work_part, (-21000,y,z), (-15800,y,z), f"POD_{i+1:02d}_AXIS", 40)

    # Layer 50: Skimmer envelope centreline and maximum-width cross line
    add_line(work_part, (21000,0,0), (29000,0,0), "SKIMMER_CL", 50)
    add_line(work_part, (25200,-2750,0), (25200,2750,0), "SKIMMER_MAX_WIDTH", 50)
    add_line(work_part, (25200,0,-1050), (25200,0,1050), "SKIMMER_MAX_HEIGHT", 50)

    session.SetUndoMarkName(mark, "ASTERION V0.2 skeleton complete")
    work_part.ModelingViews.WorkView.Fit()


if __name__ == "__main__":
    main()
