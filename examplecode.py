from neuron import h
pc = h.ParallelContext()
nhost = int(pc.nhost())
rank = int(pc.id())

#Keep host output from being intermingled.
#Not always completely successful.
import sys
def serialize():
  for r in range(nhost):
    pc.barrier()
    if r == rank:
      yield r
      sys.stdout.flush()
  pc.barrier()

data = [(rank, i) for i in range(nhost)]

if rank == 0:
    print 'source data'
    for r in serialize():
        print rank, data

    data = pc.py_alltoall(data)

if rank == 0:
    print 'destination data'
    for r in serialize():
        print rank, data

pc.runworker()
pc.done()
h.quit()
