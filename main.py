from src.reader import MeshReader
from src.renderer import Renderer
from PIL import Image

if __name__ == '__main__':

    mesh = MeshReader("/Users/sonaal/Downloads/EasyRenderer/tinyrenderer/obj/african_head.obj")
    renderer = Renderer()

    image = Image.new("RGB", (800,800), "black")
    renderer.get_ShadedObj(image, mesh)
    image = image.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    image.save("ShadedObjV2.bmp")

    zbuf = renderer.get_zbuffer()
    zbuf = zbuf.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
    zbuf.save("zbuf.bmp")