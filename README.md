# bash_zero_gpt

Command-line program that takes input text(s) and evaluates whether they are human-like or if GPT generated. If the input is anything above 0% score, it fails the test; All or nothing evaluation.

No zero-gpt api? So what! Automate it!

## Why?
Because I didn't want to copy paste copy paste... copy paste. Put it all in a text file and watch me go boom.
Useful for automating curation of large datasets: llm training data, class assignments, etc.

## How?
The program opens up a browser and automatically inputs it for you using pyautogui and openCV to build the automous agent. Best to run int the provided Dockerfile which produces a virtual frame buffer (xvfb) in which it can complete the task without overriding your entire system or having to set up unecessary VMs. Overkill? maybe. Cool? Convenient? very.

Enjoy!

## How to Use
`$ python3 filter_zero_gpt.py --help`

```bash
ZeroGPT checker - given a contiguous chunk of text input, outputs whether or not an AI model could have generated it. All or nothing, meaning if it has any sort of doubt above 0% that it could be AI generated, then it will fail the test.

options:
  -h, --help            show this help message and exit
  -is INPUT_STRING, --input-string INPUT_STRING
                        a string to be evaluated
  -of OUTPUT_FILE, --output-file OUTPUT_FILE
                        output file for passing texts
  -fof FAIL_OUTPUT_FILE, --fail-output-file FAIL_OUTPUT_FILE
                        output file for the failed texts
  -s SKIP, --skip SKIP  number of texts to skip in the input file

  -if INPUT_FILE, --input-file INPUT_FILE
                        the file containing chunks of text to be evaluated individually
  -d DELIMITER, --delimiter DELIMITER
                        the delimeter that seperates the texts to be evaluated in the file
```

