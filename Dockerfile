# build as fredhutch/activators

FROM idealo/nvidia-docker-keras

RUN apt-get update -y && apt-get install -y curl unzip

RUN pip3 install awscli

RUN curl -L https://raw.githubusercontent.com/FredHutch/url-fetch-and-run/master/fetch-and-run/fetch_and_run.sh > /usr/local/bin/fetch_and_run.sh

RUN chmod +x /usr/local/bin/fetch_and_run.sh

ENTRYPOINT ["/usr/local/bin/fetch_and_run.sh"]
