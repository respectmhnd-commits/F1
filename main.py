import os
import subprocess
import streamlink
import threading

c1_name = os.getenv("C1_NAME")
k1_key = os.getenv("K1_KEY")
c2_name = os.getenv("C2_NAME")
k2_key = os.getenv("K2_KEY")

def start_bridge(channel_name, stream_key, destination):
    print(f"[{channel_name}] Fetching stream...")
    try:
        streams = streamlink.streams(f"https://kick.com/{channel_name}")
        if "best" not in streams:
            print(f"[{channel_name}] Error: Active stream not found.")
            return
            
        playback_url = streams["best"].url
        
        if destination == "restream":
            rtmp_url = f"rtmp://live.restream.io/live/{stream_key}"
        else:
            rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
        
        print(f"[{channel_name}] Bridging to {destination}...")
        cmd = [
            "ffmpeg", "-re", "-i", playback_url,
            "-c:v", "libx264", "-preset", "veryfast",
            "-maxrate", "4500k", "-bufsize", "9000k",
            "-pix_fmt", "yuv420p", "-g", "60",
            "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
            "-f", "flv", rtmp_url
        ]
        subprocess.run(cmd)
    except Exception as e:
        print(f"[{channel_name}] Error: {e}")

# تشغيل القناتين معاً (الأولى يوتيوب، الثانية ريستريم)
t1 = threading.Thread(target=start_bridge, args=(c1_name, k1_key, "youtube"))
t2 = threading.Thread(target=start_bridge, args=(c2_name, k2_key, "restream"))

t1.start()
t2.start()
t1.join()
t2.join()
