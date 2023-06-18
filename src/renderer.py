from PIL import Image
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
        
class Renderer:
    def __init__(self):
        pass
    
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
    
    def get_ShadedObj(self, mesh):
        pass


class Test:
    def __init__(self):
        pass
    
    def test_line(self, image):
        line(Vector2d([13, 20]), Vector2d([80, 40]), image, WHITE)
        line(Vector2d([20, 13]), Vector2d([40, 80]), image, RED)
        line(Vector2d([80, 40]), Vector2d([13, 20]), image, RED)

if __name__ == '__main__':
    test = Test()
    image = Image.new('RGB', (100, 100), "black")
    test.test_line(image.load())
    image.save("out.bmp")