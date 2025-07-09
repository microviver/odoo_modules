from odoo import http
from odoo.http import request
from openai import OpenAI
import time

client = OpenAI(api_key="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")
ASSISTANT_ID = "asst_jixSPwckEBK7bR6jxIYZP3K0"

class AIChatbotController(http.Controller):

    @http.route('/ai_chatbot/ask', type='json', auth='public', csrf=False)
    def ask_openai(self, **kwargs):
        question = kwargs.get('question')
        if not question:
            return {'error': 'Pergunta vazia'}

        try:
            thread = client.beta.threads.create()
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=question
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSISTANT_ID
            )

            while True:
                run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    return {'error': f'Execução falhou: {run_status.status}'}
                time.sleep(1)

            messages = client.beta.threads.messages.list(thread_id=thread.id)
            response_text = messages.data[0].content[0].text.value
            return {'answer': response_text}

        except Exception as e:
            return {'error': str(e)}

