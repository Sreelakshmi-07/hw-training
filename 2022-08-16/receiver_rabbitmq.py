import pika

def on_message_received(ch, method, properties, body):
    print(f"received detailed page url: {body}")
    print()
  

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue='costplusdrugs')

channel.basic_consume(queue='costplusdrugs', auto_ack=True,
    on_message_callback=on_message_received)

print("Starting Consuming")

channel.start_consuming()
