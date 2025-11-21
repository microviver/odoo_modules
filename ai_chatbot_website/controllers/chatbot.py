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
        """
        Lê a API key a partir de um ficheiro config.txt no diretório do módulo.
        O ficheiro deve conter: OPENAI_API_KEY=xxx
        """
        try:
            # Caminho absoluto e seguro ao próprio módulo
            module_path = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(module_path, "config.txt")

            if not os.path.exists(config_path):
                _logger.error(f"[AI Chatbot] config.txt não encontrado em: {config_path}")
                return None

            with open(config_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENAI_API_KEY="):
                        return line.split("=", 1)[1].strip()

            _logger.error("[AI Chatbot] OPENAI_API_KEY não encontrada no config.txt")
            return None

        except Exception as e:
            _logger.error(f"[AI Chatbot] Falha ao carregar API key: {str(e)}")
            return None

    @http.route('/ai_chatbot/ask', type='json', auth='public', csrf=False)
    def ask_openai(self, **kwargs):
        try:
            # Diagnóstico de JSON
            if hasattr(request, 'jsonrequest') and request.jsonrequest:
                data = request.jsonrequest
            else:
                raw = request.httprequest.data
                data = json.loads(raw.decode('utf-8'))

            question = data.get('question', '').strip()
            if not question:
                return {'error': 'Pergunta não fornecida'}

            api_key = AIChatbotController.carregar_api_key()
            if not api_key:
                return {'error': 'API Key ausente ou inválida'}

            client = OpenAI(api_key=api_key)

            assistant_id = "asst_jixSPwckEBK7bR6jxIYZP3K0"

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

            # ⚠ Importante: NÃO esperas aqui.
            # Evita loops, sleep e freezes no Odoo.sh.
            return {
                'status': 'processing',
                'thread_id': thread.id,
                'run_id': run.id
            }

        except Exception as e:
            _logger.exception("[AI Chatbot] Erro inesperado")
            return {'error': f'Erro interno: {str(e)}'}from odoo import http
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
        """
        Lê a API key a partir de um ficheiro config.txt no diretório do módulo.
        O ficheiro deve conter: OPENAI_API_KEY=xxx
        """
        try:
            # Caminho absoluto e seguro ao próprio módulo
            module_path = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(module_path, "config.txt")

            if not os.path.exists(config_path):
                _logger.error(f"[AI Chatbot] config.txt não encontrado em: {config_path}")
                return None

            with open(config_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENAI_API_KEY="):
                        return line.split("=", 1)[1].strip()

            _logger.error("[AI Chatbot] OPENAI_API_KEY não encontrada no config.txt")
            return None

        except Exception as e:
            _logger.error(f"[AI Chatbot] Falha ao carregar API key: {str(e)}")
            return None

    @http.route('/ai_chatbot/ask', type='json', auth='public', csrf=False)
    def ask_openai(self, **kwargs):
        try:
            # Diagnóstico de JSON
            if hasattr(request, 'jsonrequest') and request.jsonrequest:
                data = request.jsonrequest
            else:
                raw = request.httprequest.data
                data = json.loads(raw.decode('utf-8'))

            question = data.get('question', '').strip()
            if not question:
                return {'error': 'Pergunta não fornecida'}

            api_key = AIChatbotController.carregar_api_key()
            if not api_key:
                return {'error': 'API Key ausente ou inválida'}

            client = OpenAI(api_key=api_key)

            assistant_id = "asst_jixSPwckEBK7bR6jxIYZP3K0"

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

            # ⚠ Importante: NÃO esperas aqui.
            # Evita loops, sleep e freezes no Odoo.sh.
            return {
                'status': 'processing',
                'thread_id': thread.id,
                'run_id': run.id
            }

        except Exception as e:
            _logger.exception("[AI Chatbot] Erro inesperado")
            return {'error': f'Erro interno: {str(e)}'}
