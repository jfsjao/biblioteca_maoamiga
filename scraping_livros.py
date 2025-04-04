import requests
from bs4 import BeautifulSoup
import json
import re  # Para manipulação de strings corretamente

def corrigir_nome(nome):
    """
    Remove números seguidos de parênteses no início da string.
    Exemplo: '22) Guy de Maupassant' vira 'Guy de Maupassant'.
    """
    return re.sub(r"^\d+\)", "", nome).strip()

def corrigir_link(link):
    """
    Corrige a URL de download, substituindo espaços por '%20' e mantendo outros caracteres especiais.
    """
    return link.replace(" ", "%20").replace("%28", "(").replace("%29", ")")

def pegar_imagem(livro_soup):
    """
    Tenta pegar a URL da imagem de capa do livro.
    Tenta primeiro pegar o data-src e depois o src.
    """
    # Busca a tag <img> com a classe da capa do livro
    imagem_tag = livro_soup.find('img', class_='aligncenter')
    if imagem_tag:
        # Primeiro, tentamos pegar o link da imagem de 'data-src'
        imagem_url = imagem_tag.get('data-src')
        if not imagem_url:
            # Se não encontrar, tenta pegar o link do 'src'
            imagem_url = imagem_tag.get('src')
        
        # Se a imagem tiver um link, completamos o caminho se necessário (se for um link relativo)
        if imagem_url:
            if imagem_url.startswith("/"):
                imagem_url = "https://www.infolivros.org" + imagem_url
            return imagem_url
    return None  # Caso não encontre a imagem

def scraping_livros_autores():
    """
    Faz o scraping da página de todos os autores listados para coletar os livros, descrição, links de download e imagens.
    Limita o número de livros coletados a 100, pegando apenas os 2 melhores por autor.
    """
    
    # URL da página principal com a lista de autores
    url_autores = "https://www.infolivros.org/autores/classicos/"

    # Para armazenar os dados dos livros
    dados = {"livros": []}

    print(f"Coletando dados de {url_autores}...")

    # Requisição para acessar a página de autores
    resposta = requests.get(url_autores)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.content, 'html.parser')

        # Encontrar todos os divs que contêm o link e o nome do autor
        autores_div = soup.find_all('div', class_='content_raiz')

        contador_livros = 0  # Contador de livros

        # Para cada autor, coletar os livros
        for autor_div in autores_div:
            # Tentar encontrar o nome do autor dentro do h2
            nome_autor_tag = autor_div.find('h2', class_='has-text-align-center')
            if nome_autor_tag:
                nome_autor = nome_autor_tag.text.strip()
                nome_autor = corrigir_nome(nome_autor)  # Corrigir o nome do autor removendo números e parênteses
            else:
                print("Erro: Não foi possível encontrar o nome do autor.")
                continue  # Pular para o próximo autor se o nome não for encontrado

            link_autor = autor_div.find('a', href=True)['href']

            # Acessa a página do autor
            resposta_autor = requests.get(link_autor)
            if resposta_autor.status_code == 200:
                soup_autor = BeautifulSoup(resposta_autor.content, 'html.parser')

                # Encontrar os livros na página do autor
                livros = soup_autor.find_all('div', class_='content_libro_autor')

                # Limitar a 2 livros por autor
                livros_por_autor = livros[:2]

                # Para cada livro encontrado, coletar título, descrição, link de download e imagem
                for livro in livros_por_autor:
                    titulo = livro.find('h2', class_='has-text-align-center').text.strip()
                    titulo = corrigir_nome(titulo)  # Corrigir o título removendo números e parênteses
                    descricao = livro.find('div', class_='descripcion').text.strip()

                    # Procurar pelos links de download (div com classe 'btn-descargar' ou 'btn-leer')
                    link_download_elemento = livro.find('div', class_='btn-descargar').find('a', href=True) if livro.find('div', class_='btn-descargar') else None
                    if not link_download_elemento:
                        link_download_elemento = livro.find('div', class_='btn-leer').find('a', href=True) if livro.find('div', class_='btn-leer') else None
                    
                    link_download = link_download_elemento['href'] if link_download_elemento else None

                    # Corrigir o link de download para garantir que os espaços e caracteres especiais sejam bem formatados
                    if link_download:
                        link_download = corrigir_link(link_download)

                    # Obter a imagem de capa do livro
                    imagem_capa = pegar_imagem(livro)

                    # Adicionar as informações do livro ao dicionário
                    dados["livros"].append({
                        'autor': nome_autor,
                        'titulo': titulo,
                        'descricao': descricao,
                        'link_download': link_download,  # Link de download corrigido
                        'imagem_capa': imagem_capa  # Adiciona a imagem de capa
                    })

                    # Incrementar o contador de livros
                    contador_livros += 1

                    # Imprimir o número de livros coletados até o momento
                    print(f"Livros coletados: {contador_livros}")

                    # Se já tivermos coletado 100 livros, parar o processo
                    if contador_livros >= 100:
                        print("Limite de 100 livros alcançado.")
                        break
            if contador_livros >= 100:
                break

        # Salvar os dados no formato JSON
        with open('livros_autores.json', 'w', encoding='utf-8') as json_file:
            json.dump(dados, json_file, ensure_ascii=False, indent=4)

        print(f"Arquivo JSON 'livros_autores.json' criado com sucesso.")
    else:
        print(f"Erro ao acessar a página {url_autores}: {resposta.status_code}")

# Chama a função de scraping
if __name__ == "__main__":
    scraping_livros_autores()
