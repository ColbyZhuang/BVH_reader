# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:12:13 2020

@author: zhuang
"""

import numpy as np
from matrix import *

class Bone(object):
    def __init__(self):
        self.parent = None
        self.parent_name = None
        self.children = []
        self.children_name = []
        self.bone_id = 0
        self.name = ""
        self.trans = np.mat([0.0, 0.0, 0.0]).T

        
        self.t_mat = translation(self.trans[0, 0], self.trans[1, 0], self.trans[2, 0])
        
        self.local_mat = self.t_mat
        self.world_mat = self.local_mat
    
    def update_local_matrix(self):
        self.t_mat = translation(self.trans[0, 0], self.trans[1, 0], self.trans[2, 0])
        self.local_mat = self.t_mat

    def update_world_matrix(self, rx, ry, rz):
        self.update_local_matrix()
        
        arr_local_mat = self.local_mat.getA()
        for i in range(arr_local_mat.shape[0]):
            for j in range(arr_local_mat.shape[1]):
                if abs(arr_local_mat[i][j]) > 1e7 or abs(arr_local_mat[i][j]) < 1e-7:
                    arr_local_mat[i][j] = 0.
                    
        self.local_mat = np.mat(arr_local_mat)
        if self.parent:
            mat_rot = rotation_from_angle(rx, ry, rz)
            parent_world_mat = self.parent.world_mat
            self.world_mat = parent_world_mat * self.local_mat * mat_rot
        else:
            mat_rot = rotation_from_angle(rx, ry, rz)
            self.world_mat = self.local_mat * mat_rot

    def update_world_matrix_for_debug(self, rx, ry, rz):
        self.update_local_matrix()

        arr_local_mat = self.local_mat.getA()
        for i in range(arr_local_mat.shape[0]):
            for j in range(arr_local_mat.shape[1]):
                if abs(arr_local_mat[i][j]) > 1e7 or abs(arr_local_mat[i][j]) < 1e-7:
                    arr_local_mat[i][j] = 0.

        self.local_mat = np.mat(arr_local_mat)
        cur_local_mat = self.local_mat
        cur_global_mat = self.local_mat
        if self.parent:
            mat_rot = rotation_from_angle(rx, ry, rz)
            parent_world_mat = self.parent.world_mat
            self.world_mat = parent_world_mat * self.local_mat * mat_rot
            cur_local_mat = self.local_mat * mat_rot
            cur_global_mat = self.world_mat
        else:
            mat_rot = rotation_from_angle(rx, ry, rz)
            self.world_mat = self.local_mat * mat_rot
            cur_local_mat = self.local_mat * mat_rot
            cur_global_mat = self.world_mat
        return cur_local_mat.getA(), cur_global_mat.getA()
            
    def set_parent(self, bone):
        self.parent = bone

    def add_child(self, bone):
        self.children.append(bone)

    def set_bone_id(self, ind):
        self.bone_id = ind

    def get_bone_id(self):
        return self.bone_id

    def set_name(self, b_name):
        self.name = b_name

    def get_name(self):
        return self.name

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def set_parent_null(self):
        self.parent = None

    def get_translation(self):
        return self.trans

    def set_translation(self, new_trans):
        self.trans = new_trans

    def get_rotate(self):
        return self.rotate

    def set_rotate(self, new_rotate):
        self.rotate[0, 0] = new_rotate


    def set_source_rotate(self, s_ro):
        self.s_rotate = s_ro

    def get_source_rotate(self):
        return self.joint_rotate

    def get_world_matrix(self):
        return self.world_mat

    def get_local_matrix(self):
        return self.local_mat
        