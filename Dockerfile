ARG        PYTHON_TAG=latest
FROM       python:${PYTHON_TAG}

ENV        PYTHONUNBUFFERED=1

ARG        IPFS_VERSION=v0.4.15
RUN        cd /tmp \
           && wget -q https://dist.ipfs.io/go-ipfs/${IPFS_VERSION}/go-ipfs_${IPFS_VERSION}_linux-amd64.tar.gz \
           && tar xvfz go-ipfs*.tar.gz \
           && mv go-ipfs/ipfs /usr/local/bin/ipfs \
           && rm -rf go-ipfs* \
           && ipfs init

ARG        IPFSAPI_VERSION=">=0"
RUN        pip install ipfsapi${IPFSAPI_VERSION}

WORKDIR    /src
COPY       . ./
RUN        chmod a+x entrypoint.sh main.py

ENTRYPOINT ["./entrypoint.sh"]
CMD        ["./main.py"]
