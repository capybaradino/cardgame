import os
import uuid

import card_db
import card_util
from werkzeug.utils import secure_filename

from flask import Flask, redirect, render_template, request
from flask.helpers import send_from_directory

UPLOAD_FOLDER = "./uploads"
TMP_FOLDEF = "/tmp"
