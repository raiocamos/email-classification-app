import os
import re
from typing import Tuple

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


PRODUCTIVE_KEYWORDS = [
    "urgente", "asap", "prazo", "reunião", "agendar", "proposta",
    "fatura", "pagamento", "contrato", "revisão", "aprovação", "ação necessária",
    "acompanhamento", "solicitação", "confirmar", "atualização", "projeto", "tarefa",
    "entregável", "marco", "orçamento", "relatório", "apresentação"
]

UNPRODUCTIVE_KEYWORDS = [
    "newsletter", "cancelar inscrição", "promoção", "desconto", "venda",
    "propaganda", "spam", "oferta", "grátis", "tempo limitado",
    "parabéns", "ganhador", "loteria", "inscrever", "marketing"
]

FRAUD_KEYWORDS = [
    "será bloqueada", "será bloqueado", "bloqueio permanente", "suspensa",
    "clique no link", "clique aqui", "atualize seus dados", "verifique sua identidade",
    "confirme seus dados", "evitar o bloqueio", "perderá acesso",
    "24 horas", "imediatamente", "urgente", "ação imediata",
    ".xyz", ".ru", ".net.ru", "banco-seguro", "verificacao",
    "você ganhou", "prêmio", "transferência", "pix", "boleto anexo"
]


def detect_fraud(email_content: str) -> Tuple[bool, list]:
    content_lower = email_content.lower()
    found_indicators = []
    
    for indicator in FRAUD_KEYWORDS:
        if indicator.lower() in content_lower:
            found_indicators.append(indicator)
    
    if re.search(r'http[s]?://[^\s]*\.(xyz|ru|tk|ml|ga|cf)', content_lower):
        found_indicators.append("Link suspeito detectado")
    
    is_fraud = len(found_indicators) >= 2
    return is_fraud, found_indicators

PRODUCTIVE_RESPONSES = {
    "meeting": "Recebi sua solicitação de reunião. Vou encaminhar para minha assistente verificar a agenda e confirmar com você.",
    "invoice": "Recebi a fatura. Já encaminhei para o departamento Financeiro processar o pagamento.",
    "deadline": "Ciente do prazo. Já acionei a equipe responsável para garantir a entrega a tempo.",
    "proposal": "Recebi a proposta. Vou encaminhar para o comitê de análise e retornaremos em breve.",
    "urgent": "Entendo a urgência. Estou escalando este assunto para a equipe técnica tratar como prioridade máxima.",
    "approval": "Recebi a solicitação de aprovação. Encaminhei para o setor de Compliance validar antes de eu assinar.",
    "default": "Recebi seu email. Vou direcionar para a área responsável e garantirei que você tenha um retorno em breve."
}


def classify_with_keywords(email_content: str) -> Tuple[str, float, str]:
    content_lower = email_content.lower()
    
    productive_score = sum(1 for kw in PRODUCTIVE_KEYWORDS if kw in content_lower)
    unproductive_score = sum(1 for kw in UNPRODUCTIVE_KEYWORDS if kw in content_lower)
    
    total_keywords = productive_score + unproductive_score
    
    if total_keywords == 0:
        return "Improdutivo", 0.6, "Nenhuma palavra-chave de ação encontrada. Email classificado como improdutivo (não requer resposta)."
    
    if productive_score > unproductive_score:
        confidence = min(0.95, 0.5 + (productive_score - unproductive_score) * 0.1)
        return "Produtivo", confidence, f"Encontradas {productive_score} palavras-chave produtivas vs {unproductive_score} palavras-chave improdutivas."
    elif unproductive_score > productive_score:
        confidence = min(0.95, 0.5 + (unproductive_score - productive_score) * 0.1)
        return "Improdutivo", confidence, f"Encontradas {unproductive_score} palavras-chave improdutivas vs {productive_score} palavras-chave produtivas."
    else:
        return "Improdutivo", 0.5, "Correspondência igual de palavras-chave. Classificado como improdutivo por padrão."


def generate_keyword_response(email_content: str) -> str:
    content_lower = email_content.lower()
    
    if "reunião" in content_lower: return PRODUCTIVE_RESPONSES["meeting"]
    if "fatura" in content_lower: return PRODUCTIVE_RESPONSES["invoice"]
    if "prazo" in content_lower: return PRODUCTIVE_RESPONSES["deadline"]
    if "proposta" in content_lower: return PRODUCTIVE_RESPONSES["proposal"]
    if "urgente" in content_lower: return PRODUCTIVE_RESPONSES["urgent"]
    if "aprovação" in content_lower: return PRODUCTIVE_RESPONSES["approval"]
            
    return PRODUCTIVE_RESPONSES["default"]


