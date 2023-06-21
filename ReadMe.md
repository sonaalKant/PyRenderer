# PyRenderer : Simple renderer in python for practice

Usage : 
```py
from src.reader import MeshReader # Reader for .obj files
from src.renderer import Renderer # basic renderer
from PIL import Image

WIDTH  = 800
HEIGHT = 800
DEPTH  = 255

if __name__ == '__main__':

    mesh = MeshReader("african_head.obj", tex_filname="african_head_diffuse.tga")
    
    renderer = Renderer(width=WIDTH, height=HEIGHT, depth=DEPTH)

    image = Image.new("RGB", (WIDTH, HEIGHT), "black")

    # You can get textured image if you have texture map
    renderer.get_textureObj(image, mesh)
    image = image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    image.save("TexImage.bmp")


    # Compatible shaders as of now : [Flat shader and Gourard shader]
    image = Image.new("RGB", (WIDTH, HEIGHT), "black")

    renderer.get_GouraudShaderObj(image, mesh)
    image = image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    image.save("GourardShader.bmp")


    # You can also play with camera, light
    renderer.update_camera_params([1,1,0])
    renderer.update_light([1,-1,1])
```


### Sample Demo
![](https://github.com/sonaalKant/PyRenderer/blob/main/camera.gif)
![](https://github.com/sonaalKant/PyRenderer/blob/main/light.gif)

### TODO

- [ ] Add Phong Shader 
- [ ] Add Shadow  



