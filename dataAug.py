import cv2
import numpy as np
import os
import imutils

# A classe Augmentation é responsável pelas funções 
# estáticas responsáveis pelo data aug
class Augmentation:
    # Aplica um filtro em uma imagem
    def applyFilter(image: np.ndarray, filter: str) -> np.ndarray:
        # Aplica o filtro de ruido
        if filter == 'noise':
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
        elif filter == 'flip':
            image = cv2.flip(image, 1)

        # Aplica o filtro que rotaciona a imagem
        elif filter == 'random_rotation':
            # Gera um angulo aleatório entre 0 e 360
            angle = np.random.randint(0, 360)
            # Rotaciona a imagem
            image = imutils.rotate_bound(image, angle)
        
        # Aplica o filtro que transforma a imagem em escala de cinza
        elif filter == 'grayscale':
            # Converte a imagem para um canal de cor
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Converte de volta para 3 canais de cor
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        return image

    # Aplica todos os filtros em uma imagem
    def applyAllFilters(image: np.ndarray, filtersStr: str) -> np.ndarray:
        # Cria a lista de filtros a serem aplicados
        filters: list[str] = filtersStr.split('|')

        # Aplica os filtros na imagem
        for filter in filters:
            image = Augmentation.applyFilter(image, filter)

        return image
  
    # Carrega, aplica os filtros e salva, retorna o nome do arquivo
    def dataAugAndSave(imagePath: str, filtersStr: str, imageSrc: np.ndarray = None) -> str:
        # Carrega a imagem se não tiver sido passada como parâmetro
        imageSrc: imageSrc or cv2.Mat = cv2.imread(imagePath)

        # Aplica os filtros na imagem
        image = Augmentation.applyAllFilters(imageSrc, filtersStr)

        # Inicializa os paths a serem utilizados
        outputPath = imagePath.replace('images', 'output', 1)
        outputPath = outputPath.replace('.jpg', f'_{filtersStr}', 1)

        # Verifica se a pasta output existe
        # Se não existir, cria a pasta
        if not os.path.exists('output'):
            os.makedirs('output')

        # Cria o nome do arquivo
        nome = f'{outputPath}.jpg'

        # Salva a imagem desejada
        cv2.imwrite(nome, image)

        return nome


# Augmentation.dataAugAndSave('images/video_1_mp4_60.jpg', 'random_noise|greyscale|flip|random_rotation')
