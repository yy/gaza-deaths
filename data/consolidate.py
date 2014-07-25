import sys
import os
import urllib
import csv

class BTselem(object):
    """Data object of B'Tselem fatality statistics"""

    def __init__(self):
        self.era = ['before-cast-lead', 
                    'during-cast-lead', 
                    'after-cast-lead']
        self.aff = ['palestinians', 
                    'israeli-security-forces', 
                    'israeli-civilians',
                    'foreign-citizens']
        self.loc = ['wb-gaza', 
                    'israel']

    def gen_url(self, era_id=0, killed_id=0, by_id=1, loc_id=0):
        url_fmt = 'http://www.btselem.org/statistics/fatalities/{era}/' +\
                  'by-date-of-event/{loc}/{killed}-killed-by-{by}/csv'
        return url_fmt.format(era=self.era[era_id], loc=self.loc[loc_id], 
                              killed=self.aff[killed_id], by=self.aff[by_id])

    def process(self, era_id=0, killed_id=0, by_id=1, loc_id=0):
        url = self.gen_url(era_id, killed_id, by_id, loc_id)
        reader = csv.reader(urllib.urlopen(url))
        reader.next() # skipping the header

        # columns:
        # 0 eventdate | 1 deathdate | 2 name | 3 age | 4 gender | 5 citizenship
        #   | 6 affiliation | 7 residence | 8 event loc | 9 took part in
        #   hostilities | 10 type of injury | 11 source of gunfire | 12
        #   ammunition | 13 notes
        #
        # let's keep 0: the date of event, 2: name, 3: age, 4: gender, and 
        # 9: combatant or not 
        #
        # and add the citizenship of the person and killed by which group. I
        # simplify nationality into p(alestinian), i(sraeli), and f(oreigner)
        # 
        # The output becomes
        # 0 eventdate | 1 name | 2 age | 3 gender | 4 combatant or not | 
        # 5 nationality of the deceased | 6 nationality of the killing party

        data = []
        for row in reader: 
            data.append([ row[0], row[2], row[3], row[4], row[9], 
                          self.aff[killed_id][0], self.aff[by_id][0] ])
        return data

if __name__ == '__main__':
    bt = BTselem()
    data = bt.process()
    print data[:10]


