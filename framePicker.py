import av
import av.datasets
import os

def extractFrame(filename, seconds):

    # Inicializa os paths a serem utilizados
    videoPath = os.path.join('.', 'videos', filename)
    outputFolder = os.path.join('.', 'images')
    outputPath = os.path.join(outputFolder, filename.replace('.', '_'))

    # Cria o diretório de saída caso não exista
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    # Abre o video como uma stream
    with av.open(videoPath) as container:
        stream = container.streams.video[0]

        # Itera sobre os frames do video 
        # até encontrar o frame desejado
        for frame in container.decode(stream):   
            if frame.time >= seconds:
                break

        # Salva o frame desejado
        frame.to_image().save(
                    f'{outputPath}_{seconds}.jpg',
                    quality=80,
        )
            