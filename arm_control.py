import numpy as np
import threading
import socket
import time

class RobotArm:
    def __init__(self) -> None:
        self.address=('192.168.43.234',8000) #机械臂上树莓派的地址
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        #初始位置
        self.init_position=np.array([200,10,250,np.pi-0.01,0,0])
        #等待连接
        time.sleep(1)
        #移动到初始位置
        self.move(self.init_position[0],self.init_position[1],self.init_position[2],self.init_position[3],self.init_position[4],self.init_position[5],30)

    def move(self, x, y, z, rx, ry, rz, v):
        #注：向机械臂发送的单位要求为：xyz为mm，关节角度为°，速度mm/min且为0-2000之间的整数。
        rx*=(180 / np.pi) 
        ry*=(180 / np.pi)
        rz*=(180 / np.pi)
        v=int(v*60)
        mes="set_coords(" + str(x) + "," + str(y) + "," + str(z) + "," + str(rx) + "," + str(ry) + ", " + str(rz) + ", " + str(v) + ")"
        r=self.sock.sendto(mes.encode('utf-8'), self.address)
        if r>=0:
            print("发送move指令到树莓派成功: "+str(mes))
        else:
            print("发送move指令失败！")

    def glue(self,points,t0,dt,pose_given=0):
        if not pose_given:
            current_points=np.hstack([self.init_position[0:3].reshape(3,1), points]) #起始点+所有涂胶点
            next_points=np.hstack([points, self.init_position[0:3].reshape(3,1)]) #所有涂胶点+起始点
            dists=np.linalg.norm(next_points-current_points, axis=0) #相邻点距离
            #计算每一段的速度
            speeds=np.zeros(dists.shape[0])
            speeds[1:-1]=dists[1:-1]/dt
            speeds[0]=dists[0]/t0
            speeds[-1]=dists[-1]/t0
            #逐个点涂胶
            for i in range(speeds.shape[0]):
                #发出移动指令
                self.move(next_points[0],next_points[1],next_points[2],np.pi-0.01,0,0,speeds[i])
                #等待移动
                time.sleep(t0+0.02) if i==0 else time.sleep(dt)
        else:
            current_points=np.hstack([self.init_position[0:3].reshape(3,1), points[0:3,:]]) #起始点+所有涂胶点
            next_points=np.hstack([points[0:3,:], self.init_position[0:3].reshape(3,1)]) #所有涂胶点+起始点
            dists=np.linalg.norm(next_points-current_points, axis=0) #相邻点距离
            #计算每一段的速度
            speeds=np.zeros(dists.shape[0])
            speeds[1:-1]=dists[1:-1]/dt
            speeds[0]=dists[0]/t0
            speeds[-1]=dists[-1]/t0
            #逐个点涂胶
            for i in range(speeds.shape[0]):
                #发出移动指令
                self.move(next_points[0],next_points[1],next_points[2],next_points[3],next_points[4],next_points[5],speeds[i])
                #等待移动
                time.sleep(t0+0.02) if i==0 else time.sleep(dt)
        print("涂胶完成！")
