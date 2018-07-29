import os, hashlib, requests
def get_hash(name):
	readsize = 64 * 1024
	with open(name, 'rb') as f:
		size = os.path.getsize(name)
		data = f.read(readsize)
		f.seek(-readsize, os.SEEK_END)
		data += f.read(readsize)
	return hashlib.md5(data).hexdigest()

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
	hash = get_hash(path)

	try:
		request = requests.get("http://api.thesubdb.com/?action=download&language=en&hash=%s" % (hash), headers={"User-Agent": "SubDB/1.0 (Subs.py; nothing)"})
		request.raise_for_status()

	except requests.exceptions.HTTPError:
		code = request.status_code
		if (code == 404):
			print("Subtitles for this file could not be found.")
			main()
			return
		else:
			print("\nAn HTTP error has occured. Please try again.")
			main()
			return
	
	except requests.ConnectionError:
		print("\nA network error has occured. Please try again.")
		main()
		return
	else:
		ext = os.path.splitext(path)
		with open("%s.srt" % ext[0], 'w+') as f:
			f.write(request.text)
		f.close()
		print("\nSubtitles downloaded successfully! Enter [y] for another file.");
		if (str(input()).lower()=="y"):
			main()
			return

print(' ___       _                    \n/ __> _ _ | |_  ___    ___  _ _ \n\__ \| | || . \<_-< _ | . \| | |\n<___/`___||___//__/<_>|  _/`_. |\n                      |_|  <___  v0.2 by @sheikhuzairhussain\n')
main()