from odoo import http
from odoo.http import request
import logging
import json
import os
from openai import OpenAI

_logger = logging.getLogger(__name__)


class AIChatbotController(http.Controller):

    @staticmethod
    def carregar_api_key():
        """
        Lê a API key a partir de um ficheiro config.txt no diretório do módulo.
        O ficheiro deve conter: OPENAI_API_KEY=xxxx
        """
        try:
            module_path = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(module_path, "config.txt")

            if not os.path.exists(config_path):
                _logger.error(f"[AI Chatbot] config.txt não encontrado em: {config_path}")
                return None

            with open(config_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENAI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        if api_key:
                            return api_key

            _logger.error("[AI Chatbot] OPENAI_API_KEY não encontrada no config.txt")
            return None

        except Exception as e:
            _logger.error(f"[AI Chatbot] Erro ao carregar API key: {str(e)}")
            return None

    @http.route('/ai_chatbot/ask', type='json', auth='public', csrf=False)
    def ask_openai(self, **kwargs):
        """
        Endpoint principal do chatbot: cria thread, envia pergunta,
        inicia o run e devolve thread_id + run_id sem bloquear o worker.
        """
        try:
            # Lê JSON do pedido
            if hasattr(request, 'jsonrequest') and request.jsonrequest:
                data = request.jsonrequest
            else:
                raw = request.httprequest.data
                data = json.loads(raw.decode('utf-8'))

            question = data.get('question', '').strip()
            if not question:
                return {'error': 'Pergunta não fornecida'}

            # Carrega a chave da OpenAI
            api_key = AIChatbotController.carregar_api_key()
            if not api_key:
                return {'error': 'API Key ausente ou inválida'}

            client = OpenAI(api_key=api_key)

            assistant_id = "asst_jixSPwckEBK7bR6jxIYZP3K0"

            # Cria thread
            thread = client.beta.threads.create()

            # Envia a pergunta
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=question
            )

            # Inicia o processamento do assistant
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )

            return {
                'status': 'processing',
                'thread_id': thread.id,
                'run_id': run.id
            }

        except Exception as e:
            _logger.exception("[AI Chatbot] Erro inesperado")
            return {'error': f'Erro interno: {str(e)}'}
