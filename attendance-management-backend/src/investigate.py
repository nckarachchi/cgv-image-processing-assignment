from PIL import Image, ImageOps, ImageChops

def rmsd(image1, image2):
    diff = ImageChops.difference(image1, image2)
    h = diff.histogram()
    rms = (sum(h) / (image1.size[0] * image1.size[1])) ** 0.5
    return rms
template_path = 'template_signature.png'
student_signature_path = 'student_signature.png'

template_image = Image.open(template_path).convert('L')
student_image = Image.open(student_signature_path).convert('L')
