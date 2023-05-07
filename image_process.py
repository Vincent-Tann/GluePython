import cv2
import numpy as np

def segment(img):
    # lower=np.array([0, 190, 190, 0])
    # upper=np.array([140, 255, 255, 255])
    width=img.shape[1]
    height=img.shape[0]
    lower=np.dot(np.ones([height,width,1]), np.array([[0, 190, 190]])).astype(np.uint8)
    upper=np.dot(np.ones([height,width,1]), np.array([[140, 255, 255]])).astype(np.uint8) #lower and upper bound for BGR yellow segmentation.
    print(img.shape)
    print(lower.shape)
    return cv2.inRange(img,lower,upper) #需要lower、upper和imgsize相同

def get_edge(img):
    img_f=cv2.medianBlur(img,11)
    edge_img=cv2.Canny(img_f,100.0,300.0)
    edge=cv2.findContours(edge_img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    return edge_img,edge[0][0].reshape(-1,2)



img=cv2.imread('./images/yp.bmp') #中文路径读不进来
# cv2.imshow('img',img)
# cv2.waitKey(0)
print(img.shape)
print(type(img))
print('ok')
img_s=segment(img)
print(img_s.dtype)
# img_s=cv2.medianBlur(img_s,11)
cv2.imshow('img_s',img_s)
cv2.waitKey(0)

edge_img,edge=get_edge(img_s)
print(type(edge))
print(edge.shape)
# print(edge)
cv2.imshow('edge_img',edge_img)
cv2.waitKey(0)

img_c=cv2.drawContours(img,(edge,),0,color=(0,0,255),thickness=2)
cv2.imshow('img_c',img_c)
cv2.waitKey(0)
