from odoo import http
from odoo.http import request

import time
from openai import OpenAI

# Substitui pela tua chave real
OPENAI_API_KEY = "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"
ASSISTANT_ID = "asst_jixSPwckEBK7bR6jxIYZP3K0"

# Instância do cliente
client = OpenAI(api_key=OPENAI_API_KEY)

class AIChatbotController(http.Controller):

    @http.route('/ai_chatbot/ask', type='json', auth='public', csrf=False)
    def ask_openai(self, **kwargs):
        question = kwargs.get('question', '').strip()

        # Configura o cabeçalho CORS se necessário (embora Odoo lidere isso nativamente via routes públicas)
        request._headers['Access-Control-Allow-Origin'] = '*'

        if not question:
            return {'error': 'Pergunta vazia'}

        try:
            # Cria thread para o chat
            thread = client.beta.threads.create()
            
            # Envia mensagem do usuário
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=question
            )

            # Cria execução para o assistente
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSISTANT_ID
            )

            # Aguardar a resposta ser processada
            for _ in range(30):  # timeout de ~30 segundos
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    return {'error': f'Execução falhou: {run_status.status}'}
                time.sleep(1)

            # Recupera a resposta
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            if not messages.data:
                return {'error': 'Sem resposta do assistente'}

            # Pega a última resposta útil
            for msg in messages.data:
                if msg.role == "assistant" and msg.content:
                    return {'answer': msg.content[0].text.value}

            return {'error': 'Nenhuma resposta útil encontrada'}

        except Exception as e:
            return {'error': str(e)}

