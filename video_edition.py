from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, clips_array, vfx
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from varname import nameof

#dependencies : pip install varname moviepy

interval = 0.571428571 #duration of 1 note programmed in metronome for 105bpm
mesured = 0.575076923 #duration of 1 note mesured in output video
#video clip aproximate timings:

#intro 55 43 59 50 1:15 done
#a -2:14 2:35 3:00 done
#b 2:35 3:22 done
#c 3,58 -3:38 done
#1 6:23 -5:12
#2 +-5:55
#3 7:12 -7:02
#beat1 4:20 4:27 done
#beat2 4,41 -4,33  done

timings = [ #timestamps of each clip
['intro',54.240-3*mesured,4+3],
['a1',2*60+42.977,2],
['a2',2*60+34.922,6],
['b',2*60+38.376,8],
['c1',2*60+38.376,2],
['c2',3*60+58.770,6],
['chord1',6*60+23.916-0.575,16],
['chord2',5*60+55.143-0.575,16],
['chord3',7*60+12.828-0.575,16],
['beat1',4*60+20.199,4],
['beat2',4*60+42.061,4]
]




def column(matrix, i):
    return [row[i] for row in matrix]

def bandreject(file_name): #remove metronome frequency band
  os.system("""ffmpeg -y -i in/""" + file_name + """ -c:a pcm_s16le -af "bandreject=f=3000:width_type=h:w=500 , afftdn=nr=97:nf=-35" temp/""" + file_name + """.wav -y""")
  os.system("ffmpeg -y -i in/""" + file_name + """ -i temp/""" + file_name + """.wav -map 0:v -map 1:a -c:v copy -shortest temp/""" + file_name)
  os.system("rm temp/" + file_name + ".wav")

def double_speed_no_pitch(file_name, speed_coef_sound, speed_coef_video):
  file_name_no_extension = os.path.splitext(file_name)[0]
  os.system("""ffmpeg -y -i """ + file_name + """ -filter_complex "[0:v]setpts="""+speed_coef_video+"""*PTS[v];[0:a]atempo="""+speed_coef_sound+"""[a]" -map "[v]" -map "[a]" """ + file_name_no_extension + "_x2.mp4")

def double_pitch(file_name):
  file_name_no_extension = os.path.splitext(file_name)[0]
  os.system("ffmpeg -y -i " + file_name_no_extension + ".mp4 -af 'asetrate=44100*2/1,atempo=1/2' " + file_name_no_extension + "_pitched_up.mp4")

def half_pitch(file_name):
  file_name_no_extension = os.path.splitext(file_name)[0]
  os.system("ffmpeg -y -i " + file_name + " -af 'asetrate=44100*1/2,atempo=2/1' " + file_name_no_extension + "_pitched_down.mp4")

def make_blink(x, name, repeat_every_x = 100): #white blinking
  duration = x.duration
  CompositeVideoClip([x, clips_array([[white.set_duration(x.duration)]]).fx(vfx.blink, 0.15 , repeat_every_x - 0.15) ]).write_videofile("temp/"+name+"_blinked.mp4") #removed x =
  return VideoFileClip("temp/"+name+"_blinked.mp4").subclip(0, duration) #changed duration here

def make_black_v1(x, name, blink_time = mesured, repeat_every_x = 100): #black blinking
  duration = x.duration
  CompositeVideoClip([x, clips_array([[black.set_duration(x.duration)]]).fx(vfx.blink, blink_time , repeat_every_x - mesured) ]).write_videofile("temp/"+name+"_inverted_blink.mp4")
  return VideoFileClip("temp/"+name+"_inverted_blink.mp4").subclip(0, duration)


def make_black_v2(x, name, blink_time = 0.15, repeat_every_x = 100): #white blinking time-inverted
  duration = x.duration
  CompositeVideoClip([black.set_duration(x.duration), clips_array([[x]]).fx(vfx.blink, blink_time , repeat_every_x - 0.15) ]).write_videofile("temp/"+name+"_inverted_blink.mp4")
  return VideoFileClip("temp/"+name+"_inverted_blink.mp4").subclip(0, duration)




os.system("mkdir temp temp/yamera out")
#input_file = "yamera/EWIS8487.MOV"
input_file = "yamera/compressed_video.mp4" #compression smooths image and removes flickering pixels from under-exposition
bandreject(input_file)
white = VideoFileClip("in/1920x1080-white-solid-color-background.jpg")
black = VideoFileClip("in/1920x1080-black-solid-color-background.jpg")

#CROP CLIPS IN TIME
for i, x in enumerate(column(timings,0)):
  timings[i].append(VideoFileClip("temp/" + input_file).audio_normalize().subclip(timings[i][1], timings[i][1] + timings[i][2] * mesured))

