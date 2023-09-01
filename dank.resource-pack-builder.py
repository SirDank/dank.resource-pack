import os
import zipfile
import shutil
from dankware import cls
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TimeElapsedColumn

cls()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# clean

if os.path.isfile("dank.resource-pack.zip"):
    os.remove("dank.resource-pack.zip")

if os.path.isdir("dank.resource-pack"):
    shutil.rmtree("dank.resource-pack", ignore_errors=True)
shutil.copytree("base", "dank.resource-pack")

if os.path.isdir("tmp"):
    os.rmdir("tmp")
os.mkdir("tmp")

# compress

path_to_backup = os.path.join(os.getcwd(), "dank.resource-pack")
zip_name = f'dank.resource-pack.zip'
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
job_progress = Progress("{task.description}", SpinnerColumn(), BarColumn(bar_width=width), TextColumn("[progress.percentage][bright_green]{task.percentage:>3.0f}%"), "[bright_cyan]ETA", TimeRemainingColumn(), TimeElapsedColumn())
overall_task = job_progress.add_task("[bright_green]Compressing", total=int(len(source_files)))
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


