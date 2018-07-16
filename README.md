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
Index	Start        	End          	Elapsed
0	    0.0000419617	0.1857390404	0.1856970787
1	    0.1857769489	0.3680591583	0.1822822094
2	    0.3680939674	0.5546400547	0.1865460873
Total 3 items pushed to IPFS sequentially in 0.554525375366 seconds

======= Sequential Fetch (Attempt #0) =======
Index	Start        	End          	Elapsed
0	    0.0000739098	0.0046000481	0.0045261383
1	    0.0046968460	0.0087950230	0.0040981770
2	    0.0088398457	0.0128898621	0.0040500164
Total 3 items fetched from IPFS sequentially in 0.012674331665 seconds

======= Sequential Fetch (Attempt #1) =======
Index	Start        	End          	Elapsed
0	    0.0000650883	0.0043249130	0.0042598248
1	    0.0043680668	0.0090460777	0.0046780109
2	    0.0091040134	0.0146510601	0.0055470467
Total 3 items fetched from IPFS sequentially in 0.0144848823547 seconds

======= Threaded Fetch (Attempt #0) =======
Index	Start        	End          	Elapsed
2	    0.0045330524	0.0136179924	0.0090849400
1	    0.0012850761	0.0140290260	0.0127439499
0	    0.0005128384	0.0143189430	0.0138061047
Total 3 items fetched from IPFS concurrently in 0.0356349945068 seconds

======= Threaded Fetch (Attempt #1) =======
Index	Start        	End          	Elapsed
0	    0.0002660751	0.0062069893	0.0059409142
1	    0.0014071465	0.0080530643	0.0066459179
2	    0.0026381016	0.0082631111	0.0056250095
Total 3 items fetched from IPFS concurrently in 0.0182118415833 seconds

======= SUMMARY =======
Data Items:	    3
Fetch Attempts:	2
Mean Fetch Time (Sequential):	0.0045265357 seconds/item
Mean Fetch Time (Threaded):	  0.0089744727 seconds/item
```