timings[1][3] = concatenate_videoclips([timings[1][3],timings[2][3]])
timings[1][0] = 'a'
timings.pop(2)

timings[3][3] = concatenate_videoclips([timings[3][3],timings[4][3]])
timings[3][0] = 'c'
timings.pop(4)

for i, x in enumerate(column(timings,0)):
  if 6 <= i <= 8:
    timings[i][3].volumex(0.25).write_videofile("temp/" + timings[i][0] + ".mp4")
  else :
    timings[i][3].write_videofile("temp/" + timings[i][0] + ".mp4")

#CHANGE CLIP DURATION
for i, x in enumerate(["a","b","c","chord1","chord2",'chord3','beat1','beat2','beat2_x2','beat2_x2_x2']):
  if (i == 2) :
    speed_coef_sound = 1.96
    speed_coef_video = 0.5
  elif (i < 3) :
    speed_coef_sound = 1.95
    speed_coef_video = 0.5
  elif (i < 6) :
    speed_coef_sound = 1.929
    speed_coef_video = 0.513
  elif (i < 7) :
    speed_coef_sound = 0.97
    speed_coef_video = 1.03
  else :
    speed_coef_sound = 2
    speed_coef_video = 0.5
  double_speed_no_pitch("temp/"+ x +".mp4", str(speed_coef_sound), str(speed_coef_video))
  if (i < 3) :
    double_pitch("temp/"+ x +"_x2.mp4")

#REIMPORT MODIFIED CLIPS
length = VideoFileClip("temp/" + input_file).size[0]
timings = [
['intro',0,length],
['a_x2',length/2,length*4/5],
['b_x2',length/2,length*4/5],
['c_x2',length/2,length*4/5],
['chord1_x2',length/3,length/2],
['chord2_x2',length/6,length/3],
['chord3_x2',0,length/6],
['beat1_x2',length*4/5,length],
['beat2',length*4/5,length],
['beat2_x2',length*4/5,length],
['beat2_x2_x2',length*4/5,length],
['beat2_x2_x2_x2',length*4/5,length],
['a_x2_pitched_up',length/2,length*4/5],
['b_x2_pitched_up',length/2,length*4/5],
['c_x2_pitched_up',length/2,length*4/5]
]

#CROP CLIPS IN SPACE
for i, x in enumerate(column(timings,0)):
  exec(x + """ = VideoFileClip("temp/"+ x +".mp4")""")
  exec(x + "_cropped = "+x+".crop(x1="+str(timings[i][1])+",x2="+str(timings[i][2])+")")
  exec(x+'_cropped.write_videofile("temp/'+x+'_cropped.mp4")')

#ASSEMBLE ALL CLIPS

melody_full = concatenate_videoclips([a_x2, b_x2, a_x2, c_x2])
melody_cropped_full = concatenate_videoclips([a_x2_cropped, b_x2_cropped, a_x2_cropped, c_x2_cropped])
melody_full_pitched_up = concatenate_videoclips([a_x2_pitched_up, b_x2_pitched_up, a_x2_pitched_up, c_x2_pitched_up])
melody_cropped_full_pitched_up = concatenate_videoclips([a_x2_pitched_up_cropped, b_x2_pitched_up_cropped, a_x2_pitched_up_cropped, c_x2_pitched_up_cropped])
chords_cropped_all = clips_array([[chord3_x2_cropped, chord2_x2_cropped, chord1_x2_cropped]])
chords_cropped_all_full = concatenate_videoclips([chords_cropped_all, chords_cropped_all])
beat_cropped_full = concatenate_videoclips(4*[beat1_x2_cropped])

set1 = clips_array([[melody_full]])
set1 = set1.subclip(0, 9.6)
set2 = clips_array([[chords_cropped_all_full, melody_full.crop(x1=timings[1][1])]])
set2 = set2.subclip(0, 9.6)
set3 = clips_array([[chords_cropped_all_full, melody_cropped_full, beat_cropped_full]])
set3 = set3.subclip(0, 9.6)

set4 = clips_array([[a_x2.crop(x2=timings[1][2]), beat2_cropped]])
set4 = set4.subclip(0, mesured*4)
#set4 = make_blink(set4, nameof(set4))
set4 = make_black_v1(set4, nameof(set4))
set4 = concatenate_videoclips(2*[set4])

set5 = clips_array([[a_x2.crop(x2=timings[1][2]), beat2_x2_cropped]])
set5 = set5.subclip(0, mesured*2)
#set5 = make_blink(set5, nameof(set5))
set5 = make_black_v1(set5, nameof(set5))
set5_unique = set5
set5 = concatenate_videoclips(4*[set5])

