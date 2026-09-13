from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, TextClip, ColorClip
import os
from datetime import datetime

# === सेटिंग्स ===
OUTPUT_FILE = "output_video.mp4"
VIDEO_SIZE = (1080, 1920)  # Instagram Reels / WhatsApp Status फॉर्मेट
FPS = 24
DURATION_PER_IMAGE = 2.5  # सेकंड

# === एसेट्स फोल्डर चेक करें ===
ASSETS_DIR = "assets"
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)
    print(f"⚠️ '{ASSETS_DIR}' फोल्डर नहीं मिला, नया बना दिया गया। कृपया इसमें इमेजेज़ डालें।")

# === इमेजेज़ लोड करें ===
images = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
images.sort()

if not images:
    print("❌ कोई इमेज नहीं मिली! कृपया 'assets/' फोल्डर में कम से कम 1 इमेज डालें।")
    # डमी वीडियो बनाएं (टेक्स्ट ओनली)
    print("🔄 डमी वीडियो बना रहा हूँ (टेक्स्ट के साथ)...")
    
    # बैकग्राउंड कलर
    bg = ColorClip(size=VIDEO_SIZE, color=(255, 248, 240), duration=5)
    
    # टाइटल टेक्स्ट
    title = TextClip(
        "VIP Café",
        fontsize=80,
        color="#ff6b6b",
        font="Arial-Bold",
        size=VIDEO_SIZE,
        method="caption",
        align="center"
    ).set_pos("center").set_duration(5)
    
    # सबटाइटल
    subtitle = TextClip(
        "Jorhat's Coolest Hangout ☕",
        fontsize=40,
        color="#333333",
        font="Arial",
        size=VIDEO_SIZE,
        method="caption",
        align="center"
    ).set_pos(("center", 600)).set_duration(5)
    
    video = CompositeVideoClip([bg, title, subtitle], size=VIDEO_SIZE)
    video = video.set_fps(FPS)
    video.write_videofile(OUTPUT_FILE, codec='libx264', audio_codec='aac', fps=FPS)
    print(f"✅ वीडियो बन गया: {OUTPUT_FILE}")
    exit()

# === इमेजेज़ से वीडियो बनाएं ===
print(f"📸 {len(images)} इमेजेज़ मिलीं। वीडियो बना रहा हूँ...")

clips = []
for img_file in images:
    img_path = os.path.join(ASSETS_DIR, img_file)
    try:
        clip = ImageClip(img_path, duration=DURATION_PER_IMAGE)
        # इमेज को वीडियो साइज में फिट करें (crop नहीं, पूरा दिखे)
        clip = clip.resize(height=VIDEO_SIZE[1])
        if clip.w > VIDEO_SIZE[0]:
            clip = clip.resize(width=VIDEO_SIZE[0])
        # सेंटर में सेट करें
        x_pos = (VIDEO_SIZE[0] - clip.w) // 2
        clip = clip.set_pos((x_pos, "center"))
        clips.append(clip)
    except Exception as e:
        print(f"⚠️ {img_file} लोड नहीं हो सकी: {e}")

if not clips:
    print("❌ कोई भी इमेज लोड नहीं हो सकी। प्रोग्राम बंद हो रहा है।")
    exit()

# === वीडियो कंपोज़ करें ===
video = CompositeVideoClip(clips, size=VIDEO_SIZE)
video = video.set_fps(FPS)

# === ऑडियो चेक करें ===
audio_files = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(('.mp3', '.wav', '.m4a'))]
if audio_files:
    audio_path = os.path.join(ASSETS_DIR, audio_files[0])
    print(f"🎵 ऑडियो मिला: {audio_files[0]}")
    try:
        audio = AudioFileClip(audio_path)
        # वीडियो की लंबाई के बराबर ऑडियो काटें
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)
        video = video.set_audio(audio)
    except Exception as e:
        print(f"⚠️ ऑडियो लोड नहीं हो सका: {e}")
else:
    print("ℹ️ कोई ऑडियो नहीं मिला, वीडियो बिना आवाज़ का बनेगा।")

# === वीडियो सेव करें ===
print("🎬 वीडियो रेंडर हो रहा है... (इसमें कुछ मिनट लग सकते हैं)")
video.write_videofile(
    OUTPUT_FILE,
    codec='libx264',
    audio_codec='aac',
    fps=FPS,
    preset='medium',
    bitrate='5000k'
)

print(f"✅ सफलता! वीडियो बन गया: {OUTPUT_FILE}")
print(f"📊 वीडियो साइज: {os.path.getsize(OUTPUT_FILE) / (1024*1024):.2f} MB")
print(f"⏱️ अवधि: {video.duration:.2f} सेकंड")
