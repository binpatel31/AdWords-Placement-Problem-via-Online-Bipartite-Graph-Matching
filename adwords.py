import numpy as np
import pandas as pd
import random
import sys
random.seed(0)

bidder_info = {}
bid = {}   ## Keyword -> [[bidder, bidvalue]]
bidders_info = pd.read_csv("bidder_dataset.csv")
for index,row in bidders_info.iterrows():
	if row["Advertiser"] not in bidder_info:
		bidder_info[row["Advertiser"]] = row["Budget"]
	
	if row["Keyword"] not in bid:
		bid[row["Keyword"]] = [[row["Advertiser"],row["Bid Value"]]] 
	else:
		bid[row["Keyword"]].append([row["Advertiser"],row["Bid Value"]])


with open('queries.txt') as file:
	queries = file.readlines()
#print(queries)
queries = [q.strip() for q in queries]


def calc(bud1, bud2):
    return 1 - np.exp(((bud2-bud1)/bud2) - 1)



if len(sys.argv) != 2:
	print("Enter Algorithm name")
else:
	if sys.argv[1] == 'greedy':	
		revenue=0
		#print(len(queries))
		bidder = bidder_info.copy()
		for query in queries:
			###greedy bidder
			items = bid[query]
			max_bidder = None #items[0][0]
			max_bid = -100
			done=0
			for item in items:
				if bidder[item[0]] >=  item[1]:
					done=1
					if max_bid < item[1]:
						max_bid = item[1]
						max_bidder = item[0]
					elif max_bid == item[1]:
						if max_bidder > item[0]:
							max_bidder = item[0];
			if done==0:
				pass
			else:
				revenue += max_bid
				bidder[max_bidder] = bidder[max_bidder] - max_bid
		print(round(revenue,2))
		##############################FOR COMPETITIVE RATIO
		#bidder = bidder_info.copy()
		total_all_iteration=0
		for i in range(100):
			bidder = bidder_info.copy()
			random.shuffle(queries)
			#########
			total=0
			for query in queries:
				###greedy bidder
				items = bid[query]
				max_bidder = None
				max_bid = -100
				done=0
				for item in items:
					if bidder[item[0]] >=  item[1]:
						done=1
						if max_bid < item[1]:
							max_bid = item[1]
							max_bidder = item[0]	
						elif max_bid == item[1]:
							if max_bidder > item[0]:
								max_bidder = item[0]						
								
				if done==0:
					continue
				else:
					total += max_bid
					bidder[max_bidder] = bidder[max_bidder] - max_bid
			#print("iter",total)
			total_all_iteration += total
		#print(total_all_iteration)
		avg = total_all_iteration/100
		#print(avg)
		print(round(avg/sum(bidder_info.values()),2))


        elif sys.argv[1] == "balance":
                revenue=0
                #print(len(queries))
                bidder = bidder_info.copy()
                for query in queries:
                        ###greedy bidder
                        items = bid[query]
                        max_bidder = items[0][0]
                        max_bid = items[0][1]
                        done=0
                        for item in items:
                                if bidder[item[0]] >=  item[1]:
                                        done=1
                                        if bidder[item[0]] > bidder[max_bidder]:
                                                max_bidder = item[0]
                                                max_bid = item[1]
                                        elif bidder[item[0]] == bidder[max_bidder]:
                                                if max_bidder > item[0]:
                                                        max_bidder = item[0];
							max_bid = item[1]
                        if done==0:
                                continue
                        else:
#				print(max_bid)
                                revenue += max_bid#bidder[max_bidder]
                                bidder[max_bidder] = bidder[max_bidder] - max_bid
#				print("===",max_bidder)
                print(round(revenue,2))
                ##############################FOR COMPETITIVE RATIO
                #bidder = bidder_info.copy()
                total_all_iteration=0
                for i in range(100):
                        bidder = bidder_info.copy()
                        random.shuffle(queries)
                        #########
                        total=0
                        for query in queries:
                                ###greedy bidder
                                items = bid[query]
                                max_bidder = items[0][0]
                                max_bid = items[0][1]
                                done=0
                                for item in items:
					if bidder[item[0]] >= item[1]:
						done=1;
                                        	if bidder[item[0]] > bidder[max_bidder]:
                                                	max_bidder = item[0]
                                                	max_bid = item[1]
                                        	elif bidder[item[0]] == bidder[max_bidder]:
                                                	if max_bidder > item[0]:
                                                        	max_bidder = item[0];
                                                        	max_bid = item[1]
                        	if done==0:
                                	continue
                        	else:
#                               print(max_bid)
                                	total += max_bid#bidder[max_bidder]
                                	bidder[max_bidder] = bidder[max_bidder] - max_bid

                        #print("iter",total)
                        total_all_iteration += total
		#print(total_all_iteration)
                #print(total_all_iteration)
                avg = total_all_iteration/100
                #print(avg)
                print(round(avg/sum(bidder_info.values()),2))

############################################################################

        elif sys.argv[1] == "msvv":
                revenue=0
                #print(len(queries))
                bidder = bidder_info.copy()
                for query in queries:
                        ###greedy bidder
                        items = bid[query]
                        max_bidder = None
                        max_bid = -100
                        done=0
                        for item in items:
				psi = 0;
                                if bidder[item[0]] >=  item[1]:
                                        done=1
					psi0 = item[1] * calc(bidder[item[0]], bidder_info[item[0]])
					if max_bidder is not None:
						psi1 = max_bid * calc(bidder[max_bidder], bidder_info[max_bidder])
					else:
						psi1 = -100;

					if psi0 > psi1:
						max_bid = item[1]
						max_bidder = item[0] 	
                                        elif psi0 == psi1:
                                                if max_bidder > item[0]:
                                                        max_bidder = item[0];
                                                        max_bid = item[1]
                        if done==0:
                                continue
                        else:
#                               print(max_bid)

                                revenue += max_bid#bidder[max_bidder]
                                bidder[max_bidder] = bidder[max_bidder] - max_bid
#                               print("===",max_bidder)
                print(round(revenue,2))
                ##############################FOR COMPETITIVE RATIO
                #bidder = bidder_info.copy()
                total_all_iteration=0
                for i in range(100):
                        bidder = bidder_info.copy()
                        random.shuffle(queries)
                        #########
                        total=0
                        for query in queries:
	                        items = bid[query]
        	                max_bidder = None
                	        max_bid = -100
                        	done=0
           	             	for item in items:
                	        	psi = 0;
                               		if bidder[item[0]] >=  item[1]:
                                        	done=1
                                        	psi0 = item[1] * calc(bidder[item[0]], bidder_info[item[0]])
                                        	if max_bidder is not None:
                                                	psi1 = max_bid * calc(bidder[max_bidder], bidder_info[max_bidder])
                                        	else:
                                                	psi1 = -1000;

                                        	if psi0 > psi1:
                                                	max_bid = item[1]
                                                	max_bidder = item[0]
                                        	elif psi0 == psi1:
                                                	if max_bidder > item[0]:
                                                        	max_bidder = item[0];
                                                        	max_bid = item[1]
                        	if done==0:
                                	continue
                        	else:
#                               print(max_bid)

                                	total += max_bid#bidder[max_bidder]
                                	bidder[max_bidder] = bidder[max_bidder] - max_bid
                        #print("iter",total)
                        total_all_iteration += total
                #print(total_all_iteration)
                avg = total_all_iteration/100
                #print(avg)
                print(round(avg/sum(bidder_info.values()),2))


	
						 
					
				



