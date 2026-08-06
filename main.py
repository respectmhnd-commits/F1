import os
import subprocess
import streamlink
import sys

channel_name = os.getenv("CHANNEL_NAME")
stream_key = os.getenv("STREAM_KEY")
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

print(f"Fetching stream URL for Kick channel: {channel_name}...")

try:
    streams = streamlink.streams(f"https://kick.com/{channel_name}")
    if "best" not in streams:
        print(f"Error: Could not find active stream for {channel_name}. Make sure it is live.")
        sys.exit(1)
        
    playback_url = streams["best"].url
    print(f"Successfully got URL: {playback_url}")
    
    print("Starting bridge to YouTube...")
    cmd = [
        "ffmpeg",
        "-re",
        "-i", playback_url,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-maxrate", "4500k",
        "-bufsize", "9000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-f", "flv",
        rtmp_url
    ]

    subprocess.run(cmd)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
