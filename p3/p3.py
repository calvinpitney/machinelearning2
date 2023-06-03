#!/usr/bin/env python3

# Calvin Pitney


import sys

class NaiveBayes():
    """implement Naive Bayes"""

    def train(self, datafile):
        """
        Train a Naive Bayes on the data in datafile.

        datafile will always be a file in the same format as
        house-votes-84.data, i.e. a comma-seperated values file where
        the first field is the class and the other 16 fields are 'y',
        'n' or '?'.
        
        train() should estimate the appropriate probabilities from
        datafile. The conditional probabilities should be estimated
        with Laplace smoothing (also known as add-one smoothing).
        """
        self.arr_givenR = [[0,0,0], [0,0,0], [0,0,0], [0,0,0],
                     [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
                     [0,0,0], [0,0,0], [0,0,0], [0,0,0],
                     [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
        self.arr_givenD = [[0,0,0], [0,0,0], [0,0,0], [0,0,0],
                     [0,0,0], [0,0,0], [0,0,0], [0,0,0], 
                     [0,0,0], [0,0,0], [0,0,0], [0,0,0],
                     [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
        self.numR = 0.0
        self.numD = 0.0
        raw_data = open(datafile, "r" )
        ch = raw_data.read(1)
        while ch != "":
            if ch == 'r':
                raw_data.read(9)
                self.numR +=1
                for x in range(0,32):
                    ch = raw_data.read(1)
                    if ch == 'y':
                        self.arr_givenR[x/2][0] += 1
                    elif ch == 'n':
                        self.arr_givenR[x/2][1] += 1
                    elif ch == '?':
                        self.arr_givenR[x/2][2] += 1

            if ch == 'd':
                raw_data.read(7)
                self.numD += 1
                for x in range(0,32):
                    ch = raw_data.read(1)
                    if ch == 'y':
                        self.arr_givenD[x/2][0] += 1
                    elif ch == 'n':
                        self.arr_givenD[x/2][1] += 1
                    elif ch == '?':
                        self.arr_givenD[x/2][2] += 1
            ch = raw_data.read(1)
        #print(self.numR)
        #print(self.arr_givenR)
        #print(self.numD)
        #print(self.arr_givenD)
        pass


    def predict(self, evidence):
        """
        Return map of {'class': probability, ...}, based on evidence
        """
        prob_r_numerator = (self.numR/ self.numR+self.numD)
        prob_d_numerator = (self.numD/ self.numR+self.numD)
        #prob_denomenator = 1.0
        for x in range(0, 16):
            if evidence[x] == 'y':
                prob_r_numerator *= (self.arr_givenR[x][0]+1/self.numR+3)
                prob_d_numerator *= (self.arr_givenD[x][0]+1/self.numD+3)
                #prob_denomenator *= (self.arr_givenR[x][0]+self.arr_givenD[x][0])/(self.numR+self.numD)
            elif evidence[x] == 'n':
                prob_r_numerator *= (self.arr_givenR[x][1]+1/self.numR+3)
                prob_d_numerator *= (self.arr_givenD[x][1]+1/self.numD+3)
                #prob_denomenator *= (self.arr_givenR[x][1]+self.arr_givenD[x][1])/(self.numR+self.numD)
            elif evidence[x] == '?':
                prob_r_numerator *= (self.arr_givenR[x][2]+1/self.numR+3)
                prob_d_numerator *= (self.arr_givenD[x][2]+1/self.numD+3)
                #prob_denomenator *= (self.arr_givenR[x][2]+self.arr_givenD[x][2])/(self.numR+self.numD)

        dem = (prob_d_numerator/(prob_r_numerator + prob_d_numerator))
        rep = (prob_r_numerator/(prob_r_numerator + prob_d_numerator))

        return {'democrat': dem, 'republican': rep}


def main():
    """Example usage"""

    classifier = NaiveBayes()
    
    classifier.train('house-votes-84.data')

    some_dem=['y','y','y','n','y','y','n','n','n','n','y','?','y','y','y','y']
    some_rep=['n','y','n','y','y','y','n','n','n','y','?','y','y','y','n','y']

    print(classifier.predict(some_dem))
    print(classifier.predict(some_rep))  


if __name__ == "__main__":
    main()

