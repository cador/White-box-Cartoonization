import glob
import os
from moviepy.editor import VideoFileClip, ImageSequenceClip, AudioFileClip
from PIL import Image
import multiprocessing
import shutil
import imageio
import math
import time
from pathlib import Path
from cartoonize import style
import hashlib


def get_md5(x):
    m = hashlib.md5()
    m.update(str(x).encode('utf-8'))
    return str(m.hexdigest()).upper()


def check_dir(x):
    if not Path(x).exists():
        Path(x).mkdir()
        return False
    return True


def sub_process(frame_index_array, __key__):
    __video__ = imageio.get_reader('storage/' + rand_key + '/' + target_name)
    index = 0
    for _f_ in __video__:
        if index in frame_index_array:
            __file_name = 'storage/' + __key__ + '/input/' + format(index, '0>10') + '.png'
            Image.fromarray(_f_).save(__file_name)
        index = index + 1
        if index > max(frame_index_array):
            break


def update_transform(target_dir, total_count):
    while True:
        files = glob.glob(pathname=target_dir)
        i = int(len(files)*100.0/total_count)
        num = i // 2
        if i == 100:
            process = "\r[%3s%%]: |%-50s|\n" % (i, '█' * num)
        else:
            process = "\r[%3s%%]: |%-50s|" % (i, '█' * num)
        print(process, end='', flush=True)
        if i == 100:
            return
        time.sleep(5)


input_files = glob.glob(pathname='data/*.mov') + glob.glob(pathname='data/*.mp4') + \
              glob.glob(pathname='data/*.mkv') + glob.glob(pathname='data/*.webm')
for current_file in input_files:
    print(current_file)
    # 1.转换
    rand_key = current_file.split('/')[-1] + '.' + get_md5(current_file)
    path = '/'.join(current_file.split('/')[:-1])
    file_name = current_file.split('/')[-1]
    target_name = '.'.join(file_name.split('.')[:-1])+'.mp4'
    check_dir('storage/' + rand_key)
    check_dir(path + '/results')
    check_dir('storage/' + rand_key + '/input')
    check_dir('storage/' + rand_key + '/output')
    __tmp__ = VideoFileClip(current_file)
    scale = '-vf scale=%s:%s,hflip' % (__tmp__.size[0], __tmp__.size[1])
    trans_cmd = """
        ffmpeg  -i data/{a} -f mp4 -vcodec libx264 -preset fast -profile:v main -acodec aac {scale} -r 24 storage/{b}
    """.format(a=file_name, b=rand_key+'/'+target_name, scale=scale)
    print(trans_cmd)
    os.system(trans_cmd)

    # 2.产生图片
    n_frames = math.floor(__tmp__.duration*24)
    process_list = []
    __l = range(0, n_frames)
    n = math.ceil(len(__l)/6)
    print('正在产生图片...')
    tmp_process = multiprocessing.Process(target=update_transform, args=('storage/' + rand_key + '/input/*.png', n_frames))
    tmp_process.start()
    process_list.append(tmp_process)
    for v in [__l[i:i+n] for i in range(0, len(__l), n)]:
        tmp_process = multiprocessing.Process(target=sub_process, args=(v, rand_key))
        tmp_process.start()
        process_list.append(tmp_process)
    for __process__ in process_list:
        __process__.join()
    print('产生完图片!')

    # 3.转换图片
    style('storage/' + rand_key + '/input', 'storage/' + rand_key + '/output')

    # 4.产生视频
    clip = ImageSequenceClip('storage/' + rand_key + '/output', fps=24)
    out = clip.set_audio(AudioFileClip('data/' + file_name))
    out.write_videofile(filename='data/results/'+target_name, fps=24, codec='libx264', audio_codec='aac', audio=True)

    # 删除文件夹
    shutil.rmtree('storage/' + rand_key)
