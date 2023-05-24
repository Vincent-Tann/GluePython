from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import cv2
import numpy as np
import camera
import serial_with_arduino
import planner
import arm_control
def main():
    #初始化相机
    my_camera=camera.Camera()
    if my_camera.kinect:
        print("Initialize Kinect succeeded!")
    else:
        print("Initialize Kinect failed!")
        return
    
    # 初始化机械臂
    arm=arm_control.RobotArm()

    # 初始化串口（与Arduino通讯）
    arduino=serial_with_arduino.Arduino()

    while True:
        # 利用接近传感器检测物体是否进入相机范围
        object_detected=arduino.detect_object_for_camera()
        if not object_detected:
            continue
        else: # 检测到物体，每个物体只进入一次该分支
            # 利用机器视觉算法求解世界坐标系下：3D涂胶轮廓（含法向量）、零件三维模型和传送带速度
            contour3d,model3d,v_belt=my_camera.get_glue_contour() #coutour3d.shape==(3,x),每个点包含xyz和nxnynz
            if (contour3d==None).any():
                continue
            # 在涂胶轮廓上采样,得到静态涂胶点
            point_num=10
            points_s=planner.sample_on_contour(contour3d,point_num)
            # 求解动态涂胶点
            t0=1
            dt=0.2
            points_d=planner.dynamicalize(points_s,v_belt,t0,dt)
            #涂胶
            arm.glue(points_d,t0,dt)

            print("finish glueing object!")

if __name__ == '__main__':
    print('oh yeah')
    main()








