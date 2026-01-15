# Desafio de Classificação de Emails - Roteiro de Vídeo

---

## 📌 Introdução (30 segundos)

> *"Olá! Meu nome é [SEU NOME] e vou apresentar minha solução para o Desafio de Classificação de Emails."*

**Sobre o Desafio:**
Empresas financeiras recebem centenas de emails por dia. Classificar manualmente é lento, caro e arriscado (golpes passam despercebidos).

**Minha Solução:**
Criei um sistema inteligente que:
- Classifica emails como **Produtivo** ou **Improdutivo**.
- Detecta **tentativas de fraude** automaticamente.
- Gera **respostas profissionais** no tom de um Gerente de Operações.

---

## �️ Demonstração (3 minutos)

### Parte 1: A Interface Web
> *Mostrar a tela inicial do sistema.*

- **Campos de Entrada:**
  - Campo "Assunto do Email" para contexto rápido.
  - Área "Corpo do Email" para o conteúdo completo.
  - Opção de upload de arquivos (.txt ou .pdf).

- **Feedback Visual:**
  - Pop-up "Analisando seu email..." aparece ao clicar no botão.
  - Interface 100% em Português do Brasil.

### Parte 2: Classificando um Email Legítimo
> *Colar um email de exemplo (fatura, reunião, proposta).*

- Mostrar o resultado:
  - **Classificação:** Produtivo ✅
  - **Confiança:** ~85%
  - **Justificativa:** "Encontrado contexto de [fatura/reunião]."
  - **Resposta Sugerida:** Texto no estilo "Gerente que delega".
    - *"Recebi sua solicitação. Já encaminhei para a equipe responsável."*

### Parte 3: Detectando um Email de Fraude
> *Colar um email suspeito (urgência falsa, link estranho, erros de português).*

- Mostrar o resultado:
  - **Classificação:** Produtivo ✅ *(requer ação: denúncia!)*
  - **Justificativa:** "ALERTA DE SEGURANÇA: Detectados sinais de phishing..."
  - **Resposta Sugerida:** Alerta interno.
    - *"⚠️ NÃO RESPONDER. Encaminhar para a equipe de segurança."*

---

## 🧠 Explicação Técnica (1 minuto)

### Tecnologias Utilizadas
| Camada | Tecnologia |
|--------|------------|
| **Backend** | Python 3 + Flask |
| **Frontend** | HTML5, CSS3, JavaScript |
| **IA** | OpenRouter API (Modelo: Gemini 2.0 Flash) |
| **Segurança** | Variáveis de ambiente (.env) |

### Como o Algoritmo Funciona
1. **Entrada:** O usuário envia Assunto + Corpo do email.
2. **Classificação (IA):** A API recebe um prompt de sistema instruindo a detectar:
   - Contexto produtivo (fatura, prazo, reunião).
   - Sinais de fraude (urgência, erros, links suspeitos).
3. **Geração de Resposta:**
   - Se for fraude → Retorna alerta de segurança fixo.
   - Se for legítimo → IA gera resposta no tom de Gerente.
4. **Fallback:** Se a API falhar, usa análise de palavras-chave.

### Decisões Técnicas Importantes
- **Persona "Gerente":** A IA não tenta resolver, apenas delega. Evita alucinações.
- **Fraude = Produtivo:** Mudei a lógica para exigir ação humana (denúncia).
- **Alerta Fixo:** Respostas de fraude são hardcoded para segurança máxima.

---

## 🎯 Conclusão (30 segundos)

### O Que Foi Feito
- ✅ Sistema de classificação inteligente.
- ✅ Detecção de fraude com alerta automático.
- ✅ Respostas humanizadas no tom de Gerente.
- ✅ Interface moderna, segura e em Português.

### Pontos de Aprendizado
- A importância de **prompts bem estruturados** para controlar a IA.
- Como **separar lógica de negócio** (backend.py) da interface (app.py).
- Que segurança não é só código: é também **não confiar em respostas de IA** para emails de risco.

> *"Obrigado pela oportunidade! Estou à disposição para perguntas."*
