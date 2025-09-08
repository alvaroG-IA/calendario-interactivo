def date_format(day:str, month, year):
    day = '0'+day if len(day) == 1 else day
    month = '0'+str(month) if len(str(month)) == 1 else str(month)
    return f'{str(year)}-{month}-{day}'