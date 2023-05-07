from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import cv2
import numpy as np
import image_process

class Camera():
    def __init__(self) -> None:
        self.kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Color)

    # 获取深度图, 默认尺寸 424x512
    def get_last_depth(self):
        frame = self.kinect.get_last_depth_frame()
        frame = frame.astype(np.uint8)
        dep_frame = np.reshape(frame, [424, 512])
        return cv2.cvtColor(dep_frame, cv2.COLOR_GRAY2RGB)

    #获取rgb图, 1080x1920x3
    def get_last_rbg(self)->np.ndarray:
        frame = self.kinect.get_last_color_frame()
        return np.reshape(frame, [1080, 1920, 4])[:, :, 0:3]

    def get_glue_contour(self):
        x1,x2,y1,y2=810,1160,440,580
        srcImg=self.get_last_rbg()
        roiImg=srcImg[y1:y2+1,x1:x2+1,:]
        roiImg_copy=np.array(roiImg)

        #分割rgb零件图得到二值图像（零件为白色）
        roiImg=image_process.segment(roiImg)

        #计算轮廓的二值图像（轮廓为白色）
        roiImg,edge=image_process.get_edge(roiImg) #edge.shape=(x,2)
        
        #在rgb图上画出找到的轮廓用以显示
        roiImg=cv2.drawContours(roiImg_copy, (edge,), 0, color=(0,0,255))
        cv2.imshow("glue contour",roiImg)