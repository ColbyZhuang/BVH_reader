# -*- coding: utf-8 -*-
import numpy as np
import math
from scipy.spatial.transform import Rotation as R

def degree2radian(theta):
    return theta * np.pi / 180.0


def radian2degree(theta):
    return theta / np.pi * 180.0


def rotation_x(theta_x):
    theta_x = degree2radian(theta_x)
    rx = np.mat([[1.0, 0.0, 0.0, 0.0],
                 [0.0, np.cos(theta_x), -np.sin(theta_x), 0.0],
                 [0.0, np.sin(theta_x), np.cos(theta_x), 0.0],
                 [0.0, 0.0, 0.0, 1.0]])

    return rx

def rotation_x_radian(theta_x):
    rx = np.mat([[1.0, 0.0, 0.0, 0.0],
                 [0.0, np.cos(theta_x), -np.sin(theta_x), 0.0],
                 [0.0, np.sin(theta_x), np.cos(theta_x), 0.0],
                 [0.0, 0.0, 0.0, 1.0]])

    return rx

def rotation_y(theta_y):
    theta_y = degree2radian(theta_y)
    ry = np.mat([[np.cos(theta_y), 0.0, np.sin(theta_y), 0.0],
                 [0.0, 1.0, 0.0, 0.0],
                 [-np.sin(theta_y), 0.0, np.cos(theta_y), 0.0],
                 [0.0, 0.0, 0.0, 1.0]])

    return ry

def rotation_y_radian(theta_y):
    ry = np.mat([[np.cos(theta_y), 0.0, np.sin(theta_y), 0.0],
                 [0.0, 1.0, 0.0, 0.0],
                 [-np.sin(theta_y), 0.0, np.cos(theta_y), 0.0],
                 [0.0, 0.0, 0.0, 1.0]])

    return ry

def rotation_z(theta_z):
    theta_z = degree2radian(theta_z)
    rz = np.mat([[np.cos(theta_z), -np.sin(theta_z), 0.0, 0.0],
                 [np.sin(theta_z), np.cos(theta_z), 0.0, 0.0],
                 [0.0, 0.0, 1.0, 0.0],
                 [0.0, 0.0, 0.0, 1.0]])

    return rz

def rotation_z_radian(theta_z):
    rz = np.mat([[np.cos(theta_z), -np.sin(theta_z), 0.0, 0.0],
                 [np.sin(theta_z), np.cos(theta_z), 0.0, 0.0],
                 [0.0, 0.0, 1.0, 0.0],
                 [0.0, 0.0, 0.0, 1.0]])

    return rz

def rotation_from_mat(rx, ry, rz):
    return rz * ry * rx


    
def rotation_from_angle(theta_x, theta_y, theta_z):
    rx = rotation_x(theta_x)
    ry = rotation_y(theta_y)
    rz = rotation_z(theta_z)
    rot2 = rx * ry * rz
    #print(rot2)
    #rot2 = R.from_euler(r[:3, :3])
    # rot = R.from_euler('ZXY', [theta_z, theta_x, theta_y], degrees=True)
    # #print("rot:", rot.as_dcm())
    #
    # rot2 = np.mat([[1.0, 0.0, 0.0, 0.0],
    #              [0.0, 0, 0, 0.0],
    #              [0.0, 0, 0, 0.0],
    #              [0.0, 0.0, 0.0, 1.0]])
    #
    # #print(np.asarray(rot))
    # #import pdb
    # #pdb.set_trace()
    # rot2[:3, :3] = np.asmatrix(rot.as_dcm())


    return rot2

def mat2euler(r):
    rot2 = R.from_dcm(r[:3, :3])
    return rot2.as_euler("yxz", degrees=True)


def rotation_from_radian(theta_x, theta_y, theta_z):
    rx = rotation_x_radian(theta_x)
    ry = rotation_y_radian(theta_y)
    rz = rotation_z_radian(theta_z)

    return rz * rx * ry

