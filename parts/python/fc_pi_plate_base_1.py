# first run fc_cubic_plate.py
# run it with execfile("your_path_to_this_script") in freecad

name = "PiPlateBase1"
# RaspBerryPi3Case
case_width = 90
case_height = 60

m_hight = 3 # material thickness
cp = CubicPlate(m_hight)
cp.doc(name)

baseplate = Part.makeBox(case_width,case_height,m_hight)
cp.add_shape(baseplate, 'Baseplate')

# latches
latch = cp.latch_short(cp.hole_length,m_hight)
latch.Placement = cp.placement_xyz(cp.hole_length,0 - m_hight,0)
cp.add_shape(latch, 'latch')

latch1 = cp.latch_short(cp.hole_length,m_hight)
latch1.Placement = cp.placement_xyz(cp.hole_length,case_height,0)
cp.add_shape(latch1, 'latch1')

r_dist = case_width - cp.length + cp.hole_length
latch2 = cp.latch_short(cp.hole_length,m_hight)
latch2.Placement = cp.placement_xyz(r_dist,0 - m_hight,0)
cp.add_shape(latch2, 'latch2')

latch3 = cp.latch_short(cp.hole_length,m_hight)
latch3.Placement = cp.placement_xyz(r_dist,case_height,0)
cp.add_shape(latch3, 'latch3')

# finished
App.ActiveDocument.recompute()
