echo "Launch tgi endpoint"
nohup singularity run --nv \
    --bind $GPFS_MODELS_REGISTRY_PATH:/data  \
    $GPFS_TGI_SINGULARITY  \
    --model-id /data/$GPFS_TGI_MODEL \
    --hostname 0.0.0.0 \
    --port 8080 --max-input-length 8000 --max-batch-prefill-tokens 8000 --max-total-tokens 12000 > $JOB_PATH/logs/tgi.log 2>&1 &