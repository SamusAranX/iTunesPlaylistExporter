#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
import sys
import math
import re
import argparse
import plistlib
import unicodedata as ud
from urllib.parse import unquote, urlparse
from html import unescape

RE_PATH = re.compile(r"[^-\w. &'…,～%!()–]", re.U)

def get_valid_filename(s):
	s = str(s).strip()
	return RE_PATH.sub("", s)

def join(sep, *args):
	args = [str(s) for s in list(args) if s is not None]
	return sep.join(args)

def normalize(s: str) -> str:
	return ud.normalize("NFC", s)

def main(input_file, out_dir, make_relative=False):
	# this list is entirely arbitrary. add your own here if you want
	ignored_playlists = [
		"Library",
		"Downloaded",
		"Music",
		"All Playlists",
		"Alfred Playlist",
		"Albums without Artwork",
		"Orphaned Tracks",
	]

	# plist vars. do not touch
	PLAYLISTS = "Playlists"
	NAME = "Name"
	PLAYLIST_ITEMS = "Playlist Items"
	TRACK_ID = "Track ID"
	TRACKS = "Tracks"
	LOCATION = "Location"
	ARTIST = "Artist"
	ALBUM = "Album"
	ALBUM_ARTIST = "Album Artist"
	GENRE = "Genre"
	TOTAL_TIME = "Total Time"

	# preparation
	print("Parsing XML file…")
	library = plistlib.load(input_file)
	os.makedirs(out_dir, exist_ok=True)

	# workload
	for pl in library[PLAYLISTS]:
		pl_name = pl[NAME]
		if pl_name in ignored_playlists:
			continue

		new_fname = os.path.join(out_dir, normalize(get_valid_filename(f"{pl_name}.m3u8")))

		with open(new_fname, "w", encoding="utf8") as f:
			f.write("#EXTM3U")

			for tr in pl[PLAYLIST_ITEMS]:
				tr_id = str(tr[TRACK_ID])
				lib_tr = library[TRACKS][tr_id]

				tr_title = lib_tr.get(NAME, None)
				tr_artist = lib_tr.get(ARTIST, None)
				tr_album = lib_tr.get(ALBUM, None)
				tr_album_artist = lib_tr.get(ALBUM_ARTIST, None)
				tr_genre = lib_tr.get(GENRE, None)
				tr_runtime = lib_tr.get(TOTAL_TIME, None)

				runtime = math.ceil(tr_runtime / 1000)
				title_artist = unescape(join(" - ", tr_title, tr_artist))
				f.write(f"\n\n#EXTINF:{join(',', runtime, title_artist)}\n")

				if tr_album:
					f.write(f"#EXTALB:{unescape(unquote(tr_album))}\n")

				if tr_album_artist:
					f.write(f"#EXTART:{unescape(unquote(tr_album_artist))}\n")

				if tr_genre:
					f.write(f"#EXTGENRE:{unescape(unquote(tr_genre))}\n")

				tr_path = urlparse(lib_tr[LOCATION])

				final_path = os.path.abspath(os.path.join(tr_path.netloc, tr_path.path))
				final_path = unquote(final_path) # urldecode step
				# final_path = os.path.splitdrive(final_path)[1][1:] # remove leading slash

				if args.replace:
					oldpath, newpath = args.replace
					final_path = final_path.replace(oldpath, newpath)

				if make_relative:
					final_path = os.path.relpath(final_path, out_dir)

				final_path = normalize(final_path)

				f.write(f"{final_path}")

			print()
			print(f"Successfully exported playlist \"{pl_name}\" to:")
			print(new_fname)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Extract iTunes playlists from an exported Library.xml to individual M3U files")
	parser.add_argument("-i", "--input", metavar="input", type=argparse.FileType("rb"), required=True, help="Library.xml file")
	parser.add_argument("-r", "--relative", action="store_true", help="Makes audio file paths relative")
	parser.add_argument("-R", "--replace", nargs=2, metavar=("oldpath", "newpath"), help="Replace playlist file paths")
	parser.add_argument("out", type=str, default="./", help="output folder")
	args = parser.parse_args()
	main(args.input, os.path.expanduser(args.out), make_relative=args.relative)