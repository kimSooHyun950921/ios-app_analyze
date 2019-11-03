from PIL import Image, ImageChops
from skimage import io
from skimage.measure import compare_ssim as ssim

import csv
import os
import subprocess
from math import sqrt
import scipy.integrate as integrate
import sys
import logging
import logging.config
import xml.etree.ElementTree as ET
from operator import itemgetter

MP4DIR = '/home/kimsoohyun/00-Research/02-Graph/ios/ios-app_analyze/mp4/'
CUTFILE = '/home/kimsoohyun/00-Research/02-Graph/ios/ios-app_analyze/00-UIAutomator/csv_file/'
TEMPDIR = './a5-lte-init/'
OUTPUTDIR = './output/'
OUTPUTFILE = '190929-a5-ios-init-si.csv'
FPS = 10

def get_event_time(get_event_list):
    for index in range(to_index, from_index -1):
      if index - 1 == from_index:
        list_split_point.append((from_index, index))
        break
      try:
        image1 = io.imread(files_list[index])
        image2 = io.imread(files_list[index-1])
      except IndexError as e:
        print(e)
      similarity = ssim(image1, image2, multichannel=True)
      if similarity < 0.9:
        list_split_point.append((from_index, index))
        break
      return list_split_point

def sync(real_touch, record_time):
    '''sync: real touc와 record_time 의 sync를 맞추는 것
       input: real_touch list, record_time list
       output: record_time list


    '''
    

def get_split_point(files_list, cut_point):
    list_split_point = list()
    for index in range(0, len(cut_point)):
        from_index = 0
        if index > 0:
            from_index = cut_point[index-1]*FPS ## 10
        to_index = cut_point[index]*FPS ## 10
        print("index", from_index, to_index)
        for index in range(to_index, from_index, -1):
            if index-1 == from_index:
                list_split_point.append((from_index, index))
                break
            try:
              image1 = io.imread(files_list[index])
              image2 = io.imread(files_list[index-1])
            except IndexError as e:
              print(e)
            similarity = ssim(image1, image2, multichannel=True)
            if similarity < 0.9:
                
                list_split_point.append((from_index, index))
                break
    return list_split_point


def get_speed_index(files_list, list_split_point):
    speed_index = list()
    for from_index, to_index in list_split_point:
        speed = 0
        sim_list = list()
        for snaps in files_list[from_index:to_index]:
            try:
              image1 = io.imread(snaps)
              image2 = io.imread(files_list[to_index])
            except IndexError as e:
              print(e)
            similarity = (1-ssim(image1, image2, multichannel=True))*(1000/FPS)
            sim_list.append(similarity)
            speed = speed + similarity
        speed_index.append((speed, sim_list))
        print(speed, sim_list)
    return speed_index


def run_ffmpeg(video_name, mp4_dir):
    try:
        os.makedirs(TEMPDIR + str(video_name), exist_ok = True)
    except FileExistsError as e:
        print(e)
    except Exception as e:
        print(e)
        raise e

    # ffmpeg 실행
    # LuHa: fps=2 로 변경
    # command = 'ffmpeg -i ' + MP4DIR + str(video_name) + '.mp4 -vf fps=10 ' + TEMPDIR + str(video_name) + '/out%04d.jpg'
    command = 'ffmpeg -i ' + mp4_dir + str(video_name) + '.mp4 -vf fps={0} '.format(FPS) + TEMPDIR + str(video_name) + '/out%04d.jpg'
    try:
        ffmpeg = subprocess.check_call(command, stdout=subprocess.PIPE, shell=True)
    except Exception as e:
        print(e)
        raise e

    return True


def list_mp4(path):
    result = []
???LINES MISSING
from PIL import Image, ImageChops
from skimage import io
from skimage.measure import compare_ssim as ssim

import csv
import os
import subprocess
from math import sqrt
import scipy.integrate as integrate
import sys
import logging
import logging.config
import xml.etree.ElementTree as ET
from operator import itemgetter

MP4DIR = '/home/kimsoohyun/00-Research/02-Graph/ios/ios-app_analyze/mp4/'
CUTFILE = '/home/kimsoohyun/00-Research/02-Graph/ios/ios-app_analyze/00-UIAutomator/csv_file/'
TEMPDIR = './a5-lte-init/'
OUTPUTDIR = './output/'
OUTPUTFILE = '190929-a5-ios-init-si.csv'
FPS = 10

def get_event_time(get_event_list):
    for index in range(to_index, from_index -1):
      if index - 1 == from_index:
        list_split_point.append((from_index, index))
        break
      try:
        image1 = io.imread(files_list[index])
        image2 = io.imread(files_list[index-1])
      except IndexError as e:
        print(e)
      similarity = ssim(image1, image2, multichannel=True)
      if similarity < 0.9:
        list_split_point.append((from_index, index))
        break
      return list_split_point

def sync(real_touch, record_time):
    '''sync: real touc와 record_time 의 sync를 맞추는 것
       input: real_touch list, record_time list
       output: record_time list


    '''
    

def get_split_point(files_list, cut_point):
    list_split_point = list()
    for index in range(0, len(cut_point)):
        from_index = 0
        if index > 0:
            from_index = cut_point[index-1]*FPS ## 10
        to_index = cut_point[index]*FPS ## 10
        print("index", from_index, to_index)
        for index in range(to_index, from_index, -1):
            if index-1 == from_index:
                list_split_point.append((from_index, index))
                break
            try:
              image1 = io.imread(files_list[index])
              image2 = io.imread(files_list[index-1])
            except IndexError as e:
              print(e)
            similarity = ssim(image1, image2, multichannel=True)
            if similarity < 0.9:
                
                list_split_point.append((from_index, index))
                break
    return list_split_point


def get_speed_index(files_list, list_split_point):
    speed_index = list()
    for from_index, to_index in list_split_point:
        speed = 0
        sim_list = list()
        for snaps in files_list[from_index:to_index]:
            try:
              image1 = io.imread(snaps)
              image2 = io.imread(files_list[to_index])
            except IndexError as e:
              print(e)
            similarity = (1-ssim(image1, image2, multichannel=True))*(1000/FPS)
            sim_list.append(similarity)
            speed = speed + similarity
        speed_index.append((speed, sim_list))
        print(speed, sim_list)
    return speed_index


def run_ffmpeg(video_name, mp4_dir):
    try:
        os.makedirs(TEMPDIR + str(video_name), exist_ok = True)
    except FileExistsError as e:
        print(e)
    except Exception as e:
        print(e)
        raise e

    # ffmpeg 실행
    # LuHa: fps=2 로 변경
    # command = 'ffmpeg -i ' + MP4DIR + str(video_name) + '.mp4 -vf fps=10 ' + TEMPDIR + str(video_name) + '/out%04d.jpg'
    command = 'ffmpeg -i ' + mp4_dir + str(video_name) + '.mp4 -vf fps={0} '.format(FPS) + TEMPDIR + str(video_name) + '/out%04d.jpg'
    try:
        ffmpeg = subprocess.check_call(command, stdout=subprocess.PIPE, shell=True)
    except Exception as e:
        print(e)
        raise e

