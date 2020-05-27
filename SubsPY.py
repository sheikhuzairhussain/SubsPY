import os
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
from pathlib import Path
from termcolor import colored, cprint

def title():
	print(colored(' ___       _                    \n/ __> _ _ | |_  ___    ___  _ _ \n\__ \| | || . \<_-< _ | . \| | |\n<___/`___||___//__/<_>|  _/`_. |\n                      |_|  <___  ', 'yellow') + colored("v0.5.0", 'magenta') + " by " + colored("@sheikhuzairhussain\n", 'magenta'))

def is_video(path):
	extensions = ["mp4", "mkv", "m4a", "avi", "mpg", "mpeg"]
	ext = path.split(".")[-1]
	if ext in extensions:
		return True

def get_path():
	path = ""
	i = 0
	while (os.path.isfile(path) != True and os.path.isdir(path) != True):
		if (i>0):
			print(colored("[ ERROR ] Invalid file/folder selected. \n", "red"))
		path = input("Drag the " + colored('movie/TV episode/folder', 'blue') + " to this window and press enter:\n").strip("/'").strip('/"');
		i+=1
	return path

def download(path, dir_mode = False):
	ost = OpenSubtitles() 
	ost.login('subspy', 'subspy')

	f = File(path)

	
	data = ost.search_subtitles([{'sublanguageid': 'eng', 'moviehash': f.get_hash(), 'moviebytesize': f.size}])

	if data is None or len(data) == 0:
		print("Subtitles could not be found for " + os.path.basename(path))
		return

	if not dir_mode:
		print("")

	print(colored('=============================================================================', 'yellow'))

	print("[ TITLE  ] " + colored(data[0].get('MovieName') + " (" + data[0].get('MovieYear') + ")", 'cyan'))
	print("[ RATING ] " + colored(data[0].get('MovieImdbRating') + "/10 on IMDb", 'cyan'))

	id_subtitle_file = data[0].get('IDSubtitleFile')

	#CONFLICT
	existing_subtitle = os.path.join(os.path.dirname(path), Path(os.path.basename(path)).stem + ".srt")


	abort_flag = False
	suffix = ""

	if (os.path.isfile(existing_subtitle)):
		suffix = ".subspy"
		print(colored("\nSubtitles already exist for this file.", 'red'))
		r = input(colored('Overwrite [o], keep existing [k], or keep both [b]? : ', 'magenta'))
		if r.lower() == "o":
			suffix = ""
			print(colored("Overwriting existing Subtitles", "cyan"));
		elif r.lower() == "k":
			print(colored("Skipping this download.", "cyan"));
			abort_flag = True
		else:
			print(colored("Keeping both files (added prefix).", "cyan"))


	if not abort_flag:
		overrides = {id_subtitle_file: Path(os.path.basename(path)).stem + suffix + ".srt"}
		status = ost.download_subtitles([id_subtitle_file], override_filenames=overrides, output_directory=os.path.dirname(path), extension='srt')

		if status is None:
			input("\nSubtitles could not be downloaded for " + os.path.basename(path))
			return

		print(colored("\nSubtitles downloaded successfully!", "green"));
		
	if not dir_mode:
		print(colored('=============================================================================', 'yellow'))


def main():
	path = get_path()

	if os.path.isfile(path):
		if not is_video(path):
			print(colored("[ ERROR ] The file you selected is not a video. \n", "red"))
			main()
			return

		download(path)

	if os.path.isdir(path):
		print("")
		for root, dirs, files in os.walk(path):
			for file in files:
				filepath = os.path.join(root,file)
				if(is_video(filepath)):
					download(filepath, True)
		if len(files) > 0:
			print(colored('=============================================================================', 'yellow'))
			print(colored('\n[ YAY! ] All downloads completed.', 'green'))

	if (str(input(colored("\nPress 'y' and Enter to download more: ", 'blue'))).lower()=="y"):
		print("")
		main()
		return

os.system('color')
title()
main()