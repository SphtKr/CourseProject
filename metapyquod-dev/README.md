# `metapyquod-dev` - Self-Contained MeTA/metapy development environment

[<img src="https://img.youtube.com/vi/P4U69kkqC00/0.jpg" data-canonical-src="https://img.youtube.com/vi/P4U69kkqC00/0.jpg" align="right" height="240" width="320">](https://youtu.be/P4U69kkqC00)
The object of this container is to make getting up and running with [metapy](https://github.com/meta-toolkit/metapy) as fast and easy as possible. There are ready-made [images on Docker Hub](https://hub.docker.com/r/sphtkr/metapyquod-dev/tags?page=1&ordering=last_updated) so you do *not* need to build this yourself. Images are also built for 32-bit and 64-bit ARM processors, if you have a Raspberry Pi handy!

## Quick Start

1. [Install Docker](https://docs.docker.com/engine/install/) (see also my [helpful background references](https://github.com/SphtKr/MeTAPyquod/blob/main/README.md#helpful-background))
2. Right-click and "Save As..." either [run.bat](https://github.com/SphtKr/MeTAPyquod/raw/main/metapyquod-dev/run.bat) (Windows) or [run.sh](https://github.com/SphtKr/MeTAPyquod/raw/main/metapyquod-dev/run.sh) (macOS/Linux) to some location on your computer
3. Open a command prompt or terminal and change your working directory to where your code is (or will be)
4. Run the downloaded script, at whatever path you saved it in step 2, e.g.:
  * Windows: `run.bat`
  * macOS/Linux: `/bin/sh run.sh` or `chmod a+x run.sh; ./run.sh`
  
The container image will download and the container will start. You will be presented with a shell (bash) inside the container, looking something like this:

```
root@2208d3041186:/usr/src/app# _
```

Within that shell, MeTA, metapy, and several other useful tools are available 

```python
sphtkr@macOS > ./run.sh 
root@f78c3a5829f4:/usr/src/app# python
Python 3.8.6 (default, Nov 18 2020, 13:49:49) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import metapy
>>> doc = metapy.index.Document()
>>> tok = metapy.analyzers.ICUTokenizer()
>>> doc.content("I said that I can't believe that it only costs $19.95! I could only find it for more than $30 before.")
>>> tok.set_content(doc.content())
>>> tokens = [token for token in tok]
>>> print(tokens)
['<s>', 'I', 'said', 'that', 'I', "can't", 'believe', 'that', 'it', 'only', 'costs', '$', '19.95', '!', '</s>', '<s>', 'I', 'could', 'only', 'find', 'it', 'for', 'more', 'than', '$', '30', 'before', '.', '</s>']
>>> quit()
root@f78c3a5829f4:/usr/src/app# exit
exit
sphtkr@macOS > _
```

Note that the working directory within the container (`/usr/src/app`) is attached to the directory in which you launched the container, so changes you make *in or below* that directory are concurrently available to both environments:

```sh
sphtkr@macOS > echo "file 1" > file1.txt
sphtkr@macOS > ls
file1.txt run.sh
sphtkr@macOS > ./run.sh 
root@8b3e06512300:/usr/src/app# cat file1.txt 
file 1
root@8b3e06512300:/usr/src/app# echo "file 2" > file2.txt
root@8b3e06512300:/usr/src/app# ls
file1.txt  file2.txt  run.sh
root@8b3e06512300:/usr/src/app# exit
exit
sphtkr@macOS > ls
file1.txt file2.txt run.sh
sphtkr@macOS > cat file2.txt 
file 2
sphtkr@macOS > _
```
This means you can use Visual Studio Code, PyCharm, Spyder, or whatever other editors you were already using on your desktop to edit your code, and then run it inside the container. (Note that IDE-based debuggers will not work automatically in this configuration, see the section on [web_pdb](#web_pdb) and [Advanced Topics](#advanced-topics))

And, especially note that any changes you make *above or outside* of `/usr/src/app` within the container will *not* be available outside the container and will--by default--*be destroyed* when you exit the container. (See [Gotchas](#gotchas) and [Advanced Topics](#advanced-topics) below.)

## What's Included

The following tools are included and available for use

* Python 3.8 (Python 3.6 is also available in a separate image)
  * metapy
  * scipy
  * numpy
  * sympy
  * matplotlib
  * pandas
  * ipython
* Jupyter
* web_pdb
* git
* Build tools, including
  * gcc
  * gfortran
  * cmake

### Using Jupyter

Using Jupyter notebooks should be mostly exactly the same as doing so on your desktop environment, but you'll need to choose the correct address. The correct address should be displayed when you run `jupyter notebook`, you will probably need to choose the one that references `localhost` or `127.0.0.1`:

```sh
sphtkr@macOS > ./run.sh 
root@e80ea36a71a0:/usr/src/app# jupyter notebook
[I 16:09:45.867 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[W 16:09:46.542 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
[I 16:09:46.546 NotebookApp] Serving notebooks from local directory: /usr/src/app
[I 16:09:46.546 NotebookApp] Jupyter Notebook 6.1.5 is running at:
[I 16:09:46.546 NotebookApp] http://e80ea36a71a0:8888/?token=b2abea9baffa546f8dbfada17f42770d9d0dae2a4c199d04
[I 16:09:46.546 NotebookApp]  or http://127.0.0.1:8888/?token=b2abea9baffa546f8dbfada17f42770d9d0dae2a4c199d04
[I 16:09:46.546 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 16:09:46.551 NotebookApp] 
    
    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-7-open.html
    Or copy and paste one of these URLs:
        http://e80ea36a71a0:8888/?token=b2abea9baffa546f8dbfada17f42770d9d0dae2a4c199d04
     or http://127.0.0.1:8888/?token=b2abea9baffa546f8dbfada17f42770d9d0dae2a4c199d04
```
In this case, the last address is the correct one. Copy that address into your browser location bar and the notebook should open.

#### Setting `JUPYTER_PORT`

In some cases, you may need to adjust the port that Jupyter listens on (e.g. if port 8888 is in use or security software prevents use of that port). You can do this by setting the `JUPYTER_PORT` environment variable *before* using `run.sh` or `run.bat`

* Windows
```
C:\Users\sphtkr > setx JUPYTER_PORT=58888
C:\Users\sphtkr > run.bat
```
* macOS/Linux
```
sphtkr@macOS > JUPYTER_PORT=58888 ./run.sh 
```
The changed port should be reflected in the URL showed in the output, copy and paste this URL as before.

### Using web_pdb

Because the Python interpreter runs inside the container's isolated environment, a debugger in an IDE outside the container can't easily inspect the process state. For this reason, [web_pdb](https://github.com/romanvm/python-web-pdb) is pre-installed and can be accessed by default on port 5555:

```python
sphtkr@macOS > ./run.sh 
root@b6a112f56e10:/usr/src/app# python
Python 3.8.6 (default, Nov 18 2020, 13:49:49) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> watchval = "inside"
>>> import web_pdb; web_pdb.set_trace()
2020-12-09 16:30:36,475: root - web_console:108 - CRITICAL - Web-PDB: starting web-server on b6a112f56e10:5555...
```

When the web_pdb debugger is activated, you can access it by going to [http://localhost:5555](http://localhost:5555) a browser from your desktop. This allows you to inspect variable values, step through code in real-time, execute Python expressions in the current stack context, etcetera, similar to what is possible within an IDE debugger. 

#### Setting `WEB_PDB_PORT`

As discussed above with Jupyter, you may need to adjust the port that web_pdb listens on, and you can do this by setting the `WEB_PDB_PORT` environment variable *before* using `run.sh` or `run.bat`

* Windows
```
C:\Users\sphtkr > setx WEB_PDB_PORT=55555
C:\Users\sphtkr > run.bat
```
* macOS/Linux
```
sphtkr@macOS > WEB_PDB_PORT=55555 ./run.sh 
```
Unlike Jupyter, however, the address displayed in the container will *not* be adjusted to the configured port--you will need to remember to connect to the port that you have set, i.e. in this example [http://localhost:55555](http://localhost:55555)

## Advanced Topics

The above documentation covers use with `run.sh` or `run.bat`. Of course, you can use the image to start a container directly, using all the options and customizability that Docker offers. That is largely out of scope of this documentation, but a few scenarios are worth briefly mentioning. For reference, here is the line that runs the container from `run.sh`:

```
docker run --rm -it \
  -v "`pwd`":/usr/src/app -e JUPYTER_PORT=${JUPYTER_PORT} \
  -p ${JUPYTER_PORT}:${JUPYTER_PORT} -p ${WEB_PDB_PORT}:5555 \
  sphtkr/metapyquod-dev:python3.8
```
To hit the high points *very* briefly, `-it` connects an interactive terminal to the container when it is run, `-v` attaches filesystem "volumes" to the container environment, and `-p` ensures ports are forwarded through to the container environment. Consult the Docker documentation for further details.

### Creating a persistent container

In the above command, the `--rm` option makes the container that is started "self-destruct" after you exit it, and anything you modified in the filesystem will disappear and be reset to what it was before the next time you run the command. This is by design and best practice--the best way to think of a container is the way you think of a process, and when a process exits all its state goes away unless persisted elsewhere. However, if you need to install additional python libraries for example, it may grow tiresome to reinstall them every time you exit and restart the container. One solution would be to make a persistent container with 
```
docker create --name my-metapy-container -it -v `pwd`:/usr/src/app sphtkr/metapyquod-dev:python3.8 /bin/bash`
```
and thereafter use the container with:
```
docker start -ai my-metapy-container
```
(note this specific `create` command forwards *no ports*, and would always be attached to the directory in which it was first `create`d, instead of where it was `start`ed!)

This may be a recipe for tears however, as if you "mess up" this container somehow and can't get back into it, *and* you have put anything into it that you can't reproduce (configuration changes in `/etc`, for example), it may not be easy to extract that data from the container environment--many people (myself included) have started using Docker containers this way and it is not really the way they are intended to be used.

### Using Python 3.6

There are currently [two "tags"](https://hub.docker.com/r/sphtkr/metapyquod-dev/tags?page=1&ordering=last_updated), or versions of the image on Docker Hub--`run.sh` and `run.bat` are configured to use `python3.8`, but `python3.6` is available. To switch, all you should have to do is edit your copy of the script to use the `python3.6` tag.

### Remote debugging

Instead of using [web_pdb](#using-web_pdb), it should be possible to use a "remote" debugger to debug running Python inside the container, such as Visual Studio Code's [debugpy](https://github.com/microsoft/debugpy/) with Visual Studio Code. This is outside of the scope of this documentaion, but should work fine if the ports are forwarded through to the container environment properly.

### Extending the Image

Instead of creating a persistent container as described above, in most cases it would be better to extend the existing image and create your own, for instance installing additional python modules or packages. You would do this by creating your own `Dockerfile` and using `metapyquod-dev` in the `FROM` directive. For instance, this creates a derivative image that includes the `less` command in the shell (if you really wanted):

```
FROM sphtkr/metapyquod-dev:python3.8
RUN apt-get install less
CMD ["/bin/bash"]
```

You would then build the image with `docker build . -t my-metapy-image` and run that image instead.

You could also use a derivative image to "bottle" your own python app by changing the `CMD`, and many other scenarios.

## Gotchas

* Generally, ***DON'T*** edit or store anything outside of `/usr/src/app` unless you've mapped a volume to that location. As mentioned many times here, anything stored outside a mapped volume will be destroyed when the container exits, unless you have taken steps to prevent this!
* This image is set up to emphasize utility and ease of use, ***NOT*** security. Keep your firewalls up and do not use this image for serving anything in production--it is a sandbox environment only.
