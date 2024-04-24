import psutil
import subprocess
import RPi.GPIO as GPIO
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Set up GPIO
FAN_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

# Function to get CPU temperature
def get_cpu_temperature():
    process = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    temperature = float(output.decode().split('=')[1].split('\'')[0])
    return temperature

# Function to get GPU temperature
def get_gpu_temperature():
    gpu_temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8')
    gpu_temp = float(gpu_temp.strip().split('=')[1][:-2])
    return gpu_temp

# Function to check GPU usage
def get_gpu_usage():
    process = subprocess.Popen(['vcgencmd', 'get_mem', 'gpu'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    gpu_mem = int(output.decode().split('=')[1].split('M')[0])
    return 100 - gpu_mem / 1024 * 100

# Function to check CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Function to check temperatures and system status
def check_system_status():
    cpu_temp = get_cpu_temperature()
    gpu_temp = get_gpu_temperature()
    gpu_usage = get_gpu_usage()
    cpu_usage = get_cpu_usage()

    ram_usage = psutil.virtual_memory().percent

    return {
        "cpu_temp": cpu_temp,
        "ram_usage": ram_usage,
        "gpu_temp": gpu_temp,
        "gpu_usage": gpu_usage,
        "cpu_usage": cpu_usage
    }

# Route to render the web page
@app.route('/')
def index():
    return render_template('index.html')

# Route to provide system status data
@app.route('/data')
def data():
    return jsonify(check_system_status())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
