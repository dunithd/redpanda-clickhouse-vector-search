# Real-time Brand Sentiment Analysis with ClickHouse and Redpanda

This repo contains the source code for the brand sentiment analysis demo.


Steps:

* Write reviews on a Redpanda topic
* Store reviews + embeddings in CH
* Do sentiment analysis + similarity search on reviews
* $$$$

Connect to ClickHouse Server

```bash
./clickhouse client --host ${CH_HOST} --secure --password ${CH_PASSWORD} -m
```