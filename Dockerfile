FROM gw000/keras-full:latest

USER root

RUN apt-get update -y && apt-get install -y curl

RUN pip3 install awscli

RUN curl -L https://raw.githubusercontent.com/FredHutch/url-fetch-and-run/master/fetch-and-run/fetch_and_run.sh > /usr/local/bin/fetch_and_run.sh

RUN chmod +x /usr/local/bin/fetch_and_run.sh

ENV PATH="/usr/local/bin:${PATH}"

USER USER

ENV PATH="/usr/local/bin:${PATH}"


ENTRYPOINT ["/usr/local/bin/fetch_and_run.sh"]
