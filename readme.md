# ⚡ Chief — AI Agent V3

ผู้จัดการส่วนตัว AI ที่ค้นเว็บได้ จำเป้าหมายได้ และทำงานแทนคุณได้

---

## 🚀 วิธีติดตั้ง (ครั้งแรกครั้งเดียว)

### 1. ติดตั้ง dependencies
เปิด Terminal แล้วรัน:
```bash
pip install -r requirements.txt
```

### 2. สร้างไฟล์ `.env`
สร้างไฟล์ชื่อ `.env` ในโฟลเดอร์ `agent_webapp/`:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```
> ดู API Key ได้ที่ https://platform.openai.com/api-keys

### 3. สร้างไฟล์ `memory.json`
สร้างไฟล์ชื่อ `memory.json` ในโฟลเดอร์เดียวกัน:
```json
{
  "owner": "Apple",
  "project": "AI Agent V3",
  "goal": "Become AI Automation Developer"
}
```

---

## ▶️ วิธีรัน

```bash
cd agent_webapp
python app.py
```

แล้วเปิดเบราว์เซอร์ไปที่ → **http://localhost:5000**

---

## 💬 คำสั่งที่ใช้ได้

| คำสั่ง | ทำอะไร |
|--------|--------|
| `/research [หัวข้อ]` | ค้นหาเว็บและสรุปผล |
| `/plan [เรื่อง]` | วาง Action Plan พร้อม timeline |
| `/decide [ปัญหา]` | วิเคราะห์ทางเลือกและแนะนำ |
| `/draft [ประเภท]` | ร่างอีเมล / เอกสาร / โพสต์ |
| `/goal [ข้อความ]` | บันทึกเป้าหมายใหม่ |
| `/goals` | ดูเป้าหมายทั้งหมด |
| `/clear` | ล้างประวัติการสนทนา |

---

## 📁 โครงสร้างไฟล์

```
agent_webapp/
├── app.py                ← Flask backend (ตัวหลัก)
├── requirements.txt      ← dependencies
├── .env                  ← API Key (สร้างเอง ห้าม commit ขึ้น Git)
├── memory.json           ← ข้อมูลเจ้าของ (สร้างเอง)
├── session_history.json  ← ประวัติการสนทนา (auto)
├── goals.json            ← เป้าหมาย (auto)
└── static/
    └── index.html        ← Web UI
```

---

## ❗ แก้ปัญหาเบื้องต้น

**localhost refused to connect**
→ ยังไม่ได้รัน `python app.py` หรือ terminal ปิดอยู่

**ModuleNotFoundError**
→ รัน `pip install -r requirements.txt` ก่อน

**Error: OPENAI_API_KEY not found**
→ ตรวจสอบว่าสร้างไฟล์ `.env` แล้วและใส่ key ถูกต้อง

---

## 🛠️ Built with

- Python + Flask
- OpenAI GPT-4.1-mini
- DuckDuckGo (Web Search ฟรี)
- Vanilla HTML/CSS/JS
