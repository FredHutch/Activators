#!/bin/bash

set -e # exit after any error

# this script is downloaded via url-fetch-and-run (https://github.com/FredHutch/url-fetch-and-run)

# it expects the following environment variables to be set:

# X_TRAIN_S3_URL - S3 URL to X training set
# X_TEST_S3_URL - S3 URL to X test set

# Y_TRAIN_S3_URL - S3 URL to Y training set
# Y_TEST_S3_URL - S3 url to Y test set

# OUTPUT_S3_URL - S3 URL to which to write the output (evaluation file from keras)


git clone https://github.com/FredHutch/Activators.git
cd Activators


echo downloading input files...

aws s3 cp $X_TRAIN_S3_URL ./train-images-idx3-ubyte
aws s3 cp $X_TEST_S3_URL ./t10k-images-idx3-ubyte
aws s3 cp $Y_TRAIN_S3_URL ./train-labels-idx1-ubyte
aws s3 cp $Y_TEST_S3_URL ./t10k-labels-idx1-ubyte

echo "done downloading, running python script..."

time python3 testOnMnist.py

echo "done with computation, uploading output"

aws s3 cp model_evaluation.csv $OUTPUT_S3_URL

echo "done."