set6 = clips_array([[a_x2.crop(x2=timings[1][2]), beat2_x2_x2_cropped]])
set6 = set6.subclip(0, mesured*1)
#set6 = make_blink(set6, nameof(set6))
set6 = make_black_v2(set6, nameof(set6))
set6 = concatenate_videoclips(4*[set6])

set7 = clips_array([[a_x2.crop(x2=timings[1][2]), beat2_x2_x2_x2_cropped]])
set7 = set7.subclip(0, mesured*0.5)
#set7 = make_blink(set7, nameof(set7))
set7 = make_black_v2(set7, nameof(set7))
set7 = concatenate_videoclips(4*[set7])

pause = clips_array([[beat2.crop(x2=length*4/5), c_x2.crop(x1=length*4/5)]]).subclip(0, mesured*0.5).volumex(0)
pause = concatenate_videoclips(4*[pause])

set8 = clips_array([[chords_cropped_all_full, melody_cropped_full_pitched_up, beat_cropped_full]])
set8 = set8.subclip(0, 9.6)
#set8 = make_blink(set8, "set8", melody_cropped_full_pitched_up.duration / 16)
set8 = make_black_v2(set8, "set8", repeat_every_x = melody_cropped_full_pitched_up.duration / 16)

set9 = concatenate_videoclips([set3, set1])


#ALTERNATIVE ENDING 1 :
"""set9 = set4.subclip(0, set4.duration/2)
set10 = set5.subclip(0, set5.duration/2)
set11 = set6.subclip(0, set6.duration/2)
set12 = set7.subclip(0, set7.duration/2)
#set9 = clips_array([[chords_cropped_all_full, melody_full_pitched_up.crop(x1=timings[1][1])]])
#set9 = set8.subclip(0, 9.6)
#set9 = make_blink(set9, "set9", melody_full_pitched_up.duration / 16) #.volumex(3) #todo increase only beat (or nothing) and add blink"""

"""double_speed_no_pitch("temp/intro.mp4", str(0.5), str(2))
intro_slowed = VideoFileClip("temp/intro_x2.mp4")
set10 = concatenate_videoclips([intro.subclip(0, intro.duration/8*7), intro_slowed.subclip(intro_slowed.duration/8*7, intro_slowed.duration)]) #mettre plus grave
set10.write_videofile("temp/set10.mp4")
half_pitch("temp/set10.mp4")
set10a = VideoFileClip("temp/set10_pitched_down.mp4").volumex(0.15)
set10b = VideoFileClip("temp/set10.mp4").volumex(0.15)
set10 = CompositeVideoClip([set10a, set10b])"""

#ALTERNATIVE ENDING 2 :
"""set10 = concatenate_videoclips([set3, set4, set5, set6, set7.set_duration(0, set7.duration/4)])
set10 = concatenate_videoclips([set1, set4, set5] +4*[set5_unique.subclip(set5_unique.duration/2,set5_unique.duration)] + [set10])
set10 = concatenate_videoclips([set1] + 2 * [a_x2.subclip(0, mesured*4)] + 4 * [a_x2.subclip(0, mesured*2)] + 4 * [a_x2.subclip(mesured, mesured*2)] + [set10])
set10 = concatenate_videoclips([set1] + 3 * [a_x2.subclip(0, mesured*4).volumex(0.5)] + 3 * [a_x2.subclip(0, mesured*2).volumex(0.75)] + 3 * [a_x2.subclip(mesured, mesured*2)] + [a_x2.subclip(0, mesured)] + [pause, pause.subclip(0, mesured), set10.volumex(2)])
set10 = concatenate_videoclips([set1] + 3 * [a_x2.subclip(0, mesured*4).volumex(0.5)] + 3 * [a_x2.subclip(0, mesured*2).volumex(0.75)] + 3 * [a_x2.subclip(mesured, mesured*2)] + [make_black_v2(a_x2.subclip(0, mesured), "end_note", blink_time = 10)])"""

set10 = concatenate_videoclips(3 * [a_x2.subclip(0, mesured*4).volumex(0.5)] + 3 * [a_x2.subclip(0, mesured*2).volumex(0.75)] + 3 * [a_x2.subclip(mesured, mesured*2)] + [make_black_v1(a_x2.subclip(0, mesured), "end_note", blink_time = 10)] + 2 * [make_black_v1(pause, "black_end", blink_time = 10)])


final_clip = concatenate_videoclips([intro, set1, set2, set3, set4, set5, set6, set7, pause, set8, set9, set10])
#OUTPUT FINAL VIDEO
final_clip.write_videofile("out/hellov10_compressed.mp4")
os.system("ffmpeg -i out/hellov10_compressed.mp4 -vcodec libx265 -crf 28 out/hellov10_compressed_again.mp4 -y")
