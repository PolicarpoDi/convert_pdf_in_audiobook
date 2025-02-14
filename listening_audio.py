import asyncio
import os
import time

import fitz
from deep_translator import GoogleTranslator
from edge_tts import Communicate
from pydub import AudioSegment
from pydub.playback import play
from tqdm.asyncio import tqdm


async def extract_text_from_pdf(pdf_path):
    """Extrai o texto de um PDF."""
    text=""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()

async def translate_text(text, target_lang = 'pt-br'):
    """Traduz o texto usando GoogleTranslator"""
    return GoogleTranslator(source="auto", target=target_lang).translate(text)

async def text_to_speech(text, output_audio, voice="pt-BR-FranciscaNeural", rate="+5%"):
    """Converte texto em fala e salva como um arquivo de áudio."""
    
    # Inicializa o processo de conversão de texto para fala
    tts = Communicate(text, voice=voice, rate=rate)
    await tts.save(output_audio)
    print("✅ Áudio gerado com sucesso!")
    
async def play_audio(file_path):
    """Reproduz o arquivo de áudio gerado."""
    audio = AudioSegment.from_file(file_path, format="mp3")
    play(audio)
    
async def main(pdf_path, translate = False):
    """Processo completo: Extrai texto, traduz (se ativado), gera e reproduz áudio."""
    print("📥 Extraindo texto do PDF...")
    text = await extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ Nenhum texto encontrado no PDF!")
        return
    
    if translate:
        print("🌍 Traduzindo texto para português...")
        text = await translate_text(text)
        
    # Obter o nome do arquivo PDF sem a extensão .pdf
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    
    print(base_filename)
    
    # Definir o nome do arquivo de áudio
    output_audio = f"{base_filename}.mp3"
    
    print(f"🎧 O áudio será salvo como: {output_audio}")
        
    print("⏳ Gerando áudio...")
    task = text_to_speech(text, output_audio)
    
    with tqdm(total=1, desc="Processando", position=0, leave=True) as pbar:
        await task
        pbar.update(1)
    
    print("🎧 Reproduzindo áudio...")
    await play_audio(output_audio)
    
if __name__ == "__main__":
    pdf_file = "pdf/Quem sou eu.pdf"
    #pdf_file = "PDF/A Sutil Arte de Ligar o Foda-se - Mark Manson.pdf"
    asyncio.run(main(pdf_file, translate=False))
