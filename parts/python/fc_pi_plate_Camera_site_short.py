# first run fc_cubic_plate.py
# run it with execfile("your_path_to_this_script") in freecad

# config
name = "PiPlateCameraSiteShort"
case_width = 60
case_height = 12

m_hight = 3 # material thickness
cp = CubicPlate(m_hight)
cp.doc(name)

baseplate = Part.makeBox(case_width,case_height,m_hight)

# camera flat wire hole
camera_wire_hole = 26
cb_camera = Part.makeBox(camera_wire_hole,m_hight,m_hight)
cb_camera.Placement = cp.placement_xyz(case_width / 2 - camera_wire_hole / 2, m_hight)
cut = baseplate.cut(cb_camera)

cp.add_shape(cut, 'PlateWithLatches')

# latches
latch = cp.latch(cp.hole_length,cp.hole_length,m_hight)
latch.Placement = cp.placement_xyz(m_hight,0 -cp.hole_length,0)
cp.add_shape(latch, 'latch')

latch1 = cp.latch(cp.hole_length,cp.hole_length,m_hight)
latch1.Placement = cp.placement_xyz(m_hight,case_height,0)
cp.add_shape(latch1, 'latch1')

r_dist = case_width - m_hight * 4
latch2 = cp.latch(cp.hole_length,cp.hole_length,m_hight)
latch2.Placement = cp.placement_xyz(r_dist,0 -cp.hole_length,0)
cp.add_shape(latch2, 'latch2')

latch3 = cp.latch(cp.hole_length,cp.hole_length,m_hight)
latch3.Placement = cp.placement_xyz(r_dist,case_height,0)
cp.add_shape(latch3, 'latch3')

App.ActiveDocument.recompute()
