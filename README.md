# Phomemo M02 - Driver & CLI em Python

Driver nativo e utilitário de linha de comando para impressoras térmicas portáteis **Phomemo M02** no Windows, comunicando-se via Bluetooth (perfil Serial RFCOMM / ESC-POS).

## Características

* **Compatibilidade nativa:** Funciona diretamente via porta serial Bluetooth do Windows (ex: `COM6`).
* **Resolução nativa:** 203 DPI (384 dots de largura por linha, 48 bytes/linha).
* **Processamento de imagem inteligente:** Redimensionamento proporcional automático e dithering Floyd-Steinberg para ótima reprodução de tons em preto e branco.
* **Quebra de linha de texto automática:** Ajusta parágrafos e textos longos para a largura exata da fita térmica.
* **Suporte a QR Codes:** Gera e centraliza QR codes com legendas opcionais.
* **Cartão de calibração incluso:** Permite testar a uniformidade da queima térmica, escala de cinzas e resolução.

---

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/.../phomemo-m02.git
cd phomemo-m02
pip install -r requirements.txt
```

---

## Como usar via Linha de Comando (CLI)

### 1. Imprimir texto ou notas
```bash
python phomemo.py text "Comprar café, pão e leite." --title "Lista de Compras"
```
* Parâmetros opcionais:
  * `--title "Meu Título"`: Adiciona um cabeçalho destacado.
  * `--font-size 26`: Altera o tamanho da fonte (padrão: 22).

### 2. Imprimir imagens e fotos (PNG, JPG, BMP)
```bash
python phomemo.py image "caminho/para/imagem.png"
```

### 3. Imprimir QR Code
```bash
python phomemo.py qr "https://github.com" --caption "Acesse nosso site"
```

### 4. Executar folha de calibração
```bash
python calibration_test.py
```

---

## Como usar como biblioteca Python

```python
from phomemo import PhomemoM02

# Conecta automaticamente à porta da Phomemo (detectada via Bluetooth)
with PhomemoM02() as printer:
    # Imprime texto formatado
    printer.print_text("Olá mundo térmico!", title="Aviso")

    # Imprime um QR Code
    printer.print_qr("https://seusite.com", caption="Escaneie aqui")

    # Imprime uma imagem (arquivo no disco ou objeto PIL Image)
    printer.print_image("recibo.png")
```

---

## Configuração do Bluetooth no Windows

1. Ligue a Phomemo M02 (luz verde/azul acesa).
2. Vá em **Configurações do Windows > Dispositivos > Bluetooth**.
3. Adicione um novo dispositivo Bluetooth e selecione a impressora (`Mr.in_M02` ou `Phomemo`).
4. O Windows criará automaticamente uma porta serial virtual (ex: `COM6`). O script detecta essa porta automaticamente.
