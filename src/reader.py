from src.maths.vector import Vector3d, Vector2d
from PIL import Image

class MeshReader:
    def __init__(self, filename, tex_filname=None):
        self.__faces = []
        self.__verts = []
        
        self.__facesNormal = []
        self.__vertsNormal = []

        self.__facesTexture = []
        self.__vertsTexture = []

        self.open(filename)

        if tex_filname:
            self.diffusionMap = Image.open(tex_filname)
    
    def open(self, filename):
        objFile = open(filename, "r")

        for line in objFile:
            if len(line) == 1:
                continue
            split = line.split()
            if split[0] == "#":
                continue
            elif split[0] == "v":
                v = Vector3d(list(map(float, split[1:])))
                self.__verts.append(v)
            elif split[0] == "vt":
                v = Vector2d(list(map(float, split[1:3])))
                v[1] = 1 - v[1]
                self.__vertsTexture.append(v)
            elif split[0] == "vn":
                v = Vector3d(list(map(float, split[1:])))
                self.__vertsNormal.append(v)
            elif split[0] == "f":
                t = []
                tn = []
                tt = []
                for i in range(1,4):
                    l = list(map(int, split[i].split("/")))
                    t.append(l[0]-1)
                    tn.append(l[2]-1)
                    tt.append(l[1]-1)
                self.__faces.append(t)
                self.__facesTexture.append(tt)
                self.__facesNormal.append(tn)
        objFile.close()
    
    def getVert(self, idx):
        return self.__verts[idx]
    
    def getFace(self, idx):
        return self.__faces[idx]
    
    def nfaces(self):
        return len(self.__faces)
    
    def getVertTex(self, idx):
        return self.__vertsTexture[idx]
    
    def getFaceTexCoord(self, idx):
        return self.__facesTexture[idx]
    
    def getVertNormal(self, idx):
        return self.__vertsNormal[idx]
    
    def getFaceNormalCoord(self, idx):
        return self.__facesNormal[idx]
    
    def computeFaceNormal(self, idx):
        pass
    
    def computeAllVertNormal(self):
        pass


if __name__ == '__main__':
    mesh = MeshReader("/Users/sonaal/Downloads/EasyRenderer/tinyrenderer/obj/african_head.obj")