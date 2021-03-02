import docker
import multiprocessing as mp

output = mp.Queue()

lock = mp.Lock()


def stats(server, lock):
    client = docker.from_env()
    client_lowlevel = docker.APIClient(base_url='unix://var/run/docker.sock')
    client_stats = client_lowlevel.stats(container=server, stream=False)
    output.put(client_stats)


processes = [mp.Process(target=stats, args=(server, lock)) for server in ('d1526144706d', '2b02193ba7dd')]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()


print(output.get())
print(output.get())