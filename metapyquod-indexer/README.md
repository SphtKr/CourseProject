
## Using wget to Download content

```sh
wget --recursive -o ./log.txt \
     -R "*.jpg,*.jpeg,*.css,*.js,*.gif,*.png,*.pdf,*.tar,*.*z" \
     --domains "toscrape.com" --timestamping --timeout=5 --force-directories \
     --protocol-directories --directory-prefix=data \
     http://books.toscrape.com/ http://quotes.toscrape.com/
```

### Why are we doing this?

There is a valid question, "Why would we waste space by downloading the content and keeping it on disk, rather than just indexing it as we download and throwing it away immediately? Wouldn't that be more efficient?" The answer is, that might be a better answer, but this way has some advantages, mainly having to do with updating the index.
1. This automatically maintains timestamps of the files corresponding to the `Last-Modified` header sent by the server, and wget will use those timestamps to prevent re-downloading content if it has not changed, speeding the crawling process.
2. Given #1, if a document with links in it has not changed, therefore we do not re-download it, but we still have its HTML on disk from last time, we can still crawl its links even though we didn't re-download it--which we need to do to check if any of the linked content has changed.
3. If we have the content, we have the possibility of making that content available to a retrieval engine (such as [metapyquod-server](https://github.com/sphtkr/MeTAPyquod/metapyquod-server)) such that it could generate summaries of query results, perhaps extracting and presenting relevant sections of the content and highlighting query terms, as most search engines do.
