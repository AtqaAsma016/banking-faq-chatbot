from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from faq_data import BANKING_FAQS
import datetime

load_dotenv()

SYSTEM_PROMPT = f"""You are Asma, a warm and knowledgeable banking assistant for a Pakistani bank.
Use this FAQ knowledge to answer questions accurately:

{BANKING_FAQS}

Guidelines:
- Always greet warmly on first message
- Use PKR for currency, reference Pakistani banking norms
- If asked something outside banking, politely redirect
- For urgent issues (lost card, fraud), always give the helpline: 111-000-111
- Keep answers concise but complete
- Use bullet points for multi-step answers
- Always be professional yet approachable
"""

class Chatbot:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
        self.history = []
        self.message_count = 0
        self.session_start = datetime.datetime.now()

    def predict(self, user_input):
        history_str = ""
        for msg in self.history:
            if isinstance(msg, HumanMessage):
                history_str += f"User: {msg.content}\n"
            else:
                history_str += f"Asma: {msg.content}\n"

        full_prompt = f"{SYSTEM_PROMPT}\n\nConversation History:\n{history_str}\nUser: {user_input}\nAsma:"

        try:
            response = self.llm.invoke(full_prompt)
            answer = response.content
            self.message_count += 1
        except Exception as e:
            answer = "I'm sorry, I'm having trouble connecting right now. Please call our helpline at **111-000-111** for immediate assistance."

        self.history.append(HumanMessage(content=user_input))
        self.history.append(AIMessage(content=answer))

        return answer

    def get_stats(self):
        duration = datetime.datetime.now() - self.session_start
        minutes = int(duration.total_seconds() / 60)
        return {
            "messages": self.message_count,
            "duration": f"{minutes} min" if minutes > 0 else "Just started"
        }

    def clear_history(self):
        self.history = []
        self.message_count = 0
        self.session_start = datetime.datetime.now()

    def export_chat(self):
        lines = [f"Banking Chat Export — {self.session_start.strftime('%Y-%m-%d %H:%M')}\n", "="*50 + "\n"]
        for msg in self.history:
            if isinstance(msg, HumanMessage):
                lines.append(f"You: {msg.content}\n")
            else:
                lines.append(f"Asma: {msg.content}\n")
            lines.append("\n")
        return "".join(lines)

def create_chatbot():
    return Chatbot()