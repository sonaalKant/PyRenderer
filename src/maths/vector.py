
class Vector:
    def __init__(self, v):
        self.__v = v
        self.dim = len(self.__v)
    
    def __add__(self, other):
        assert len(self) == len(other), "Vectors should be of equal length"
        return Vector([i+j for i,j in zip(self, other)])
    
    def dot(self, other):
        assert len(self) == len(other), "Vectors should be of equal length"
        return sum([i*j for i,j in zip(self, other)])
    
    def __mul__(self, other):
        assert len(self) == len(other), "Vectors should be of equal length"
        return Vector([i*j for i,j in zip(self, other)])
    
    def cross(self, other):
        pass
    
    def __str__(self):
        return f"Vector : {self.__v}"
    
    def __getitem__(self, idx):
        return self.__v[idx]
    
    def __setitem__(self, idx, val):
        self.__v[idx] = val
    
    def __len__(self):
        return self.dim
    
class Vector3d(Vector):
    def __init__(self, v=None):
        if v is None:
            v = [0,0,0]
        super().__init__(v)
    
    def cross(self):
        pass
    
class Vector2d(Vector):
    def __init__(self, v):
        if v is None:
            v = [0,0]
        super().__init__(v)
    
    def cross(self):
        pass

if __name__ == '__main__':
    v = Vector3d([0,0,0])
