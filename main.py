from src.reader import MeshReader
from src.renderer import Renderer
from PIL import Image

if __name__ == '__main__':

    mesh = MeshReader("/Users/sonaal/Downloads/EasyRenderer/tinyrenderer/obj/african_head.obj", "/Users/sonaal/Downloads/EasyRenderer/tinyrenderer/obj/african_head_diffuse.tga")
    renderer = Renderer()

    image = Image.new("RGB", (800,800), "black")
    renderer.get_textureObj(image, mesh)
    image = image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    image.save("ShadedObjV2.bmp")

    # zbuf = renderer.get_zbuffer()
    # zbuf = zbuf.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    # zbuf.save("zbuf.bmp")