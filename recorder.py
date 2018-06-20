import subprocess
import json
import requests
import datetime

CMD = 'rtl_433 -G -F json'
SERVER = 'http://10.0.0.36:5000/data'

def start_process(cmd):
    return subprocess.Popen(cmd.split(),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    
def read_stderr(process):
    return process.stderr.readline().strip()

def read_stdout(process):
    return process.stdout.readline().strip()

def send_data(data):
    try:
        requests.post(SERVER, json=data, timeout=5)
    except Exception:
        print("ERR: " + str(datetime.datetime.now()) + ": Could not connect to Server")
        pass

def main():
    process = start_process(CMD)

    while True:
        try:
            text = read_stdout(process)
            data = json.loads(text)
        except Exception:
            print("ERR: " + str(datetime.datetime.now()) + ": Unable to read JSON")
            pass
        try:
            id = data['sensor_id']
            if str(id)  == "2734":
                send_data(data)
        except Exception:
            print("ERR: " + str(datetime.datetime.now()) + ": No Sensor ID or incorrect Sensor ID")
            pass



if __name__ == '__main__':
    main()
