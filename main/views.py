from django.shortcuts import render
from django.http import JsonResponse
import sqlite3
import json


def index(request):
    return render(request, 'main/index.html')


def loadSelectButtons(request):
    conn = sqlite3.connect('demo_db.db')
    c = conn.cursor()
    c.execute('SELECT name FROM clients;')
    clients = c.fetchall()
    c.execute('SELECT name FROM equipment;')
    equipment = c.fetchall()
    c.execute('SELECT name FROM modes;')
    modes = c.fetchall()
    return JsonResponse({'clients': clients, 'equipment': equipment, 'modes': modes})


def getDurations(request):
    clients = request.GET['clients']
    equipment = request.GET['equipment']
    modes = request.GET['modes']
    minutes = request.GET['inputData[Minutes]']
    startDate = request.GET['inputData[StartDate]']
    endDate = request.GET['inputData[EndDate]']
    startTime = request.GET['inputData[StartTime]']
    endTime = request.GET['inputData[EndTime]']
    numOfRecords = request.GET['inputData[NumOfRecords]']
    whereOperator = 'WHERE '
    if startTime == '' and int(startTime) < 0:
        startTime = '00:00:00'
    else:
        if len(startTime) == 1:
            startTime = '0' + startTime + ':00:00'
        else:
            startTime += ':00:00'
    if endTime == '' and int(endTime) < 0:
        endTime = '00:00:00'
    else:
        if len(endTime) == 1:
            endTime = '0' + endTime + ':00:00'
        else:
            endTime += ':00:00'
    if clients != '' and clients != 'All':
        whereOperator += f"cl.name = '{clients}'"
    if equipment != '' and equipment != 'All':
        if whereOperator != 'WHERE ':
            whereOperator += ' AND '
        whereOperator += f"eq.name = '{equipment}'"
    if modes != '' and modes != 'All':
        if whereOperator != 'WHERE ':
            whereOperator += ' AND '
        whereOperator += f"m.name = '{modes}'"
    if minutes != '' and int(minutes) > 0:
        if whereOperator != 'WHERE ':
            whereOperator += ' AND '
        whereOperator += f"dur.minutes <= {minutes}"
    if startDate != '' and endDate == '':
        if whereOperator != 'WHERE ':
            whereOperator += ' AND '
        whereOperator += f"dur.start = '{startDate} {startTime}'"
    if startDate != '' and endDate != '':
        if whereOperator != 'WHERE ':
            whereOperator += ' AND '
        whereOperator += f"dur.start BETWEEN '{startDate} {startTime}' AND '{endDate} {endTime}'"
    print(whereOperator)
    if whereOperator == 'WHERE ':
        whereOperator = ''
    if numOfRecords == '':
        numOfRecords = 0
    conn = sqlite3.connect('demo_db.db')
    c = conn.cursor()
    c.execute(
        f'''select dur.id, cl.name, eq.name, dur.start, dur.stop, m.name, dur.minutes
        from durations dur
        join clients cl
        on dur.client_id=cl.id
        join equipment as eq
        on dur.equipment_id=eq.id
        join modes m
        on dur.mode_id=m.id
        {whereOperator}
        LIMIT {numOfRecords}
        ''')
    durations = c.fetchall()
    return JsonResponse({'durations': durations})
