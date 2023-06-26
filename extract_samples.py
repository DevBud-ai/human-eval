import re
import json
import argparse


def main(args):
    output_data = []
    a = 0
    # Read text from "samples.jsonl" file
    with open(args.sample_path, "r") as file:
        for line in file:
            code = json.loads(line)
            task_id = code['task_id']
            completion = code['completion']
            completion = completion.replace("\r", "")
            completion = completion.replace("```python", "```")            
            if '```' in completion: 
                def_line = completion.index('```')
                completion = completion[def_line+3:].strip()
                
                try:
                    next_line = completion.index('```')
                    completion = completion[:next_line].strip()
                    # print(completion)
                except:
                    a += 1
                    print(completion)
                    print("================\n")
                # print(completion)
            if "__name__ == \"__main__\"" in completion:
                next_line = completion.index('if __name__ == "__main__":')
                completion = completion[:next_line].strip()
                # print(completion)
            
            if "# Example usage" in completion:
                # print(completion)
                next_line = completion.index('# Example usage')
                completion = completion[:next_line].strip()
            
            
            code['completion'] = completion
            output_data.append(code)
            # if code['completion']:
            #     output_data.append(code)
            # else:
            #     print(code)
            #     a += 1
            # break

    print(a)
    print(len(output_data))
    # Write updated data to a new JSONL file
    output_file = args.output_path
    with open(output_file, "w") as file:
        for data in output_data:
            json.dump(data, file)
            file.write("\n")

    print("Updated data saved in", output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, default="samples/samples-extracted.jsonl")
    args = parser.parse_args()

    main(args)