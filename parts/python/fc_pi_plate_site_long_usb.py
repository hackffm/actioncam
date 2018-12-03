# first run fc_cubic_plate.py
# run it with execfile("your_path_to_this_script") in freecad

name = "PiPlateSiteLongUSB"
case_width = 129
case_height = 30

m_hight = 3 # material thickness
cp = CubicPlate(m_hight)
cp.doc(name)

baseplate = Part.makeBox(case_width,case_height,m_hight)
cut = baseplate

# gab for usb and hdmi
cb_gap_length = 39
cb_hole = Part.makeBox(cb_gap_length,m_hight * 4,m_hight)
cb_hole.Placement = cp.placement_xyz(53, m_hight,0)
cut = cut.cut(cb_hole)

cp.add_shape(cut, 'baseplate')

# latches
cb_number = int(case_width / cp.length)
for cube in range(cb_number):
    latch_position = cp.hole_length + cube * cp.length
    #
    latch = cp.latch_short(cp.hole_length,m_hight)
    latch.Placement = cp.placement_xyz(latch_position,0-m_hight,0)
    cp.add_shape(latch, "latch" + str(cube))
    #
    latch_top = cp.latch_short(cp.hole_length,m_hight)
    latch_top.Placement = cp.placement_xyz(latch_position,case_height,0)
    cp.add_shape(latch_top, "latchtop" + str(cube))
# finish adding latches
App.ActiveDocument.recompute()
