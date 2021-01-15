from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, clips_array, vfx
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os 

def column(matrix, i):
    return [row[i] for row in matrix]
    
def bandreject(file_name):
  os.system("""ffmpeg -y -i in/""" + file_name + """ -c:a pcm_s16le -af "bandreject=f=3000:width_type=h:w=500" temp/""" + file_name + """.wav -y""")
  os.system("ffmpeg -y -i in/""" + file_name + """ -i temp/""" + file_name + """.wav -map 0:v -map 1:a -c:v copy -shortest temp/""" + file_name)
  os.system("rm temp/" + file_name + ".wav")

def double_speed_no_pitch(file_name, speed_coef_sound, speed_coef_video):
  file_name_no_extension = os.path.splitext(file_name)[0]
  os.system("""ffmpeg -y -i """ + file_name + """ -filter_complex "[0:v]setpts="""+speed_coef_video+"""*PTS[v];[0:a]atempo="""+speed_coef_sound+"""[a]" -map "[v]" -map "[a]" """ + file_name_no_extension + "_x2.mp4")


def make_blink(x):
  x = CompositeVideoClip([x, clips_array([[white.set_duration(x.duration)]]).fx(vfx.blink, 0.05 , 100) ]).write_videofile("temp/x.mp4")
  return VideoFileClip("temp/x.mp4")  



os.system("mkdir yamera")
bandreject("yamera/EWIS8487.MOV")

interval = 0.571428571
mesured = 0.575666667
mesured = 0.575125
mesured = 0.575076923
timings = [
['intro',54.240,4],
['a1',2*60+42.977,2],
['a2',2*60+34.922,6],
['b',2*60+38.376,8],
['c1',2*60+38.376,2],  
['c2',3*60+58.770,6],
['chord1',6*60+23.916-0.575,16],
['chord2',5*60+55.143-0.575,16], #todo check start
['chord3',7*60+12.828-0.575,16],
['beat1',4*60+20.199,4],
['beat2',4*60+42.061,4]
]



for i, x in enumerate(column(timings,0)):
  timings[i].append(VideoFileClip("temp/yamera/EWIS8487.MOV").subclip(timings[i][1], timings[i][1] + timings[i][2] * mesured))

timings[1][3] = concatenate_videoclips([timings[1][3],timings[2][3]])
timings[1][0] = 'a'
timings.pop(2)

timings[3][3] = concatenate_videoclips([timings[3][3],timings[4][3]])
timings[3][0] = 'c'
timings.pop(4)

for i, x in enumerate(column(timings,0)):
  if 6 <= i <= 8:
    timings[i][3].volumex(0.5).write_videofile("temp/" + timings[i][0] + ".mp4")
  else :
    timings[i][3].write_videofile("temp/" + timings[i][0] + ".mp4")
  
  
for i, x in enumerate(["a","b","c","chord1","chord2",'chord3','beat1','beat2','beat2_x2','beat2_x2_x2']):
  if (i == 2) :
    speed_coef_sound = 1.96
    speed_coef_video = 0.5
  elif (i < 3) :
    speed_coef_sound = 1.95
    speed_coef_video = 0.5
  elif (i < 6) :
    speed_coef_sound = 1.929 #todo chord 1 and 3 missing 1 frame
    speed_coef_video = 0.513
  elif (i < 7) :
    speed_coef_sound = 0.97
    speed_coef_video = 1.03
  else :
    speed_coef_sound = 2 #todo verify
    speed_coef_video = 0.5
  double_speed_no_pitch("temp/"+ x +".mp4", str(speed_coef_sound), str(speed_coef_video))


length = VideoFileClip("temp/yamera/EWIS8487.MOV").size[0]
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
['beat2_x2_x2_x2',length*4/5,length]
]

for i, x in enumerate(column(timings,0)):
  #timings[i].append(VideoFileClip("temp/"+ x +".mp4"))
  exec(x + """ = VideoFileClip("temp/"+ x +".mp4")""")
  exec(x + "_cropped = "+x+".crop(x1="+str(timings[i][1])+",x2="+str(timings[i][2])+")")
  exec(x+'_cropped.write_videofile("temp/'+x+'_cropped.mp4")')
  
white = VideoFileClip("in/1920x1080-white-solid-color-background.jpg")


melody_full = concatenate_videoclips([a_x2, b_x2, a_x2, c_x2])
melody_cropped_full = concatenate_videoclips([a_x2_cropped, b_x2_cropped, a_x2_cropped, c_x2_cropped]) #todo fix repeat last note (ca modifie le tempo ca: ffmpeg -f concat -safe 0 -i mylist.txt -c copy h_ffmpeg.mp4                  )
chords_cropped_all = clips_array([[chord3_x2_cropped, chord2_x2_cropped, chord1_x2_cropped]])
chords_cropped_all_full = concatenate_videoclips([chords_cropped_all, chords_cropped_all])
beat_cropped_full = concatenate_videoclips(4*[beat1_x2_cropped])

