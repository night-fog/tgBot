from bot import Bot


if __name__ == '__main__':
    bot = Bot()

# ToDo:обрабатывать исключение
"""
2018-09-25 00:48:13,935 - WARNING - A TelegramError was raised while processing the Update
2018-09-25 00:48:13,935 - ERROR - No error handlers are registered, logging exception.
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connectionpool.py", line 402, in _make_request
    six.raise_from(e, None)
  File "<string>", line 2, in raise_from
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connectionpool.py", line 398, in _make_request
    httplib_response = conn.getresponse()
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/http/client.py", line 1331, in getresponse
    response.begin()
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/http/client.py", line 297, in begin
    version, status, reason = self._read_status()
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/http/client.py", line 258, in _read_status
    line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/socket.py", line 586, in readinto
    return self._sock.recv_into(b)
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/ssl.py", line 1009, in recv_into
    return self.read(nbytes, buffer)
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/ssl.py", line 871, in read
    return self._sslobj.read(len, buffer)
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/ssl.py", line 631, in read
    v = self._sslobj.read(len, buffer)
socket.timeout: The read operation timed out
"""
