from PIL import Image
import random
import numpy as np
from src.maths.vector import Vector3d, Vector2d

WHITE = (255,255,255)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def Homo(np_vector):
    ones = np.ones((len(np_vector)+1,1))
    ones[:len(np_vector)] = np_vector
    return ones

def NonHomo(np_vector):
    np_vector = np_vector / np_vector[-1]
    return np_vector[:len(np_vector)-1]

def Mat2vec(m):
    v = NonHomo(m)[:,0].tolist()
    return Vector3d(v)
    


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

def triangle(pts, image, z_buffer, color):
    
    def barycentric(A, B, C, P):
        AC = C - A
        AB = B - A
        PA = A - P
        u = Vector3d([AC[1], AB[1], PA[1]]).cross(Vector3d([AC[0], AB[0], PA[0]]))

        if abs(u[2] < 1):
            return Vector3d([-1,1,1])

        return [1.0 - (u[0]+u[1])/u[2], u[1]/u[2], u[0]/u[2]]

    pixels = image.load()
    bbox_min = [float('inf'), float('inf')]
    bbox_max = [-float('inf'), -float('inf')]
    clamp = [image.width -1, image.height-1]
    for i in range(3):
        for j in range(2):
            bbox_min[j] = max(0, min(pts[i][j], bbox_min[j]))
            bbox_max[j] = min(clamp[j], max(pts[i][j], bbox_max[j]))
    
    # print(bbox_min, bbox_max)
    for x in range(bbox_min[0], bbox_max[0]+1):
        for y in range(bbox_min[1], bbox_max[1]+1):
            P = Vector3d([x,y,0])
            bary_coords = barycentric(pts[0], pts[1], pts[2], P)

            if bary_coords[0]<0 or bary_coords[1]<0 or bary_coords[2]<0 :
                continue
            
            P[2] = 0
            for i in range(3):
                P[2] += pts[i][2]*bary_coords[i]
            
            if z_buffer[x][y] < P[2]:
                z_buffer[x][y] = P[2]
                pixels[x,y] = color

def triangle(pts, image, z_buffer, uvs=None, diffusionMap=None, intensity=None):
    
    def barycentric(A, B, C, P):
        AC = C - A
        AB = B - A
        PA = A - P
        u = Vector3d([AC[1], AB[1], PA[1]]).cross(Vector3d([AC[0], AB[0], PA[0]]))

        if abs(u[2] < 1):
            return Vector3d([-1,1,1])

        return [1.0 - (u[0]+u[1])/u[2], u[1]/u[2], u[0]/u[2]]

    pixels = image.load()
    bbox_min = [float('inf'), float('inf')]
    bbox_max = [-float('inf'), -float('inf')]
    clamp = [image.width -1, image.height-1]
    for i in range(3):
        for j in range(2):
            bbox_min[j] = max(0, min(pts[i][j], bbox_min[j]))
            bbox_max[j] = min(clamp[j], max(pts[i][j], bbox_max[j]))
    
    # print(bbox_min, bbox_max)
    for x in range(bbox_min[0], bbox_max[0]+1):
        for y in range(bbox_min[1], bbox_max[1]+1):
            P = Vector3d([x,y,0])
            bary_coords = barycentric(pts[0], pts[1], pts[2], P)

            if bary_coords[0]<0 or bary_coords[1]<0 or bary_coords[2]<0 :
                continue
            
            P[2] = 0
            new_uv = [0, 0]
            pIntensity = 0
            for i in range(3):
                P[2] += pts[i][2]*bary_coords[i]
                if uvs is not None:
                    new_uv[0] += uvs[i][0]*bary_coords[i]
                    new_uv[1] += uvs[i][1]*bary_coords[i]
                pIntensity += intensity[i]*bary_coords[i]
            
            if diffusionMap is not None:
                new_uv[0] = new_uv[0] * diffusionMap.width
                new_uv[1] = new_uv[1] * diffusionMap.height
                color = diffusionMap.getpixel((new_uv[0], new_uv[1]))
            else:
                color = (255,255,255)
            
            if z_buffer[x][y] < P[2]:
                z_buffer[x][y] = P[2]
                pixels[x,y] = (int(color[0]*pIntensity), int(color[1]*pIntensity), int(color[2]*pIntensity))

