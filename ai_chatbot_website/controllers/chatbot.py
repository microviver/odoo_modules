from odoo import http
from odoo.http import request
import logging
import time
import json
from openai import OpenAI
import os


_logger = logging.getLogger(__name__)

class AIChatbotController(http.Controller):

    @staticmethod
    def carregar_api_key():
        try:
            with open('config.txt', 'r') as f:
                for linha in f:
                    if linha.startswith('OPENAI_API_KEY='):
                        return linha.strip().split('=', 1)[1]
                        
        except Exception as e:
            _logger.error(f"[AI Chatbot] Erro ao ler config.txt: {str(e)}")
            return None

    @http.route('/ai_chatbot/ask', type='json', auth='public', csrf=False)
    def ask_openai(self, **kwargs):
        try:
            # Diagnóstico: conteúdo da requisição
            try:
                if hasattr(request, 'jsonrequest') and request.jsonrequest:
                    data = request.jsonrequest
                    _logger.info(f"[AI Chatbot] jsonrequest OK: {data}")
                else:
                    raw_data = request.httprequest.data
                    _logger.info(f"[AI Chatbot] httprequest raw data: {raw_data}")
                    data = json.loads(raw_data.decode('utf-8'))
                    _logger.info(f"[AI Chatbot] httprequest fallback: {data}")
            except Exception as e:
                _logger.error(f"[AI Chatbot] Falha ao ler corpo da requisição: {str(e)}")
                return {'error': 'Falha ao ler JSON'}

            # Pegando a pergunta
            question = data.get('question', '').strip()
            if not question:
                return {'error': 'Pergunta não fornecida'}

            _logger.info(f"[AI Chatbot] Pergunta recebida: {question}")

            # OpenAI setup
            client = OpenAI(api_key=AIChatbotController.carregar_api_key())
            assistant_id = "asst_jixSPwckEBK7bR6jxIYZP3K0"

            thread = client.beta.threads.create()
            _logger.info(f"[AI Chatbot] Thread criada: {thread.id}")

            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=question
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )
            _logger.info(f"[AI Chatbot] Run iniciado: {run.id}")

            # Aguarda resposta
            start_time = time.time()
            while time.time() - start_time < 30:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if run_status.status == "completed":
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    resposta = messages.data[0].content[0].text.value
                    _logger.info(f"[AI Chatbot] Resposta: {resposta}")
                    return {'answer': resposta}
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    _logger.error(f"[AI Chatbot] Run falhou: {run_status.status}")
                    return {'error': f'Execução falhou: {run_status.status}'}

                time.sleep(1)

            _logger.error("[AI Chatbot] Timeout ao aguardar resposta")
            return {'error': 'Timeout ao aguardar resposta'}

        except Exception as e:
            _logger.exception("[AI Chatbot] Erro inesperado")
            return {'error': f'Erro interno: {str(e)}'}

