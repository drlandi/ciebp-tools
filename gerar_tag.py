import qrcode
from PIL import Image, ImageDraw, ImageFont

# 1. OS SEUS DADOS (Pode alterar como quiser nas próximas!)
URL = "https://drlandi.github.io/ciebp-tools/"
TITULO = "CIEBP Zuleika"
PERGUNTA = "Leia-me!"
FERRAMENTA = "Jogo de Chaves Combinadas"
SAIDA = "tag_impressao.png"

print("🎨 Desenhando a Tag Física...")

# 2. CRIAR O PAPEL DA TAG (600x1000 pixels - Formato Vertical)
tag = Image.new('RGB', (600, 1000), color='white')
draw = ImageDraw.Draw(tag)

# Desenhar uma borda preta grossa para ajudar na hora de cortar
draw.rectangle([(5, 5), (595, 995)], outline="black", width=5)

# Desenhar o furo para o "engasga gato" no topo
draw.ellipse([(270, 30), (330, 90)], outline="black", width=4)
draw.text((250, 100), "(Furo P/ Lacre)", fill="black") # Texto simples

# 3. GERAR O SUPER QR CODE
print("🔗 Gerando QR Code Nível H...")
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=15, border=2)
qr.add_data(URL)
qr.make(fit=True)
img_qr = qr.make_image(fill_color="black", back_color="white")

# Redimensionar para ficar GIGANTE (480x480)
img_qr = img_qr.resize((480, 480))

# 4. TENTAR CARREGAR FONTES DO LINUX (Ubuntu)
try:
    font_titulo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
    font_perg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    font_ferr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 35)
except IOError:
    # Se não achar a fonte, usa a padrão
    font_titulo = ImageFont.load_default()
    font_perg = ImageFont.load_default()
    font_ferr = ImageFont.load_default()

# 5. ESCREVER OS TEXTOS NA TAG
print("✍️ Escrevendo informações...")
draw.text((60, 150), TITULO, fill="black", font=font_titulo)
draw.text((100, 220), PERGUNTA, fill="#d32f2f", font=font_perg) # Pergunta em tom avermelhado
draw.text((40, 850), FERRAMENTA, fill="black", font=font_ferr)

# 6. COLAR O QR CODE NO MEIO DA TAG
# (Largura da tag 600 - Largura QR 480) / 2 = Posicionamento X no 60
tag.paste(img_qr, (60, 320))

# 7. SALVAR
tag.save(SAIDA)
print(f"✅ SUCESSO! Abra o arquivo '{SAIDA}' e mande para a impressora!")