class Renderer:
    def __init__(self, width, height, depth):
        self.light = Vector3d([-4, 0., 1])
        self.light.normalize()

        self.width = width
        self.height = height
        self.depth = depth

        self.eye = Vector3d([0, 0, 3])
        self.center = Vector3d([0., 0., 0.])
        self.up = Vector3d([0, 1, 0])

        self.Projection = np.eye(4)
        self.Projection[3][2] = -1 / (self.eye - self.center).norm()
        # Not sure why this configuration works??
        self.build_viewport(self.width/8, self.height/8, self.width*3/4, self.height*3/4) 
    
    def build_viewport(self, x, y, w, h):
        self.Viewport = np.eye(4)
        self.Viewport[0][0] = w/2.
        self.Viewport[1][1] = h/2.
        self.Viewport[2][2] = self.depth/2.

        self.Viewport[0][3] = x + w/2.
        self.Viewport[1][3] = y + h/2.
        self.Viewport[2][3] = self.depth/2.
    
    def get_ModelViewMatrix(self):
        z = (self.eye - self.center).normalize()
        x = self.up.cross(z).normalize()
        y = z.cross(x).normalize()
        M = np.eye(4)
        
        M[0][:3] = x.tonumpy()[:,0]
        M[1][:3] = y.tonumpy()[:,0]
        M[2][:3] = z.tonumpy()[:,0]
        M.T[3][:3] = -self.center.tonumpy()[:,0] 

        return M

    
    def update_camera_params(self, eye, center=None, up=None):
        
        self.eye = Vector3d(eye)
        self.center = Vector3d([0,0,0]) if center is None else Vector3d(center)
        self.up = Vector3d([0,1,0]) if up is None else Vector3d(up)

        self.Projection = np.eye(4)
        self.Projection[3][2] = -1 / (self.eye - self.center).norm()
    
    def update_light(self, light):
        self.light = Vector3d(light)
        self.light.normalize()

    def get_eye(self):
        return self.eye._v

    def get_light(self):
        return self.light._v

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

    
    def get_textureObj(self, image, mesh):
        self.z_buffer = [[-float('inf')]*image.width for i in range(image.height)]
        diffusionMap = mesh.diffusionMap
        
        ModelView = self.get_ModelViewMatrix()

        for idx in range(mesh.nfaces()):
            face = mesh.getFace(idx)
            faceTex = mesh.getFaceTexCoord(idx)
            faceNormal = mesh.getFaceNormalCoord(idx)

            world_coords = []
            screen_coords = []
            uvs = []
            intensity = []

            for i in range(3):
                world_coords.append(mesh.getVert(face[i]))
                # sc = Vector3d([ int((world_coords[i][0] + 1)*image.width /2), int((world_coords[i][1] + 1)*image.height /2), world_coords[i][2] ])
                
                vec = Homo(world_coords[i].tonumpy())
                sc = Mat2vec(self.Viewport @ self.Projection @ ModelView @ vec )
                screen_coords.append(sc.toint())

                uvs.append(mesh.getVertTex(faceTex[i]))

                normal = mesh.getVertNormal(faceNormal[i])
                normal.normalize()
                intensity.append(normal.dot(self.light))

            triangle(screen_coords, image, self.z_buffer, uvs, diffusionMap, intensity)
    
    def get_intensity(self, world_coords):
        normal = (world_coords[2] - world_coords[0]).cross((world_coords[1]-world_coords[0]))
        normal.normalize()
        return normal.dot(self.light)

    # Flat Shader
    def get_ShadedObj(self, image, mesh):
        self.z_buffer = [[-float('inf')]*image.width for i in range(image.height)]
        for idx in range(mesh.nfaces()):
            face = mesh.getFace(idx)

            world_coords = []
            screen_coords = []

            for i in range(3):
                world_coords.append(mesh.getVert(face[i]))
                sc = Vector3d([ int((world_coords[i][0] + 1)*image.width /2), int((world_coords[i][1] + 1)*image.height /2), world_coords[i][2] ])
                screen_coords.append(sc)

            intensity = self.get_intensity(world_coords)
            # triangle(screen_coords, image, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            if intensity > 0:
                triangle(screen_coords, image, self.z_buffer, (int(intensity*255), int(intensity*255), int(intensity*255)))
    
    def get_GouraudShaderObj(self, image, mesh):
        self.z_buffer = [[-float('inf')]*image.width for i in range(image.height)]
        
        ModelView = self.get_ModelViewMatrix()

        for idx in range(mesh.nfaces()):
            face = mesh.getFace(idx)
            faceNormal = mesh.getFaceNormalCoord(idx)

            world_coords = []
            screen_coords = []
            intensity = []

            for i in range(3):
                world_coords.append(mesh.getVert(face[i]))
                # sc = Vector3d([ int((world_coords[i][0] + 1)*image.width /2), int((world_coords[i][1] + 1)*image.height /2), world_coords[i][2] ])
                
                vec = Homo(world_coords[i].tonumpy())
                sc = Mat2vec(self.Viewport @ self.Projection @ ModelView @ vec )
                screen_coords.append(sc.toint())
                

                normal = mesh.getVertNormal(faceNormal[i])
                normal.normalize()
                intensity.append(normal.dot(self.light))

            triangle(screen_coords, image, self.z_buffer, None, None, intensity)
    
    def get_zbuffer(self):
        
        width,height = len(self.z_buffer[0]), len(self.z_buffer)
        image = Image.new('L', (width, height), 'black')
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                # import pdb;pdb.set_trace()
                if self.z_buffer[x][y] == -float('inf'):
                    continue
                pixels[x,y] = int(abs(self.z_buffer[x][y]*255))
        return image
    

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