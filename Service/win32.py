import win32ts

def get_logged_in_username():
    session_id = win32ts.WTSGetActiveConsoleSessionId()
    username = win32ts.WTSQuerySessionInformation(None, session_id, win32ts.WTSUserName)
    return username