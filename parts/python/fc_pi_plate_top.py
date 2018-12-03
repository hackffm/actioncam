# first run fc_cubic_plate.py
# run it with execfile("your_path_to_this_script") in freecad

name = "PiPlateTop"
case_length = 129
case_width = 72

m_hight = 3 # material thickness
cp = CubicPlate(m_hight)
cp.doc(name)

# create base elements
baseplate = Part.makeBox(case_length,case_width,m_hight)

# cb_holes are latche holes in the quebe !
cb_hole_length = m_hight * 3
cb_hole = Part.makeBox(cb_hole_length,m_hight,m_hight)

# cut holes
cut = baseplate

cb_hole_number = int(case_length / cp.length)

# border cb_holes around case in quebic distance
for wn in range(cb_hole_number):
    cb_hole_position = cb_hole_length + wn * cp.length
    cb_hole.Placement = cp.placement_xyz(cb_hole_position,m_hight,0)
    cut = cut.cut(cb_hole)
    cb_hole.Placement = cp.placement_xyz(cb_hole_position,case_width - m_hight * 2,0)
    cut = cut.cut(cb_hole)
# network side and sd card side mount cb_holes
border_distance = m_hight *2
# network
cb_hole.Placement = cp.placement_complete(border_distance, cb_hole_length,0,0,0,1, 90)
cut = cut.cut(cb_hole)
cb_hole.Placement = cp.placement_complete(border_distance, case_width - cb_hole_length * 2,0,0,0,1, 90)
cut = cut.cut(cb_hole)
# sdcard
cb_hole.Placement = cp.placement_complete(case_length - cp.length, cb_hole_length,0,0,0,1, 90)
cut = cut.cut(cb_hole)
cb_hole.Placement = cp.placement_complete(case_length - cp.length , case_width - cb_hole_length * 2,0,0,0,1, 90)
cut = cut.cut(cb_hole)

# gab for human interface things as display and buttons
hid_hight = 35
hid_width = 108
hid_hole = Part.makeBox(hid_width,hid_hight,m_hight)
hid_hole.Placement = cp.placement_xyz(m_hight * 2, case_width - m_hight * 2 - hid_hight,0)
cut = cut.cut(hid_hole)
cp.add_shape(cut, 'baseplate')

#finished
App.ActiveDocument.recompute()
