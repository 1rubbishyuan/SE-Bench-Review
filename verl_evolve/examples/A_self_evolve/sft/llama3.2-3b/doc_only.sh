# set -x

# # if [ "$#" -lt 2 ]; then
# #     echo "Usage: run_deepseek_6b7.sh <nproc_per_node> <save_path> [other_configs...]"
# #     exit 1
# # fi

# # nproc_per_node=$1
# # save_path=$2

# # # Shift the arguments so $@ refers to the rest
# # shift 2

# torchrun --standalone --nnodes=1 --nproc_per_node=8 \
#      -m verl.trainer.fsdp_sft_trainer \
#     data.train_files=/data3/yuanjiarui/online_evolve/search-numpy/data/sft_dataset/train.parquet \
#     data.val_files=/data3/yuanjiarui/online_evolve/search-numpy/data/sft_dataset/test.parquet \
#     data.prompt_key=extra_info \
#     data.response_key=extra_info \
#     data.prompt_dict_keys=['question'] \
#     +data.response_dict_keys=['answer'] \
#     data.micro_batch_size_per_gpu=4 \
#     model.partial_pretrain=/data3/yuanjiarui/rl-midtrain/checkpoints/Llama-3.2-3B-Instruct \
#     trainer.default_local_dir=/data3/yuanjiarui/online_evolve/search-numpy/checkpoints/baseline/llama3.2-3b/sft/doc_only \
#     trainer.project_name=llama3.2-3b-sft \
#     trainer.experiment_name=doc-only-debug \
#     trainer.total_epochs=2 \
#     trainer.logger='["console","wandb"]'


#!/bin/bash
set -x

torchrun --nnodes=1 --nproc_per_node=8 \
     -m verl.trainer.fsdp_sft_trainer \
    data.train_files=/data3/yuanjiarui/online_evolve/search-numpy/data/sft_dataset/train.parquet \
    data.val_files=/data3/yuanjiarui/online_evolve/search-numpy/data/sft_dataset/test.parquet \
    data.multiturn.enable=true \
    data.multiturn.messages_key=messages \
    data.micro_batch_size=4 \
    model.partial_pretrain=/data3/yuanjiarui/rl-midtrain/checkpoints/Llama-3.2-3B-Instruct \
    trainer.default_local_dir=/data3/yuanjiarui/online_evolve/search-numpy/checkpoints/baseline/llama3.2-3b/sft/doc_only \
    trainer.project_name=llama3.2-3b-sft \
    trainer.experiment_name=doc-only \
    trainer.logger=console \
    trainer.total_training_steps=20 $@ \
    ulysses_sequence_parallel_size=2 \
    use_remove_padding=true