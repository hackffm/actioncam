# first run fc_cubic_plate.py
# run it with execfile("your_path_to_this_script") in freecad

# config
name = "PiPlateCameraSiteLong"
case_width = 60
case_height = 30

m_hight = 3 # material thickness
cp = CubicPlate(m_hight)
cp.doc(name)

baseplate = Part.makeBox(case_width,case_height,m_hight)

cb_hole = Part.makeBox(cp.hole_length,m_hight,m_hight)

# cut holes in base plate
cut = baseplate
cb_hole.Placement = cp.placement_xyz(m_hight,m_hight,0)
cut = cut.cut(cb_hole)
cb_hole.Placement = cp.placement_xyz(case_width - cp.hole_length - m_hight,m_hight,0)
cut = cut.cut(cb_hole)
border_distance = case_height - m_hight *2
cb_hole.Placement = cp.placement_xyz(m_hight,border_distance,0)
cut = cut.cut(cb_hole)
cb_hole.Placement = cp.placement_xyz(case_width - cp.hole_length - m_hight,border_distance,0)
cut = cut.cut(cb_hole)
# camera hole
cb_camera = Part.makeBox(cp.hole_length,cp.hole_length,m_hight)
camera_to_button = 10
cb_camera.Placement = cp.placement_xyz(case_width / 2 - m_hight * 2 , camera_to_button)
cut = cut.cut(cb_camera)

cp.add_shape(cut, 'TwoCubesWithCut')

App.ActiveDocument.recompute()
