# iTunes Playlist Exporter

Building this was faster than trying to export my ~200 playlists one by one and fixing the paths by hand.

## Usage

If you're on Windows, don't run this in a WSL shell or the script will produce playlist files with the wrong paths.
Also, before using this script, make sure your exported Library.xml correctly points to the actual music files.

The script itself is fairly easy to use:

```sh
$ itunes_playlist_exporter.py -i Library.xml -r ~/Music/Playlists
```

This will make the script read Library.xml and write a bunch of playlists to ~/Music/Playlists, using paths that are relative to that directory. To use absolute paths, simply omit `-r`.