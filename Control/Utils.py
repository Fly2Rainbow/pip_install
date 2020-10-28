# The MIT License
#
# Copyright (c) 2018 Sanghyeon Jeon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import logging
import logging.handlers


def CreateLogger(loggerName):
    logger = logging.getLogger(loggerName)
    if len(logger.handlers) > 0:
        # logger already exists
        return logger

    logPath = os.path.join(os.path.realpath(""), "logs", loggerName + ".log")
    Mkdirs(logPath)

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(filename)s:%(lineno)s] %(asctime)s > %(levelname)s | %(message)s')

    # Create Handlers
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    streamHandler.setFormatter(formatter)
    rotatingHandler = logging.handlers.RotatingFileHandler(logPath, maxBytes=1024 * 1024 * 1024)
    rotatingHandler.setLevel(logging.DEBUG)
    rotatingHandler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(streamHandler)
    logger.addHandler(rotatingHandler)
    return logger

def Mkdirs(filePath):
    dirPath = os.path.sep.join(filePath.split(os.path.sep)[:-1])
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

def RemoveFile(target, retryCount = 0):
    for i in range(retryCount + 1):
        try:
            os.remove(target)
        except Exception as e:
            print(e)
            continue
        else:
            return True
    return False


def longString(str_list):
    result = []
    for num in str_list:
        result.append(num)
    # print(result)
    return ''.join(result)