import subprocess
import time
from json import loads
from concurrent.futures import ThreadPoolExecutor
from os import path
import os
import sys

if os.name == 'Windows':
    EXECUTABLE = path.abspath('build\\LMCEmulator.exe')
    BINARY = path.abspath(sys.argv[1])
    CORRECT_DATA = path.abspath('src\\collatz.json')
else:
    EXECUTABLE = path.abspath('lmc_app/LMCEmulator')
    BINARY = path.abspath(sys.argv[1])
    CORRECT_DATA = path.abspath('lmc_app/collatz.json')

def filter_correct_under_1000(answer):
    correct_answer = []
    for e in answer:
        if e < 1000:
            correct_answer.append(e)
        else:
            correct_answer.append(0)
            break
    return correct_answer

def check_output(command, answer, i) -> bool:
    out = subprocess.check_output(command, shell=True)
    
    passed = all(map(lambda x:x[0]==x[1], zip(
        answer,
        tuple(map(int, filter(lambda x:x, map(str.strip, out.decode().split('\n')))))
    )))

    if not passed:
        print(f"Failed n = {i}")
        # print(out)
        # print(answer)
    else:
        # print(out)
        # print(answer)
        print(f"passed {i}")
        pass

    return {
        'i':i,
        'passed':passed,
        'output':','.join(out.decode().split('\n')[:-1]),
        'expected_output': ','.join(map(str, answer))  # Convert integers to strings

    }


def run_tests(path_f):
    with open(CORRECT_DATA, 'r') as file:
        collatz_data = loads(file.read())

    def return_params(i):
        return (
            f"{EXECUTABLE} {path_f} {i}",
            filter_correct_under_1000(collatz_data[i-1]),
            i
        )

    parameters = tuple(map(return_params, range(1, 1000)))
    start = time.time()

    with ThreadPoolExecutor() as executor:
        results = tuple(executor.map(lambda p:check_output(*p), parameters))

    end = time.time()
    passed = all(result['passed'] for result in results)
    # failed_tests = []

    if passed:
        print("All tests passed.")
    else:
        # failed_tests = [result for i, result in enumerate(results, 1) if not result['passed']]
        print("Not all tests passed.")
        # print(f"Failed tests: {failed_tests}")

    print("Time taken:", end - start)
    return (results, passed, end - start)
