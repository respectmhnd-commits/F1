import os
import subprocess
import streamlink
import sys

# جلب البيانات من الإعدادات اللي أدخلتها في جيثوب
platform = os.getenv("PLATFORM")
channel_name = os.getenv("CHANNEL_NAME")
stream_key = os.getenv("STREAM_KEY")

print(f"Fetching stream for: {channel_name} on {platform}...")

try:
    # سحب الرابط عبر ستريم لينك لتجاوز الحماية
    streams = streamlink.streams(f"https://kick.com/{channel_name}")
    if "best" not in streams:
        print("Error: Could not find active stream.")
        sys.exit(1)
        
    playback_url = streams["best"].url
    
    # تحديد رابط الإرسال بناءً على المنصة
    if platform == "restream":
        rtmp_url = f"rtmp://live.restream.io/live/{stream_key}"
    else:
        rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    print(f"Starting bridge to {platform}...")

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
