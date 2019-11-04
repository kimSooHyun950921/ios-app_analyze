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
DEBUG = True
                                                                                
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
                                                                                
                                                                                
def sync(jpg_list, cut_list):                                                   
    sync_cut_point = list()                                                     
    for index in range(0, len(cut_list)):                                       
      cut_index = int(float(cut_list[index])*FPS)                               
      if DEBUG: print("cut_index", cut_index)                                   
                                                                                
      for index in range(cut_index,len(jpg_list)):                              
        sync_index = index                                                      
        if DEBUG: print("sync_index", sync_index)                               
                                                                                
        image1 = io.imread(jpg_list[cut_index])                                 
        image2 = io.imread(jpg_list[sync_index])                                
        similarity = ssim(image1, image2, multichannel=True)                    
        if DEBUG: print(similarity)                                             
        if similarity < 0.9:                                                    
          sync_cut_point.append(sync_index)                                     
          break                                                                 
    if DEBUG: print(sync_cut_point)                                             
    return sync_cut_point

                                                                                
def get_split_point(files_list, cut_point):                                     
    list_split_point = list()                                                   
    for index in range(0, len(cut_point)):                                      
        from_index = 0                                                          
        if index > 0:                                                           
            from_index = cut_point[index-1]*FPS ## 10                           
        to_index = cut_point[index]*FPS ## 10                                   
                                                                                
        for index in range(to_index, from_index, -1):                           
            if index-1 == from_index:                                           
                list_split_point.append((from_index, index))                    
                break                                                           
            image1 = io.imread(files_list[index])                               
            image2 = io.imread(files_list[index-1])                             
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
            image1 = io.imread(snaps)                                           
            image2 = io.imread(files_list[to_index])                            
            similarity = (1-ssim(image1, image2, multichannel=True))*(1000/FPS) 
            sim_list.append(similarity)                                         
            speed = speed + similarity                                          
        speed_index.append((speed, sim_list))  
    return speed_index                                                          
                                                                                
                                                                                
def run_ffmpeg(MP4DIR, video_name, ext):                                                     
    try:                                                                        
        os.makedirs(TEMPDIR +str(video_name), exist_ok = True)                 
    except FileExistsError as e:                                                
        print(e)                                                                
    except Exception as e:                                                      
        print(e)                                                                
        raise e                                                                 
                                                                                
    # ffmpeg 실행                                                               
    # LuHa: fps=2 로 변경                                                       
    # command = 'ffmpeg -i ' + MP4DIR + str(video_name) + '.mp4 -vf fps=10 ' + TEMPDIR + str(video_name) + '/out%04d.jpg'
    command = 'ffmpeg -i ' + MP4DIR + str(video_name) + '.' + ext + ' -vf fps={0} '.format(FPS) + TEMPDIR + str(video_name) + '/out%04d.jpg'
    try:                                                                        
        ffmpeg = subprocess.check_call(command, stdout=subprocess.PIPE, shell=True)
    except Exception as e:                                                      
        print(e)                                                                
        raise e                                                                 
    return True                                                                 
                                                                                
                                                                                
def list_mp4(path):
    movie_ex_list = ['mp4', 'mkv']
    result = []                                                                 
    for f in os.listdir(path):
      for movie in movie_ex_list:
        if f.endswith(movie):                                                  
          result.append((f.split('.'+movie)[0], movie))                                     
    return result                                                               
                                                                                
                                                                                
def list_jpg(path):                                                             
    result = []                                                                 
    for f in os.listdir(path):                                                  
        if f.endswith('.jpg'):                                                  
            result.append(path + f)                                             
    return result                                                      
                    

def get_similarity_list(files_list):
    list_similarity = []

    for index in range(len(files_list)):
        try:
            image1 = io.imread(files_list[index])
            image2 = io.imread(files_list[index+1])
        except OSError as e:
            continue
        except IndexError as e:
            continue
        similarity = ssim(image1, image2, multichannel = True)
        list_similarity.append((files_list[index], files_list[index+1], similarity))
    return list_similarity


def write2csv(video_name, list_split_point, speed_list):
    with open(OUTPUTDIR+OUTPUTFILE, 'a') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for index in range(0, len(speed_list)):
            writer.writerow([video_name, list_split_point[index], speed_list[index][0], speed_list[index][1]])


def get_num_of_touch_event(cut_file_path):
    return len(list(csv.reader(open(cut_file_path))))


def get_cut_point(cut_file_path):
    cuts_t = list()
    with open(cut_file_path,'r') as csvfile:
      reader = csv.DictReader(csvfile, delimiter=",")
      for row in reader:
        cuts_t.append(row['time'])
    return cuts_t


def main(args):                                                                     
    mp4_dir = MP4DIR + args.device+"/" 
    cut_file = CUTFILE + args.device+"/"

    mp4_list = list_mp4(mp4_dir)                                                 
    print(MP4DIR+args.device)                                                                            
    os.makedirs(TEMPDIR, exist_ok = True)                                       
    os.makedirs(OUTPUTDIR, exist_ok = True)                                     
                                                                                
    cut_point = list()
    #get_cut_point(CUTFILE+args.device)                                       
                                                                                
    for video_name, ext in mp4_list:                                                 
        if DEBUG: print("VIDEO NAME:", video_name, "EXT:", ext)                                       
        cut_point = get_cut_point(cut_file+video_name+'.csv')                                       
        try:                                                                    
            if not(run_ffmpeg(mp4_dir, video_name, ext)):                                     
                raise Exception                                                 
        except Exception as e:                                                  
            logging.error(video_name + ' : run_ffmpeg error')                   
            continue                                                            
        files_list = list_jpg(TEMPDIR+video_name+'/')                           
        files_list.sort()                                                       
                                                                                
                                                                       
        print(cut_point)
        cut_point = sync(files_list, cut_point)
        list_split_point = get_split_point(files_list, cut_point)   
        print(list_split_point)                                                 
        speed_list = get_speed_index(files_list, list_split_point)              
        print(speed_list)                                                       
        write2csv(video_name, list_split_point, speed_list)                     
                                                                                
                                                                                
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='calculate speedindex')
    parser.add_argument('--device', '-d',
                        type=str,
                        required=True,
                        help='input ios or android')
    args = parser.parse_args()
    main(args)                                                                      
                                                                                                   
