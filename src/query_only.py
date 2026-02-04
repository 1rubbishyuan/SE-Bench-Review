import json
import random
import os
from tqdm import tqdm
from pipline.pipline import Pipline
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed

argument_parser = ArgumentParser()
argument_parser.add_argument("--num_workers", type=int, default=64, help="Max workers")

argument_parser.add_argument("--input_path", type=str, required=True, help="Path of query jsonl")
argument_parser.add_argument("--output_path", type=str, required=True, help="Path of output jsonl")

argument_parser.add_argument("--model_name", type=str, default="llama")
argument_parser.add_argument("--base_url", type=str, default=None, help="OpenAI base url")
argument_parser.add_argument("--api_key", type=str, default="empty_api_key", help="Openai api key")

argument_parser.add_argument("--host", type=str, default="localhost", help="Host of model")
argument_parser.add_argument("--ports", type=str, default="8800", help="Ports of model, separated by commas")

argument_parser.add_argument("--sample_count", type=int, default=1, help="Sample count per question")
argument_parser.add_argument("--max_length", type=int, default=16384, help="Max token length per trajectories")
argument_parser.add_argument("--temperature", type=float, default=0.6, help="Generation temperature")

args = argument_parser.parse_args()
if __name__ == "__main__":
    ports = args.ports.split(",")
    pipline = Pipline(
        model_name=args.model_name,
        search_alg=None,
        temperature=args.temperature,
        max_length=args.max_length,
        doc_path=None,
        output_path=args.output_path,
        api_key=args.api_key
    )

    parameter_list = []
    existing_queries = {}
    with open(args.input_path, "r") as f:
        for line in f:
            data = json.loads(line)
            existing_queries[data["query"]] = 0

    if args.output_path is not None:
        # make sure output_path exists
        dirname = os.path.dirname(args.output_path)
        os.makedirs(dirname, exist_ok=True)
        if not os.path.exists(args.output_path):
            with open(args.output_path, "w", encoding="utf-8") as f:
                pass
        else:
            print(f"Output file {args.output_path} already exists. It will be added instead of overwritten.")
            with open(args.output_path, "r", encoding="utf-8") as f:
                # load existing trajectories
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            record = json.loads(line)
                            if "query" in record:
                                existing_queries[record["query"]] += 1
                        except json.JSONDecodeError:
                            continue

    parameter_list = []
    with open(args.input_path, "r") as f:
        for line in f:
            data = json.loads(line)
            if data["is_valid"]:
                for i in range(0, args.sample_count - existing_queries[data["query"]]):
                    parameter_list.append(data)

    with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        futures = {
            executor.submit(
            pipline.query_only, 
            base_url=args.base_url if args.base_url else f"http://{args.host}:{random.choice(ports)}/v1",
            data=data
            ): data for data in parameter_list
        }
        with tqdm(total=len(parameter_list), desc="Processing tasks") as pbar:
            for future in as_completed(futures):
                pbar.update(1)
                pass
