#!/bin/bash

# run locally
# PYTHONPATH=. python trainer/c07_knn.py --dataset ../datasets/animals

export BUCKET_NAME=${GBUCKET}
export JOB_NAME="bjdlsb_c07_$(date +%Y%m%d_%H%M%S)"
export JOB_DIR="gs://$BUCKET_NAME/gmllog/bjdlsb"
export REGION=${CLOUDSDK_COMPUTE_REGION}


echo ${BUCKET_NAME}
echo ${JOB_NAME}
echo ${JOB_DIR}
echo ${REGION}


#For more details on the following commands, see the [`gcloud ml-engine` documentation].
# gcloud run locally
#gcloud ml-engine local train \
#  --job-dir tmp \
#  --module-name trainer.c07_knn \
#  --package-path ./trainer \
#  -- \
#  --dataset ../datasets/animals

gcloud ml-engine jobs submit training $JOB_NAME \
    --job-dir $JOB_DIR \
    --packages ./dist/cvdl_c07_knn-0.0.1.tar.gz \
    --runtime-version 1.0 \
    --module-name trainer.c07_knn \
    --package-path . \
    --region $REGION \
    --config config.yaml \
    --runtime-version 1.4 \
    -- \
    --dataset gs://$BUCKET_NAME/gmldata/bjdlsb/animals 

