# Conversor de PDF para Áudio

Um aplicativo web que converte arquivos PDF em audiobooks usando síntese de voz de alta qualidade.

## 🎯 Funcionalidades

- Conversão de PDF para áudio usando Edge TTS
- Interface web amigável com Streamlit
- Múltiplas opções de voz em português
- Controle de velocidade da fala
- Opção de tradução automática
- Player de áudio integrado
- Download do arquivo de áudio
- Informações detalhadas do áudio gerado

## 🚀 Como Usar

1. Clone o repositório:
```bash
git clone https://github.com/PolicarpoDi/convert_pdf_in_audiobook.git
cd convert_pdf_in_audiobook
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run app.py
```

4. Acesse o aplicativo no navegador (geralmente em http://localhost:8501)

## ⚙️ Configurações

- **Voz**: Escolha entre diferentes vozes em português
- **Velocidade**: Ajuste a velocidade da fala (-50% a +50%)
- **Tamanho do Chunk**: Controle o tamanho dos segmentos de texto (100-500 caracteres)
- **Tradução**: Opção para traduzir automaticamente para português

## 🎵 Player de Áudio

O aplicativo inclui um player de áudio integrado com:
- Controle de play/pause
- Barra de progresso
- Controle de volume
- Exibição do tempo de reprodução

## 📁 Estrutura do Projeto

```
convert_pdf_in_audiobook/
├── app.py              # Interface web com Streamlit
├── listening_audio.py  # Lógica de conversão
├── requirements.txt    # Dependências do projeto
└── audios/            # Diretório para os áudios gerados
```

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Streamlit
- Edge TTS
- PyMuPDF (fitz)
- Deep Translator
- Pydub

## 📝 Licença

Este projeto está licenciado sob a GPL-3.0 - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

Policarpo

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request
