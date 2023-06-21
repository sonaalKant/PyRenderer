from src.reader import MeshReader
from src.renderer import Renderer
from PIL import Image

WIDTH  = 800
HEIGHT = 800
DEPTH  = 255

if __name__ == '__main__':

    mesh = MeshReader("african_head.obj", "african_head_diffuse.tga")
    renderer = Renderer(width=WIDTH, height=HEIGHT, depth=DEPTH)


    for i in range(1):
        print(i)
        light = renderer.get_light()

        tex_image = Image.new("RGB", (WIDTH, HEIGHT), "black")
        shaded_image = Image.new("RGB", (WIDTH, HEIGHT), "black")
        
        renderer.get_textureObj(tex_image, mesh)
        renderer.get_GouraudShaderObj(shaded_image, mesh)
        
        tex_image = tex_image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
        shaded_image = shaded_image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
        
        image = Image.new("RGB", (2*WIDTH, HEIGHT), "black")
        image.paste(shaded_image, (0,0))
        image.paste(tex_image, (WIDTH, 0))
        
        image.save(f"outputs2/{i}.bmp")

        new_light = [x+y for x,y in zip(light, [0.5, 0, 0])]
        renderer.update_light(new_light)