set1 = clips_array([[melody_full]])
set2 = clips_array([[chords_cropped_all_full, melody_full.crop(x1=timings[1][1])]])
set3 = clips_array([[chords_cropped_all_full, melody_cropped_full, beat_cropped_full]])
set4 = clips_array([[a_x2.crop(x2=timings[1][2]), beat2_cropped]])
set4 = set4.subclip(0, mesured*4)

set4 = CompositeVideoClip([set4, clips_array([[white.set_duration(set4.duration)]]).fx(vfx.blink, 0.1 , 100) ]).write_videofile("temp/set4.mp4")
set4 = concatenate_videoclips(4*[VideoFileClip("temp/set4.mp4")])

#set4 = concatenate_videoclips(4*[set4])
set5 = clips_array([[a_x2.crop(x2=timings[1][2]), beat2_x2_cropped]])
set5 = set5.subclip(0, mesured*2)

set5 = CompositeVideoClip([set5, clips_array([[white.set_duration(set5.duration)]]).fx(vfx.blink, 0.1 , 100) ]).write_videofile("temp/set5.mp4")
set5 = concatenate_videoclips(4*[VideoFileClip("temp/set5.mp4")])


#set5 = concatenate_videoclips(4*[set5])
set6 = clips_array([[a_x2.crop(x2=timings[1][2]), beat2_x2_x2_cropped]])
set6 = set6.subclip(0, mesured*1)
#set6 = concatenate_videoclips(4*[set6])

set6 = CompositeVideoClip([set6, clips_array([[white.set_duration(set6.duration)]]).fx(vfx.blink, 0.1 , 100) ]).write_videofile("temp/set6.mp4")
set6 = concatenate_videoclips(4*[VideoFileClip("temp/set6.mp4")])

set7 = clips_array([[a_x2.crop(x2=timings[1][2]), beat2_x2_x2_x2_cropped]])
set7 = set7.subclip(0, mesured*0.5)
set7 = make_blink(set7)
set7 = set7.subclip(0, mesured*0.5)

#set7 = CompositeVideoClip([set7, clips_array([[white.set_duration(set7.duration)]]).fx(vfx.blink, 0.1 , 100) ]).write_videofile("temp/set7.mp4")
set7 = concatenate_videoclips(4*[set7])
#set7 = concatenate_videoclips(4*[VideoFileClip("temp/set7.mp4")])


#CompositeVideoClip([set7, clips_array([[white.set_duration(set7.duration)]]).fx(vfx.blink, 0.1 , 100) ])

#CompositeVideoClip([set7.fx(vfx.blink, 0.1 , mesured), VideoFileClip("in/1920x1080-white-solid-color-background.jpg") ])


#final_clip = concatenate_videoclips([set4, set5, set6, set7])

final_clip = concatenate_videoclips([intro, set1, set2, set3, set4, set5, set6, set7])
final_clip.write_videofile("out/hellov5.mp4")  #todo audio_normalize()

#final_clip = concatenate_videoclips([set3, set4])
#final_clip.write_videofile("out/hellov4b.mp4")  #todo audio_normalize()


exit()


melody_full = concatenate_videoclips([a_x2, b_x2, a_x2, c_x2])
chords_all = clips_array([[chord3_x2, chord2_x2, chord1_x2]])
chords_all_full = concatenate_videoclips([chords_all, chords_all])
beat_full = concatenate_videoclips([beat1, beat1, beat1, beat1])

set1 = clips_array([[melody_full]])
set2 = clips_array([[chords_all_full, melody_full]])
set3 = clips_array([[chords_all_full, melody_full, beat_full]])
set4 = clips_array([[chords_all_full, a_x2, beat2]])
set4 = set4.subclip(0, mesured*4)

final_clip = concatenate_videoclips([intro, set1, set2, set3, set4])
final_clip.write_videofile("out/hellov4.mp4")  #todo audio_normalize()

final_clip = concatenate_videoclips([set3, set4])
final_clip.write_videofile("out/hellov4b.mp4")  #todo audio_normalize()


exit()





mesure_1 = clips_array([[l_beat_abab_5,a_x2]])

r_melody_m2 = r_melody.subclip(4,8)
mesure_2_once = clips_array([[l_beat_abab,r_melody_m2]])
mesure_2 = concatenate_videoclips([mesure_2_once, mesure_2_once, mesure_2_once, mesure_2_once])

double_speed_no_pitch("temp/l_beat_cut.webm")
l_beat_cut_x2 = VideoFileClip("temp/l_beat_cut_x2.webm")
#ffmpeg -i l_beat_cut.webm -af asetrate=44100*0.5,atempo=2.03 output.mp4
mesure_3_once = r_melody_m2.subclip(0,2)
mesure_3_once = clips_array([[l_beat_cut_x2, mesure_3_once]])
mesure_3 = concatenate_videoclips([mesure_3_once, mesure_3_once, mesure_3_once, mesure_3_once])

