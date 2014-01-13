"""
 Solid 3D cube simulation.
 graphics.py version by James Futhey <james@jamesfuthey.com>
 Original by Leonel Machava <leonelmachava@gmail.com>
"""
import math
from graphics import *
from time import sleep

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)

class Simulation:
    def __init__(self, win_width = 640, win_height = 480):

        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]

        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        
    def run(self):
        """ Main Loop """
        w=GraphWin("3D Wireframe cube Simulation", 640, 480)
        w.setBackground('black')
        zzyzx=0
        l1 = []        
        while 1:
            sleep(0.02)

            # Will hold transformed vertices.
            t = []
            gx = 0
            
            for v in self.vertices:
                # Rotate the point around X axis, then around Y axis, and finally around Z axis.
                r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
                # Transform the point from 3D to 2D
                p = r.project(640, 480, 500, 4)
                # Put the point in the list of transformed vertices
                t.append(p)


            if(zzyzx == 1):
                l1[0].undraw()
                l1[1].undraw()
                l1[2].undraw()
                l1[3].undraw()
                l1[4].undraw()
                l1[5].undraw()
            else:
                zzyzx=1

            for f in self.faces:
                l1.append([])
                l1[gx]=Polygon(Point(t[f[0]].x, t[f[0]].y), Point(t[f[1]].x, t[f[1]].y), Point(t[f[2]].x, t[f[2]].y), Point(t[f[3]].x, t[f[3]].y))
                l1[gx].setFill('white')
                l1[gx].draw(w)
                gx+=1
                
            self.angleX += 1
            self.angleY += 1
            self.angleZ += 1

if __name__ == "__main__":
    Simulation().run()
