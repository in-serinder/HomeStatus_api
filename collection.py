import subprocess

#日志消息
import log_make


def read_log_msg(read_line,file):
    contect=[]
    try:
        with open(file,'r')as file_data:
            lines=file_data.readlines()
            last_lines=lines[-read_line:]
            for line in last_lines:
                contect.append(line.strip())
            return contect
    except FileNotFoundError as e:
        log_make.err_log(e)


def size_format(value):
    if value>1073741824: #gb
        return ['Gb', ((value / 1024) / 1024) / 1024]
    else:
        if value > 1048576:  # mb
            return ['Mb', (value / 1024) / 1024]
        else:
            if value>=1024: #kb
                return ['Kb', value / 1024]

            else:
                if value < 1024:  # bit
                    return ['bit', value]



def byte_upward_format(value,type): #byte,bit,kb
    if type=='bit' and value<=1024:
        return f"{size_format(value/8)[1]:.2f}bit"
    else:
        return f"{size_format(value)[1]:.2f}{size_format(value)[0]}"

def get_command_output(command):
    res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,text=True)
    res=res.stdout.strip()
    res = res if res else '0'
    return res
