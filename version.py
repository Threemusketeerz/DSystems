import subprocess as subp
import re

def get_version():
    command = 'git describe --abbrev=0 --tags'
    tag = subp.run(command, shell=True, stdout=subp.PIPE)
    tag = tag.stdout.decode('utf-8')
    regex = re.compile('[a-z\s]')
    cleaned_tag = re.sub(regex, '', tag)

    print(cleaned_tag)

    return cleaned_tag

if __name__ == "__main__":
    get_version()
