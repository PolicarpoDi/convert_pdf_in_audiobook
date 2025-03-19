import asyncio
import os
import tempfile

import streamlit as st
from pydub import AudioSegment

from listening_audio import PDFToAudioConverter

# Configuração da página
st.set_page_config(
    page_title="Conversor de PDF para Áudio",
    page_icon="🎧",
    layout="wide"
)

# Título e descrição
st.title("🎧 Conversor de PDF para Áudio")
st.markdown("""
    Converta seus arquivos PDF em audiobooks de alta qualidade.
    Basta fazer upload do arquivo PDF e escolher as configurações desejadas.
""")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")

    # Seleção de voz
    voice = st.selectbox(
        "Voz para narração",
        ["pt-BR-FranciscaNeural", "pt-BR-AntonioNeural", "pt-BR-ValerioNeural"],
        index=0
    )

    # Velocidade da fala
    rate = st.slider(
        "Velocidade da fala",
        min_value="-50%",
        max_value="+50%",
        value="+5%",
        step="5%"
    )

    # Tamanho do chunk
    chunk_size = st.slider(
        "Tamanho do chunk",
        min_value=100,
        max_value=500,
        value=300,
        step=50
    )

    # Opção de tradução
    translate = st.checkbox("Traduzir para português", value=False)

    st.markdown("---")
    st.markdown("""
        ### ℹ️ Sobre
        Este aplicativo utiliza:
        - Edge TTS para síntese de voz
        - PyMuPDF para extração de texto
        - Deep Translator para tradução
    """)

# Área principal
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

if uploaded_file is not None:
    # Criar diretório temporário para o PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        pdf_path = tmp_file.name

    # Criar diretório para os áudios se não existir
    if not os.path.exists("audios"):
        os.makedirs("audios")

    # Nome do arquivo de áudio
    base_filename = os.path.splitext(uploaded_file.name)[0]
    output_audio = f"audios/{base_filename}.mp3"

    # Botão para converter
    if st.button("🔄 Converter PDF para Áudio"):
        try:
            with st.spinner("Processando..."):
                # Criar conversor com as configurações selecionadas
                converter = PDFToAudioConverter(
                    voice=voice,
                    rate=rate,
                    chunk_size=chunk_size
                )

                # Processar o PDF
                asyncio.run(converter.process_pdf(
                    pdf_path, translate=translate))

                st.success("✅ Conversão concluída com sucesso!")

                # Verificar se o arquivo de áudio foi criado
                if os.path.exists(output_audio):
                    # Carregar o áudio
                    audio = AudioSegment.from_file(output_audio)

                    # Exibir informações do áudio
                    st.info(f"""
                        📊 Informações do áudio:
                        - Duração: {len(audio) / 1000:.2f} segundos
                        - Tamanho: {os.path.getsize(output_audio) / 1024:.2f} KB
                    """)

                    # Player de áudio
                    st.audio(output_audio)

                    # Botão para download
                    with open(output_audio, "rb") as file:
                        st.download_button(
                            label="📥 Download do áudio",
                            data=file,
                            file_name=f"{base_filename}.mp3",
                            mime="audio/mp3"
                        )
                else:
                    st.error("❌ Erro ao gerar o arquivo de áudio")

        except Exception as e:
            st.error(f"❌ Erro durante o processamento: {str(e)}")

        finally:
            # Limpar arquivo temporário
            try:
                os.unlink(pdf_path)
            except:
                pass

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Desenvolvido com ❤️ por Policarpo</p>
        <p>Licenciado sob GPL-3.0</p>
    </div>
""", unsafe_allow_html=True)
