# first run fc_cubic_plate.py
# run it with execfile("your_path_to_this_script") in freecad

# config
name = "Lock30"
case_width = 30
case_height = 15

m_hight = 3 # material thickness
cp = CubicPlate(m_hight)
cp.doc(name)

baseplate = Part.makeBox(case_width,case_height,m_hight)

cb_hole = Part.makeBox(case_width - m_hight,m_hight,m_hight)

# cut holes in base plate
cut = baseplate
cb_hole.Placement = cp.placement_xyz(m_hight,m_hight,0)
cut = cut.cut(cb_hole)
cb_hole.Placement = cp.placement_xyz(m_hight,case_height - m_hight * 2,0)
cut = cut.cut(cb_hole)

cp.add_shape(cut, 'Lock30mm')

App.ActiveDocument.recompute()
