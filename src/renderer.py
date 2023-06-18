from PIL import Image
import random
from src.maths.vector import Vector3d, Vector2d

WHITE = (255,255,255)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def line(v1, v2, image, color=(255,255,255)):
    x0,y0 = v1[0], v1[1]
    x1,y1 = v2[0], v2[1]

    steep = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0,y0 = y0,x0
        x1,y1 = y1,x1
        steep = True
    
    if x0 > x1:
        x0,x1 = x1,x0
        y0,y1 = y1,y0

    for x in range(x0, x1):
        t = (x-x0) / float(x1 - x0)
        y = int(y0*(1.-t) + y1*t)

        try:
            if steep:
                image[y,x] = color
            else:
                image[x,y] = color
        except:
            continue

# Optimized version of Line
def line(v1, v2, image, color=(255,255,255)):
    x0,y0 = v1[0], v1[1]
    x1,y1 = v2[0], v2[1]

    steep = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0,y0 = y0,x0
        x1,y1 = y1,x1
        steep = True
    
    if x0 > x1:
        x0,x1 = x1,x0
        y0,y1 = y1,y0

    dx = x1-x0; 
    dy = y1-y0; 
    derror2 = abs(dy)*2; 
    error2 = 0; 
    y = y0; 
    for x in range(x0, x1+1): 
        try:
            if (steep):
                image[y,x] = color
            else: 
                image[x,y] = color 
        except:
            continue
        error2 += derror2 
        if (error2 > dx):
            y += 1 if y1>y0 else -1 
            error2 -= dx*2; 



def triangle(pts, image, color):
    
    def barycentric(A, B, C, P):
        AC = C - A
        AB = B - A
        PA = A - P
        u = Vector3d([AC[0], AB[0], PA[0]]).cross(Vector3d([AC[1], AB[1], PA[1]]))

        if abs(u[2] < 1e-2):
            return Vector3d([-1,1,1])

        return [1. - (u[0]+u[1])/u[2], u[0]/u[2], u[1]/u[2]]

    pixels = image.load()
    bbox_min = [float('inf'), float('inf')]
    bbox_max = [-float('inf'), -float('inf')]
    clamp = [image.width -1, image.height-1]
    for i in range(3):
        for j in range(2):
            bbox_min[j] = max(0, min(pts[i][j], bbox_min[j]))
            bbox_max[j] = min(clamp[j], max(pts[i][j], bbox_max[j]))
    
    for x in range(bbox_min[0], bbox_max[0]+1):
        for y in range(bbox_min[1], bbox_max[1]+1):
            P = Vector3d([x,y,0])
            bary_coords = barycentric(pts[0], pts[1], pts[2], P)

            if bary_coords[0]<0 or bary_coords[1]<0 or bary_coords[2]<0 :
                continue

            pixels[x,y] = color


class Renderer:
    def __init__(self):
        self.light = Vector3d([0., 0., -1])
    
    def get_wireFrame(self, image, mesh):
        pixels = image.load()
        for idx in range(mesh.nfaces()):
            face = mesh.getFace(idx)

            for i in range(3):
                wc1 = mesh.getVert(face[i])
                wc2 = mesh.getVert(face[(i+1)%3])
                x0 = int((wc1[0] + 1)*image.width / 2)
                x1 = int((wc2[0] + 1)*image.width / 2)
                y0 = int((wc1[1] + 1)*image.height / 2)
                y1 = int((wc2[1] + 1)*image.height / 2)
                
                if (x0 == x1): 
                    continue

                line(Vector2d([x0, y0]), Vector2d([x1,y1]), pixels, WHITE)

    
    def get_textureObj(self, mesh):
        pass
    
    def get_ShadedObj(self, image, mesh):
        for idx in range(mesh.nfaces()):
            face = mesh.getFace(idx)

            world_coords = []
            screen_coords = []

            for i in range(3):
                world_coords.append(mesh.getVert(face[i]))
                sc = Vector3d([ int((world_coords[i][0] + 1)*image.width /2), int((world_coords[i][1] + 1)*image.height /2), world_coords[i][2] ])
                screen_coords.append(sc)

            
            triangle(screen_coords, image, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

class Test:
    def __init__(self):
        pass
    
    def test_line(self, image):
        line(Vector2d([13, 20]), Vector2d([80, 40]), image, WHITE)
        line(Vector2d([20, 13]), Vector2d([40, 80]), image, RED)
        line(Vector2d([80, 40]), Vector2d([13, 20]), image, RED)
    
    def test_triangle(self, image):
        t1 = [Vector3d([10,70,0]), Vector3d([50,160,0]), Vector3d([70,80,0])]
        t2 = [Vector3d([180,50,0]), Vector3d([150,1,0]), Vector3d([70,180,0])]
        t3 = [Vector3d([180, 150,0]), Vector3d([120,160,0]), Vector3d([130,180,0])]

        triangle(t1, image, RED)
        triangle(t2, image, WHITE)
        triangle(t3, image, GREEN)


if __name__ == '__main__':
    test = Test()
    image = Image.new('RGB', (100, 100), "black")
    test.test_line(image.load())
    image.save("out.bmp")

    image = Image.new('RGB', (200, 200), "black")
    test.test_triangle(image)
    image.save("out.bmp")