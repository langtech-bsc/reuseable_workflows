echo "Launch jupyter lab"
if [ -n "$GPFS_JUPYTER_WORKING_DIR" ]; then
    mkdir -p $GPFS_JUPYTER_WORKING_DIR
    BIND_WORKING_DIR="--bind $GPFS_JUPYTER_WORKING_DIR:/home/bsc/$USER/working_dir"
fi

singularity exec --nv --no-home \
    --bind /gpfs:/gpfs \
    --bind $JOB_PATH:/home/bsc/$USER \
    $BIND_WORKING_DIR \
    $GPFS_SINGULARITY_IMAGE_REGISTRY_PATH/python-jupyter.sif jupyter-lab \
    --notebook-dir=/home/bsc/$USER \
    --no-browser --ip=0.0.0.0 --port=8888 > $JOB_PATH/logs/jupyter.log 2>&1 &
