import argparse
import requests
import json
from tqdm import tqdm

from human_eval.data import write_jsonl, read_problems

MODEL_API = "http://216.48.187.144:8000/v1/chat/completions"

def get_prompt(prompt):
    new_prompt = prompt + ' Write a python script for this problem'
    return new_prompt


def generate_one_completion(model_name, prompt):
    url = MODEL_API

    payload = json.dumps({
    "model": model_name,
    "max_tokens": "2048",
    "messages": [
        {
        "role": "user",
        "content": get_prompt(prompt)
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    result = json.loads(response.text)
    # print(result['choices'][0]['message']['content'])
    return result['choices'][0]['message']['content']

    

def main(args):
    problems = read_problems()

    num_samples_per_task = int(args.samples_per_task)
    samples = [
        dict(task_id=task_id, completion=generate_one_completion(args.model_name, problems[task_id]["prompt"]))
        for task_id in tqdm(problems)
        for _ in range(num_samples_per_task)
    ]
    write_jsonl(args.output_path, samples)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--output_path", type=str, default="samples/samples.jsonl")
    parser.add_argument("--samples_per_task", type=str, default=20)
    args = parser.parse_args()

    main(args)