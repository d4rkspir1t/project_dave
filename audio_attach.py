import moviepy.editor as mpe
import cv2


my_clip = mpe.VideoFileClip('vid_out/hch_142.avi')
audio_background = mpe.AudioFileClip('src_audio/HCH4.wav')
print(audio_background.end)
print(my_clip.end)

# final_audio = mpe.CompositeAudioClip([my_clip.audi, audio_background])
final_clip = my_clip.set_audio(audio_background)

# print(final_clip.fps)
# my_clip.set_audio(audio_background)
# final_clip.write_videofile("output.avi", codec='png', audio_codec='pcm_s16le')
final_clip.write_videofile("output_raw_libmp3lame.avi", codec='rawvideo', audio_codec='libmp3lame')
# "output/output.mp4",codec= 'mpeg4' ,audio_codec='libvorbis'

