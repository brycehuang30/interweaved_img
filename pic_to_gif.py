import glob
import moviepy.editor as mpy

gif_name = 'outputName'
fps = 20
file_list = glob.glob('pic/*.png') # Get all the pngs in the current directory
print (file_list)
list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('{}.gif'.format(gif_name), fps=fps)
