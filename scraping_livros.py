import os
import json
import requests
import re
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# ========== CONFIGURAÇÃO API GEMINI ==========
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# ========== CLASSIFICAÇÃO DE SENTIMENTOS ==========
def classificar_sentimentos(titulo, descricao):
    prompt = f"""
Classifique esse livro em até 3 sentimentos baseando-se no título e descrição. Os sentimentos podem incluir:
- Felicidade → livros interessantes
- Raiva → livros de terapias alternativas
- Paixão → livros de romance
- Tristeza → livros de superação pessoal
Você pode inventar novos sentimentos se fizer sentido com o conteúdo.

Título: {titulo}
Descrição: {descricao}

Responda apenas com uma lista JSON:
["sent1", "sent2", "sent3"]
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    while True:
        try:
            response = requests.post(GEMINI_API_URL, json=payload, headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                data = response.json()
                gemini_text = data["candidates"][0]["content"]["parts"][0]["text"]
                gemini_text = gemini_text.replace("```json", "").replace("```", "").strip()
                match = re.search(r"\[(.*?)\]", gemini_text, re.DOTALL)
                if match:
                    return json.loads("[" + match.group(1).strip() + "]")
                else:
                    return []

            elif response.status_code == 429:
                data = response.json()
                retry_delay = 60  # valor padrão
                try:
                    retry_str = data['error']['details'][-1]['retryDelay']
                    retry_delay = int(retry_str.replace('s', '').strip())
                except Exception:
                    pass
                print(f"⚠️ Limite excedido. Aguardando {retry_delay}s...")
                time.sleep(retry_delay)

            else:
                print(f"Erro Gemini: {response.status_code} - {response.text}")
                return []

        except Exception as e:
            print(f"Erro ao classificar '{titulo}': {e}")
            return []

# ========== FUNÇÕES DE SCRAPING ==========
def corrigir_link(link):
    return link.replace(" ", "%20").replace("%28", "(").replace("%29", ")")

def corrigir_nome(nome):
    return re.sub(r"^\#\d+\s", "", nome).strip()

def pegar_imagem(imagem_tag):
    if imagem_tag:
        imagem_url = imagem_tag.get('data-src') or imagem_tag.get('src')
        if imagem_url and imagem_url.startswith("/"):
            imagem_url = "https://www.infolivros.org" + imagem_url
        return corrigir_link(imagem_url) if imagem_url else None
    return None

def scrape_livros(url):
    livros = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    livros_na_pagina = soup.find_all('div', class_='gb-loop-item caja-pdfs caja-pdfs-nuevo')

    for livro in livros_na_pagina:
        try:
            titulo_tag = livro.find('h3', class_='gb-text titulo-caja-pdfs')
            descricao_tags = livro.find_all('p', class_='gb-text descripcion-caja-pdfs')
            link_download_tag = livro.find('a', class_='gb-text boton-descarga-caja-pdfs')
            imagem_tag = livro.find('img')

            if titulo_tag and descricao_tags and link_download_tag and imagem_tag:
                titulo = corrigir_nome(titulo_tag.text.strip())
                descricao = descricao_tags[1].text.strip() if len(descricao_tags) > 1 else ''
                link_download = corrigir_link(link_download_tag['href'])
                imagem_capa = pegar_imagem(imagem_tag)

                livros.append({
                    'titulo': titulo,
                    'descricao': descricao,
                    'link_download': link_download,
                    'imagem_capa': imagem_capa
                })
        except Exception as e:
            print(f"Erro ao processar livro: {e}")

    return livros

# ========== EXECUÇÃO COMPLETA ==========
if __name__ == "__main__":
    urls = [
        "https://www.infolivros.org/livros-pdf-gratis/terapia-alternativa/meditacao/",
        "https://www.infolivros.org/livros-pdf-gratis/terapia-alternativa/ioga/",
        "https://www.infolivros.org/livros-pdf-gratis/superacao-pessoal/auto-estima/",
        "https://www.infolivros.org/livros-pdf-gratis/superacao-pessoal/inteligencia-emocional/",
        "https://www.infolivros.org/livros-pdf-gratis/superacao-pessoal/reflexao/",
        "https://www.infolivros.org/livros-pdf-gratis/arte/fotografia/",
        "https://www.infolivros.org/livros-pdf-gratis/temas-varios/astronomia/",
        "https://www.infolivros.org/livros-pdf-gratis/amor/amor-de-verao/",
        "https://www.infolivros.org/livros-pdf-gratis/amor/romance/"
    ]

    todos_livros = []

    for url in urls:
        print(f"🔎 Scraping: {url}")
        livros = scrape_livros(url)
        for livro in livros:
            titulo = livro['titulo']
            descricao = livro['descricao']
            print(f"💬 Classificando sentimentos: {titulo}")
            sentimentos = classificar_sentimentos(titulo, descricao)
            livro['sentimentos'] = sentimentos
            time.sleep(1.5)  # Pausa entre chamadas para evitar rate limit
        todos_livros.extend(livros)

    with open("livros_com_sentimentos.json", "w", encoding="utf-8") as f:
        json.dump({"livros": todos_livros}, f, ensure_ascii=False, indent=4)

    print("✅ Arquivo 'livros_com_sentimentos.json' salvo com sucesso.")
