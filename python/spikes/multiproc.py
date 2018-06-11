from multiprocessing import Process, Queue

def f(q, i):
    q.put((i, i*10))

if __name__ == '__main__':
	q = Queue()
	processes = []
	for i in range(0, 5):
		p = Process(target=f, args=(q, i, ))
		p.start()
		processes.append(p)

	for p in processes:
		print q.get()    # prints "[42, None, 'hello']"

	for p in processes:
		p.join()
