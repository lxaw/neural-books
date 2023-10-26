from ttslearn.pretrained import create_tts_engine
from tqdm.notebook import tqdm
import torch
from pydub import AudioSegment
import re
import soundfile as sf
import torch
import multiprocessing
import os
import string
import argparse
import sys

AUDIO_FOLDER = "audio"
CWD = os.getcwd()
AUDIO_PATH = os.path.join(CWD,AUDIO_FOLDER)

# create audio directory if not present
if not os.path.exists(AUDIO_PATH):
    os.makedirs(AUDIO_PATH)

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


# TTS engine
PWG_ENGINE = create_tts_engine("tacotron2_hifipwg_jsut24k", device=device)

# check if there are already audio files from a prior generation.
# we do not want to regenerate files.
# this allows us to pause the processing and restart at a later time
PREXISTING_AUDIO_FILES = os.listdir(os.path.join(CWD,AUDIO_PATH))

def gen_mp3(text,mp3_file_name):
    """
    Generate mp3 file from text.
    """
    wav, sr = PWG_ENGINE.tts(text)
    audio = AudioSegment(
        wav.tobytes(),
        frame_rate=sr,
        sample_width = wav.dtype.itemsize,
        channels=1 if len(wav.shape) == 1 else 2
    )
    mp3_file_path = os.path.join(AUDIO_PATH,mp3_file_name)
    audio.export(mp3_file_path,format="mp3")

def is_bad_txt_string(text):
    """
    Check if txt_string is bad
    """
    return all(char in string.punctuation for char in text)

def process_partition(partition, index):
    """
    Process a partition of audio.
    """
    for i, txt_string in enumerate(partition):
        try:
            mp3_file_name = f"{index}__{i}.mp3"
            if mp3_file_name not in PREXISTING_AUDIO_FILES and not is_bad_txt_string(txt_string):
                gen_mp3(text=txt_string,mp3_file_name=mp3_file_name)
        except Exception as e:
            print(f"Exception at i = {i}:\n{e}")
            print(f"txt_string was: {txt_string}")

def generate(strings):
    # Get the number of CPU cores
    num_cores = multiprocessing.cpu_count()

    # Split the list into partitions
    partition_size = len(strings) // num_cores
    # NOTE:
    # if only one string, then could get partition size zero
    # that would screw up the code, so need at least one
    if partition_size == 0:
        partition_size = 1

    partitions = [strings[i:i + partition_size] for i in range(0, len(strings), partition_size)]

    # Create a list to hold the process objects
    processes = []

    # Initialize a global index value
    global_index = 0

    # Start a process for each partition
    for partition in partitions:
        process = multiprocessing.Process(target=process_partition, args=(partition, global_index))
        processes.append(process)
        process.start()
        global_index += len(partition)

    # Wait for all processes to finish
    for process in processes:
        process.join()

def handle_generate(input_file_path):
    # generates audio files
    with open(input_file_path,"r") as f: text = f.readlines()

    strings = []
    for txt_string in text:
        parsed = re.sub(r'\s','',txt_string)
        parsed_list = parsed.split("。")
        strings += parsed_list

    # get strings
    cleaned_strings = []
    for str in strings:
        if str != "" and not is_bad_txt_string(str):
            cleaned_strings.append(str)
    # free mem
    del strings

    generate(cleaned_strings)

def handle_combine(file_name):
    pass

def is_existing_file(file_path):
    return os.path.isfile(file_path)
def is_txt_file(file_path):
    return file_path.endswith('.txt')
def is_existing_text_file(file_path):
    return is_existing_file(file_path) and is_txt_file(file_path)

def print_usage():
    print("usage (generate audio files): `python gen_mp3s.py -g [input txt file name]`")
    print("usage (combine audio files): `python gen_mp3s.py -c [output mp3 file name]`")

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print_usage()
        exit(-1)

    parser = argparse.ArgumentParser(description="Generate something from an input file to an output file.")
    parser.add_argument("-g", "--generate", metavar="input_file", help="Generate using an input file")
    parser.add_argument("-c", "--combine", metavar="output_file", help="Specify the output file to combine into")

    args = parser.parse_args()

    if args.generate and args.combine:
        print("Error: -g and -c flags cannot be used together.")
    elif args.generate:
        # the third argument should be file
        file_name = sys.argv[2]
        if not is_existing_text_file(file_name):
            print(f'The file "{file_name}" does not exist.')
            exit(-1)
        else:
            handle_generate(file_name)
    elif args.combine:
        file_name = sys.argv[2]
        if not is_txt_file(file_name):
            print(f'The file "{file_name}" is not a txt file.')
            exit(-1)
        else:
            handle_combine(file_name)
    else:
        print_usage()
        exit(-1)
    
    
