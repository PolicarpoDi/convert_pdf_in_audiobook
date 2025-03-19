# Conversor de PDF para Audiobook

Um conversor de PDF para áudio que utiliza tecnologias modernas para criar audiobooks de alta qualidade a partir de arquivos PDF.

## 📌 Funcionalidades

✅ **Extrai texto de um PDF** usando `PyMuPDF` (`fitz`)  
✅ **Opção de tradução** (ativada/desativada por flag) usando `deep_translator`  
✅ **Gera áudio** com `edge-tts` e salva como `.mp3`  
✅ **Reproduz o áudio automaticamente** usando `pydub`  
✅ **Código assíncrono** para melhor desempenho  
✅ **Barras de progresso** para acompanhamento em tempo real  
✅ **Processamento em chunks** para melhor performance  
✅ **Informações detalhadas** sobre o processo de conversão  
✅ **Interface web amigável** com Streamlit  
✅ **Player de áudio integrado**  
✅ **Download do áudio gerado**

## 📌 Requisitos

### Dependências Python
```bash
pip install pymupdf deep-translator edge-tts pydub tqdm streamlit
```

### FFmpeg
O pydub requer FFmpeg instalado no sistema:

**Windows:**
- Baixe o FFmpeg do [site oficial](https://ffmpeg.org/download.html)
- Adicione ao PATH do sistema

**Linux:**
```bash
sudo apt install ffmpeg
```

## 📌 Como Usar

### Interface Web (Recomendado)

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Execute a aplicação web:**
```bash
streamlit run app.py
```

3. **Acesse a interface:**
- Abra seu navegador
- Acesse http://localhost:8501

4. **Use a interface:**
- Faça upload do arquivo PDF
- Configure as opções desejadas na barra lateral:
  - Voz para narração
  - Velocidade da fala
  - Tamanho do chunk
  - Opção de tradução
- Clique em "Converter PDF para Áudio"
- Aguarde o processamento
- Ouça o áudio diretamente no navegador
- Faça download do arquivo MP3

### Linha de Comando

Se preferir usar via linha de comando:

```python
from listening_audio import PDFToAudioConverter

converter = PDFToAudioConverter(
    voice="pt-BR-FranciscaNeural",  # Voz para narração
    rate="+5%",                      # Velocidade da fala
    chunk_size=300                   # Tamanho do chunk para processamento
)

# Converter sem tradução
await converter.process_pdf("seu_arquivo.pdf", translate=False)

# Converter com tradução
await converter.process_pdf("seu_arquivo.pdf", translate=True)
```

## 📊 Informações de Processamento

O conversor fornece informações detalhadas durante o processo:

- Total de páginas encontradas
- Quantidade de caracteres extraídos
- Número de chunks processados
- Tamanho do arquivo de áudio gerado
- Duração do áudio
- Tempo total de processamento

## 🚀 Performance

O código foi otimizado para melhor performance através de:

- Processamento assíncrono
- Chunks menores para processamento
- Gerenciamento eficiente de memória
- Limpeza automática de arquivos temporários

## 📝 Licença

Este projeto está licenciado sob a licença GPL-3.0 - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request
