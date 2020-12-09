# MeTAPyquod 
* [Proposal PDF](https://github.com/SphtKr/MeTAPyquod/blob/main/MeTAPyquod_Proposal_20201025.pdf)
* [Progress Report PDF](https://github.com/SphtKr/MeTAPyquod/blob/main/MeTAPyquod_Progress_20201127.pdf)

## Containerized metapy Appliances

The object of this project is to simplify the use of MeTA and the metapy bindings by creating pre-packaged docker containers ready to use with all dependencies for different use cases. The result is three reusable containers:

### [`metapyquod-dev`](./metapyquod-dev/REAME.md)

With this container users can instantiate a full working environment for metapy development with a single "docker run ..." command, instead of fighting python versions and build issues. This container includes the metapy libraries and a functional development environment including a known good version of Python, metapy dependencies and useful related libraries (e.g. scipy, numpy), Git version control binaries, and a Linux shell, suitable for experimentation and basic development (e.g., all the UIUC CS410 programming assignments should be able to be completed with only the tools in this container). This container builds on multiple architectures including i386, amd64, armv7l and aarch64--so it will run on Windows, macOS, Linux, and Raspberry Pi 2, 3, and 4, 32-bit and 64-bit OS's! (It's also believed to be ready for Windows ARM64 and MacOS M1 ARM64 processors when Docker supports them!)

### [`metapyquod-server`](./metapyquod-server/REAME.md)
This container provides a simple search engine core as a microservice behind a REST API. This server is *almost* capable enough to serve in basic production use as a simple search appliance in an intranet search scenario, but lacks some robustness. Mainly it can facilitate experimentation with different metapy components in a real world use case. The search service is intended for use with English language corpora.

### [`metapyquod-indexer`](./metapyquod-indexer/REAME.md)
This container expedites the creation of MeTA indexes from a directory structure like that produced by `wget --recursive`. It captures a few useful fields in the index metadata including the original URL, the title from HTML documents, and the modification time of the file (which can be made to correspond to the modification date of the web page when retrieving with `wget`). This is intended to be used in conjunction with `metapyquod-server`, but may be useful in other contexts.
