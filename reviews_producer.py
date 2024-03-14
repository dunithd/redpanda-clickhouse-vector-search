import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

def load_reviews(path):
    f = open(path)
    reviews = json.load(f)

    review_objects = list()
    for review in reviews:
        review_objects.append(review)
        # print(review['review'])

    f.close()
    return review_objects

# Load reviews from the JSON file
reviews = load_reviews('./data/reviews.json')

# Connects to Redpanda cloud with SASL credentials and produces JSON-formatted events.
producer = KafkaProducer(
  bootstrap_servers="cnkan84tluj4mbfiavk0.any.eu-central-1.mpx.prd.cloud.redpanda.com:9092",
  security_protocol="SASL_SSL",
  sasl_mechanism="SCRAM-SHA-256",
  sasl_plain_username="",
  sasl_plain_password="",
  value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "reviews"

# Hydrate the topics with our fake reviews. It's ugly. But let's get on with it.
for review in reviews:
    producer.send(topic, value=review)

print("Produced {count} messages to Redpanda topic: {topic}".format(count=len(reviews), topic=topic))

# Close the Kafka producer
producer.close()
