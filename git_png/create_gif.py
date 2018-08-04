# -*- coding: utf-8 -*-
# @Author: jyt_Chiang
# @Date:   2018-08-04 21:47:12
# @Last Modified by:   jyt_Chiang
# @Last Modified time: 2018-08-04 22:49:34
'''
@describe: create a .gif file from several .png
@param: path:code path and .png file path
		out_gif : the .gif file name
'''

import imageio
import os 


path = 'F:\\temp_dat\\git_png'
out_gif = 'my_gif.gif'
def convert_to_gif(path, out_gif):
	filenames = []
	frames = []

	#search all .png files under the path
	for filename in os.listdir(path):
		if os.path.splitext(filename)[1] == '.png':
			filenames.append(filename)
	print(filenames)
	#read all .png file as a list
	for image_name in filenames:
		img_file = imageio.imread(image_name)
		frames.append(img_file)

	#convert to a gif file
	imageio.mimsave( path + '\\' + out_gif, frames, 'GIF', duration=0.6)
	return

convert_to_gif(path, out_gif)