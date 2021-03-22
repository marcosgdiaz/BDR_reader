# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:04:41 2020

@author: MGD
"""
import numpy as np
import struct

class transitions:
    
    def __init__(self,title):
        self.title = title
        self.site = []
        self.hfre = []
        self.hfim = []
        self.lfre = []
        self.lfim = []
        self.tt = []
        self.center = []
        self.origin = []
        
    def add(self,site, hfre, hfim, lfre, lfim, tt, center, origin):
        self.site.append(site)
        self.hfre.append(hfre)
        self.hfim.append(hfim)
        self.lfre.append(lfre)
        self.lfim.append(lfim)
        self.tt.append(tt)
        self.center.append(center)
        self.origin.append(origin)
        
    def add_freq(self,freq):
        self.freq = np.ones(len(self.lfre)) * freq
        
    def list2array(self):
        self.site = np.asarray(self.site)
        self.hfre = np.asarray(self.hfre)
        self.hfim = np.asarray(self.hfim)
        self.lfre = np.asarray(self.lfre)
        self.lfim = np.asarray(self.lfim)
        self.tt = np.asarray(self.tt)
        self.center = np.asarray(self.center)
        self.lf_phase = np.arctan2(self.lfim,self.lfre)
        self.hf_phase = np.arctan2(self.hfim,self.hfre)
        self.hf_amp = np.sqrt(np.add(np.square(self.hfim), np.square(self.hfre)))
        self.lf_amp = np.sqrt(np.add(np.square(self.lfim), np.square(self.lfre)))
        self.opacity = np.divide(self.hf_amp,self.lf_amp)
         
 

def path_reader(i,TRANS):
    _SIGNATURE = b'\x89BDR\x0D\x0A\x1A\x0A'
    name = i.split("/")[-1][0:-4]
      
    TRANS.append(transitions(name))
    
    with open(i,"rb") as f:
        signature = f.read(8)
        if signature == _SIGNATURE:
            while 1:
                length = f.read(4)
                length = int.from_bytes(length,"little")
                ch_type = f.read(4)
                
                if ch_type == b'' or length == 0:
                    return TRANS
                    break
                elif ch_type == b'AHDR':
                    site = f.read(5)
                    f.read(length - 5 + 4)
                elif ch_type == b'tRAN':
                    if length % 400 != 0:
                        raise ValueError('Invalid chunk')
                    N_trans = length // 400
                    for i in range(N_trans):
                        f.read(16)
                        HFRE = f.read(8)
                        center = f.read(8)
                        f.read(16)
                        tt = f.read(8)
                        f.read(56)
                        HFIM = f.read(8)
                        f.read(88)
                        LFRE = f.read(8)
                        f.read(88)
                        LFIM = f.read(8)
                        f.read(84)
                        origin = f.read(4)
                        HFRE = struct.unpack('d',HFRE)[0]
                        HFIM = struct.unpack('d',HFIM)[0]
                        LFRE = struct.unpack('d',LFRE)[0]
                        LFIM = struct.unpack('d',LFIM)[0]
                        tt = struct.unpack('d',tt)[0]
                        center = struct.unpack('d',center)[0]
                        origin = struct.unpack('i',origin)[0]
                        TRANS[-1].add(site,HFRE,HFIM,LFRE,LFIM,tt, center, origin)
                    f.read(4)
                else:
                    f.read(length+4)
                
                
        else:
            print("No proper signature found")
        
def BDR_reader(paths):
    TRANS = []
    for i in paths:
        try:
            TRANS = path_reader(i,TRANS)   
        except AttributeError:
            print(f'Skipped empty file: {i.title}')
            continue
            
    return TRANS
