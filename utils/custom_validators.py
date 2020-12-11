from PIL import Image

def is_valid_image(image):
	try:
		Image.open(image)
		return True
	except IOError:
		return False