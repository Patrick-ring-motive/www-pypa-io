import sys, threading


def handle_exception(exc_type, exc_value, exc_traceback):
  print("Unhandled Exception")


sys.excepthook = handle_exception

run_old = threading.Thread.run


def run(*args, **kwargs):
  try:
    run_old(*args, **kwargs)
  except:
    handle_exception()


threading.Thread.run = run
