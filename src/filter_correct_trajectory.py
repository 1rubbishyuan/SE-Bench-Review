import json
import threading
from argparse import ArgumentParser
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from evaluation.evaluation import Evaluator
from utils.EqualityChecker import EqulityChecker, analyze_source
from utils.data_process import np_array_to_zwc_yitaf
from utils.ast_zwc_checker import ASTSourceValidator
import os

argument_parser = ArgumentParser()
argument_parser.add_argument("--input_path", type=str, required=True, help="Input path of the generated trajectories")
argument_parser.add_argument("--output_path", type=str, default=None, help="Output path of the correct trajectories")
argument_parser.add_argument("--num_workers", type=int, default=128, help="Number of worker threads")
argument_parser.add_argument("--host", type=str, default="localhost", help="Host of zwc sandbox")
argument_parser.add_argument("--port", type=str, default="8111", help="Port of zwc sandbox")

args = argument_parser.parse_args()

class JudgeWorker:
    def __init__(self):
        self.evaluator = Evaluator(worker_url=f"http://{args.host}:{args.port}/run")
        self.validator = ASTSourceValidator()
        
    def judge(self, data):
        """Judge if the response of data passed all test cases."""
        response = data.get("response", "")
        test_cases = data.get("test_cases", [])
        ground_truth_str = data.get("right_exe_result", "")
        
        # parse code
        raw_code = self.evaluator.parse_raw_code_from_response(response)

        for test_case in test_cases:
            test_case["input"] = np_array_to_zwc_yitaf(test_case["input"])

        code = self.evaluator.code_preprocess(raw_code=raw_code, test_cases=test_cases)
        function_name = self.evaluator.parse_function(code)
        result = self.validator.check_source(code, function_name)
        if not result["passed"]:
            # without_zwc_count
            return data, 4
        
        try:
            used_numpy, _ = analyze_source(code)
        except:
            # exe_error_count
            return data, 3
            
        if used_numpy:
            # use_numpy_count
            return data, 2  

        # Execution
        exe_result = self.evaluator.code_execute(code=code)
        if exe_result.json()["stdout"] == "":
            # exe_error_count
            return data, 3

        exe_result = exe_result.json()["stdout"].split("====================")[-1]

        # Evaluation
        ground_truth_list = ground_truth_str.split("#")
        exe_result = exe_result.split("#")[:-1]
        exe_result = [s.strip() for s in exe_result]
        equality_checker = EqulityChecker(tolerance=1e-2)
        try:
            if equality_checker.judge(
                ground_truth_list=ground_truth_list,
                exe_result=exe_result
            ):
                # right_count
                return data, 1
            else:
                # result_error_count
                return data, 0
        except:
            # Exe_error
            return data, 3

class CounterManager:

    def __init__(self):
        self.use_numpy_count = 0
        self.exe_error_count = 0
        self.result_error_count = 0
        self.right_count = 0
        self.without_zwc_count = 0
        self.all_count = 0
        self.lock = threading.Lock()
    
    def update_counter(self, result_code):
        with self.lock:
            self.all_count += 1
            if result_code == 0:
                self.result_error_count += 1
            elif result_code == 1:
                self.right_count += 1
            elif result_code == 4:
                self.without_zwc_count += 1
            elif result_code == 2:
                self.use_numpy_count += 1
            elif result_code == 3:
                self.exe_error_count += 1
    
    def get_statistics(self):
        total = self.all_count if self.all_count > 0 else 1
        return {
            "total": self.all_count,
            "acc": self.right_count / total,
            "without_zwc": self.without_zwc_count / total,
            "numpy": self.use_numpy_count / total,
            "result_error": self.result_error_count / total,
            "exe_error": self.exe_error_count / total
        }

def process_item(data, counter_manager, output_path, file_lock):
    worker = JudgeWorker()
    data, result_code = worker.judge(data)
    counter_manager.update_counter(result_code)

    if output_path is not None and result_code == 1:
        with file_lock:
            with open(output_path, "a", encoding="utf-8") as fout:
                fout.write(json.dumps(data) + "\n")
    
    return result_code

if __name__ == "__main__":
    if args.output_path is not None:
        # Make sure output_path exists
        dirname = os.path.dirname(args.output_path)
        os.makedirs(dirname, exist_ok=True)
        if not os.path.exists(args.output_path):
            with open(args.output_path, "w", encoding="utf-8") as f:
                pass
        else:
            print(f"Output file {args.output_path} already exists. It will be added instead of overwritten.")
    
    all_data = []
    with open(args.input_path, "r") as f:
        for line in f:
            all_data.append(json.loads(line))
    
    counter_manager = CounterManager()
    file_lock = threading.Lock() 

    with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        futures = []
        for data in all_data:
            future = executor.submit(
                process_item, 
                data, 
                counter_manager, 
                args.output_path, 
                file_lock
            )
            futures.append(future)
        
        for future in tqdm(as_completed(futures), total=len(all_data), desc="Processing"):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing item: {e}")
    
    # Print statistics
    stats = counter_manager.get_statistics()
    print(f"Total processed: {stats['total']}")
    print(f"Acc: {stats['acc']}")
    print(f"Without_zwc: {stats['without_zwc']}")
    print(f"Numpy: {stats['numpy']}")
    print(f"Result_error: {stats['result_error']}")
    print(f"Exe_error: {stats['exe_error']}")