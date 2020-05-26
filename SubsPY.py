import os
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
from pathlib import Path

def get_path():
	path = ""
	i = 0
	while (os.path.isfile(path) != True):
		if (i>0):
			print("Invalid/No file selected. ")
		path = input("Drag the movie/TV episode file to this window and press enter: \n\n").strip("/'").strip('/"');
		i+=1
	return path

def main():
	path = get_path()
	dirname = os.path.dirname(path)

	ost = OpenSubtitles() 
	ost.login('subspy', 'subspy')

	f = File(path)

	data = ost.search_subtitles([{'sublanguageid': 'eng', 'moviehash': f.get_hash(), 'moviebytesize': f.size}])

	id_subtitle_file = data[0].get('IDSubtitleFile')
	overrides = {id_subtitle_file: Path(os.path.basename(path)).stem + ".srt"}

	status = ost.download_subtitles([id_subtitle_file], override_filenames=overrides, output_directory=dirname, extension='srt')

	if status is None:
		input("\nSubtitles could not be downloaded.")
		exit()

	print("\nTitle: " + data[0].get('MovieName') + " (" + data[0].get('MovieYear') + ")")
	print("Rating: " + data[0].get('MovieImdbRating') + "/10 on IMDb")

	print("\nSubtitles downloaded successfully! Enter [y] for another file.");

	if (str(input()).lower()=="y"):
		main()
		return

print(' ___       _                    \n/ __> _ _ | |_  ___    ___  _ _ \n\__ \| | || . \<_-< _ | . \| | |\n<___/`___||___//__/<_>|  _/`_. |\n                      |_|  <___  v0.5.0 by @sheikhuzairhussain\n')
main()