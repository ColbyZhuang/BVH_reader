# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:10:29 2020

@author: zhuang
"""

import re
import numpy as np
from bone import *

channelmap = {
    'Xrotation' : 'x',
    'Yrotation' : 'y',
    'Zrotation' : 'z'   
}

channelmap_inv = {
    'x': 'Xrotation',
    'y': 'Yrotation',
    'z': 'Zrotation',
}

ordermap = {
    'x' : 0,
    'y' : 1,
    'z' : 2,
}


class BonePose(object):
    def __init__(self):
        self.bone_name = ""
        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0
        self.rx = 0.0
        self.ry = 0.0
        self.rz = 0.0

    def set_name(self, name):
        self.bone_name = name
        
        
class BvhHead(object):
    def __init__(self):
        self.bone_num = 0
        self.root = Bone()
        self.bone_list = []
        self.bone_id_map = {}
        self.names = []
    
    def load(self, filename, order=None):
        """
        read a bvh file, head part
        """
        f = open(filename, "r")
        bone_ind = 0
        end_site = False
        parents = np.array([], dtype=int)
        active = -1
        for line in f: 
            if "HIERARCHY" in line: continue
            if "MOTION" in line: continue
            rmatch = re.match(r"ROOT (\w+:?\w+)", line)
            if rmatch:
                bone = Bone()
                bone.set_bone_id(bone_ind)
                bone.set_name(rmatch.group(1))
                self.bone_list.append(bone)
                self.root = bone
                self.bone_id_map[rmatch.group(1)] = bone_ind
                self.names.append(rmatch.group(1))
                bone_ind += 1
                parents = np.append(parents, active)
                active = (len(parents)-1)
                continue
            if "{" in line: continue
            if "}" in line:
                if end_site: end_site = False
                else: active = parents[active]
                continue
            
            offmatch = re.match(r"\s*OFFSET\s+([\-\d\.e]+)\s+([\-\d\.e]+)\s+([\-\d\.e]+)", line)
            if offmatch:
                if not end_site:
                    offsets = np.array([list(map(float, offmatch.groups()))])
                    if len(self.bone_list) > 1:
                        self.bone_list[active].set_translation(np.mat([[offsets[0][0], offsets[0][1], offsets[0][2]]]).T)

                continue
            
            chanmatch = re.match(r"\s*CHANNELS\s+(\d+)", line)
            if chanmatch:
                channels = int(chanmatch.group(1))
                if order is None:
                    channelis = 0 if channels == 3 else 3
                    channelie = 3 if channels == 3 else 6
                    parts = line.split()[2+channelis:2+channelie]
                    if any([p not in channelmap for p in parts]):
                        continue
                    order = "".join([channelmap[p] for p in parts])
                continue
               
            jmatch = re.match("\s*JOINT\s+(\w+:?\w+)", line)
            if jmatch:
                bone = Bone()
                bone.set_bone_id(bone_ind)
                bone.set_name(jmatch.group(1))
                
                bone.set_parent(self.bone_list[active])
                self.bone_list[active].add_child(bone)
                self.bone_list.append(bone)
                self.bone_id_map[jmatch.group(1)] = bone_ind
                self.names.append(jmatch.group(1))
                bone_ind += 1
                parents  = np.append(parents, active)
                active = (len(parents)-1)
                continue
            
            if "End Site" in line:
                end_site = True
                continue

            fmatch = re.match("\s*Frames:\s+(\d+)", line)
            if fmatch:
                self.pose_num = int(fmatch.group(1))
                continue
            
            fmatch = re.match("\s*Frame Time:\s+([\d\.]+)", line)
            if fmatch:
                self.frametime = float(fmatch.group(1))
                continue

        f.close()   
            

     
class BvhMotion(object):
    def __init__(self):
        self.pose_num = 0
        self.frametime = 0
        self.poses = []
        
    def load(self, filename, order=None):
        """
        read a bvh file, motion part
        """
        f = open(filename, "r")
        bvhhead = BvhHead()
        bvhhead.load(filename)
        joint_names = bvhhead.names

        p=0
        for line in f: 
            dmatch = line.strip().split(' ')
            if dmatch and len(dmatch)>30:
                p += 1
                data_block = np.array(list(map(float, dmatch)))
                pose = []
                for i, name in enumerate(joint_names):
                    if i == 0:
                        bone_pose = BonePose()
                        bone_pose.set_name(name)
                        bone_pose.tx = data_block[0]
                        bone_pose.ty = data_block[1]
                        bone_pose.tz = data_block[2]
                        bone_pose.rx = data_block[3]
                        bone_pose.ry = data_block[4]
                        bone_pose.rz = data_block[5]
                        pose.append(bone_pose)
                    else:
                        bone_pose = BonePose()
                        bone_pose.set_name(name)
                        bone_pose.rx = data_block[i*3+3]
                        bone_pose.ry = data_block[i*3+4]
                        bone_pose.rz = data_block[i*3+5]
                        pose.append(bone_pose)
                self.poses.append(pose)
        self.pose_num = len(self.poses)
        f.close()
        
        
    def write(self, filename, template_bvhhead_file, poses):
        """
        write a bvh file, motion part
        """
        pose_num = len(poses)
        head_file = open(template_bvhhead_file, "r")
        write_file = open(filename, "w")
        
        for line in head_file:
            write_file.write(line)
            
        write_file.write("MOTION\n")
        write_file.write("Frames: %i"%pose_num)
        write_file.write("\n")
        write_file.write("Frame Time: %f"%self.frametime)
        
        for pose in poses:
            line = ""
            for i, bone in enumerate(pose):
                if i == 0:
                    line += str(bone.tx)
                    line += " "
                    line += str(bone.ty)
                    line += " "
                    line += str(bone.tz)
                    line += " "
                    line += str(bone.rz)
                    line += " "
                    line += str(bone.rx)
                    line += " "
                    line += str(bone.ry)
                    line += " "
                else:
                    line += str(bone.rz)
                    line += " "
                    line += str(bone.rx)
                    line += " "
                    line += str(bone.ry)
                    line += " "
            write_file.write("\n")
            write_file.write(line)
        
        write_file.close()
           
                    
                

    



















