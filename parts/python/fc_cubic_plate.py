# run it with execfile("your_path_to_this_script") in freecad

class CubicPlate():
    def __init__(self, material_hight):
        self.hight = material_hight
        self.hole_length = material_hight * 3
        self.length = material_hight * 10

    def add_shape(self, shape, name):
        plate_obj = App.ActiveDocument.addObject("Part::Feature", name)
        plate_obj.Shape = shape

    def doc(self, name):
        Gui.activateWorkbench("PartWorkbench")
        App.newDocument(name)
        App.setActiveDocument(name)
        App.ActiveDocument = App.getDocument(name)
        Gui.ActiveDocument = Gui.getDocument(name)

    def latch(self, l_x, l_y, l_z):
        _latch = Part.makeBox(l_x, l_y, l_z)
        _latch_hole = Part.makeBox(l_z, l_z, l_z)
        _latch_hole.Placement = self.placement_xyz(l_z, l_z, 0)
        _latch = _latch.cut(_latch_hole)
        return _latch

    def latch_short(self, l_x, l_z):
        l_y = l_z
        _latch = Part.makeBox(l_x,l_y,l_z)
        return _latch

    def placement_complete(self, x=0,y=0,z=0, yaw=0, pitch=0, roll=0, degree=0):
        # todo make this work
        pl = FreeCAD.Placement(App.Vector(x,y,z),App.Rotation(App.Vector(yaw,pitch,roll),degree))
        return pl

    def placement_xyz(self, x=0,y=0,z=0):
        pl = FreeCAD.Placement()
        pl.move(FreeCAD.Vector(x,y,z))
        return pl
