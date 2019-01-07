# first run fc_cubic_plate.py
# run it with execfile("your_path_to_this_script") in freecad

# config
name = "PiPlateCameraSiteLong"
case_width = 60
case_height = 30

m_hight = 3 # material thickness
cp = CubicPlate(m_hight)
cp.doc(name)


cb_hole1 = Part.makeBox(cp.hole_length,m_hight,m_hight)
cb_hole2 = Part.makeBox(cp.hole_length,m_hight,m_hight)
cb_hole3 = Part.makeBox(cp.hole_length,m_hight,m_hight)
cb_hole4 = Part.makeBox(cp.hole_length,m_hight,m_hight)

# cut holes in base plate
cb_hole1.Placement = cp.placement_xyz(m_hight,m_hight,0)
cp.add_shape(cb_hole1, 'hole 1')
cb_hole2.Placement = cp.placement_xyz(case_width - cp.hole_length - m_hight,m_hight,0)
cp.add_shape(cb_hole2, 'hole 2')

border_distance = case_height - m_hight *2
cb_hole3.Placement = cp.placement_xyz(m_hight,border_distance,0)
cp.add_shape(cb_hole3, 'hole 3')
cb_hole4.Placement = cp.placement_xyz(case_width - cp.hole_length - m_hight,border_distance,0)
cp.add_shape(cb_hole4, 'hole 4')

# camera hole
cb_camera = Part.makeBox(cp.hole_length,cp.hole_length,m_hight)
camera_to_button = 10
cb_camera.Placement = cp.placement_xyz(case_width / 2 - m_hight * 2 , camera_to_button)
cp.add_shape(cb_camera, 'camera')

App.ActiveDocument.recompute()
