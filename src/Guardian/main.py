from resource_hunter import ResourceHunter

def start():

    rscHunter = ResourceHunter()

    subs = ['ee611083-4581-4ba1-8116-a502d4539206']
    rscHunter.get_all_resources(subs)

if __name__ == '__main__':
    start()
