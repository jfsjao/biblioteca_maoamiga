
# Scraping de Livros

Este projeto utiliza **web scraping** para coletar dados de livros de um site de literatura. Ele extrai informações como o nome do autor, título do livro, descrição, link para download e imagem da capa do livro.

## Funcionalidade

O script realiza o scraping a partir da página de autores e coleta as seguintes informações para cada livro:

- **Autor**: Nome do autor do livro.
- **Título**: Nome do livro.
- **Descrição**: Resumo ou descrição do livro.
- **Link de Download**: Link para baixar o livro.
- **Imagem da Capa**: URL da imagem da capa do livro.

Até 100 livros são coletados, com um máximo de dois livros por autor.

## Tecnologias Utilizadas

- **Python**: Linguagem utilizada para desenvolver o scraper.
- **BeautifulSoup**: Biblioteca para análise e extração de dados de páginas HTML.
- **Requests**: Biblioteca para fazer requisições HTTP.
- **Regex**: Utilizada para manipulação de strings e limpeza de dados.

## Como Usar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/jfsjao/biblioteca_m-o_amiga.git
   cd biblioteca_m-o_amiga
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o script de scraping:**

   ```bash
   python scraping_livros.py
   ```

   O script irá criar um arquivo JSON (`livros_autores.json`) com os dados dos livros coletados.

## Estrutura do Projeto

- `scraping_livros.py`: O script principal que coleta dados dos livros e salva no arquivo `livros_autores.json`.
- `requirements.txt`: Arquivo com as dependências do projeto.

## Exemplo de Dados no `livros_autores.json`

O arquivo JSON gerado terá o seguinte formato:

```json
{
    "livros": [
        {
            "autor": "Júlio Verne",
            "titulo": "Dois Anos de Férias",
            "descricao": "Dois Anos de Férias é uma emocionante história de sobrevivência e amizade em uma ilha deserta, escrita pelo lendário autor Júlio Verne.Este clássico literário aborda temas como coragem, trabalho em equipe e superação de desafios em um ambiente hostil, capturando a imaginação dos leitores.Mergulhe nas páginas de “Dois Anos de Férias” e deixe-se levar pela intriga e emoção desta aventura inesquecível. Descubra por que esta obra-prima de Júlio Verne tem cativado gerações de leitores!",
            "link_download": "https://dl.dropboxusercontent.com/scl/fi/u47258mu5mj8vytmw8nuk/Dois-Anos-de-F-rias-Julio-Verne.pdf?rlkey=38qrja3pwtb4d7yfz6z9avfwz&dl=0",
            "imagem_capa": "https://www.infolivros.org/wp-content/uploads/2024/03/Dois-Anos-de-Ferias-de-Julio-Verne.webp"
        }
    ]
}
```

## Contribuindo

Contribuições são bem-vindas! Se você deseja melhorar o projeto ou adicionar novas funcionalidades, por favor, envie um pull request.

