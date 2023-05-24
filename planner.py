import numpy as np

def transform(points_camera):
    return 1

def sample_on_contour(contour,point_num):
    return contour

# 计算世界坐标系下的动态涂胶点坐标
# @param points_s: 静态涂胶点坐标，shape=(3,x) if norm_available else (6,x)
# @param v_belt: 传送带速度大小
# @param t_delay: 从静态涂胶点时间（拍照时间）到涂第一个涂胶点的时间差
# @param dt: 两个涂胶点间的时间差
def dynamicalize(points_s,v_belt,t_delay,dt):
    #把起始点加到最后，形成闭环
    points_s=np.hstack([ points_s, points_s[:,0].reshape(-1,1) ])
    point_num=points_s.shape[1]
    #计算所有点的平移量（y方向）
    delta_t=np.array(range(point_num))*dt+t_delay
    delta_y=delta_t*v_belt
    #计算动态涂胶点坐标
    points_s[1,:]=points_s[1,:]-delta_y
    return points_s