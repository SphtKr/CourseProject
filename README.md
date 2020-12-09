# MeTAPyquod 
* [Proposal PDF](https://github.com/SphtKr/MeTAPyquod/blob/main/MeTAPyquod_Proposal_20201025.pdf)
* [Progress Report PDF](https://github.com/SphtKr/MeTAPyquod/blob/main/MeTAPyquod_Progress_20201127.pdf)

## Containerized metapy Appliances

The object of this project is to simplify the use of MeTA and the metapy bindings by creating pre-packaged docker containers ready to use with all dependencies for different use cases. The result is three reusable containers:

### [`metapyquod-dev`](./metapyquod-dev)

With this container users can instantiate a full working environment for metapy development with a single "docker run ..." command, instead of fighting python versions and build issues. This container includes the metapy libraries and a functional development environment including a known good version of Python, metapy dependencies and useful related libraries (e.g. scipy, numpy), Git version control binaries, and a Linux shell, suitable for experimentation and basic development (e.g., all the UIUC CS410 programming assignments should be able to be completed with only the tools in this container). This container builds on multiple architectures including i386, amd64, armv7l and aarch64--so it will run on Windows, macOS, Linux, and Raspberry Pi 2, 3, and 4, for 32-bit and 64-bit OS's! (It's also believed to be ready for Windows ARM64 and MacOS M1 ARM64 processors when Docker supports them!)

### [`metapyquod-server`](./metapyquod-server)
This container provides a simple search engine core as a microservice behind a REST API. This server is *almost* capable enough to serve in basic production use as a simple search appliance in an intranet search scenario, but lacks some robustness. Mainly it can facilitate experimentation with different metapy components in a real world use case. The search service is intended for use with English language corpora.

### [`metapyquod-indexer`](./metapyquod-indexer)
This container expedites the creation of MeTA indexes from a directory structure like that produced by `wget --recursive`. It captures a few useful fields in the index metadata including the original URL, the title from HTML documents, and the modification time of the file (which can be made to correspond to the modification date of the web page when retrieving with `wget`). This is intended to be used in conjunction with `metapyquod-server`, but may be useful in other contexts.

## What Docker/Why Docker?

Docker is perhaps many things, but you can view it as yet another attempt to deliver "Write Once Run Anywhere" capability for software. Java did this by abstracting away the operating system and hardware and presenting a new, "virtual machine" (the Java VM runtime) that never existed before in concrete form. Hardware virtualization (e.g. VMWare, VirtualBox, KVM) does this by presenting a software-based abstraction of existing physical hardware, upon which you can run any whole OS and software.

Docker does something in between, by creating a virtual OS running inside a "container" within another running OS (usually Linux) that to your software looks like a dedicated instance of an OS, and--crucially--provides efficient mechanisms to package that virtual OS *and all of the dependencies necessary to run your software*. In this way, software can be packaged, delivered, and used in a way that is predictable and repeatable regardless of the system on which it is run.

With the above explanation, it may be clear why Docker can be useful for distributing and using software like MeTA/metapy, especially for learning or research: it has dependencies or proclivities for certain versions of python, certain operating systems (i.e. Windows) present problems, and gathering and/or building the software and its dependencies can be tedious and error prone and may require a level of proficiency in a number of different technical areas. For the containers in this project, one essentially needs only to install Docker and run a single command to get started.

### Helpful Background

While it is not necessary to have a thorough understanding of Docker to use these containers (especially `metapyquod-dev`), the following references are helpful in understanding key concepts:

* [Docker Simplified: A Hands-On Guide for Absolute Beginners](https://www.freecodecamp.org/news/docker-simplified-96639a35ff36/) (text)
* [Learn Docker in 12 Minutes](https://www.youtube.com/watch?v=YFl2mCHdv24) (video)

### Other References

* [Install Docker Desktop on Windows](https://docs.docker.com/docker-for-windows/install/) ([Windows Home specific instructions](https://docs.docker.com/docker-for-windows/install-windows-home/))
* [Install Docker Desktop on Mac](https://docs.docker.com/docker-for-mac/install/)
* [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/) (other distros also described on [docs.docker.com](https://docs.docker.com/engine/install/ubuntu/), and pay special notice to the [Optional post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/))
* [Installing Docker on the Raspberry Pi](https://pimylifeup.com/raspberry-pi-docker/) 

## How were these images built?

The [Dockerfile](https://docs.docker.com/engine/reference/builder/) within each directory defines the build steps necessary for each container, and you should be able to reproduce the build by using (or reading) these Dockerfiles. Note, however, that images for each container have been pushed to [Docker Hub](https://hub.docker.com/u/sphtkr), so you should not have to build them yourself (e.g. `docker build . -t metapyquod-indexer`) unless you want to--you should be able to simply run them (e.g. `docker run --rm sphtkr/metapyquod-indexer --help`).

The images on Docker Hub were [built as "multiarch" images using buildx/BuildKit](https://medium.com/nttlabs/buildx-multiarch-2c6c2df00ca2), using an `amd64` host, a Raspberry Pi 3 running Raspbian Buster as an `arm7l` (32-bit ARM) build host and a Raspbery Pi 4 running Ubuntu as an `aarch64` (64-bit ARM) build host. The result is that you should be able to use a single tag to pull/run any of these images from any x86_64 Linux Docker host (including macOS's HypervisorKit driver and Windows' WSL driver) or any ARMv7 or ARMv8 system supported by Docker (e.g. Raspberry Pi 2, 3, and 4 systems). As the above link points out, this is probably also crucial to support use on Windows and Mac systems with ARM processors, though Docker is not *yet* supported on these systems.

The base image for all containers are the [official Python images], which are (thankfully) already multiarch images, simplifying the build process. Since the MeTAPyquod containers rely on the build system components being in the base image, the "full" official images are used and not the `slim` or `alpine` variants, which does result in a larger image/download size. (This could be improved for `-server` and `-indexer` in the future with a [multi-stage build](https://docs.docker.com/develop/develop-images/multistage-build/).)

One notable aspect of all three Dockerfiles is that they build metapy from source with a small patch (instead of using `pip install metapy`). In short, all current branches of MeTA include a specified URL for downloading the ICU library, but the [ICU project has changed all their download links to a new location on GitHub](http://site.icu-project.org/download). This problem should be avoidable by installing `libicu` and `libicu-dev` via the package manager (apt), but on some architectures the Cmake build scripts for MeTA force a static build of ICU (for reasons that are not entirely clear), which forces the use of the download URL. Furthermore, the metapy in pip and at the head of the master branch in GitHub [builds from a specific commit of MeTA](https://github.com/meta-toolkit/metapy/tree/master/deps) that is no longer at the head of any branch, so to fix the problem both repositories would have to be updated. Therefore, to simplify the cross-architecture build process, we simply checkout the metapy source from GitHub recursively (including the specific commit of MeTA), patch the broken URL (the MD5 hash still matches) and build from that patched source.

## What's With the Name?

The *[Pequod](https://en.wikipedia.org/wiki/Pequod_(Moby-Dick))* was the ship sailed by [Captain Ahab](https://en.wikipedia.org/wiki/Captain_Ahab) in *[Moby Dick](https://en.wikipedia.org/wiki/Moby-Dick)*. The Whale mascot in the Docker Logo is named [Moby Dock](https://www.docker.com/blog/call-me-moby-dock/). So, [ba dum tss](https://www.docker.com/blog/call-me-moby-dock/) (or [womp womp](https://www.urbandictionary.com/define.php?term=womp+womp)).
