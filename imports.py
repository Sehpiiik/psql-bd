from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine, text, func, MetaData
import psycopg2
import psycopg
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import user, password, host, db_name
from sqlalchemy.orm import sessionmaker