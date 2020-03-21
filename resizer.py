import cv2

path = './data/3888471.jpg'

# Reading an image in grayscale mode
image = cv2.imread(path, 1)

r = 1080.0 / image.shape[1]
dim = (1080, int(image.shape[0] * r))
# perform the actual resizing of the image and show it
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)


box_x =  int(resized.shape[0] * 0.90)
box_y = 0
print(resized.shape[0], box_x, box_y)


text = "I don't like morning people, or mornings, or people."
print("text_len", len(text))
# setup text
font = cv2.FONT_HERSHEY_SIMPLEX
# get boundary of this text
textsize = cv2.getTextSize(text, font, 1, 2)[0]
# get coords based on boundary
textX = (resized.shape[1] - textsize[0]) // 2
textY = (resized.shape[0] + textsize[1]) // 2 + (box_x // 2)

print(resized.shape[1], textsize[0])
print(resized.shape[0], textsize[1])
# add text centered on image

resized= cv2.rectangle(resized, (0, box_x), (1080, resized.shape[1]),(255,255,255),-1)
cv2.putText(resized, text, (textX, textY ), font, 1, (0, 0, 0), 2, lineType=cv2.LINE_AA)




cv2.imwrite("image.jpg", resized)