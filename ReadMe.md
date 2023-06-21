# PyRenderer : Simple renderer in python for practice

You can find some obj files [here](https://github.com/ssloy/tinyrenderer/tree/f037c7a0517a632c7391b35131f9746a8f8bb235/obj)

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

    # You can get textured image if you have texture map
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



### References

1. Thanks to [@ssloy](https://github.com/ssloy/tinyrenderer/wiki) work. Explained clearly and really hands on.
2. https://learnopengl.com/ is also a great source of reading.
3. If you are video guy then this is for you https://www.youtube.com/playlist?list=PLAwxTw4SYaPlaHwnoGxJE7NFhEWRCIyet