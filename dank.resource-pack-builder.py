import os
import json
import time
import requests
import zipfile
import shutil
import pretty_errors
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from dankware import cls, clr, rm_line, white, red, multithread
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TimeElapsedColumn

def prepare():
    if not os.path.isdir("downloads"):
        os.mkdir("downloads")

    if os.path.isfile("dank.resource-pack.zip"):
        os.remove("dank.resource-pack.zip")

    if os.path.isdir("dank.resource-pack"):
        shutil.rmtree("dank.resource-pack")

def file_downloader(url, file_name):
    while True:
        try:
            response = requests.get(url, headers=headers, allow_redirects=True)
            response.raise_for_status()
            file_size = int(response.headers.get('Content-Length', 0)) / 1024 / 1024
            with open(file_name, "wb") as file:
                file.write(response.content)
            print(clr(f"  > Downloaded [ {file_name} ] [ {file_size:.3f} MB ]\n"))
            break
        except requests.exceptions.RequestException as e:
            input(clr(f"  > Failed [ {file_name} ] Press {white}ENTER{red} to try again... \n", 2))
            rm_line()
            rm_line()

def download_zips():
    
    os.chdir("downloads")

    to_download_urls = []
    to_download_file_names = []

    '''response = session.get("https://vanillaccurate.space/2021/07/17/vanillaccurate/#download").content.decode().splitlines()
    for line in response:
        if "hardtop-vanillaccurate-32x" in line:
            url = line.split('href="')[2].split('"')[0]
            zip_name = url.split("/")[-1]
            if not os.path.exists(zip_name):
                for existing_file in os.listdir():
                    if "hardtop-vanillaccurate-32x" in existing_file:
                        os.remove(existing_file)
                to_download_urls.append(url)
                to_download_file_names.append(zip_name)
            break'''

    if to_download_urls:
        print(clr("\n  > Starting Multiple Downloads... [ this might take a few minutes ]\n"))

        while True:
            try:
                start_time = time.time()
                multithread(file_downloader, 10, to_download_urls, to_download_file_names)
                time_taken = int(time.time() - start_time)
                print(clr(f"\n  > Finished Downloads in {time_taken} seconds\n"))
                break
            except:
                input(clr(f"\n  > Failed to download files! Do not use [ Ctrl + C ]! Press [ENTER] to try again... ", 2))
                cls()
    
    os.chdir("..")

def merge_dicts(dict1, dict2):
    """
    Recursively merge two dictionaries.
    """
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            dict1[key] = merge_dicts(dict1[key], value)
        elif key in dict1 and isinstance(dict1[key], list) and isinstance(value, list):
            dict1[key].extend(value)
        else:
            dict1[key] = value
    return dict1

def merge_json_files(file1_path, file2_path):

    file1_data = open(file1_path, 'r', encoding='utf-8').read().splitlines()
    file2_data = open(file2_path, 'r', encoding='utf-8').read().splitlines()
    
    file1_data = "\n".join(line for line in file1_data if not line.strip().startswith("//"))
    file2_data = "\n".join(line for line in file2_data if not line.strip().startswith("//"))
    
    file1_data = json.loads(file1_data)
    file2_data = json.loads(file2_data)
    
    merged_data = merge_dicts(file1_data, file2_data)
    return merged_data

def copy_and_overwrite(src, dst):
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        if os.path.isdir(src_item):
            if not os.path.isdir(dst_item):
                os.makedirs(dst_item)
            copy_and_overwrite(src_item, dst_item) 
        else:
            if dst_item.endswith(".json"):
                if os.path.isfile(dst_item):
                    combined_file_data = json.dumps(merge_json_files(src_item, dst_item), indent=4)
                    open(dst_item, "w").write(combined_file_data)
                    print(clr(f"  > Merged [ {dst_item} ]"))
                    continue
            shutil.copy(src_item, dst_item)

def extract_zips():

    for dir in ["downloads", "github", "github_ordered"]:
        for zip_file in sorted(os.listdir(dir)):
            if os.path.isdir("tmp"):
                shutil.rmtree("tmp")
            with zipfile.ZipFile(os.path.join(dir, zip_file), "r") as zip_ref:
                zip_ref.extractall("tmp")
            copy_and_overwrite("tmp", "dank.resource-pack")

def cleanup():
    
    os.chdir("dank.resource-pack")
    
    paths = [
        "readme.txt",
        "Changelog.txt",
        "credits.txt",
        #"assets/minecraft/texts/splashes.txt",
        "LICENSE",
        "LICENSE.txt",
    ]
    
    for path in paths:
        if os.path.exists(path):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                print(clr(f"Failed to remove {path}: {e}"))

    os.chdir("..")
    
    shutil.rmtree("tmp")

def compress_to_zip():

    path_to_backup = os.path.join(os.getcwd(), "dank.resource-pack")
    zip_name = 'dank.resource-pack.zip'
    compression_level = 9
    source_files = []
    prefixes = []

    for root, dirs, files in os.walk(path_to_backup):
        for file in files:
            filepath = os.path.join(root, file)
            prefix = str(filepath.split("dank.resource-pack")[1]).replace(f"\\{file}",'')
            source_files.append(filepath)
            prefixes.append(prefix)

    width = os.get_terminal_size().columns
    job_progress = Progress("{task.description}", SpinnerColumn(), BarColumn(bar_width=width),
                            TextColumn("[progress.percentage][bright_green]{task.percentage:>3.0f}%"), "[bright_cyan]ETA",
                            TimeRemainingColumn(), TimeElapsedColumn())
    overall_task = job_progress.add_task("[bright_green]Compressing", total=len(source_files))
    progress_table = Table.grid()
    progress_table.add_row(Panel.fit(job_progress, title="[bright_white]Jobs", border_style="bright_red", padding=(1, 2)))

    with Live(progress_table, refresh_per_second=10):
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, True, compression_level) as zf:
            for i, filepath in enumerate(source_files):
                prefix = prefixes[i]
                relpath = os.path.relpath(filepath, path_to_backup)
                zip_path = os.path.join(prefix, relpath)
                zf.write(filepath, zip_path)
                job_progress.update(overall_task, advance=1)

if __name__ == "__main__":
    
    cls()
    session = requests.Session()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    headers = {'User-Agent': 'dank.tool', 'Content-Type': 'application/zip'}

    print(clr(f"\n  > Preparing..."))
    prepare()
    print(clr(f"\n  > Checking Downloaded Zips..."))
    download_zips()
    print(clr(f"\n  > Extracting Zips...\n"))
    extract_zips()
    print(clr(f"\n  > Copying and Overwriting Base..."))
    copy_and_overwrite("base", "dank.resource-pack")
    print(clr(f"\n  > Cleaning Up..."))
    cleanup()
    print(clr(f"\n  > Compressing to Zip...\n"))
    compress_to_zip()
