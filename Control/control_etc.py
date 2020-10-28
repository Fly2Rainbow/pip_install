import datetime

def timestamp2datetime(t_stamp):
    _date = datetime.datetime.fromtimestamp(int(t_stamp)).strftime('%Y-%m-%d %H:%M:%S')
    #print(_date)
    return _date



timestamp2datetime('1602773999')