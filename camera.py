from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import cv2
import numpy as np
import image_process
import mapper

class Camera():
    def __init__(self) -> None:
        self.kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Color)

    # 获取深度图, 默认尺寸 424x512
    def get_last_depth(self):
        frame = self.kinect.get_last_depth_frame()
        frame = frame.astype(np.uint8)
        dep_frame = np.reshape(frame, [424, 512])
        return cv2.cvtColor(dep_frame, cv2.COLOR_GRAY2RGB)

    # 获取rgb图, 1080x1920x3
    def get_last_rbg(self)->np.ndarray:
        frame = self.kinect.get_last_color_frame()
        return np.reshape(frame, [1080, 1920, 4])[:, :, 0:3]

    # 获取涂胶轮廓的核心函数
    # @return contour3d.shape=(3,x), x为轮廓上的点数
    # @return model3d
    # @return v_belt
    def get_glue_contour(self):
        #获取图像
        srcImg=self.get_last_rbg()

        #获取rgb到depth的映射表
        depth_map=mapper.depth_2_color_space(self.kinect, PyKinectV2._DepthSpacePoint, self.kinect._depth_frame_data, return_aligned_image=True)

        #roi范围
        x1,x2,y1,y2=810,1160,440,580
        roiImg=srcImg[y1:y2+1,x1:x2+1,:]
        roiImg_copy=np.array(roiImg)

        #分割rgb零件图得到二值图像（零件为白色）
        roiImg=image_process.segment(roiImg)

        #计算轮廓的二值图像（轮廓为白色）和轮廓点像素坐标
        _,edge=image_process.get_edge(roiImg) #edge.shape=(x,2)

        #在rgb图上画出找到的轮廓用以显示
        roiImg=cv2.drawContours(roiImg_copy, (edge,), 0, color=(0,0,255))
        cv2.imshow("glue contour",roiImg)

        #转换为原图像的像素坐标
        edge[:,0]=edge[:,0]+x1
        edge[:,1]=edge[:,1]+y1

        #涂胶点的像素坐标u和v
        u=edge[:,0].reshape(-1)
        v=edge[:,1].reshape(-1)

        #获取轮廓的深度信息
        depths=depth_map[v,u]

        #相机参数
        fx = 1068.169623
        fy = 1068.258222
        u0 = 952.5807635 #1920
        v0 = 537.6288875 #1080

        #求解相机坐标系下的轮廓点坐标
        Zc=depths.reshape(-1) 
        Xc=(u-u0)*Zc/fx
        Yc=(v-v0)*Zc/fy
        contour_in_camera=np.vstack([Xc,Yc,Zc]) #shape=(3,x)

        #转换到世界坐标系
        T_c_w=np.array([[0,1,0,329.4],
                         [1,0,0,129.9],
                         [0,0,-1,835],
                         [0,0,0,1]])
        contour_in_world=np.dot(T_c_w,contour_in_camera)


        return contour_in_world,None,10