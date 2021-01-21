import asyncio
import re

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


async def run_command_on_file(arguments, options, file_path, callback_change, callback_finish):
    cmd = 'k2pdfopt -ui- -x {} {} {}'.format(' '.join(arguments),' '.join(options), file_path)
    print('Running command {}'.format(cmd))
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    while True:
        line = await proc.stdout.readline()
        if line:
            decoded_line = ansi_escape.sub('', line.decode()).strip()
            print(decoded_line)
            callback_change(decoded_line)
        else:
            await proc.communicate()
            print('Return code {}'.format(proc.returncode))
            callback_finish(proc.returncode)
            break
