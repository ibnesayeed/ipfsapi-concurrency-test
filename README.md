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
0      0.0000340939  0.1755928993  0.1755588055
1      0.1756749153  0.3476080894  0.1719331741
2      0.3477320671  0.6154038906  0.2676718235
Total 3 items pushed to IPFS sequentially in 0.615420103073 seconds

======= Sequential Fetch (Attempt #0) =======
Index  Start         End           Elapsed
0      0.0000329018  0.0025489330  0.0025160313
1      0.0025768280  0.0053529739  0.0027761459
2      0.0053858757  0.0131359100  0.0077500343
Total 3 items fetched from IPFS sequentially in 0.0131340026855 seconds

======= Sequential Fetch (Attempt #1) =======
Index  Start         End           Elapsed
0      0.0000140667  0.0036051273  0.0035910606
1      0.0036320686  0.0061681271  0.0025360584
2      0.0061969757  0.0097150803  0.0035181046
Total 3 items fetched from IPFS sequentially in 0.00974893569946 seconds

======= Threaded Fetch (Attempt #0) =======
Index  Start         End           Elapsed
0      0.0003600121  0.0075919628  0.0072319508
1      0.0076868534  0.0114269257  0.0037400723
2      0.0114920139  0.0147988796  0.0033068657
Total 3 items fetched from IPFS concurrently in 0.014839887619 seconds

======= Threaded Fetch (Attempt #1) =======
Index  Start         End           Elapsed
0      0.0002071857  0.0067441463  0.0065369606
1      0.0024530888  0.0104010105  0.0079479218
2      0.0030150414  0.0108411312  0.0078260899
Total 3 items fetched from IPFS concurrently in 0.0109150409698 seconds

======= SUMMARY =======
Data Items:      3
Fetch Attempts:  2
Mean Fetch Time (Sequential):  0.0038138231 seconds/item
Mean Fetch Time (Threaded):    0.0042924881 seconds/item
```
