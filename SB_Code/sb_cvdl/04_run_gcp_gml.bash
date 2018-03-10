#!/bin/bash

export BUCKET_NAME=${GBUCKET}
export JOB_NAME="mnist_mlp_train_$(date +%Y%m%d_%H%M%S)"
export JOB_DIR=gs://$BUCKET_NAME/gmllog/mnist_mlp_train
export REGION=${CLOUDSDK_COMPUTE_REGION}


echo ${BUCKET_NAME}
echo ${JOB_NAME}
echo ${JOB_DIR}
echo ${REGION}


#For more details on the following commands, see the [`gcloud ml-engine` documentation].

#To run the model locally:
###
### shell

gcloud ml-engine jobs submit training $JOB_NAME \
    --job-dir $JOB_DIR \
    --runtime-version 1.0 \
    --module-name trainer.mnist_mlp \
    --package-path ./trainer \
    --region $REGION \
    -- \
    --train-file gs://$BUCKET_NAME/gmldata/mnist.pkl

