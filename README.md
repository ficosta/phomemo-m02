# Phomemo M02 - Driver & CLI (Node.js & Python)

Driver nativo e utilitário de linha de comando para impressoras térmicas portáteis **Phomemo M02** (203 DPI, 384 pixels / 48 bytes por linha) no Windows via Bluetooth Serial (RFCOMM / ESC-POS).

Disponível tanto em **Node.js** quanto em **Python**!

---

## 🚀 Versão Node.js

### Instalação
```bash
npm install
```

### Uso via Linha de Comando (CLI)

```bash
# Imprimir texto
node phomemo.js text "Comprar café e pão" --title "Lista de Compras"

# Imprimir qualquer imagem (PNG, JPG, WebP)
node phomemo.js image setup_news_logo.png
```

### Uso como Biblioteca / Módulo Node.js

```javascript
const { PhomemoM02 } = require('./phomemo');

async function main() {
  const printer = new PhomemoM02();
  await printer.connect();

  // Imprime texto formatado com quebra automática
  await printer.printText('Olá mundo do Node.js!', { title: 'Aviso' });

  // Imprime imagem (caminho de arquivo ou Buffer)
  await printer.printImage('setup_news_logo.png');

  await printer.close();
}

main();
```

---

## 🐍 Versão Python

### Instalação
```bash
pip install -r requirements.txt
```

### Uso via Linha de Comando (CLI)

```bash
# Imprimir texto
python phomemo.py text "Seu texto aqui" --title "Título"

# Imprimir imagem
python phomemo.py image setup_news_logo.png

# Imprimir QR Code
python phomemo.py qr "https://setup.news" --caption "setup.news"

# Folha de calibração de tons de cinza e resolução
python calibration_test.py
```

### Uso como Biblioteca Python

```python
from phomemo import PhomemoM02

with PhomemoM02() as printer:
    printer.print_text("Olá do Python!", title="Notificação")
    printer.print_image("setup_news_logo.png")
```

---

## ⚙️ Conexão Bluetooth no Windows

1. Ligue a Phomemo M02 (botão power).
2. Vá em **Configurações do Windows > Bluetooth > Adicionar dispositivo** e pareie a impressora (`Mr.in_M02`).
3. O Windows cria automaticamente uma porta serial virtual (ex: `COM6`). Ambos os drivers detectam a porta automaticamente.

---

## 📄 Licença
MIT © Felipe Iasi
