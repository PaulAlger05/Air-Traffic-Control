#!/usr/bin/env python
# -*- coding utf-8 -*-

import psycopg2
import os
import sys

try:
    con = psycopg2.connect(database=os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password = os.environ.get("DB_PASSWORD"))
    print('Connection success')
except:
    print('Connection failure')

try:
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM public.auth_user")
        records = cur.fetchall()
        print(records)
except:
    print('error')
con.close()