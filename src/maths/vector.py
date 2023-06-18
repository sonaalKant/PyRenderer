
class Vector:
    def __init__(self, v):
        self._v = v
        self.dim = len(self._v)
    
    def __add__(self, other):
        assert len(self) == len(other), "Vectors should be of equal length"
        return type(self)([i+j for i,j in zip(self, other)])
    
    def __sub__(self, other):
        assert len(self) == len(other), "Vectors should be of equal length"
        return type(self)([i-j for i,j in zip(self, other)])
    
    def dot(self, other):
        assert len(self) == len(other), "Vectors should be of equal length"
        return sum([i*j for i,j in zip(self, other)])
    
    def __mul__(self, val):
        assert len(self) == len(other), "Vectors should be of equal length"
        return type(self)([i*val for i in self])
    
    def cross(self, other):
        pass
    
    def normalize(self):
        norm = (sum([i**2 for i in self]))**0.5
        self._v = [i/norm for i in self]
    
    def __str__(self):
        return f"Vector : {self._v}"
    
    def __getitem__(self, idx):
        return self._v[idx]
    
    def __setitem__(self, idx, val):
        self._v[idx] = val
    
    def __len__(self):
        return self.dim
    
class Vector3d(Vector):
    def __init__(self, v=[0,0,0]):
        super().__init__(v)
    
    def cross(self, v):
        return Vector3d([self._v[1]*v[2] - self._v[2]*v[1],
                        self._v[2]*v[0] - self._v[0]*v[2],
                        self._v[0]*v[1] - self._v[1]*v[0]])

    
class Vector2d(Vector):
    def __init__(self, v=[0,0]):
        super().__init__(v)
    
    def cross(self):
        pass

if __name__ == '__main__':
    v = Vector3d([0,0,0])
