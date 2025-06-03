from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timezone

app = Flask(__name__)

# Configure SQLAlchemy
