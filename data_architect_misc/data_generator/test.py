## Takes too long: https://stackoverflow.com/a/9631635
# def blocks(files, size=65536):
#     while True:
#         b = files.read(size)
#         if not b: break
#         yield b
#

# import time
# start = time.time()
# with open('20190822105328_1000000.csv',
#           "r",
#           encoding="utf-8",
#           errors='ignore') as f:
#     print(sum(bl.count("\n") for bl in blocks(f)))
# end=time.time()
# print(end - start) # ~ 96 seconds to count


## This seems promising but the code isn't complete, and I couldn't figure out what
## exactly are supposed to be 'inputs'
## https://stackoverflow.com/a/41005151/1330974
# def blocks(f, cut, size=64*1024): # 65536
#     start, chunk =cut
#     iter=0
#     read_size=int(size)
#     _break =False
#     while not _break:
#         if _break: break
#         if f.tell()+size>start+chunk:
#             read_size=int(start+chunk- f.tell() )
#             _break=True
#         b = f.read(read_size)
#         iter +=1
#         if not b: break
#         yield b
#
#
# def get_chunk_line_count(data):
#     fn,  chunk_id, cut = data
#     start, chunk =cut
#     cnt =0
#     last_bl=None
#
#     with open(fn, "r") as f:
#         if 0:
#             f.seek(start)
#             bl = f.read(chunk)
#             cnt= bl.count('\n')
#         else:
#             f.seek(start)
#             for i, bl  in enumerate(blocks(f,cut)):
#                 cnt +=  bl.count('\n')
#                 last_bl=bl
#
#         if not last_bl.endswith('\n'):
#             cnt -=1
#
#         return cnt
#
# import multiprocessing
# pool = multiprocessing.Pool(processes=4)
# pool_outputs = pool.map(get_chunk_line_count, '20190822105328_1000000.csv')#inputs)
# pool.close() # no more tasks
# pool.join()


## Seems to be running forever
# # https://stackoverflow.com/a/36973958
# import timeit
# import csv
# import pandas as pd
#
# filename = './20190822105328_1000000.CSV'
#
# def talktime(filename, funcname, func):
#     print(f"# {funcname}")
#     t = timeit.timeit(f'{funcname}("{filename}")', setup=f'from __main__ import {funcname}', number = 100) / 100
#     print('Elapsed time : ', t)
#     print('n = ', func(filename))
#     print('\n')
#
# def sum1forline(filename):
#     with open(filename, encoding='utf-8') as f:
#         return sum(1 for line in f)
# talktime(filename, 'sum1forline', sum1forline)
#
# def lenopenreadlines(filename):
#     with open(filename, encoding='utf-8') as f:
#         return len(f.readlines())
# talktime(filename, 'lenopenreadlines', lenopenreadlines)
#
# def lenpd(filename):
#     return len(pd.read_csv(filename, encoding='utf-8')) + 1
# talktime(filename, 'lenpd', lenpd)
#
# def csvreaderfor(filename):
#     cnt = 0
#     with open(filename, encoding='utf-8') as f:
#         cr = csv.reader(f)
#         for row in cr:
#             cnt += 1
#     return cnt
# talktime(filename, 'csvreaderfor', csvreaderfor)
#
# def openenum(filename):
#     cnt = 0
#     with open(filename, encoding='utf-8') as f:
#         for i, line in enumerate(f,1):
#             cnt += 1
#     return cnt
# talktime(filename, 'openenum', openenum)

## The best multiprocess approach found
# https://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
import multiprocessing, sys, time, os, mmap
import logging, logging.handlers

def init_logger(pid):
    console_format = 'P{0} %(levelname)s %(message)s'.format(pid)
    logger = logging.getLogger()  # New logger at root level
    logger.setLevel( logging.INFO )
    logger.handlers.append( logging.StreamHandler() )
    logger.handlers[0].setFormatter( logging.Formatter( console_format, '%d/%m/%y %H:%M:%S' ) )

def getFileLineCount( queues, pid, processes, file1 ):
    init_logger(pid)
    logging.info( 'start' )

    physical_file = open(file1, "r")
    #  mmap.mmap(fileno, length[, tagname[, access[, offset]]]

    m1 = mmap.mmap( physical_file.fileno(), 0, access=mmap.ACCESS_READ )

    #work out file size to divide up line counting

    fSize = os.stat(file1).st_size
    chunk = (fSize / processes) + 1

    lines = 0

    #get where I start and stop
    _seedStart = chunk * (pid)
    _seekEnd = chunk * (pid+1)
    seekStart = int(_seedStart)
    seekEnd = int(_seekEnd)

    if seekEnd < int(_seekEnd + 1):
        seekEnd += 1

    if _seedStart < int(seekStart + 1):
        seekStart += 1

    if seekEnd > fSize:
        seekEnd = fSize

    #find where to start
    if pid > 0:
        m1.seek( seekStart )
        #read next line
        l1 = m1.readline()  # need to use readline with memory mapped files
        seekStart = m1.tell()

    #tell previous rank my seek start to make their seek end

    if pid > 0:
        queues[pid-1].put( seekStart )
    if pid < processes-1:
        seekEnd = queues[pid].get()

    m1.seek( seekStart )
    l1 = m1.readline()

    while len(l1) > 0:
        lines += 1
        l1 = m1.readline()
        if m1.tell() > seekEnd or len(l1) == 0:
            break

    logging.info( 'done' )
    # add up the results
    if pid == 0:
        for p in range(1,processes):
            lines += queues[0].get()
        queues[0].put(lines) # the total lines counted
    else:
        queues[0].put(lines)

    m1.close()
    physical_file.close()

if __name__ == '__main__':
    init_logger( 'main' )
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        logging.fatal( 'parameters required: file-name [processes]' )
        exit()

    t = time.time()
    processes = multiprocessing.cpu_count()
    if len(sys.argv) > 2:
        processes = int(sys.argv[2])
    queues=[] # a queue for each process
    for pid in range(processes):
        queues.append( multiprocessing.Queue() )
    jobs=[]
    prev_pipe = 0
    for pid in range(processes):
        p = multiprocessing.Process( target = getFileLineCount, args=(queues, pid, processes, file_name,) )
        p.start()
        jobs.append(p)

    jobs[0].join() #wait for counting to finish
    lines = queues[0].get()

    logging.info( 'finished {} Lines:{}'.format( time.time() - t, lines ) )

## Simplest approaches (Line count by commandline), and somewhat respectable performances.
# https://superuser.com/q/942079/289562
# find "" /v /c <filename> takes about 30-40 seconds to read 12.15 gb wide CSV file
# time wc -l <filename> takes about 15 secs to read 12.15 gb wide CSV file
