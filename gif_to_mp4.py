import moviepy.editor as mp
clip = mp.VideoFileClip("outputName.gif")
clip.write_videofile("output.mp4")
