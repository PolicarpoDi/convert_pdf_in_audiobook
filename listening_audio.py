import asyncio
import os
import tempfile
import time
from typing import Optional

import fitz
from deep_translator import GoogleTranslator
from edge_tts import Communicate
from pydub import AudioSegment
from pydub.playback import play
from tqdm import tqdm
from tqdm.asyncio import tqdm as async_tqdm


class PDFToAudioConverter:
    def __init__(self, voice: str = "pt-BR-FranciscaNeural", rate: str = "+5%", chunk_size: int = 300):
        self.voice = voice
        self.rate = rate
        self.chunk_size = chunk_size
        print(
            f"🔧 Configurações: Voz={voice}, Velocidade={rate}, Tamanho do chunk={chunk_size}")

    async def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrai o texto de um PDF com barra de progresso."""
        text = ""
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"📄 Total de páginas encontradas: {total_pages}")

        with tqdm(total=total_pages, desc="Extraindo texto do PDF", unit="página") as pbar:
            for page in doc:
                text += page.get_text("text") + "\n"
                pbar.update(1)
        doc.close()
        print(f"📝 Total de caracteres extraídos: {len(text)}")
        return text.strip()

    async def translate_text(self, text: str, target_lang: str = 'pt-br') -> str:
        """Traduz o texto usando GoogleTranslator com barra de progresso."""
        translator = GoogleTranslator(source="auto", target=target_lang)
        chunks = [text[i:i+self.chunk_size]
                  for i in range(0, len(text), self.chunk_size)]
        print(f"🌍 Iniciando tradução de {len(chunks)} chunks")
        translated_chunks = []

        with tqdm(total=len(chunks), desc="Traduzindo texto", unit="chunk") as pbar:
            for chunk in chunks:
                translated_chunks.append(translator.translate(chunk))
                pbar.update(1)

        return " ".join(translated_chunks)

    async def text_to_speech(self, text: str, output_audio: str) -> None:
        """Converte texto em fala e salva como um arquivo de áudio com barra de progresso."""
        chunks = [text[i:i+self.chunk_size]
                  for i in range(0, len(text), self.chunk_size)]
        print(f"🎙️ Iniciando geração de áudio para {len(chunks)} chunks")
        temp_files = []

        try:
            with tqdm(total=len(chunks), desc="Gerando áudio", unit="chunk") as pbar:
                for i, chunk in enumerate(chunks):
                    temp_file = tempfile.NamedTemporaryFile(
                        delete=False, suffix='.mp3')
                    temp_files.append(temp_file.name)

                    tts = Communicate(chunk, voice=self.voice, rate=self.rate)
                    await tts.save(temp_file.name)
                    pbar.update(1)

            print("🔄 Combinando arquivos de áudio...")
            combined = AudioSegment.empty()
            for temp_file in temp_files:
                audio = AudioSegment.from_mp3(temp_file)
                combined += audio

            print(f"💾 Salvando arquivo final: {output_audio}")
            combined.export(output_audio, format="mp3")

            # Verificar se o arquivo foi criado e tem tamanho maior que 0
            if not os.path.exists(output_audio) or os.path.getsize(output_audio) == 0:
                raise Exception("Falha ao gerar o arquivo de áudio")

            print(
                f"✅ Áudio gerado com sucesso! Tamanho: {os.path.getsize(output_audio) / 1024:.2f} KB")

        except Exception as e:
            print(f"❌ Erro ao gerar áudio: {str(e)}")
            raise  # Re-lançar a exceção para tratamento adequado
        finally:
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass

    async def play_audio(self, file_path: str) -> None:
        """Reproduz o arquivo de áudio gerado."""
        try:
            print(f"🎧 Carregando áudio: {os.path.basename(file_path)}")
            audio = AudioSegment.from_file(file_path, format="mp3")
            print(f"⏱️ Duração do áudio: {len(audio) / 1000:.2f} segundos")
            play(audio)
        except Exception as e:
            print(f"❌ Erro ao reproduzir áudio: {str(e)}")

    async def process_pdf(self, pdf_path: str, translate: bool = False) -> None:
        """Processo completo com todas as etapas e barras de progresso."""
        try:
            print(
                f"📚 Iniciando processamento do arquivo: {os.path.basename(pdf_path)}")
            start_time = time.time()

            text = await self.extract_text_from_pdf(pdf_path)

            if not text:
                print("❌ Nenhum texto encontrado no PDF!")
                return

            if translate:
                text = await self.translate_text(text)

            # Criar diretório audios se não existir
            if not os.path.exists("audios"):
                os.makedirs("audios")

            # Salvar o áudio no diretório audios
            output_audio = os.path.join("audios", os.path.splitext(
                os.path.basename(pdf_path))[0] + ".mp3")

            print(
                f"🎯 Arquivo de áudio será salvo como: {os.path.basename(output_audio)}")

            await self.text_to_speech(text, output_audio)

            # Verificar se o arquivo foi criado com sucesso
            if not os.path.exists(output_audio):
                raise Exception("Arquivo de áudio não foi gerado corretamente")

            end_time = time.time()
            print(
                f"⏱️ Tempo total de processamento: {end_time - start_time:.2f} segundos")

        except Exception as e:
            print(f"❌ Erro durante o processamento: {str(e)}")
            raise  # Re-lançar a exceção para que a interface possa tratá-la
        finally:
            # Limpar arquivos temporários
            try:
                if 'temp_dir' in locals():
                    for file in os.listdir(temp_dir):
                        os.remove(os.path.join(temp_dir, file))
                    os.rmdir(temp_dir)
            except Exception as e:
                print(f"⚠️ Erro ao limpar arquivos temporários: {str(e)}")


async def main():
    converter = PDFToAudioConverter(chunk_size=300)
    pdf_file = "pdf/Quem sou eu.pdf"
    await converter.process_pdf(pdf_file, translate=False)


if __name__ == "__main__":
    asyncio.run(main())
