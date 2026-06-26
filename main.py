from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import datetime
import urllib.request
import urllib.parse

load_dotenv()

# ============================================================
# LOAD MEMORY
# ============================================================
with open("memory.json", "r", encoding="utf-8") as f:
    memory = json.load(f)

# ============================================================
# LOAD / INIT SESSION HISTORY (ถาวรข้ามวัน)
# ============================================================
HISTORY_FILE = "session_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# ============================================================
# WEB SEARCH (DuckDuckGo — ฟรี ไม่ต้อง API key)
# ============================================================
def web_search(query: str, max_results: int = 5) -> str:
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read().decode())

        results = []

        if data.get("AbstractText"):
            results.append(f"📌 สรุป: {data['AbstractText']}")

        for item in data.get("RelatedTopics", [])[:max_results]:
            if isinstance(item, dict) and item.get("Text"):
                results.append(f"• {item['Text']}")

        if not results:
            return "ไม่พบผลลัพธ์ที่ชัดเจน ลองค้นด้วยคำอื่น"

        return "\n".join(results)
    except Exception as e:
        return f"ค้นหาไม่สำเร็จ: {e}"

# ============================================================
# GOAL TRACKER
# ============================================================
GOALS_FILE = "goals.json"

def load_goals():
    if os.path.exists(GOALS_FILE):
        with open(GOALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_goal(goal_text):
    goals = load_goals()
    goals.append({
        "goal": goal_text,
        "created": datetime.datetime.now().isoformat(),
        "status": "active"
    })
    with open(GOALS_FILE, "w", encoding="utf-8") as f:
        json.dump(goals, f, ensure_ascii=False, indent=2)
    return f"✅ บันทึกเป้าหมายแล้ว: {goal_text}"

def show_goals():
    goals = load_goals()
    if not goals:
        return "ยังไม่มีเป้าหมายที่บันทึกไว้"
    lines = ["🎯 เป้าหมายของคุณ:"]
    for i, g in enumerate(goals, 1):
        status = "✅" if g["status"] == "done" else "🔄"
        lines.append(f"{i}. {status} {g['goal']} (เพิ่มเมื่อ {g['created'][:10]})")
    return "\n".join(lines)

# ============================================================
# SYSTEM PROMPT
# ============================================================
def build_system_prompt():
    goals = load_goals()
    goal_text = "\n".join([f"- {g['goal']}" for g in goals if g["status"] == "active"]) or "ยังไม่มีเป้าหมาย"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""คุณคือ AI Agent V3 ผู้จัดการส่วนตัวของ {memory['owner']}
วันที่และเวลาปัจจุบัน: {now}

## ข้อมูลเจ้าของ
- ชื่อ: {memory['owner']}
- โปรเจกต์: {memory['project']}
- เป้าหมายหลัก: {memory['goal']}

## เป้าหมายที่บันทึกไว้:
{goal_text}

## บทบาทของคุณ
- ทำงานเหมือนผู้จัดการส่วนตัวระดับ Executive
- เชื่อมทุกคำตอบกลับสู่เป้าหมายของเจ้าของเสมอ
- กระชับ actionable และเชิงรุก
- ถ้าเห็นโอกาสหรือความเสี่ยง ให้บอกเลย

## คำสั่งพิเศษที่รองรับ (ระบบจัดการให้อัตโนมัติ)
/goals, /goal [เป้าหมาย], /plan [เรื่อง], /research [หัวข้อ], /decide [ปัญหา], /draft [ประเภท], /clear, /help

## สไตล์การตอบ
- ภาษาไทยเป็นหลัก สลับอังกฤษเมื่อจำเป็น
- ตรงไปตรงมา ไม่ยืดยาว
- จบทุก task ด้วย "⚡ ขั้นต่อไป:" เสมอ"""

# ============================================================
# CLIENT
# ============================================================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = load_history()

# ============================================================
# MAIN LOOP
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI Agent V3 — Personal Manager")
    print(f"👤 Owner: {memory['owner']}")
    print(f"🎯 Project: {memory['project']}")
    print(f"📚 ประวัติการสนทนา: {len(conversation_history)} messages")
    print("=" * 50)
    print("พิมพ์ /help เพื่อดูคำสั่ง | exit เพื่อออก")

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            save_history(conversation_history)
            print("💾 บันทึก session แล้ว | 👋 ปิด Agent")
            break

        if user_input == "/help":
            print("""
📋 คำสั่งทั้งหมด:
  /goals              — แสดงเป้าหมายทั้งหมด
  /goal [ข้อความ]     — บันทึกเป้าหมายใหม่
  /plan [เรื่อง]      — วาง action plan
  /research [หัวข้อ]  — ค้นเว็บและสรุป
  /decide [ปัญหา]     — วิเคราะห์และเสนอทางเลือก
  /draft [ประเภท]     — ร่างเอกสาร/อีเมล/โพสต์
  /clear              — ล้างประวัติการสนทนา
  exit                — ออกจากโปรแกรม
            """)
            continue

        if user_input == "/goals":
            print(show_goals())
            continue

        if user_input.startswith("/goal "):
            goal_text = user_input[6:].strip()
            print(save_goal(goal_text))
            continue

        if user_input == "/clear":
            conversation_history = []
            save_history([])
            print("🗑️ ล้างประวัติการสนทนาแล้ว")
            continue

    # ---- SEARCH COMMAND ----
    if user_input.startswith("/research "):
        query = user_input[10:].strip()
        print(f"\n🔍 กำลังค้นหา: {query}...")
        search_result = web_search(query)
        user_input = f"ค้นหาข้อมูลเรื่อง '{query}' และได้ผลลัพธ์นี้:\n{search_result}\n\nสรุปและวิเคราะห์ให้หน่อย พร้อม insight ที่เกี่ยวกับเป้าหมายของฉัน"

    # ---- PLAN COMMAND ----
    elif user_input.startswith("/plan "):
        topic = user_input[6:].strip()
        user_input = f"ช่วยวาง action plan สำหรับ '{topic}' ให้หน่อย แตกเป็น steps ชัดเจน พร้อม timeline และเจ้าของ task"

    # ---- DECIDE COMMAND ----
    elif user_input.startswith("/decide "):
        problem = user_input[8:].strip()
        user_input = f"ช่วยวิเคราะห์ปัญหา '{problem}' ให้หน่อย เสนอทางเลือกพร้อม pros/cons และแนะนำว่าควรเลือกอะไร"

    # ---- DRAFT COMMAND ----
    elif user_input.startswith("/draft "):
        doc_type = user_input[7:].strip()
        user_input = f"ช่วยร่าง {doc_type} ให้หน่อย ในสไตล์ที่เหมาะสม professional และ effective"

    # ---- CALL AI ----
    try:
        messages = [{"role": "system", "content": build_system_prompt()}]
        messages.extend(conversation_history[-20:])
        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        agent_reply = response.choices[0].message.content
        print(f"\n🤖 Agent: {agent_reply}")

        # Save to history
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": agent_reply})

        # Auto-save every turn
        save_history(conversation_history)

    except Exception as e:
        print(f"\n❌ Error: {e}")