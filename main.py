from src.reader import MeshReader
from src.renderer import Renderer
from PIL import Image

WIDTH  = 800
HEIGHT = 800
DEPTH  = 255

if __name__ == '__main__':

    mesh = MeshReader("/Users/sonaal/Downloads/EasyRenderer/tinyrenderer/obj/african_head.obj", "/Users/sonaal/Downloads/EasyRenderer/tinyrenderer/obj/african_head_diffuse.tga")
    renderer = Renderer(width=WIDTH, height=HEIGHT, depth=DEPTH)

    image = Image.new("RGB", (WIDTH, HEIGHT), "black")
    renderer.get_textureObj(image, mesh)
    image = image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    image.save("ShadedObjV21.bmp")

    # zbuf = renderer.get_zbuffer()
    # zbuf = zbuf.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    # zbuf.save("zbuf.bmp")