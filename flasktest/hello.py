import sys
import os
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
from .raspberry.raspberry import is_raspberrypi, Stats

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello Flask Homepage"


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/system')
def system():
    cpu = Stats.get_cpu()
    system = Stats.get_system()
    free, used = Stats.get_disk_space()
    memory = Stats.get_free_memory()
    return render_template('system.html', cpu=cpu, system=system, free=free, used=used, memory=memory)

