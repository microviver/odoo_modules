from odoo import http
from odoo.http import request
import logging
import json
from openai import OpenAI
import os

_logger = logging.getLogger(__name__)


class AIChatbotController(http.Controller):

    @staticmethod
    def carregar_api_key():
        """Lê a API key a partir de config.txt no diretório do módulo."""
        try:
            # Caminho real da pasta onde este ficheiro .py está
            module_path = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(module_path, "config.txt")

            _logger.warning(f"[AI Chatbot] A procurar config.txt em: {config_path}")

            if not os.path.exists(config_path):
                _logger.error(f"[AI Chatbot] config.txt não encontrado em: {config_path}")
                return None

            with open(config_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENAI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        if api_key:
                            _logger.info("[AI Chatbot] API Key carregada com sucesso.")
                            return api_key
                        else:
                            _logger.error("[AI Chatbot] API Key está vazia.")
                            return None

            _logger.error("[AI Chatbot] OPENAI_API_KEY não encontrada dentro do config.txt")
            return None

        except Exception as e:
            _logger.exception(f"[AI Chatbot] Erro ao carregar API key: {str(e)}")
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
                return {'error': 'API Key ausente / inválida'}

            client = OpenAI(api_key=api_key)

            assistant_id = "asst_jixSPwckEBK7bR6jxIYZP3K0"

            response = client.responses.create(
                model="gpt-4.1",
                assistant_id=assistant_id,
                input=question
            )

            # Extrair resposta
            output = response.output or []
            answer_text = ""

            if output:
                block = output[0]
                if block.type == "output_text":
                    for seg in block.text:
                        answer_text += seg["text"]

            return {
                'status': 'completed',
                'answer': answer_text.strip()
            }

        except Exception as e:
            _logger.exception("[AI Chatbot] Erro inesperado")
            return {'error': f'Erro interno: {str(e)}'}
