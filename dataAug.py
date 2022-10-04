import cv2
import numpy as np
import os
import imutils


def dataAug(imagePath: str, filtersStr: str):

    # Inicializa os paths a serem utilizados
    outputPath = imagePath.replace('images', 'output', 1)
    outputPath = outputPath.replace('.jpg', f'_{filtersStr}', 1)

    # Verifica se a pasta output existe
    # Se não existir, cria a pasta
    if not os.path.exists('output'):
        os.makedirs('output')

    # Cria a lista de filtros a serem aplicados
    filters: list[str] = filtersStr.split('|')

    # Carrega a imagem
    image: cv2.Mat = cv2.imread(imagePath)

    # Aplica o filtro de ruido
    if 'random_noise' in filters:
        # cria uma matriz de zeros do mesmo tamanho de 
        # uma camada da imagem
        noise = np.zeros((image.shape[0], image.shape[1]), 
            dtype=np.uint8)
        
        # Preenche a matriz com valores aleatórios
        cv2.randn(noise, 0, 40)

        # Converte o tipo da matriz para matriz de inteiros uint8
        noise = noise.astype(np.uint8)

        # Percorre os canais da imagem adicionando ruido
        for i in range(image.shape[2]):
            image[:, :, i] = cv2.add(image[:, :, i], noise)
    
    # Aplica o filtro flip que inverte a imagem horizontalmente
    if 'flip' in filters:
        image = cv2.flip(image, 1)

    # Aplica o filtro que rotaciona a imagem
    if 'random_rotation' in filters:
        # Gera um angulo aleatório entre 0 e 360
        angle = np.random.randint(0, 360)
        # Rotaciona a imagem
        image = imutils.rotate_bound(image, angle)
    
    # Aplica o filtro que transforma a imagem em escala de cinza
    if 'greyscale' in filters:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Salva a imagem desejada
    cv2.imwrite(f'{outputPath}.jpg', image)


# dataAug('images/video_1_mp4_60.jpg', 'random_noise|greyscale|flip|random_rotation')
