#! /usr/bin/python3


from argparse import ArgumentParser

#spracovanie argumentov programu
parser = ArgumentParser(description="Program to add OSD to video file. Values for OSD are read from CSV file.\nTypical use is to merge OpenTX SDlog with onboard footage from RC model")


parser.add_argument("-v", "--video", dest="video_filename", required=True,
					help="Source video", metavar="FILE")

parser.add_argument("-l", "--logfile", dest="log_filename", required=True,
					help="Source logfile in CSV format", metavar="FILE")

parser.add_argument("-o", "--out", dest="out_filename", default="out.mp4", 
					help="target filename", metavar="FILE")

parser.add_argument("-t", "--title", dest="title", type=str,
					help="Video title", metavar="TITLE")

parser.add_argument("-i", "--item", dest="vals", type=str, action='append',
					help="Add item to display. LOG_NAME is value name from logfile. \"-i \'ALT(m),Alt,m\'\" will result in \"Alt:10m\"", metavar="LOG_NAME,TITLE,UNIT")

parser.add_argument("-O", "--offset", dest="log_offset", type=float, default=0,
					help="Offset the logfile by n seconds. Can be negative", metavar="n")

parser.add_argument("-p", "--preview", action="store_true", dest="preview", default=False,
					help="Only preview the result, don't save")

parser.add_argument("-T", "--threads", dest="threads", type=int,
					help="Use n threads for encoding", metavar="n")

parser.add_argument("-b", "--bitrate", dest="bitrate", type=str,
					help="Output video bitrate", metavar="n")


args = parser.parse_args()


#potrebne moduly sa importuju az tu; ak sa iba zobrazuje help alebo doslo ku chybe pri citani argumentov, nebudu potrebne (program sa skonci)
from moviepy.editor import *
import csv
from tqdm import tqdm



#import zdrojoveho videa zo suboru
video_in = VideoFileClip(args.video_filename)



#pridanie nadpisu (ak je zadany)
if args.title:
	title = TextClip(args.title, font='Noto-Mono', fontsize=200, color='white', stroke_color='black', stroke_width=1).set_duration(3).resize(0.25)
	pos = (int((video_in.w-title.w)/2), 30)		#zarovnane na stred videa, 30px zhora
	title = title.set_pos(pos)
	video_out = CompositeVideoClip([video_in, title])
else:
	video_out = video_in

print("\n\nVideo length: %.3fs" % (video_out.duration))



#generovanie vrstvy s textom
osd_list = []
cnt = 0
print("Generating overlay from logfile")
with open(args.log_filename, mode='r') as csv_file:
	pbar = tqdm(total=int(video_in.duration), leave=False)	#progress bar

	csv_reader = csv.DictReader(csv_file)
	for row in csv_reader:									#precita sa kazdy zaznam v logu
		time = row["Time"].split(":")						#podla casu v logu sa zisti trvanie jedneho zaznamu
		new_time = (float(time[0]) * 3600) + (float(time[1]) * 60) + (float(time[2]))
		if cnt > 0:
			duration = new_time - last_time
			osd_list[cnt-1] = osd_list[cnt-1].set_duration(duration)

		osd = ''
		for val in args.vals:								#kazda zadana polozka sa precita z logu a prida do 'osd'
			line = ''
			if(val.split(",")[1]):
				line = val.split(",")[1] + ':'
			line += row[val.split(",")[0]] + val.split(",")[2]
			osd += line.ljust(15) + '\n'

		new_osd = TextClip(osd, font='Noto-Mono', fontsize=90, color='red', stroke_color='black', stroke_width=1).resize(0.2)	#vytvorenie noveho klipu z vytvoreneho textu
		cnt += 1
		osd_list.append(new_osd)							#novy klip sa prida do zoznamu na spojenie
		last_time = new_time
		pbar.update(1)										#aktualizuje sa progress bar
pbar.close()

if cnt > 0:													#trvanie posledneho klipu bude rovnake ako predposledneho
	osd_list[cnt-1] = osd_list[cnt-1].set_duration(duration)



osd = concatenate_videoclips(osd_list).set_pos((5,5))		#spojenie klipov do jedneho
print("# of logs: %d (%.3fs)\nAverage log period: %.3fs" % (cnt, osd.duration, osd.duration/cnt))



if args.log_offset < 0:										#posunutie vrstvy s textom voci videu
	osd = osd.subclip(-args.log_offset)
	args.log_offset = 0

if args.log_offset > 0:
	osd = osd.set_start(args.log_offset)



if (osd.duration + args.log_offset) > video_out.duration:	#ak je log dlhsi ako video, skrati sa
	print("Log longer than video (by %0.3fs), cutting" % ((osd.duration + args.log_offset) - video_out.duration))
	osd = osd.set_duration(video_out.duration - args.log_offset)
print()



video_out = CompositeVideoClip([video_out, osd])			#klip s textom sa vlozi do videa
video_out = video_out.set_audio(video_in.audio)

if args.preview:											#nahlad / ulozenie vysledku
	video_out.preview()
else:
	video_out.write_videofile(args.out_filename, threads=args.threads, bitrate=args.bitrate)
