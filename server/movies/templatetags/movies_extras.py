from django import template

register = template.Library()

@register.filter
def msecs_to_string(value):
    """ Converts milliseconds to printable string in days, hours, minutes, seconds """
    seconds = int(value)/1000
    totalseconds = seconds
    days = seconds//86400
    seconds -= days * 86400
    hours = seconds//3600
    seconds -= hours * 3600
    minutes = seconds//60
    seconds -= minutes * 60
    result = ''
    if totalseconds >= 86400:
        result += '%dd ' % days
    if totalseconds >= 3600:
        result += '%dh ' % hours
    if totalseconds >= 60:
        result += '%dm ' % minutes
    if totalseconds >= 1:
        result += '%ds ' % seconds
    return result.strip()

@register.filter
def bytes_to_string(value):
    """ Converts bytes to a human readable value, in KB, MB, GB """
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    bytes = int(value)
    if bytes >= gb:
        return '%.1f GB' % (float(bytes) / gb)
    if bytes >= mb:
        return '%d MB' % (bytes / mb)
    if bytes >= kb:
        return '%d KB' % (bytes / kb)
    return '%d B' % (bytes)
