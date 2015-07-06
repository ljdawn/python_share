import random

# this function belongs to cluster.py
def kcluster(rows,distance=pearson,k=4):
    if isinstance(k, int):
        # Determine the minimum and maximum values for each point
        ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) for i in range(len(rows[0]))]
        # Create k randomly placed centroids
        clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))] for j in range(k)]
    else:
        clusters = k
        k = len(clusters)

    lastmatches=None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches=[[] for i in range(k)]

        # Find which centroid is the closest for each row 
        for j in range(len(rows)):
            row=rows[j]
            bestmatch=0
            for i in range(k):
                d=distance(clusters[i],row)
                if d<distance(clusters[bestmatch],row):
                    bestmatch=i
            bestmatches[bestmatch].append(j)

        # If the results are the same as last time, this is complete
        if bestmatches==lastmatches:
            break
        lastmatches=bestmatches

        # Move the centroids to the average of their members
        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if len(bestmatches[i])>0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m]+=rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i]=avgs

    return bestmatches
