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

template_image = template_image.resize(student_image.size)

threshold = 128
template_image = ImageOps.invert(template_image.point(lambda p: p < threshold and 255))
student_image = ImageOps.invert(student_image.point(lambda p: p < threshold and 255))

threshold = 50 
difference = rmsd(template_image, student_image)

if difference <= threshold:
    print(f"Student signature matched with RMSD difference: {difference:.2f}")
else:
    print(f"Student signature did not match with RMSD difference: {difference:.2f}")
