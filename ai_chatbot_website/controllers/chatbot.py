from odoo import http
from odoo.http import request
import logging
import json
from openai import OpenAI
from openai import APIError
import os
import time

_logger = logging.getLogger(__name__)


class AIChatbotController(http.Controller):

    @staticmethod
    def carregar_api_key():
        """
        Lê a API key da variável de ambiente OPENAI_API_KEY.
        Esta variável deve estar definida no ambiente do Odoo.sh (.env no servidor).
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            _logger.error("[AI Chatbot] Variável de ambiente OPENAI_API_KEY não encontrada.")
        return api_key


    @http.route('/ai_chatbot/ask', type='json', auth='public', csrf=False)
    def ask_openai(self, **kwargs):
        try:
            # 1. Obter a Pergunta
            if hasattr(request, 'jsonrequest') and request.jsonrequest:
                data = request.jsonrequest
            else:
                raw = request.httprequest.data
                data = json.loads(raw.decode('utf-8'))

            question = data.get('question', '').strip()
            if not question:
                return {'error': 'Pergunta não fornecida'}

            # 2. Buscar API Key da variável de ambiente
            api_key = AIChatbotController.carregar_api_key()

            if not api_key:
                return {'error': 'API Key ausente ou inválida'}

            # 3. Inicializar o Cliente
            client = OpenAI(api_key=api_key)
            assistant_id = "asst_jixSPwckEBK7bR6jxIYZP3K0"

            # =======================================================
            # 4. Lógica do Assistant
            # =======================================================
            thread = client.beta.threads.create()

            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=question
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )

            max_polling_time = 10
            start_time = time.time()

            while run.status not in ["completed", "failed", "cancelled", "expired"]:
                if time.time() - start_time > max_polling_time:
                    _logger.error(f"[AI Chatbot] Timeout no run. Status: {run.status}")
                    return {'error': 'Assistente demorou demasiado tempo.'}

                time.sleep(0.5)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

            if run.status != "completed":
                return {'error': f"Assistente falhou: {run.status}"}

            messages = client.beta.threads.messages.list(
                thread_id=thread.id,
                order="desc",
                limit=1
            )

            answer_text = ""
            if messages.data and messages.data[0].content and messages.data[0].content[0].type == "text":
                answer_text = messages.data[0].content[0].text.value

            return {
                'status': 'completed',
                'answer': answer_text.strip()
            }

        except APIError as e:
            _logger.exception(f"[AI Chatbot] Erro na API OpenAI: {str(e)}")
            return {
                'error': f'Erro da API OpenAI: {e.status_code} - '
                         f'{e.response.json().get("error", {}).get("message", "Detalhes indisponíveis")}'
            }

        except Exception as e:
            _logger.exception(f"[AI Chatbot] Erro inesperado: {str(e)}")
            return {'error': f'Erro interno: {str(e)}'}
