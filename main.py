# Group Name: Kappa
# Group Members: Kanishk, Kibrom, Oliver

import os
import json
import requests
import unittest
import sqlite3
from insider import fetch_finnhub_transactions, stock_tickers, FH_KEY
from databases import APIdatamanager
import time

def main():
    db_manager = APIdatamanager(db_path="")
