# Conversor de livro em pdf para áudio.

# 📌 Funcionalidades

✅ **Extrai texto de um PDF** usando `PyMuPDF` (`fitz`).  
✅ **Opção de tradução** (ativada/desativada por flag) usando `deep_translator`.  
✅ **Gera áudio** com `edge_tts` e salva como `.mp3`.  
✅ **Reproduz o áudio automaticamente** usando `pydub`.  
✅ **Código assíncrono** para melhor desempenho.  

# 📌 Instale as dependências antes de rodar

```bash
pip install pymupdf deep-translator edge-tts pydub tqdm
```

⚠️ O pydub requer FFmpeg instalado no sistema. Instale via:

Windows: [Baixar FFmpeg](https://ffmpeg.org/download.html)

Linux:
```bash
sudo apt install ffmpeg
```

# 📌 Como Usar

1️⃣ **Crie a pasta "PDF" na raiz do projeto e coloque seu PDF desejado.**  
2️⃣ **Defina a variável `pdf_file`** com o diretório do seu arquivo PDF.  
3️⃣ **Escolha se quer traduzir para português:**

- `translate=True` → Traduz o texto antes da leitura.  
- `translate=False` → Mantém o texto original.  

4️⃣ **Execute o script:**

```bash
python script.py
