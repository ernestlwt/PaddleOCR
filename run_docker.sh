docker run -it --name paddle_docker \
    --network=host --gpus all --shm-size=8g \
    -v $PWD:/paddle \
ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddle:3.0.0-gpu-cuda12.6-cudnn9.5-trt10.5 /bin/bash