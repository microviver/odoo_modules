from odoo import http
from odoo.http import request
import logging
import json
from openai import OpenAI
from openai import APIError
import os
import time # Necessário para o polling (espera)

_logger = logging.getLogger(__name__)


class AIChatbotController(http.Controller):

    # ... (A sua função carregar_api_key pode permanecer como está)
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

            api_key =""
            #with open(config_path, "r") as f:
            #    for line in f:
            #        line = line.strip()
            #        if line.startswith("OPENAI_API_KEY="):
            #            api_key = line.split("=", 1)[1].strip()
            #            if api_key:
            #                _logger.info("[AI Chatbot] API Key carregada com sucesso.")
            #                return api_key
            #            else:
            #                _logger.error("[AI Chatbot] API Key está vazia.")
            #                return None
            # Este log e return só serão alcançados se a chave não for encontrada no ficheiro.
            #_logger.error("[AI Chatbot] OPENAI_API_KEY não encontrada dentro do config.txt")
            return api_key

        except Exception as e:
            _logger.exception(f"[AI Chatbot] Erro ao carregar API key: {str(e)}")
            return None


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

            # 2. Carregar a API Key (Ponto Crítico)
            api_key = AIChatbotController.carregar_api_key()
            if not api_key:
                # Se esta mensagem persistir, o problema está 100% no config.txt ou no caminho
                return {'error': 'API Key ausente | inválida'}

            # 3. Inicializar o Cliente
            client = OpenAI(api_key=api_key)
            
            assistant_id = "asst_jixSPwckEBK7bR6jxIYZP3K0"

            # =======================================================
            # 4. Lógica de Assistant (Threads e Runs) - CORRIGIDA
            # =======================================================
            
            # A. Criar um novo Thread para a conversa
            thread = client.beta.threads.create()

            # B. Adicionar a mensagem do utilizador ao Thread
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=question
            )

            # C. Iniciar a execução do Assistant no Thread
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )

            # D. Polling (Espera) até que o Run esteja concluído
            # Limite de 10 iterações (10 segundos) para evitar bloqueios longos
            max_polling_time = 10
            start_time = time.time()
            
            while run.status not in ["completed", "failed", "cancelled", "expired"]:
                if time.time() - start_time > max_polling_time:
                    _logger.error(f"[AI Chatbot] Tempo de espera do Run excedido. Status: {run.status}")
                    return {'error': 'O assistente demorou demasiado tempo a responder.'}
                
                time.sleep(0.5) # Espera 0.5 segundos
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            if run.status != "completed":
                return {'error': f'O Assistant falhou ou foi cancelado. Status: {run.status}'}

            # E. Obter as mensagens (a mais recente será a resposta)
            messages = client.beta.threads.messages.list(
                thread_id=thread.id,
                order="desc",
                limit=1 # Queremos apenas a última (a resposta)
            )

            answer_text = ""
            if messages.data and messages.data[0].content and messages.data[0].content[0].type == "text":
                 answer_text = messages.data[0].content[0].text.value
            
            # =======================================================
            # 5. Retornar Resposta
            # =======================================================
            return {
                'status': 'completed',
                'answer': answer_text.strip()
            }

        except APIError as e:
            # Captura erros específicos da OpenAI (Ex: chave inválida, limites, etc.)
            _logger.exception(f"[AI Chatbot] Erro (!) da API OpenAI: {str(e)}")
            return {'error': f'Erro(!) da API OpenAI: {e.status_code} - {e.response.json().get("error", {}).get("message", "Detalhes Indisponíveis")}'}

        except Exception as e:
            _logger.exception(f"[AI Chatbot] Erro inesperado: {str(e)}")
            return {'error': f'Erro interno: {str(e)}'}
