import yfinance as yf
import cvxpy as cp
from typing import Tuple, Dict
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os