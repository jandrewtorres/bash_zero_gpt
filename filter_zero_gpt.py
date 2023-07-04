import time
import webbrowser
import sys
import re
import cv2
import numpy as np
import random
import time
import platform
import subprocess
import pyautogui as pag

# auxillary copy and pasted to handle osx retina displaysCheck if it has Macbook Retina resolution (different by 2x)
is_retina = False
if platform.system() == "Darwin":
    is_retina = subprocess.call("system_profiler SPDisplaysDataType | grep 'retina'", shell=True)

# auxillary copy and pasted to handle osx retina displays
def imagesearch(image, precision=0.8):
    im = pag.screenshot()
    if is_retina:
        im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
    # im.save('testarea.png') useful for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc

# auxillary copy and pasted to handle osx retina displays
def imagesearch_loop(image, timesample, precision=0.8):
    pos = imagesearch(image, precision)
    while pos[0] == -1:
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
    return pos

# evaluate text via zerogpt website using pyautogui
def is_text_humanlike(prompt):
    # Make a request to ZeroGPT.com
    url = 'https://www.zerogpt.com/'
    webbrowser.open_new(url)
    time.sleep(2)
    
    # click on text entry box
    pag.moveTo((529,628), duration=1, tween=pag.easeInQuad)
    pag.click(clicks=2)
    time.sleep(1)
    
    # type the prompt
    pag.typewrite(prompt)
    time.sleep(1)
    
    # click on the 'enter' button
    btn_loc = imagesearch_loop('./zero_gpt_submit_btn.png',1)
    pag.moveTo((btn_loc[0]+ 50, btn_loc[1]+25), tween=pag.easeInQuad, duration=3)
    pag.click(clicks=2)
    time.sleep(1)
    
    # scroll to result
    pag.scroll(-5)
    time.sleep(1)
    
    # Look for the result, if 0% then its good, else bad
    tries = 1
    found = False
    zero_percent_gpt_txt_loc = imagesearch('./zero_gpt_zero_percent.png')

    while zero_percent_gpt_txt_loc[0] == -1 and tries <= 10:
        zero_percent_gpt_txt_loc = imagesearch('./zero_gpt_zero_percent.png') 
        if zero_percent_gpt_txt_loc[0] == -1:
            tries += 1 
        else:
            found = True
            break
    
    # clean up window
    pag.hotkey("conntrol" + "w")
    return found


# command line arguments 
#      - allows for single or multiple inputs to be evaluated.
#      - default stdout for passing and stderr for failing inputs
#           if no file is specified for output
#      - skip (optional) skips first n items 
import argparse
parser = argparse.ArgumentParser(
    description="ZeroGPT checker - given a contiguous chunk of text input, outputs" + 
                " whether or not an AI model could have generated it. All or nothing," +
                " meaning if it has any sort of doubt above 0% that it could be AI generated," +
                " then it will fail the test.")
file_input_group = parser.add_mutually_exclusive_group()
file_input_group_with_delim = parser.add_argument_group()
file_input_group_with_delim.add_argument("-if", "--input-file", 
                              help='the file containing chunks of text to be evaluated individually')
file_input_group_with_delim.add_argument("-d", "--delimiter", 
                              default='\n', 
                              help='the delimeter that seperates the texts to be evaluated in the file')
file_input_group.add_argument("-is", "--input-string", 
                              help='a string to be evaluated')
parser.add_argument_group(file_input_group)
parser.add_argument("-of", "--output-file", 
                    help="output file for passing texts", 
                    default="stdout")
parser.add_argument("-fof", "--fail-output-file", 
                    help="output file for the failed texts", 
                    default="stdout")
parser.add_argument("-s", "--skip", 
                    help="number of texts to skip in the input file", 
                    default=0, 
                    type=int)
args = parser.parse_args()
skip = args.skip
input_file = args.input_file
input_string = args.input_string
delimiter = args.delimiter
output_file = args.output_file
fail_output_file = args.fail_output_file

# read input file of text inputs and evaluate - main loop
with open(input_file, 'r') if input_file else open(input_string, 'r') as infile:
    text = infile.read()
    
    # split on given delimiter    
    prompts = text.split(delimiter)
    prompts = [p.strip() for p in prompts if p != '\n']
    
    # for each prompt, evaluate and record
    for i, p in enumerate(prompts[skip:]):
        print(str(i) + "/" + str(len(prompts)) + "....")
        print(p + '\n')
        if is_text_humanlike(p):
            with open(output_file, "a") as outfile_good:
                outfile_good.write(p + '\n\n<END PROMPT>\n\n')
        else:
            with open(fail_output_file, "a") as outfile_bad:
                outfile_bad.write(p + '\n\n<END PROMPT>\n\n')
