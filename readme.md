# 🚀 SmartLead AI Agent

> ระบบค้นหา Lead ธุรกิจอัตโนมัติด้วย AI — ดึงข้อมูลจริงจาก Google Maps วิเคราะห์คุณภาพ Lead และร่างข้อความติดต่อพร้อมส่ง

[![Live Demo](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-blue)](https://huggingface.co/spaces/vyada/smartlead-ai-agent)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-6.x-FF7C00)](https://gradio.app)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai)](https://openai.com)

---

## ✨ ฟีเจอร์

| ฟีเจอร์ | รายละเอียด |
|---|---|
| 🔍 ค้นหาธุรกิจจริง | ดึงข้อมูลจาก Google Maps ได้ทันที — ชื่อ, ที่อยู่, เบอร์โทร, เว็บไซต์, คะแนนรีวิว |
| 🤖 วิเคราะห์ Lead ด้วย AI | GPT-4o-mini ให้คะแนนความน่าสนใจ 1-10 พร้อมสรุปจุดเด่นแต่ละธุรกิจ |
| ✉️ ร่าง Cold Email อัตโนมัติ | AI เขียนข้อความติดต่อเฉพาะสำหรับแต่ละธุรกิจ พร้อมส่งได้เลย |
| 📊 แสดงผลเป็นตาราง | ดูข้อมูลทั้งหมดในรูปแบบ DataFrame ที่อ่านง่าย |
| ⬇️ Export CSV | ดาวน์โหลดข้อมูลทั้งหมดเป็นไฟล์ที่เปิดได้ใน Excel |

---

## 🖥️ Demo

🔗 **ทดลองใช้งานได้เลย:** [huggingface.co/spaces/vyada/smartlead-ai-agent](https://huggingface.co/spaces/vyada/smartlead-ai-agent)

**ตัวอย่าง:** กรอก `ร้านอาหาร` + `เกาะสมุย` → ได้ผลลัพธ์ทันที:

| Business Name | Phone | Rating | AI Score |
|---|---|---|---|
| Talay Beach Restaurant Samui | 077 300 5x | ⭐ 4.9 (1,271 รีวิว) | 9/10 |
| Day & Night of Koh Samui | 077 332 9x | ⭐ 4.6 (2,345 รีวิว) | 8/10 |
| Wok & Pan Koh Samui | 061 206 0x | ⭐ 4.9 (570 รีวิว) | 9/10 |

---

## 🛠️ Tech Stack

- **Python 3.13** + **Gradio 6** — Backend และ UI
- **Google Places API (New)** — ค้นหาข้อมูลธุรกิจจริงจาก Google Maps
- **OpenAI GPT-4o-mini** — วิเคราะห์ Lead และร่างข้อความ
- **Pandas** — จัดการและ Export ข้อมูล
- **Hugging Face Spaces** — Hosting และ Deployment

---

## ⚙️ วิธีติดตั้ง

### 1. Clone repo
```bash
git clone https://github.com/Wiyadadev/AI-Agent.git
cd AI-Agent
```

### 2. ติดตั้ง dependencies
```bash
pip install -r requirements.txt
```

### 3. ตั้งค่า API Keys
สร้างไฟล์ `.env`:
```env
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. รันแอป
```bash
python app.py
```

เปิดเบราว์เซอร์ที่ `http://localhost:7860`

---

## 🔑 API Keys ที่ต้องใช้

- **Google Places API (New)** → [Google Cloud Console](https://console.cloud.google.com) (ต้องเปิด Billing)
- **OpenAI API** → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

> ⚠️ อย่า commit API Keys ขึ้น GitHub เด็ดขาด — ใช้ `.env` หรือ Secrets เสมอ

---

## 💡 Use Cases

- **Freelancer** — รับจ้างหา Lead ให้ธุรกิจ คิดราคา 500-3,000 บาท/ครั้ง
- **Sales Team** — หาลูกค้าใหม่อัตโนมัติ ประหยัดเวลาหลายชั่วโมงต่อวัน
- **Marketing Agency** — บริการ Lead Generation ให้ลูกค้า
- **SME** — หาคู่ค้าหรือพันธมิตรในพื้นที่

---

## 👩‍💻 Developer

**Wiyada** — Building AI-powered tools for business growth 🚀

[![Hugging Face](https://img.shields.io/badge/🤗-Wiyada-yellow)](https://huggingface.co/vyada)