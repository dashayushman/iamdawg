import cv2

# path
path = './data/39317.jpg'

# Reading an image in grayscale mode
image = cv2.imread(path, 1)

# Window name in which image is displayed
window_name = 'image.jpg'

# Start coordinate, here (100, 50)
# represents the top left corner of rectangle
start_point = (100, 300)

# Ending coordinate, here (125, 80)
# represents the bottom right corner of rectangle
end_point = (125, 500)

# Black color in BGR
color = (0, 0, 0)

# Line thickness of -1 px
# Thickness of -1 will fill the entire shape
thickness = -1

# Using cv2.rectangle() method
# Draw a rectangle of black color of thickness -1 px
image = cv2.rectangle(image, start_point, end_point, color, thickness)
print(image.shape)
# Displaying the image
cv2.imwrite(window_name, image)
