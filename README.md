# 📧 Desafio de Classificação de Emails

Sistema inteligente de classificação de emails para operações financeiras, com detecção de fraude e geração de respostas automáticas.

---

## 🚀 Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| ✅ **Classificação Inteligente** | Separa emails Produtivos de Improdutivos usando IA |
| 🛡️ **Detecção de Fraude** | Identifica automaticamente phishing e golpes |
| 💬 **Respostas Automáticas** | Gera respostas no tom de Gerente de Operações |
| 📄 **Upload de Arquivos** | Suporta análise de arquivos .txt e .pdf |
| 🇧🇷 **100% em Português** | Interface e respostas em PT-BR |

---

## 🔧 Tecnologias Utilizadas

- **Backend**: Python 3.11+ / Flask 3.0
- **Frontend**: HTML5, CSS3, JavaScript
- **IA**: OpenRouter API (Google Gemini 2.0 Flash)
- **Deploy**: Vercel

---

## 📦 Instalação Local

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Conta no [OpenRouter](https://openrouter.ai) para obter a chave API

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/SEU-USUARIO/email-classification-app.git
cd email-classification-app
```

2. **Crie um ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure a variável de ambiente**

Crie um arquivo `.env` na raiz do projeto:
```env
OPENROUTER_API_KEY=sua-chave-api-aqui
```

> ⚠️ **Importante**: Nunca commite o arquivo `.env` para o repositório!

5. **Execute a aplicação**
```bash
python app.py
```

6. **Acesse no navegador**
```
http://127.0.0.1:5000
```

---

## 🖥️ Como Usar

1. **Insira o email**: Cole o assunto e o corpo do email nos campos apropriados
2. **Ou faça upload**: Envie um arquivo .txt ou .pdf
3. **Clique em "Analisar Email"**
4. **Veja os resultados**:
   - Classificação (Produtivo/Improdutivo)
   - Nível de confiança
   - Justificativa da análise
   - Resposta sugerida (ou alerta de segurança)

---

## 🛡️ Detecção de Fraude

O sistema detecta automaticamente emails suspeitos procurando por:
- Senso de urgência falso ("24 horas", "bloqueio permanente")
- Links suspeitos (.xyz, .ru, etc.)
- Solicitações de dados pessoais
- Padrões típicos de phishing

Quando fraude é detectada:
- 🚨 Um **alerta vermelho** é exibido
- A lista de **indicadores suspeitos** é mostrada
- Uma **orientação de segurança** substitui a resposta sugerida

---

## 📁 Estrutura do Projeto

```
email-classification-app/
├── app.py              # Servidor Flask e rotas
├── backend.py          # Lógica de IA e classificação
├── templates/
│   └── index.html      # Interface HTML
├── static/
│   └── style.css       # Estilos CSS
├── requirements.txt    # Dependências Python
├── .gitignore          # Arquivos ignorados pelo Git
├── .env                # Variáveis de ambiente (não commitado)
└── README.md           # Este arquivo
```

---

## ☁️ Deploy em Produção

### Vercel (Recomendado)

1. Faça push do código para o GitHub
2. Acesse [vercel.com](https://vercel.com) e conecte seu GitHub
3. Importe o repositório
4. Configure a variável de ambiente `OPENROUTER_API_KEY` em Settings > Environment Variables
5. Clique em **Deploy**

Seu app estará disponível em: `https://seu-app.vercel.app`

---

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do Desafio de Classificação de Emails.

---

## 👤 Autor

Desenvolvido por raiocamos - 2026

