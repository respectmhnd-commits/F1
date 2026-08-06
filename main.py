import os
import subprocess
import streamlink
import sys
import time

channel_name = os.getenv("CHANNEL_NAME")
stream_key = os.getenv("STREAM_KEY")
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

print(f"Starting auto-reconnecting stream bridge for: {channel_name}...")

# حلقة لا نهائية: إذا طفى البث لأي سبب، يرجع يشتغل تلقائياً
while True:
    try:
        print("Fetching stream URL from Kick...")
        streams = streamlink.streams(f"https://kick.com/{channel_name}")
        
        if "best" not in streams:
            print(f"Error: Could not find active stream for {channel_name}. Retrying in 30 seconds...")
            time.sleep(30)
            continue
            
        playback_url = streams["best"].url
        print(f"Successfully got URL! Starting bridge to YouTube...")
        
        # التعديل السحري: استخدام -c copy للنسخ المباشر بدون استهلاك المعالج
        cmd = [
            "ffmpeg",
            "-re",
            "-i", playback_url,
            "-c:v", "copy",   # نسخ الفيديو كما هو
            "-c:a", "copy",   # نسخ الصوت كما هو
            "-f", "flv",
            rtmp_url
        ]

        # تشغيل البث
        subprocess.run(cmd)
        
        # إذا وصل الكود هنا معناه البث فصل، ننتظر 10 ثواني ونعيد المحاولة
        print("Stream disconnected or finished. Reconnecting in 10 seconds...")
        time.sleep(10)

    except Exception as e:
        print(f"Error occurred: {e}. Retrying in 10 seconds...")
        time.sleep(10)
