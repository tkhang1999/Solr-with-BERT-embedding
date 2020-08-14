# Solr with BERT Embedding

## Introduction

This simple code implementation describes how to incorporate BERT embedding to Solr search engine
to achieve semantic search in Solr on a food reviews dataset

## Technologies
* [Python 3.6/3.7](https://www.python.org/)
* [BERT](https://github.com/google-research/bert)
* [Sentence Transformers](https://github.com/UKPLab/sentence-transformers)
* [Solr](https://lucene.apache.org/solr/)

## How to Run?

1. Install all dependecies
```
$ pip install -r requirements.txt
```

2. Set up Solr

* Install `Java 8`

* Download `solr-6.6.6` from [here](https://archive.apache.org/dist/lucene/solr/6.6.6/) or by running the following commands
```
$ curl -LO https://archive.apache.org/dist/lucene/solr/6.6.6/solr-6.6.6.tgz
$ mkdir solr-6.6.6
$ tar -C solr-6.6.6 -xf solr-6.6.6.tgz --strip-components=1
```

* After unzip the folder, create core `bert`
```
$ cd solr-6.6.6
$ ./bin/solr start                                    # start solr
$ ./bin/solr create -c bert -n basic_config           # create core named 'bert'
```

* Add [Vector Scoring Plugin for Solr](https://github.com/saaay71/solr-vector-scoring) (you may follow the setup guide from this repository) as following steps

i. Stop the running `solr` server
```
$ cd solr-6.6.6
$ ./bin/solr stop -all                                    # stop solr
```

ii. Download [VectorPlugin.jar](https://github.com/saaay71/solr-vector-scoring/blob/master/VectorPlugin.jar)

iii. Copy `VectorPlugin.jar` to `solr-6.6.6/dist/plugins/` (Create the `plugins` folder if not exist)

iv. Add the library to `solr-6.6.6/server/solr/bert/conf/solrconfig.xml` file:
```
<lib dir="${solr.install.dir:../../../..}/dist/plugins/" regex=".*\.jar" />
```

v. Add the plugin Query parser to `solr-6.6.6/server/solr/bert/conf/solrconfig.xml` file:
```
<queryParser name="vp" class="com.github.saaay71.solr.VectorQParserPlugin" />
```

vi. Add the fieldType `VectorField` to schema file `solr-6.6.6/server/solr/bert/conf/managed-schema`
```
  <fieldType name="VectorField" class="solr.TextField" indexed="true" termOffsets="true" stored="true" termPayloads="true" termPositions="true" termVectors="true" storeOffsetsWithPositions="true">
    <analyzer>
      <tokenizer class="solr.WhitespaceTokenizerFactory"/>
      <filter class="solr.DelimitedPayloadTokenFilterFactory" encoder="float"/>
    </analyzer>
  </fieldType>
```

vii. Add the field vector to schema file `solr-6.6.6/server/solr/bert/conf/managed-schema`:
```
<field name="vector" type="VectorField" indexed="true" termOffsets="true" stored="true" termPositions="true" termVectors="true" multiValued="true"/>
```

viii. Restart `solr` server
```
$ ./bin/solr start                                    # start solr
```

3. Add data to Solr

* Make sure that the Solr server is up and running at `localhost:8983`

* Run the file `add_BERT_embedding_to_Solr.py` to add BERT embedding from reviews data to Solr
```
$ python add_BERT_embedding_to_Solr.py
```

4. Make a search query

* Run the file `semantic_search.py` to make a sample semantic search
```
$ python semantic_search.py
```

* Sample result
```
Query:  delicious food

Top 15 semantic search results:
The food is delicious (Score: 0.9542)
Amazing tasting food! (Score: 0.9107)
Good service and tasty food. (Score: 0.9063)
Love the food. (Score: 0.8862)
Food was great... (Score: 0.8800)
Good food overall! (Score: 0.8743)
A delightful meal :) (Score: 0.8682)
Good service and location, food is great too! (Score: 0.8670)
Fun atmosphere, delicious food, good prices. (Score: 0.8657)
Cozy place with great food!! (Score: 0.8642)
Many lovely food to try :) (Score: 0.8596)
Huge menu, excellent and friendly service. Yummy food. (Score: 0.8596)
Great place with perfect food and service! (Score: 0.8542)
Good food, convenient place, great prices (Score: 0.8434)
A little pricey, but very good food and atmosphere. (Score: 0.8430)
```
