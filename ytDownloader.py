
import yt_dlp
from sys import argv

link = argv[1]

ydl_opts = {
    'format': 'best',
    'outtmpl': 'c:/Users/vyank/Downloads/Downloads/%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(link, download=True)
    title = info_dict.get('title', None)
    views = info_dict.get('view_count', None)

print(f"Title: {title}")
print(f"Views: {views}")