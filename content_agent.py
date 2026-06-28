import os
import json
import gradio as gr
from openai import OpenAI
from datetime import datetime

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

PLATFORM_STYLES = {
    "Facebook": {
        "desc": "เป็นกันเอง อ่านง่าย มี emoji เยอะ ความยาว 3-5 ย่อหน้า ลงท้ายด้วยคำถามให้คนคอมเมนต์",
        "max": 500,
    },
    "Instagram": {
        "desc": "สั้น กระชับ มี hook ประโยคแรก ใช้ emoji และ hashtag 10-15 ตัวท้ายโพสต์",
        "max": 300,
    },
    "LinkedIn": {
        "desc": "มืออาชีพ แชร์ insight หรือ lesson learned เน้น value ไม่มี emoji มากเกินไป ความยาว 3-4 ย่อหน้า",
        "max": 600,
    },
    "Twitter/X": {
        "desc": "สั้นกระชับ ไม่เกิน 280 ตัวอักษร มี hook แรงๆ และ hashtag 2-3 ตัว",
        "max": 280,
    },
}

TOPICS = [
    "AI ช่วยธุรกิจได้อย่างไร",
    "วิธีหาลูกค้าใหม่ด้วย AI",
    "SmartLead AI คืออะไร ทำอะไรได้บ้าง",
    "เทรนด์ธุรกิจ AI ในไทย",
    "Case Study: ใช้ AI หา Lead แล้วได้ผลอย่างไร",
    "5 วิธีเพิ่มยอดขายด้วย AI",
    "ทำไมธุรกิจยุคนี้ต้องใช้ AI",
    "กำหนดเอง",
]


def generate_posts(topic, custom_topic, platforms, tone, include_cta):
    if not openai_client:
        return "⚠️ ไม่พบ OPENAI_API_KEY กรุณาตั้งค่าใน Space Secrets", ""

    actual_topic = custom_topic if topic == "กำหนดเอง" else topic
    if not actual_topic or not actual_topic.strip():
        return "⚠️ กรุณากรอกหัวข้อ", ""

    if not platforms:
        return "⚠️ กรุณาเลือกอย่างน้อย 1 platform", ""

    cta_text = "\n- เพิ่ม call-to-action ให้คนทักมาหรือคลิกลิงก์" if include_cta else ""
    results = []

    for platform in platforms:
        style = PLATFORM_STYLES[platform]
        prompt = (
            f"คุณเป็น Social Media Expert ที่เชี่ยวชาญตลาดไทย\n\n"
            f"สร้างโพสต์สำหรับ {platform} เกี่ยวกับ: {actual_topic}\n\n"
            f"สไตล์: {style['desc']}\n"
            f"โทน: {tone}\n"
            f"ความยาวสูงสุด: {style['max']} ตัวอักษร\n"
            f"{cta_text}\n\n"
            f"เขียนโพสต์เป็นภาษาไทย พร้อมใช้งานได้เลย ไม่ต้องมีคำอธิบายเพิ่มเติม"
        )

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
        content = response.choices[0].message.content.strip()
        results.append(f"### 📱 {platform}\n\n{content}\n\n---")

    output = "\n\n".join(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/tmp/posts_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"หัวข้อ: {actual_topic}\n")
        f.write(f"วันที่: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("=" * 50 + "\n\n")
        for r in results:
            f.write(r.replace("### ", "").replace("---", "-" * 30) + "\n\n")

    return output, filename


with gr.Blocks() as demo:
    gr.HTML(
        '<div style="text-align:center;padding:24px 20px;border-radius:16px;'
        'background:linear-gradient(135deg,#7c3aed 0%,#db2777 100%);'
        'color:white;margin-bottom:20px;">'
        '<h1 style="margin:0;font-size:26px;">✍️ Content AI Agent</h1>'
        '<p style="margin:6px 0 0 0;opacity:0.92;font-size:14px;">'
        'สร้างโพสต์ Social Media อัตโนมัติด้วย AI — Facebook, Instagram, LinkedIn, Twitter/X'
        "</p></div>"
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ ตั้งค่าโพสต์")
            topic = gr.Dropdown(
                choices=TOPICS,
                value=TOPICS[0],
                label="🎯 หัวข้อ",
            )
            custom_topic = gr.Textbox(
                label="✏️ หัวข้อกำหนดเอง (ถ้าเลือก 'กำหนดเอง')",
                placeholder="เช่น ประกาศเปิดตัวบริการใหม่...",
                visible=False,
            )
            platforms = gr.CheckboxGroup(
                choices=list(PLATFORM_STYLES.keys()),
                value=["Facebook", "Instagram"],
                label="📱 เลือก Platform",
            )
            tone = gr.Radio(
                choices=["เป็นกันเอง", "มืออาชีพ", "สนุกสนาน", "สร้างแรงบันดาลใจ"],
                value="เป็นกันเอง",
                label="🎨 โทนของโพสต์",
            )
            include_cta = gr.Checkbox(value=True, label="เพิ่ม Call-to-Action")
            generate_btn = gr.Button("🚀 สร้างโพสต์", variant="primary", size="lg")

        with gr.Column(scale=2):
            gr.Markdown("### 📝 โพสต์ที่สร้างได้")
            output = gr.Markdown(value="*โพสต์จะแสดงที่นี่...*")
            download_file = gr.File(label="⬇️ ดาวน์โหลดโพสต์ทั้งหมด")

    def toggle_custom(t):
        return gr.update(visible=(t == "กำหนดเอง"))

    topic.change(fn=toggle_custom, inputs=topic, outputs=custom_topic)

    generate_btn.click(
        fn=generate_posts,
        inputs=[topic, custom_topic, platforms, tone, include_cta],
        outputs=[output, download_file],
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
