import sys
if len(sys.argv) != 2:
    print("The number of arguments should be 1.\n !!Exiting the program..\n")
    sys.exit()
Q = sys.argv[1]
cheery_prob = [1.0,0.75,0.5,0.25,0.0]
lime_prob = [0.0,0.25,0.5,0.75,1.0]
bag_prob=[0.1,0.2,0.4,0.2,0.1]
file_data = "Observation sequence Q: "+Q+ "\nLength of Q: "+str(len(Q))
sum_cprob = sum(list([bag_prob[x] * cheery_prob[x] for x in range(5)]))
sum_lprob = sum(list([bag_prob[x] * lime_prob[x] for x in range(5)]))
for i in range(1,len(Q)+1):
    file_data += "\n\nAfter Observation "+str(i) +" = "+ str(Q[i-1])+"\n"
    if Q[i-1] == 'C':
        for j in range(5):
            temp = (bag_prob[j] * cheery_prob[j])/sum_cprob
            bag_prob[j] = temp
            file_data+="\nP(h"+str(j+1)+" | Q) = "+str(temp)
    else:
        for j in range(5):
            temp = (bag_prob[j] * lime_prob[j])/sum_lprob
            bag_prob[j] = temp
            file_data+="\nP(h"+str(j+1)+" | Q) = "+str(temp)
    sum_cprob = sum(list([bag_prob[x] * cheery_prob[x] for x in range(5)]))
    sum_lprob = sum(list([bag_prob[x] * lime_prob[x] for x in range(5)]))
    file_data+="\n\nProbability that the next candy we pick will be C, given Q: "+str(round(sum_cprob,12)) + "\nProbability that the next candy we pick will be L, given Q: "+str(round(sum_lprob,12))
text_file = open("result.txt", "w")
text_file.write(file_data)
text_file.close()