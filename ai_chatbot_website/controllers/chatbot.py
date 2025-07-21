from odoo import http
from odoo.http import request
import logging
import time
import json
import requests
import os

_logger = logging.getLogger(__name__)

# Use variável de ambiente segura em produção!
OPENAI_API_KEY = "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"
ASSISTANT_ID = "asst_jixSPwckEBK7bR6jxIYZP3K0"
API_BASE_URL = "https://api.openai.com/v1"

class AIChatbotController(http.Controller):
    @http.route('/ai_chatbot/ask', type='json', auth='public', csrf=False)
    def ask_openai(self, **kwargs):
        try:
            # Lê o JSON da requisição
            try:
                if hasattr(request, 'jsonrequest') and request.jsonrequest:
                    data = request.jsonrequest
                else:
                    raw_data = request.httprequest.data
                    data = json.loads(raw_data.decode('utf-8'))
            except Exception as e:
                _logger.error(f"[AI Chatbot] Falha ao ler corpo da requisição: {str(e)}")
                return {'error': 'Falha ao ler JSON'}

            question = data.get('question', '').strip()
            if not question:
                return {'error': 'Pergunta não fornecida'}

            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
                "OpenAI-Beta": "assistants=v2"
            }

            # Cria thread
            thread_resp = requests.post(
                f"{API_BASE_URL}/threads",
                headers=headers,
                json={}
            )
            if thread_resp.status_code != 200:
                _logger.error(f"[AI Chatbot] Erro ao criar thread: {thread_resp.text}")
                return {'error': 'Erro ao criar sessão com OpenAI'}

            thread_id = thread_resp.json().get("id")

            # Envia mensagem do usuário
            msg_resp = requests.post(
                f"{API_BASE_URL}/threads/{thread_id}/messages",
                headers=headers,
                json={"role": "user", "content": question}
            )
            if msg_resp.status_code != 200:
                _logger.error(f"[AI Chatbot] Erro ao enviar mensagem: {msg_resp.text}")
                return {'error': 'Erro ao enviar pergunta'}

            # Inicia run
            run_resp = requests.post(
                f"{API_BASE_URL}/threads/{thread_id}/runs",
                headers=headers,
                json={"assistant_id": ASSISTANT_ID}
            )
            if run_resp.status_code != 200:
                _logger.error(f"[AI Chatbot] Erro ao iniciar run: {run_resp.text}")
                return {'error': 'Erro ao iniciar conversa'}

            run_id = run_resp.json().get("id")

            # Espera pela resposta
            start_time = time.time()
            while time.time() - start_time < 30:
                status_resp = requests.get(
                    f"{API_BASE_URL}/threads/{thread_id}/runs/{run_id}",
                    headers=headers
                )
                if status_resp.status_code != 200:
                    _logger.error(f"[AI Chatbot] Erro ao verificar status: {status_resp.text}")
                    return {'error': 'Erro ao verificar status'}

                status = status_resp.json().get("status")
                if status == "completed":
                    break
                elif status in ["failed", "cancelled", "expired"]:
                    _logger.error(f"[AI Chatbot] Execução falhou: {status}")
                    return {'error': f'Execução falhou: {status}'}
                time.sleep(1)

            # Pega a resposta
            msg_list_resp = requests.get(
                f"{API_BASE_URL}/threads/{thread_id}/messages",
                headers=headers
            )
            if msg_list_resp.status_code != 200:
                _logger.error(f"[AI Chatbot] Erro ao buscar mensagens: {msg_list_resp.text}")
                return {'error': 'Erro ao buscar resposta'}

            messages = msg_list_resp.json().get("data", [])
            if not messages:
                return {'error': 'Sem resposta do assistente'}

            answer = messages[0]["content"][0]["text"]["value"]
            return {'answer': answer}

        except Exception as e:
            _logger.exception("[AI Chatbot] Erro inesperado")
            return {'error': f'Erro interno: {str(e)}'}

