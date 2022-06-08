import argparse
import cv2
import pandas as pd

# Criando cominho para imagem no prompt de comando
parser = argparse.ArgumentParser(description='Detector de cores')
parser.add_argument('-i', '--Imagem', help='imagem caminho')
args = vars(parser.parse_args())
img_path = args['Imagem']

# Lendo a imagem com opencv (não aparece na tela)
img = cv2.imread(img_path)

data = pd.read_csv('colors.csv', names=['color', 'nome_cores', 'hex', 'R', 'G', 'B'])

# Precisa criar as variaveis antes da função
clicked = None
xpos = None
ypos = None
b = None
g = None
r = None

# Função para retornar os valores de R G B
def retorno_clique(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global r, g, b, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Nome da janela que será aberta
cv2.namedWindow('Imagem')

# Função para reagir ao um evento (duplo clique na imagem)
cv2.setMouseCallback('Imagem', retorno_clique)  # primeiro parametro tem que ser igual ao nome da janela

# Função para pegar o nome da cor
def getcolorname(r, g, b):
    minimo = 10000  # valor alto para se comparar na formula embaixo
    for i in range(len(data)):
        # somatorio da diferença do valor do rgb achado na imagem com os valores registrados no dataset
        soma_rgb = abs(r - int(data.loc[i, "R"])) + abs(g - int(data.loc[i, 'G'])) + abs(b - int(data.loc[i, 'B']))
        if (soma_rgb <= minimo):
            minimo = soma_rgb
            nome_cor = data.loc[i, 'nome_cores']

    return nome_cor

while 1:
    cv2.imshow('Imagem', img)
    if clicked:
        # criação de um retangulo prenchido pela cor clicada
        # parametros: imagem, inicio e fim do retangulo, cor, preencher o triangulo
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # texto que vai sobrepor o retangulo
        # nome da cor e valores dos R G B
        texto = getcolorname(r, g, b) + 'R=' + str(r) + 'G=' + str(g) + 'B=' + str(b)

        # Sobrepondo o texto no retangulo
        # parametros: imagem, texto, inicio, font(0-7), escala da fonte, cor, brilho, tipo de linha
        cv2.putText(img, texto, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        if r + g + b >= 400:
            # Condição para caso o brilho da cor seja alta alterar a colaração do texto para preto
            cv2.putText(img, texto, (50, 50), 2, 0.8, [0, 0, 0], 2, cv2.LINE_AA)

        clicked = False

    # Condiçao para se fechar a imagem aberta
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()