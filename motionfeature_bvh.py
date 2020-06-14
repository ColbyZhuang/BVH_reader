# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:44:32 2020

@author: zhuang
"""
from bvh import BvhHead, BvhMotion, BonePose
import numpy as np
import h5py

class BvhMotionFeature(object):
    def __init__(self, bvh_file_name, template_file):
        bvhhead = BvhHead()
        bvhhead.load(template_file)
        self.root = bvhhead.root
        self.bone_list = bvhhead.bone_list
        self.frame_time = bvhhead.frametime
        bvhmotion = BvhMotion()
        bvhmotion.load(bvh_file_name)
        self.poses = bvhmotion.poses
        print(len(self.bone_list), len(self.poses[0]))


    def one_frame_bone_position(self, frame):
        pose = self.poses[frame]
        
        bones_position = []

        for bone in self.bone_list:
            b_flag = False
            for p in pose:
                if bone.name == p.bone_name:
                    bone.update_world_matrix(p.rx, p.ry, p.rz)
                    b_flag = True
                    break
            if b_flag == False:
                print("no bone", bone.name)
                bone.update_world_matrix(0, 0, 0)

            bone_position = bone.world_mat[:3, 3].tolist()
            bones_position.append([bone_position[0][0]+pose[0].tx, bone_position[1][0]+pose[0].ty, bone_position[2][0]+pose[0].tz])
        return bones_position

    def get_bone_name_eulerorder_local_global(self, frame):
        pose = self.poses[frame]

        bone_inf = [i]

        for bone in self.bone_list:
            b_flag = False
            for p in pose:
                if bone.name == p.bone_name:
                    bone_inf_cur = []
                    bone_inf_cur.append(p.bone_name)
                    bone_inf_cur.append([p.rx, p.ry, p.rz, "xyz"])
                    local_mat, global_mat = bone.update_world_matrix_for_debug(p.rx, p.ry, p.rz)
                    bone_inf_cur.append(local_mat)
                    bone_inf_cur.append(global_mat)
                    bone_inf.append(bone_inf_cur)
                    b_flag = True
                    break
            if b_flag == False:
                print("no bone", bone.name)
                bone.update_world_matrix(0, 0, 0)
        return bone_inf



    def get_bone_id(self, bone):
        return bone.bone_id
    
    def get_bvh_motion_pair(self, frame):
        pose = self.poses[frame]
        one_frame_bone_position = self.one_frame_bone_position(frame)
        one_frame_bone_pair = self.get_bone_pair(one_frame_bone_position)
        return one_frame_bone_position, one_frame_bone_pair


    def get_bone_pair(self, bones_position):
        bones_pair = []
        for bone in self.bone_list:
            if bone.children:
                for child in bone.children:
                    bones_pair.append([bones_position[self.get_bone_id(bone)], bones_position[self.get_bone_id(child)]])
        return bones_pair
    
    
    
    

if __name__ == '__main__':
    motion_feature = BvhMotionFeature("./test_data/test.bvh", "./test_data/test.bvh")

    f = open('./test_data/information_debug.txt', 'w')

    for i in range(len(motion_feature.poses)):
        print(i, len(motion_feature.poses))
        motion_debug_information = motion_feature.get_bone_name_eulerorder_local_global(i)
        f.write(str(motion_debug_information))
        f.write("\n")
        if i >= 500:
            break

    f.close()

    