def classify_with_ai(email_content: str, api_key: str) -> Tuple[str, float, str]:
    if not OPENAI_AVAILABLE:
        return classify_with_keywords(email_content)
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[
                {
                    "role": "system",
                    "content": """Você é um assistente de classificação de emails para uma empresa financeira.
                    
                    CLASSIFICAÇÃO:
                    
                    **PRODUTIVO** = Email que REQUER UMA RESPOSTA ou AÇÃO IMEDIATA do destinatário:
                    - Solicitações diretas (reuniões, orçamentos, prazos)
                    - Perguntas que precisam ser respondidas
                    - Pedidos de aprovação ou decisão
                    - Demandas de clientes ou parceiros
                    - FRAUDE/PHISHING (requer ação de denúncia à segurança)
                    
                    **IMPRODUTIVO** = Email que NÃO requer resposta nem ação:
                    - Newsletters e informativos
                    - Marketing e promoções
                    - Notificações automáticas (confirmações de compra, atualizações de sistema)
                    - Spam e propagandas
                    - Emails apenas informativos sem pedido de ação
                    - Comunicados gerais que são só para leitura
                    
                    REGRA DE OURO: Se o email não espera uma resposta sua, é IMPRODUTIVO.

                    Responda EXATAMENTE no formato: CLASSIFICAÇÃO|CONFIANÇA|JUSTIFICATIVA
                    
                    Exemplo Produtivo: Produtivo|0.9|O cliente solicita orçamento para serviço, requer resposta.
                    Exemplo Improdutivo: Improdutivo|0.85|Newsletter informativa, não requer resposta nem ação."""
                },
                {
                    "role": "user",
                    "content": f"Analise este email minuciosamente:\n\n{email_content}"
                }
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        result = response.choices[0].message.content.strip()
        parts = result.split("|")
        
        if len(parts) >= 3:
            classification = "Produtivo" if "produtivo" in parts[0].lower() else "Improdutivo"
            try:
                confidence = float(parts[1])
            except ValueError:
                confidence = 0.8
            reasoning = parts[2]
            return classification, confidence, reasoning
        else:
            return classify_with_keywords(email_content)
            
    except Exception as e:
        return classify_with_keywords(email_content)


def generate_ai_response(email_content: str, classification: str, reasoning: str, api_key: str) -> str:
    fraud_keywords = ["fraude", "phishing", "golpe", "alerta de segurança", "suspeito", "spam", "malicioso"]
    reasoning_lower = reasoning.lower()
    
    is_fraud = any(kw in reasoning_lower for kw in fraud_keywords)
    
    if is_fraud:
        return "⚠️ **ALERTA DE SEGURANÇA** ⚠️\n\n**AÇÃO RECOMENDADA:**\n1. **NÃO RESPONDER** a este email.\n2. Encaminhar imediatamente para a equipe de segurança (security@empresa.com).\n3. Bloquear o remetente.\n4. Não clicar em nenhum link ou anexo."
    
    if not OPENAI_AVAILABLE or classification == "Improdutivo":
        if classification == "Improdutivo":
            return "Nenhuma resposta necessária para emails improdutivos."
        return generate_keyword_response(email_content)
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free",
            messages=[
                {
                    "role": "system",
                    "content": """Você é um GERENTE DE OPERAÇÕES da empresa financeira.
                    
                    Aja como um gerente não-técnico que delega:
                    - Não resolva o problema técnico você mesmo.
                    - Demonstre empatia e que entendeu a solicitação.
                    - Encaminhe para a equipe apropriada (TI, Financeiro, Jurídico, RH).
                    - Ex: "Olá, recebi sua mensagem. Já estou acionando a equipe [área] para tratar seu caso."
                    
                    Responda em Português do Brasil."""
                },
                {
                    "role": "user",
                    "content": f"Gere a resposta apropriada para este email:\n\n{email_content}"
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception:
        return generate_keyword_response(email_content)


def classify_email(email_content: str, api_key: str = None) -> dict:
    final_api_key = api_key if api_key and len(api_key) > 10 else os.getenv("OPENROUTER_API_KEY")
    
    is_fraud, fraud_indicators = detect_fraud(email_content)
    
    is_ai_mode = final_api_key and len(final_api_key) > 10
    
    if is_ai_mode:
        classification, confidence, reasoning = classify_with_ai(email_content, final_api_key)
        suggested_response = generate_ai_response(email_content, classification, reasoning, final_api_key)
    else:
        classification, confidence, reasoning = classify_with_keywords(email_content)
        if classification == "Produtivo":
            suggested_response = generate_keyword_response(email_content)
        else:
            suggested_response = "Nenhuma resposta necessária para emails improdutivos."
    
    if is_fraud:
        classification = "Produtivo"
        reasoning = f"⚠️ ALERTA DE SEGURANÇA: Detectados {len(fraud_indicators)} indicadores de fraude/phishing: {', '.join(fraud_indicators)}."
        suggested_response = "⚠️ **ALERTA DE SEGURANÇA** ⚠️\n\n**AÇÃO RECOMENDADA:**\n1. **NÃO RESPONDER** a este email.\n2. Encaminhar imediatamente para a equipe de segurança (security@empresa.com).\n3. Bloquear o remetente.\n4. Não clicar em nenhum link ou anexo."
        confidence = 0.95
    
    return {
        "classification": classification,
        "confidence": confidence,
        "reasoning": reasoning,
        "suggested_response": suggested_response,
        "mode": "IA (OpenRouter)" if is_ai_mode else "Palavras-chave",
        "is_fraud": is_fraud,
        "fraud_indicators": fraud_indicators if is_fraud else []
    }


def extract_text_from_file(uploaded_file) -> str:
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")
    
    elif file_type == "pdf":
        try:
            import PyPDF2
            import io
            
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except ImportError:
            return "Erro: PyPDF2 é necessário para ler arquivos PDF. Instale com: pip install PyPDF2"
        except Exception as e:
            return f"Erro ao ler PDF: {str(e)}"
    
    else:
        return "Formato de arquivo não suportado. Por favor, envie um arquivo .txt ou .pdf."