def translation(tx, ty, tz):
    t = np.mat([[1.0, 0.0, 0.0, tx],
                [0.0, 1.0, 0.0, ty],
                [0.0, 0.0, 1.0, tz],
                [0.0, 0.0, 0.0, 1.0]])

    return t


# def rotation2angle(r):
#     """
#     :param r:  rotation matrix
#     :return: euler angle in radian
#     """
#
#     sy = np.sqrt(r[0, 0] ** 2 + r[1, 0] ** 2)
#     rotate_angle = np.array([0.0, 0.0, 0.0])
#     singular = sy < 1e-6
#     if not singular:
#         rotate_angle[0] = math.atan2(r[2, 1], r[2, 2]) / np.pi * 180.0
#         rotate_angle[1] = math.atan2(-r[2, 0], sy) / np.pi * 180.0
#         rotate_angle[2] = math.atan2(r[1, 0], r[0, 0]) / np.pi * 180.0
#     else:
#         rotate_angle[0] = math.atan2(-r[1, 2], r[1, 1]) / np.pi * 180.0
#         rotate_angle[1] = math.atan2(-r[2, 0], sy) / np.pi * 180.0
#         rotate_angle[2] = 0
#
#     return rotate_angle



def rotation2angle(r, last_euler):
    """
    :param r:  rotation matrix
    :return: euler angle in radian
    """

    sy = np.sqrt(r[0, 0] ** 2 + r[1, 0] ** 2)
    rotate_angle = np.array([0.0, 0.0, 0.0])
    singular = sy < 1e-6
    if not singular:
        rotate_angle[0] = math.atan2(r[2, 1], r[2, 2]) / np.pi * 180.0
        rotate_angle[1] = math.atan2(-r[2, 0], sy) / np.pi * 180.0
        rotate_angle[2] = math.atan2(r[1, 0], r[0, 0]) / np.pi * 180.0
    else:
        rotate_angle[0] = math.atan2(-r[1, 2], r[1, 1]) / np.pi * 180.0
        rotate_angle[1] = math.atan2(-r[2, 0], sy) / np.pi * 180.0
        rotate_angle[2] = 0

    if 0. in rotate_angle or -180. in rotate_angle or 180. in rotate_angle:
        delta_angle = rotate_angle - last_euler
        for i in range(3):
            if delta_angle[i] >=120. and delta_angle[i] < 230.:
                rotate_angle[i] -= 180.
            if delta_angle[i] <= -120. and delta_angle[i] > -230.:
                rotate_angle[i] += 180.
        if rotate_angle[2] != 90. and rotate_angle[2] != -90.:
            ry2 = r[0, 0] / math.cos(rotate_angle[2] / 180. * np.pi)
        else:
            ry2 = r[1, 0] / math.sin(rotate_angle[2] / 180. * np.pi)

        rotate_angle[1] = math.atan2(-r[2, 0], ry2) / np.pi * 180.0
    if int(rotate_angle[2] == 18):
        print(delta_angle)

    return rotate_angle


def rotation_root_2angle(r):
    """
    :param r:  rotation matrix
    :return: euler angle in radian
    """

    sy = np.sqrt(r[0, 0] ** 2 + r[1, 0] ** 2)
    rotate_angle = np.array([0.0, 0.0, 0.0])
    singular = sy < 1e-6
    if not singular:
        rotate_angle[0] = math.atan2(r[2, 1], r[2, 2]) / np.pi * 180.0
        rotate_angle[1] = math.atan2(-r[2, 0], sy) / np.pi * 180.0
        rotate_angle[2] = math.atan2(r[1, 0], r[0, 0]) / np.pi * 180.0
    else:
        rotate_angle[0] = math.atan2(-r[1, 2], r[1, 1]) / np.pi * 180.0
        rotate_angle[1] = math.atan2(-r[2, 0], sy) / np.pi * 180.0
        rotate_angle[2] = 0



    return rotate_angle
