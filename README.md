# IPFS API Concurrency Test

This repository provides a reproducible test environment to measure concurrency performance of the [IPFS API](https://pypi.org/project/ipfsapi/).
[IPWB](https://github.com/oduwsdl/ipwb/), an [IPFS](https://ipfs.io/)-based web archival replay system, fetches two objects from the IPFS for each replay request it receives, then combines them to prepare the response.
In its initial implementation we used to fetch the two objects sequentially, but planned to fetch them concurrently later.
When [we tried concurrency using threads](https://github.com/oduwsdl/ipwb/pull/425) and benchmarked our replay response time we were surprised to see that it it was taking twice as long.
This was counter intuitive, so we started profiling our code to investigate the culprit.
We found that the API's `cat()` call was taking longer when invoked in concurrent threads.
So, we decided to create this isolated repository for further investigation.

## Run Test

Assuming that [ipfs](https://ipfs.io/docs/install/) and [ipfsapi](https://pypi.org/project/ipfsapi/) are installed and this repository is cloned, run the following commands from the repository directory:

```
$ ipfs daemon --init &
$ ./main.py -h
Usage:   ./main.py [<max-items> [<attempts>]]
<max-items> : Number of items from the data to be used (Default: 5)
<attempts>  : Number of iterations to perform fetches  (Default: 3)
```

The first command will Initialize IPFS and run its daemon in the background.
The second command shows the usage which suggests it can be run without any arguments as the two arguments are optional and have associated default values.
The script will produce timing data for both individual interactions as well as an aggregated summary.

## Run in Docker

Running this test in a Docker container is recommended as it is more reproducible and contains all the necessary requirements.
Assuming that [Docker is installed](https://docs.docker.com/install/), run the following commands:

```
$ git clone https://github.com/ibnesayeed/ipfsapi-concurrency-test
$ cd ipfsapi-concurrency-test
$ docker image build -t ipfsapitest .
$ docker container run --rm -it ipfsapitest
```

The last command will run the script with the default arguments.
An instance of the IPFS daemon will be started inside the container itself without interfering with any other instances on the host.
Every time a new container is run, it will start with a clean slate.
To run the test with only three items from the included data and repeat the task 10 times, run the following command:

```
$ docker container run --rm -it ipfsapitest ./main.py 3 10
```

The Dockerfile provides three [build-args](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg) `PYTHON_TAG`, `IPFS_VERSION`, and `IPFSAPI_VERSION` to customize the environment.
Their default values are `latest`, `v0.4.15`, and `>=0` respectively, but one or more of these can be modified as necessary.
To test the behavior of the API version `0.4.2` in Python `2.7` with IPFS version `v0.4.14`, build an image as following:

```
$ docker image build --build-arg PYTHON_TAG=2.7 \
                     --build-arg IPFS_VERSION="v0.4.14" \
                     --build-arg IPFSAPI_VERSION="==0.4.2" \
                     -t ipfsapitest:custom .
```

Then run the test in a container using this custom image as following:

```
$ docker container run --rm -it ipfsapitest:custom ./main.py 3 10
```

## Sample Output

```
$ ./main.py 3 2

======= Sequential Push (Just Once) =======
Index  Start         End           Elapsed
0      0.0000391006  0.1890790462  0.1890399456
1      0.1891169548  0.3722760677  0.1831591129
2      0.3723781109  0.5568559170  0.1844778061
Total 3 items pushed to IPFS sequentially in 0.556885957718 seconds

======= Sequential Fetch (Attempt #0) =======
Index  Start         End           Elapsed
0      0.0000429153  0.0053079128  0.0052649975
1      0.0053539276  0.0090999603  0.0037460327
2      0.0091428757  0.0153949261  0.0062520504
Total 3 items fetched from IPFS sequentially in 0.0154371261597 seconds

======= Threaded Fetch (Attempt #0) =======
Index  Start         End           Elapsed
0      0.0007300377  0.0119800568  0.0112500191
2      0.0054049492  0.0198419094  0.0144369602
1      0.0045778751  0.0214118958  0.0168340206

Total 3 items fetched from IPFS concurrently in 0.0217299461365 seconds

======= Sequential Fetch (Attempt #1) =======
Index  Start         End           Elapsed
0      0.0000441074  0.0050020218  0.0049579144
1      0.0050911903  0.0096251965  0.0045340061
2      0.0096790791  0.0137782097  0.0040991306
Total 3 items fetched from IPFS sequentially in 0.0138120651245 seconds

======= Threaded Fetch (Attempt #1) =======
Index  Start         End           Elapsed
1      0.0013508797  0.0101108551  0.0087599754
0      0.0006079674  0.0165028572  0.0158948898
2      0.0054647923  0.0182588100  0.0127940178
Total 3 items fetched from IPFS concurrently in 0.0185489654541 seconds

======= SUMMARY =======
Data Items:      3
Fetch Attempts:  2
Mean Fetch Time (Sequential):  0.0048748652 seconds/item
Mean Fetch Time (Threaded):    0.0067131519 seconds/item
```
