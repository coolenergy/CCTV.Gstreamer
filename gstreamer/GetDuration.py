
# Import everything needed to edit video clips
from moviepy.editor import *
  
def get_duration(path):
    clip = VideoFileClip(path)
    duration = clip.duration
    return duration