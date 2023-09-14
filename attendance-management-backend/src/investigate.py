from PIL import Image, ImageOps, ImageChops

def rmsd(image1, image2):
    diff = ImageChops.difference(image1, image2)
    h = diff.histogram()
    rms = (sum(h) / (image1.size[0] * image1.size[1])) ** 0.5
    return rms
