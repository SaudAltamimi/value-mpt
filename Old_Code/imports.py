from typing import Optional, Dict, List
import yfinance as yf
import pandas as pd
import json
import os
import requests
from datetime import datetime, timedelta
import cvxpy as cp
import numpy as np
from typing_extensions import Annotated
from dataclasses import dataclass, field
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import statsmodels.api as sm
import matplotlib.pyplot as plt
import streamlit as st