from resource_hunter import ResourceHunter

class App:

    def start(self):

        rscHunter = ResourceHunter()

        #subs = ['ee611083-4581-4ba1-8116-a502d4539206']

        az_subs = rscHunter.get_all_subscription_ids()
        print(az_subs)

        sub_ids = []
        for sub in az_subs:
            sub_ids.append(sub.id)

        rsc = rscHunter.get_all_resources(sub_ids)
        print(rsc)



