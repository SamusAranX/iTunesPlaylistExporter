# iTunes Playlist Exporter

Building this was faster than trying to export my ~200 playlists one by one and fixing the paths by hand.

## Usage

If you're on Windows, don't run this in a WSL shell or the script will produce playlist files with the wrong paths.
Also, before using this script, make sure your exported Library.xml correctly points to the actual music files (or use `-R` to correct the paths in flight)

The script itself is fairly straightforward to use:

```sh
$ itunes_playlist_exporter.py -R "/Users/test/Music/iTunes" "/Volumes/external/iTunes" -ri Library.xml /Volumes/external/playlists
```

### Options

`-i` specifies the Library.xml file.

`-r/--relative` will rewrite music file paths to be relative to the output directory. This can be useful if your output directory is different than the directory the actual music files are in.

`-R/--replace oldpath newpath` will simply replace all instances of `oldpath` with `newpath` in the music file paths that get written to the playlists. This can be useful if you have a copy of your iTunes library on an external drive and would like to mass-generate playlists for that.

## The playlists this script outputs aren't compatible with my music player of choice!

Well, they should be. Bug the developer of your music player about it.