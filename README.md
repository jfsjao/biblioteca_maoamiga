
# 📚 Recomendador de Livros com Análise de Sentimentos

Este projeto realiza **scraping** no site [Infolivros](https://www.infolivros.org) para coletar livros gratuitos por categoria e utiliza a **API Gemini** do Google para classificar os sentimentos associados a cada livro com base no título e na descrição. Além disso, a descrição é traduzida para o **português** antes de ser processada pela API.

Projeto finalizado utilizado na plataforma [Animus-Biblioteca](https://animus-saude-mental.netlify.app/biblioteca)

## ⚙️ Funcionalidades

- Coleta automática de livros por categoria (scraping).
- Análise de sentimentos com a API **Gemini**.
- Tradução da descrição do livro para **português**.
- Geração de um arquivo **JSON** com todos os livros e seus respectivos sentimentos.
- Identificação do **autor** com base no título e descrição do livro.

## 🧠 Exemplos de Sentimentos Detectados

- **Felicidade** → livros interessantes
- **Raiva** → livros de terapias alternativas
- **Paixão** → livros de romance
- **Tristeza** → livros de superação pessoal
- **Nostalgia**, **Esperança**, entre outros detectados pela IA.

## 🔧 Como Usar

1. Clone o repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

2. Crie um arquivo `.env` na raiz do projeto com a chave da sua **API Gemini**:

```
GEMINI_API_KEY=sua_chave_api_aqui
```

3. Execute o script principal para iniciar o **scraping** e **classificação de sentimentos**:

```bash
python scraping_livros.py
```

4. O resultado será salvo no arquivo `livros_com_sentimentos.json` na raiz do projeto.

## 📝 Estrutura do JSON

O arquivo **`livros_com_sentimentos.json`** gerado terá a seguinte estrutura:

```json
{
  "livros": [
    {
      "titulo": "Nome do Livro",
      "descricao": "Breve descrição",
      "autor": "Nome do Autor",
      "link_download": "https://...",
      "imagem_capa": "https://...",
      "sentimentos": ["Tristeza", "Paixão", "Esperança"]
    },
    ...
  ]
}
```

## 📁 Categorias Analisadas

Atualmente, o script realiza o **scraping** de livros nas seguintes categorias:

- Meditação
- Ioga
- Autoestima
- Inteligência Emocional
- Reflexão
- Fotografia
- Astronomia
- Amor de Verão
- Romance

## 🛑 Limite da API

O script controla automaticamente o limite de requisições da API (erro **429**) e aguarda o tempo necessário antes de realizar novas requisições, evitando falhas no processo de scraping.

## Contribuindo

Contribuições são bem-vindas! Se você deseja melhorar o projeto ou adicionar novas funcionalidades, por favor, envie um **pull request**.
