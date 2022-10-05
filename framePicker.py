import av
import av.datasets
import os


# A classe Extractor é responsável pelas funções 
# estáticas responsáveis pela extração de frames
class Extractor:
    # Extrai o frame desejado de um vídeo e salva em um diretório
    def extractAndSaveFrame(filename: str, seconds: int, frame = None) -> str:
        # Inicializa os paths a serem utilizados
        outputFolder = os.path.join('.', 'images')
        outputPath = os.path.join(outputFolder, filename.replace('.', '_'))
        
        # Gera o nome do arquivo
        name = f'{outputPath}_{seconds}.jpg'
        
        # Cria o diretório de saída caso não exista
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        # Checa se o arquivo output já existe
        if os.path.exists(name):
            return name

        # Extrai o frame desejado caso ele não tenha sido passado
        frame = frame or Extractor.extractFrame(filename, seconds)

        # Salva o frame desejado
        frame.to_image().save(
                    name,
                    quality=80,
        )

        return name

    # Extrai o frame desejado de um vídeo
    def extractFrame(filename: str, seconds: int, video: av.VideoFormat = None) -> av.VideoFrame:

        # Inicializa o path a ser utilizado
        videoPath: str = os.path.join('.', 'videos', filename)

        # Checa se o video existe
        if not os.path.exists(videoPath) and video is None:
            print(f'Vídeo não encontrado: {videoPath}')
            raise Exception('Vídeo não encontrado')

        # Abre o arquivo de vídeo se necessário
        video = video or av.open(videoPath)

        # Abre o video como uma stream
        with video as container:
            stream: av.VideoFormat = container.streams.video[0]

            # Itera sobre os frames do video 
            # até encontrar o frame desejado
            for frame in container.decode(stream):   
                if frame.time >= seconds:
                    break

        return frame
            