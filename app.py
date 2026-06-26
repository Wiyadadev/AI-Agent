import gradio as gr
import base64
import io
from main import *

# ============================================================
# CHAT FUNCTION
# ============================================================
def chat(message, chat_history, image):
    try:
        messages = [{"role": "system", "content": build_system_prompt()}]
        messages.extend(conversation_history[-20:])

        if image is not None:
            from PIL import Image
            img = Image.open(image)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            user_content = [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                {"type": "text", "text": message if message.strip() else "วิเคราะห์รูปภาพนี้ให้หน่อยครับ"}
            ]
        else:
            user_content = message

        messages.append({"role": "user", "content": user_content})

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=1500
        )

        agent_reply = response.choices[0].message.content
        conversation_history.append({"role": "user", "content": message or "[ส่งรูปภาพ]"})
        conversation_history.append({"role": "assistant", "content": agent_reply})
        save_history(conversation_history)

        display_msg = f"📷 {message}" if (image and message.strip()) else ("📷 [ส่งรูปภาพ]" if image else message)
        chat_history = chat_history + [
            {"role": "user", "content": display_msg},
            {"role": "assistant", "content": agent_reply}
        ]
        return chat_history, "", None

    except Exception as e:
        chat_history = chat_history + [
            {"role": "user", "content": message or ""},
            {"role": "assistant", "content": f"❌ Error: {e}"}
        ]
        return chat_history, "", None


def clear_chat():
    global conversation_history
    conversation_history = []
    save_history([])
    return [], "", None


# ============================================================
# CSS
# ============================================================
css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

body, .gradio-container { background: #0a0a0f !important; font-family: 'Inter', sans-serif !important; color: #f1f0ff !important; }

.app-header { text-align: center; padding: 2rem 1rem 1.2rem; border-bottom: 1px solid #1e1e2e; margin-bottom: 1rem; }
.app-header h1 { font-size: 2rem; font-weight: 600; color: #f1f0ff; margin: 0 0 4px; }
.app-header h1 em { font-style: normal; color: #9f67ff; }
.app-header p { font-size: 0.75rem; color: #5a5870; letter-spacing: 3px; text-transform: uppercase; margin: 0; font-family: 'JetBrains Mono', monospace; }

.wrap-col { max-width: 860px; margin: 0 auto; padding: 0 1rem 3rem; }

#chatbot { background: #11111a !important; border: 1px solid #2a2a3a !important; border-radius: 14px !important; height: 500px !important; }

.status-bar { display: flex; align-items: center; gap: 8px; padding: 6px 14px; background: #11111a; border: 1px solid #1e1e2e; border-radius: 8px; font-size: 0.72rem; color: #5a5870; font-family: 'JetBrains Mono', monospace; margin-bottom: 10px; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: #10b981; box-shadow: 0 0 6px #10b981; animation: blink 2s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

#msg-box textarea { background: #11111a !important; border: 1px solid #2a2a3a !important; border-radius: 12px !important; color: #f1f0ff !important; font-size: 0.9rem !important; padding: 10px 14px !important; resize: none !important; }
#msg-box textarea:focus { border-color: #7c3aed !important; box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important; outline: none !important; }
#msg-box textarea::placeholder { color: #3a3850 !important; }

#image-upload { border: 1px dashed #2a2a3a !important; border-radius: 12px !important; background: #11111a !important; }

#send-btn { background: #7c3aed !important; border: none !important; border-radius: 10px !important; color: #fff !important; font-weight: 500 !important; font-size: 0.88rem !important; }
#send-btn:hover { background: #9f67ff !important; box-shadow: 0 0 16px rgba(159,103,255,0.4) !important; }
#clear-btn { background: transparent !important; border: 1px solid #2a2a3a !important; border-radius: 10px !important; color: #5a5870 !important; font-size: 0.85rem !important; }
#clear-btn:hover { border-color: #5a5870 !important; color: #a09ec0 !important; }

.cmd-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.cmd-btn { background: #16161f !important; border: 1px solid #2a2a3a !important; border-radius: 20px !important; color: #5a5870 !important; font-size: 0.72rem !important; padding: 3px 12px !important; font-family: 'JetBrains Mono', monospace !important; cursor: pointer !important; }
.cmd-btn:hover { border-color: #7c3aed !important; color: #9f67ff !important; background: #2d1b69 !important; }

footer, .built-with { display: none !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #7c3aed; }
"""

# ============================================================
# UI — Gradio 6.x
# ============================================================
with gr.Blocks(css=css, title="Apple AI") as demo:

    gr.HTML("""
    <div class="app-header">
        <h1>🍎 Apple <em>AI</em></h1>
        <p>Personal Executive Agent · Vision Enabled</p>
    </div>
    """)

    with gr.Column(elem_classes="wrap-col"):

        gr.HTML("""
        <div class="status-bar">
            <div class="dot"></div>
            <span>gpt-4.1-mini &nbsp;·&nbsp; connected &nbsp;·&nbsp; vision on</span>
        </div>
        """)

        # Gradio 6.x: gr.Chatbot ต้องการ type="messages"
        chatbot = gr.Chatbot(
            elem_id="chatbot",
            show_label=False,
            height=500,
        )

        with gr.Accordion("📎 แนบรูปภาพ (Vision)", open=False):
            image_input = gr.Image(
                type="filepath",
                show_label=False,
                elem_id="image-upload",
                height=160,
            )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="พิมพ์ข้อความ หรือ /help /goals /plan /research /decide /draft ...",
                show_label=False,
                elem_id="msg-box",
                scale=5,
                lines=2,
                max_lines=6,
            )
            with gr.Column(scale=1, min_width=90):
                send_btn = gr.Button("ส่ง ⚡", elem_id="send-btn")
                clear_btn = gr.Button("🗑 ล้าง", elem_id="clear-btn")

        gr.HTML("""
        <div class="cmd-row">
            <button class="cmd-btn" onclick="fillCmd('/help')">/help</button>
            <button class="cmd-btn" onclick="fillCmd('/goals')">/goals</button>
            <button class="cmd-btn" onclick="fillCmd('/plan ')">/plan</button>
            <button class="cmd-btn" onclick="fillCmd('/research ')">/research</button>
            <button class="cmd-btn" onclick="fillCmd('/decide ')">/decide</button>
            <button class="cmd-btn" onclick="fillCmd('/draft ')">/draft</button>
        </div>
        <script>
        function fillCmd(cmd) {
            const ta = document.querySelector('#msg-box textarea');
            if (ta) { ta.value = cmd; ta.focus(); ta.dispatchEvent(new Event('input', {bubbles:true})); }
        }
        </script>
        """)

    send_btn.click(chat, inputs=[msg, chatbot, image_input], outputs=[chatbot, msg, image_input])
    msg.submit(chat, inputs=[msg, chatbot, image_input], outputs=[chatbot, msg, image_input])
    clear_btn.click(clear_chat, outputs=[chatbot, msg, image_input])

if __name__ == "__main__":
    demo.launch()