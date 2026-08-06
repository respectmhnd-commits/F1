import os
import subprocess
import streamlink
import sys

target_channel = os.getenv("CHANNEL_CHOICE")
platform = os.getenv("PLATFORM")
stream_key = os.getenv("STREAM_KEY")

print(f"Fetching stream for Kick channel: {target_channel} to platform: {platform}...")

try:
    streams = streamlink.streams(f"https://kick.com/{target_channel}")
    if "best" not in streams:
        print(f"Error: Could not find active stream for {target_channel}. Make sure it is live.")
        sys.exit(1)
        
    playback_url = streams["best"].url
    
    if platform == "restream":
        rtmp_url = f"rtmp://live.restream.io/live/{stream_key}"
    else:
        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    print(f"Starting bridge from {target_channel} to {platform}...")

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
