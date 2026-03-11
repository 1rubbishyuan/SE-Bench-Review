set -x

torchrun --nnodes=1 --nproc_per_node=8 \
     -m verl.trainer.fsdp_sft_trainer \
    data.train_files=/data3/yuanjiarui/online_evolve/search-numpy/data/sft_dataset/doc_only/train.parquet \
    data.val_files=/data3/yuanjiarui/online_evolve/search-numpy/data/sft_dataset/doc_only/test.parquet \
    data.multiturn.enable=true \
    data.multiturn.messages_key=messages \
    data.train_batch_size=32 \
    data.micro_batch_size_per_gpu=1 \
    optim.lr=5e-6 \
    model.partial_pretrain=/data3/yuanjiarui/online_evolve/search-numpy/checkpoints/Qwen3-8B/Qwen3-8B \
    trainer.default_local_dir=/data3/yuanjiarui/online_evolve/search-numpy/checkpoints/baseline/Qwen3-8B/sft/doc_only \
    trainer.project_name=Qwen3-8B-sft \
    trainer.experiment_name=doc-only \
    trainer.logger=console \
    trainer.total_epochs=2 \
    use_remove_padding=true