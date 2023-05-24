import cv2
import numpy as np

# 用于分割RGB图片得到二值图片，选出特定的颜色
def segment(img):
    # lower=np.array([0, 190, 190, 0])
    # upper=np.array([140, 255, 255, 255])
    width=img.shape[1]
    height=img.shape[0]
    lower=np.dot(np.ones([height,width,1]), np.array([[0, 190, 190]])).astype(np.uint8)
    upper=np.dot(np.ones([height,width,1]), np.array([[140, 255, 255]])).astype(np.uint8) #lower and upper bound for BGR yellow segmentation.
    # print(img.shape)
    # print(lower.shape)
    return cv2.inRange(img,lower,upper) #需要lower、upper和imgsize相同

# 用于在二值图片上找到涂胶轮廓
def get_edge(img,margin=15):
    #中值滤波
    img_f=cv2.medianBlur(img,11)
    #腐蚀缩小,margin决定腐蚀的程度大小
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,ksize=(margin,margin))
    img_e=cv2.erode(img_f,kernel)
    #提取边缘
    edge_img=cv2.Canny(img_e,100.0,300.0)
    edge=cv2.findContours(edge_img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    print("edge: ",edge)
    if edge[0]==():
        edge_return=np.array([None])
    else:
        edge_return=edge[0][0].reshape(-1,2)
    return edge_img,edge_return



# img=cv2.imread('./images/yp.bmp') #中文路径读不进来
# # cv2.imshow('img',img)
# # cv2.waitKey(0)
# print(img.shape)
# print(type(img))
# print('ok')
# img_s=segment(img)
# print(img_s.dtype)
# # img_s=cv2.medianBlur(img_s,11)
# cv2.imshow('img_s',img_s)
# cv2.waitKey(0)

# edge_img,edge=get_edge(img_s)
# print(type(edge))
# print(edge.shape)
# print(edge)
# cv2.imshow('edge_img',edge_img)
# cv2.waitKey(0)

# img_c=cv2.drawContours(img,(edge,),0,color=(0,0,255),thickness=2)
# cv2.imshow('img_c',img_c)
# cv2.waitKey(0)
