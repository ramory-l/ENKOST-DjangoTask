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
    clients = request.GET.getlist('clients[]')
    equipment = request.GET.getlist('equipment[]')
    modes = request.GET.getlist('modes[]')
    minutes = request.GET['inputData[Minutes]']
    startData = request.GET['inputData[StartData]']
    endData = request.GET['inputData[EndData]']
    startTime = request.GET['inputData[StartTime]']
    endTime = request.GET['inputData[EndTime]']
    numOfRecords = request.GET['inputData[NumOfRecords]']
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
        on dur.mode_id=m.id LIMIT {numOfRecords}
        ''')
    durations = c.fetchall()
    return JsonResponse({'durations': durations})