#mesure_4 = 


final_clip = concatenate_videoclips([timings[0,3], mesure_1, mesure_2, mesure_3])


exit()




bandreject("l_beat.webm")
bandreject("r_melodie.webm")

l_beat_abab = VideoFileClip("temp/l_beat.webm").subclip(03.823 + 5, 03.823 + 5 + 4)
r_melody = VideoFileClip("temp/r_melodie.webm").subclip(04.416 + 5, 04.416 +5 +20)
l_beat_abab = l_beat_abab.crop(x2=(l_beat_abab.size[0]/2))
l_beat_abab.write_videofile("temp/l_beat_cut.webm")
r_melody = r_melody.crop(x1=(r_melody.size[0]/2))
r_melody.write_videofile("temp/r_melody_cut.webm")

#clip3 = VideoFileClip("myvideo3.mp4")
#final_clip = concatenate_videoclips([clip1,clip2])
#final_clip = CompositeVideoClip([clip1,clip2])
l_beat_abab_5 = concatenate_videoclips([l_beat_abab,l_beat_abab,l_beat_abab,l_beat_abab,l_beat_abab])

mesure_1 = clips_array([[l_beat_abab_5,r_melody]])

r_melody_m2 = r_melody.subclip(4,8)
mesure_2_once = clips_array([[l_beat_abab,r_melody_m2]])
mesure_2 = concatenate_videoclips([mesure_2_once, mesure_2_once, mesure_2_once, mesure_2_once])

double_speed_no_pitch("temp/l_beat_cut.webm")
l_beat_cut_x2 = VideoFileClip("temp/l_beat_cut_x2.webm")
#ffmpeg -i l_beat_cut.webm -af asetrate=44100*0.5,atempo=2.03 output.mp4
mesure_3_once = r_melody_m2.subclip(0,2)
mesure_3_once = clips_array([[l_beat_cut_x2, mesure_3_once]])
mesure_3 = concatenate_videoclips([mesure_3_once, mesure_3_once, mesure_3_once, mesure_3_once])

#mesure_4 = 


final_clip = concatenate_videoclips([mesure_1, mesure_2, mesure_3])
final_clip.speedx(2).write_videofile("out/hellov3.mp4")

exit()


clip1 = VideoFileClip("2020-11-02-190418.webm")
clip2 = VideoFileClip("2020-11-02-190428.webm") #.subclip(50,60)
clip1 = clip1.crop(x2=(clip1.size[0]/2))
clip2 = clip2.crop(x1=(clip2.size[0]/2))
#clip3 = VideoFileClip("myvideo3.mp4")
#final_clip = concatenate_videoclips([clip1,clip2])
#final_clip = CompositeVideoClip([clip1,clip2])
final_clip = clips_array([[clip1,clip2]])
final_clip.write_videofile("out/my_concatenation.mp4")

# moviepy.video.fx.all.crop(clip, x1=None, y1=None, x2=None, y2=None, width=None, height=None, x_center=None, y_center=None)[source]



ffmpeg_extract_subclip("in/DLVV6366.MOV", 4, 12, targetname="temp/right.mp4")
ffmpeg_extract_subclip("in/DLVV6366.MOV", 12, 18, targetname="temp/left.mp4")
clip2 = VideoFileClip("temp/right.mp4")
clip1 = VideoFileClip("temp/left.mp4") #.subclip(50,60)
clip1 = clip1.crop(x2=(clip1.size[0]/2))
clip2 = clip2.crop(x1=(clip2.size[0]/2))
final_clip = clips_array([[clip1,clip2]]).fx(vfx.blink, 1 ,1)
final_clip.write_videofile("out/sound.mp4")
final_clip = final_clip.fx(vfx.blink, 0.1 ,0.1)

final_clip.speedx(2).write_videofile("out/soundv2.mp4")

#double speed don't affect pitch   ffmpeg -i input.mkv -filter_complex "[0:v]setpts=<1/x>*PTS[v];[0:a]atempo=<x>[a]" -map "[v]" -map "[a]" output.mkv

#blink with ffmpeg https://superuser.com/questions/710687/ffmpeg-blinking-overlay
# ffmpeg -i in -vf negate out
# ffmpeg -i 2020-11-05-205115.webm -c:a pcm_s16le -af "bandreject=f=3000:width_type=h:w=500" out.webm -y
# ffmpeg -i video.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -shortest output.mp4 #merge audio and video


#video clip timings:
#intro 55 43 59 50 1:15 done 
#a -2:14 2:35 3:00 done
#b 2:35 3:22 done
#c 3,58 -3:38 done
#1 6:23 -5:12
#2 +-5:55
#3 7:12 -7:02
#beat1 4:20 4:27 done
#beat2 4,41 -4,33  done
#
#
