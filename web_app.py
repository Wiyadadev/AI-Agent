import gradio as gr
from main import *
def chat(message):
    try: 
        messages = [{"role": "system", "content": build_system_prompt()}]
        messages.extend(conversation_history[-20:]) 
        messages.append({"role": "user", "content": message}) 
        
        response = client.chat.completions.create(
        model="gpt-4.1-mini",
           messages=messages
        ) 
        agent_reply = response.choices[0].message.content 

        conversation_history.append( 
            {"role": "user", "content": message} 
        )
        conversation_history.append(
             {"role": "assistant", "content": agent_reply} 
        )

        save_history(conversation_history) 

        return agent_reply 
    
    except Exception as e:
       return f"❌ Error: {e}"

demo = gr.ChatInterface(
     fn=chat, 
     title="🍎 Apple AI",
     description="Personal Executive Agent" 
 ) 
demo.launch()