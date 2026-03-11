set -x

# if [ "$#" -lt 1 ]; then
#     echo "Usage: run_gemma_7b.sh <nproc_per_node> [other_configs...]"
#     exit 1
# fi

nproc_per_node=8

# Shift the arguments so $@ refers to the rest
shift 2



CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \
     -m verl.trainer.fsdp_sft_trainer \
    data.train_files=../../SFT_data/valid_SFT_data.parquet \
    data.val_files=../../SFT_data/valid_SFT_data.parquet \
    data.prompt_key=extra_info \
    data.response_key=extra_info \
    data.prompt_dict_keys=['without_doc_prompt'] \
    data.response_dict_keys=['response'] \
    data.micro_batch_size_per_gpu=2 \
    data.max_length=20000 \
    model.partial_pretrain=Qwen/Qwen3-8B \
    trainer.project_name=Qwen3-8B-SFT \
    trainer.experiment_name=provided-Closed-SFT \
    trainer.total_epochs=4 \
    trainer.n_gpus_per_node=8 \
    trainer.logger='["console","wandb"]' \
    trainer.save_freq=200 \
    ulysses_sequence_parallel_size=4 \
    use_remove_padding=True
