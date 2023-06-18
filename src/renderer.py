from PIL import Image
from maths.vector import Vector3d, Vector2d

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

    for x in range(x0, x1+1):
        t = (x-x0) / float(x1 - x0)
        y = int(y0*t + y1*(1-t))

        if steep:
            image[y,x] = color
        else:
            image[x,y] = color
     

class Renderer:
    def __init__(self):
        pass
    
    def get_wireFrame(self, mesh):
        pass
    
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
        return image

if __name__ == '__main__':
    test = Test()
    image = Image.new('RGB', (100, 100), "black")
    test.test_line(image.load())
    image.save("out.bmp")