# `metapyquod-server` Canned prototype search microservice using MeTA/metapy

[<img src="https://img.youtube.com/vi/CXgVN4fOjvk/0.jpg" data-canonical-src="https://img.youtube.com/vi/CXgVN4fOjvk/0.jpg" alt="metapyquod-indexer and metapyquod-server demo video" align="right" height="240" width="320">](https://youtu.be/CXgVN4fOjvk)

## Overview

This container implements a minimal but functional search service as a REST API, which can be used as a base for rapid prototyping of either a search portal web site or mobile app (or other client). It uses the MeTA toolkit and metapy bindings, so may be suitable for research or prototyping of new rankers or techniques via that library.

## Usage

### Prerequisites

You must have an index or corpus that can be used to build an index, with a `.toml` config file suitable for passing to `metapy.index.make_inverted_index(...)`. The index must include the following metadata fields:

```toml
metadata = [{name = "title", type = "string"},
    {name = "url", type = "string"},
    {name = "mtime", type = "uint"}]
```

Note: see [`metapyquod-indexer`](https://github.com/sphtkr/MeTAPyquod/metapyquod-indexer) which works together with [wget](https://www.gnu.org/software/wget/) to generate such an index.

### Running

Invoke the server providing the path to the index's `config.toml` file in the environment variable `METAPYQUOD_IDX_TOML`. The path should be the correct path *within the container*, so if a volume is used make sure those paths line up.

```sh
docker run --rm -v `pwd`:/var/idx -e METAPYQUOD_IDX_TOML=/var/idx/sample/config.toml -p 8080:8080 sphtkr/metapyquod-server
```

Also, note that the paths *inside* the `config.toml` file must be correct in reflecting the location within the *container*, not on the host. So in the example above, the `config.toml` looks like this:

```toml
prefix = "/var/idx/sample"
stop-words = "/var/idx/sample/lemur-stopwords.txt"
dataset = "sample"
corpus = "line.toml"
index = "/var/idx/sample/idx"
metadata = [{name = "title", type = "string"},
    {name = "url", type = "string"},
    {name = "mtime", type = "uint"}]

[[analyzers]]
method = "ngram-word"
ngram = 1
filter = "default-unigram-chain"
```

The server inside the container runs on port 8080, you can pass that through to the host on whatever port is desired using `-p`.

### API

The REST API can be explored via Swagger UI running on the server by going to `/ui` in a browser, e.g. [http://localhost:8080/ui](http://localhost:8080/ui/).

By way of overview, there are three main services:

* `/search` - GET or POST
    * Takes parameters for query, top, and skip (for pagination, e.g. top 10, skip 20 gives the third page of ten results)
    * Returns a doc_id, a URL, a title, and the ranker's score value for each result
* `/click` - GET
    * A "clickthrough" handler for gathering implicit feedback
    * Takes the query text and a doc_id from the `/search` service as input
    * Rather than returning JSON, this service returns a `304` status code with a `Location` header--therefore, you can direct users' browsers directly to this endpoint and they will be redirected to the destination, while still capturing the fact that the result was chosen.
        * Presently there is no action taken or information recorded by this service, but such logic can be easily added.
* `/telemetry/stats` - GET
    * No input parameters, returns the number of documents and number of unique terms in the index (can be used for instance to validate that a new index has been loaded)

### Trying out the service

In the Swagger UI interface, you can test the endpoints by expanding a service endpoint and clicking "Try It Out", and providing input values for the parameters to each service.

### Building a Client

Since the service has a OpenAPI (a.k.a. Swagger) definition file (available at `/openapi.json`, e.g. [http://localhost:8080/openapi.json](http://localhost:8080/openapi.json)), you can use [Swagger Codegen](https://swagger.io/tools/swagger-codegen/) or other tools to generate a client library for the service in a variety of different languages or environments.
    
## Limitations and Improvement Possibilities

### Multiple Indexes / Incremental Indexing

The initial goal for this service was to be able to serve in a minimal capacity for an intranet search service, or even as an "MVP" capability for a commercial service offering such as vertical search. However, a significant impediment to such a goal is the inability of MeTA indexes to be incrementally updated or merged--so a complete re-index is necessary on update, which may be very resource intensive. To mitigate this, `metapyquod-service` was architected to be able to support multiple indexes, querying all loaded indexes and merging the *results*--though this is not yet implemented. Presently, the only way to add information to the search service is to build a new index and restart the search service pointing to the new index (which will work, but is not ideal).

### Configurable Rankers

At present, the service creates a BM25 ranker using the default values from MeTA. It is actually possible to specify different `k1`, `b`, and `k3` parameters for the BM25 ranker by embedding a `[ranker]` configuration in the `config.toml` file, but there is not a way to choose a different ranking algorithm. MeTA makes it possible to instantiate an arbitrary ranker from the `config.toml`, but the function to read the parameters from the configuration is not exposed in the metapy Python bindings--and re-implementing it would have been feasible but non-trivial. It is of course possible to change the ranker by editing `engine.py`, and at this time that is the recommended method.

## Implementation
This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.  This
is an example of building a swagger-enabled Python application with Flask and [Connexion](https://github.com/zalando/connexion). 

