# first run fc_cubic_plate.py
# run it with execfile("your_path_to_this_script") in freecad

name = "PiPlateBase"
case_length = 129
case_height = 72

m_hight = 3 # material thickness
cp = CubicPlate(m_hight)
cp.doc(name)

baseplate = Part.makeBox(case_length,case_height,m_hight)
cb_hole = Part.makeBox(cp.hole_length,m_hight,m_hight)

# cut holes
cut = baseplate

cb_hole_number = int(case_length / cp.length)
for wn in range(cb_hole_number):
    cb_hole_position = cp.hole_length + wn * cp.length
    cb_hole.Placement = cp.placement_xyz(cb_hole_position,m_hight,0)
    cut = cut.cut(cb_hole)
    cb_hole.Placement = cp.placement_xyz(cb_hole_position,case_height - m_hight * 2,0)
    cut = cut.cut(cb_hole)
# network side and sd card side mount cb_holes
border_distance = m_hight *2
# network side
cb_hole.Placement = cp.placement_complete(border_distance, cp.hole_length,0,0,0,1, 90)
cut = cut.cut(cb_hole)
cb_hole.Placement = cp.placement_complete(border_distance, case_height - cp.hole_length * 2,0,0,0,1, 90)
cut = cut.cut(cb_hole)
# sdcard side
cb_hole.Placement = cp.placement_complete(case_length - cp.length, cp.hole_length,0,0,0,1, 90)
cut = cut.cut(cb_hole)
cb_hole.Placement = cp.placement_complete(case_length - cp.length , case_height - cp.hole_length * 2,0,0,0,1, 90)
cut = cut.cut(cb_hole)
cp.add_shape(cut, 'baseplate')

# finished
App.ActiveDocument.recompute()
