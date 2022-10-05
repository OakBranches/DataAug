import json
import pika
import re
from dataAug import Augmentation
from framePicker import Extractor

class Consumer:

    def __init__(self) -> None:
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.basic_consume('payload', self.on_message)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()

    def on_message(self, channel, method_frame, header_frame, body):
        video_ref, op_type, frame_seconds_index = None, None, None

        try:
            message = json.loads(body)

            # Pega os dados da mensagem
            video_ref = message['video_ref']
            op_type = message['op_type']
            frame_seconds_index = message['frame_seconds_index']

            # Valida os dados da mensagem
            self.validate_op_type(op_type)
            try:
                framePath = Extractor.extractAndSaveFrame(video_ref, frame_seconds_index)
                try:
                    augImagePath = Augmentation.dataAugAndSave(framePath, op_type)
                except:
                    print('Erro ao aplicar as operações de data augmentation')
            except:
                print('Erro ao extrair o frame')
        except:
            print('Mensagem inválida')
        
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def validate_op_type(self, op_type):
        pattern = r"^(noise|grayscale|flip|random_rotation)(\|(noise|grayscale|flip|random_rotation))*$"
        
        if not bool(re.match(pattern, op_type)):
            print(f'op_type inválido: {op_type}')
            raise Exception('Invalid op_type')

if __name__ == '__main__':
    Consumer()