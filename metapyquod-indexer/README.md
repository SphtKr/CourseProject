# `metapyquod-indexer` - Easily prepare MeTA indexes with wget

This tool makes it relatively easy to create a MeTA index from a web site by using [wget](https://www.gnu.org/software/wget/)'s recursive retrieval features. It will create an index with metadata fields capturing:
* The (reconstructed) original URL of the retrieved page
* The title of the page (if HTML, parsed with Beautiful Soup 4)
* The `Last-Modified` header value reported for the page (captured by wget in the file `mtime`)

## Using wget to Download content

Example: 

```sh
wget --recursive -o ./log.txt \
     -R "*.jpg,*.jpeg,*.css,*.js,*.gif,*.png,*.pdf,*.tar,*.*z" \
     --domains "toscrape.com" --timestamping --timeout=5 --force-directories \
     --protocol-directories --directory-prefix=data \
     http://books.toscrape.com/ http://quotes.toscrape.com/
```

This will create a directory structure similar to the following:

```
./data
└── http
    ├── books.toscrape.com
    │   ├── catalogue
    │   │   ├── 10-day-green-smoothie-cleanse-lose-up-to-15-pounds-in-10-days_581
    │   │   │   └── index.html
    │   │   ├── 10-happier-how-i-tamed-the-voice-in-my-head-reduced-stress-without-losing-my-edge-and-found-self-help-that-actually-works_582
    │   │   │   └── index.html
    .   .   . 
    .   .   . 
    .   .   . 
```
`metapyquod-indexer` uses this retrieved directory structure to create an index.

### Do I have to use wget?

Of course not. Any off-the-shelf or bespoke tool that creates the same directory structure can be used to produce the mirror file structure. Do note that `metapyquod-indexer` will pick up the `mtime` from the files on disk and record it in the index metadata--so if your alternative tool doesn't store the `Last-Modified` header in the `mtime` of the file, then you will lose that information in the metadata.

### Why are we even doing this?

There is a valid question, "Why would we waste space by downloading the content and keeping it on disk, rather than just indexing it as we download and throwing it away immediately? Wouldn't that be more efficient?" The answer is, that might be a better answer, but this way has some advantages, mainly having to do with updating the index:
1. This automatically maintains timestamps of the files corresponding to the `Last-Modified` header sent by the server, and wget will use those timestamps to prevent re-downloading content if it has not changed, speeding the crawling process.
2. Given #1, if a document with links in it has not changed, therefore we do not re-download it, but we still have its HTML on disk from last time, we can still crawl its links even though we didn't re-download it--which we need to do to check if any of the linked content has changed.
3. If we have the content, we have the possibility of making that content available to a retrieval engine (such as [metapyquod-server](https://github.com/sphtkr/MeTAPyquod/metapyquod-server)) such that it could generate summaries of query results, perhaps extracting and presenting relevant sections of the content and highlighting query terms, as most search engines do.

## Usage

```
#> docker run metapyquod-indexer --help
usage: metapyquod-indexer [OPTION]

Build MeTA indexes from wget mirrors.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -m MIRRORPATH, --mirrorpath MIRRORPATH
                        The path where the root of the mirror is stored.
                        Should contain protocol directories like "http" and
                        "https". Defaults to "/var/mirror".
  -i INDEXPATH, --indexpath INDEXPATH
                        The directory location into which the created index
                        will be stored. Defaults to "/var/idx"
  -d DATASET, --dataset DATASET
                        The identifier for the index dataset. Default is
                        "dataset"
  -p PREFIX, --prefix PREFIX
                        A path written into the config.toml's "prefix" value
                        (and elsewhere) that relates to where the index will
                        be used, if that is different from where it is
                        written. Defaults to the value of "dest". Use this if
                        you will move the index to another path before using
                        it or if it will appear to be at a different path by
                        the reading process.

```

## Example

So, for the above example `wget` command, which places the downloaded data in `./data`:

```sh
#> mkdir output
#> docker -v `pwd`/data:/var/mirror -v `pwd`/output:/var/idx metapyquod-indexer
```

If you have multiple mirrrors and want to generate multiple indexes side-by-side, you can also do that in a slightly different way:

```sh
#> docker -v `pwd`/data1:/var/mirror -v `pwd`:/var/idx metapyquod-indexer -i /var/idx/index1
#> docker -v `pwd`/data2:/var/mirror -v `pwd`:/var/idx metapyquod-indexer -i /var/idx/index2
```

...which will actually create non-existent directories `index1` and `index2` in the current working directory.

Note that the destination path *as the container sees it* is "burned into" the `config.toml` file that is produced in the output directory. So, for example, the last command above would produce this `config.toml` in `./index2`:

```toml
prefix = "/var/idx/index2"
stop-words = "/var/idx/index2/lemur-stopwords.txt"
dataset = "dataset"
corpus = "line.toml"
index = "/var/idx/index2/idx"
metadata = [{name = "title", type = "string"},
    {name = "url", type = "string"},
    {name = "mtime", type = "uint"}]

[[analyzers]]
method = "ngram-word"
ngram = 1
filter = "default-unigram-chain"
```

You can override what goes into the `config.toml` with the `-p`/`--prefix` switch, so this command:

```sh
#> docker -v `pwd`/data2:/var/mirror -v `pwd`:/var/idx metapyquod-indexer -i /var/idx/index2 -p /home/pi/index2
```

...would produce this instead:

```toml
prefix = "/home/pi/index2"
stop-words = "/home/pi/index2/lemur-stopwords.txt"
dataset = "dataset"
corpus = "line.toml"
index = "/home/pi/index2/idx"
metadata = [{name = "title", type = "string"},
    {name = "url", type = "string"},
    {name = "mtime", type = "uint"}]

[[analyzers]]
method = "ngram-word"
ngram = 1
filter = "default-unigram-chain"
```

### This is clumsy--or, why is this a container at all?

Yes, it can be somewhat. The `metapyquod-indexer` Python script itself can be very effectively used directly, so if you have an environment with the dependencies working then feel free to use the script directly if that suits your needs. There are basically two reasons it makes sense to package this as a container:
1. All the dependencies are provided without mucking with your native Python environment or with venvs.
2. It may be advantageous to have this run in a container if you are using it alongside some other container(s) (such as [metapyquod-server](https://github.com/sphtkr/MeTAPyquod/metapyquod-server)) and you want your index to be made available to it using [Named Volumes](https://boxboat.com/2016/06/18/docker-data-containers-and-named-volumes/), or some other container storage driver, or cloud service, or similar scenarios.
