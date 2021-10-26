from threading import Thread
from time import sleep

def T(dir, pattern):
  "This is just a stub that simulate a dir operation"
  sleep(1)
  print('searching pattern %s in dir %s \n' % (pattern, dir))

threads = []
dirs = ['a/b/c', 'a/b/d', 'b/c', 'd/f']
pattern = 'hello'

for dir in dirs:
  thread = Thread(target=T, args=(dir, pattern))
  thread.start()
  threads.append(thread)

for thread in threads:
  thread.join()

print('Main thread end here')