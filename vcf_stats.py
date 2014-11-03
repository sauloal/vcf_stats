#!/usr/bin/python

import os
import sys
import gzip
import simplejson as json
from datetime import datetime as dt
from pprint   import pprint   as pp

SAMPLE_VALUE = 5000 # 1 for no sampling
SAMPLE_END   = 1000 # -1 for no end

SAMPLE_VALUE =  1 # 1 for no sampling
SAMPLE_END   = -1 # -1 for no end

def openfile(infile):
    if infile.endswith( '.gz' ):
        return gzip.open(infile, mode='rb')

    else:
        return open(infile, 'r')

class stats( object ):
    def __init__(self):
        self.min      = sys.maxint
        self.max      = (sys.maxint-1) * -1
        self.count    = 0
        self.sum      = 0
        self.Asum     = 0
        self.Raverage = 0
        self.variance = 0

    def add( self, v ):
        if self.min > v:
           self.min = v

        if self.max < v:
           self.max = v

        self.count += 1
        self.sum   += v
        self.Asum  += abs(v)

        if self.count == 1:
            self.Raverage = v

        else:
            self.Raverage  = ((   self.Raverage   *  self.count) + v ) / (self.count + 1)
            self.variance += (v - self.Raverage) ** 2
            #dev                   = (    self.variance']   /  self.count']) ** 0.5

    def get( self ):
        if self.count == 0:
            return {
                'average' : 0,
                'Aaverage': 0,
                'stddev'  : 0,
                'min'     : 0,
                'max'     : 0,
                'count'   : 0,
                'sum'     : 0,
                'Asum'    : 0,
                'Raverage': 0,
                'variance': 0
            }

        else:
            avg    = self.sum       / self.count
            Aavg   = self.Asum      / self.count
            stddev = (self.variance / self.count) ** 0.5

            return {
                'average' : avg,
                'Aaverage': Aavg,
                'stddev'  : stddev,
                'min'     : self.min,
                'max'     : self.max,
                'count'   : self.count,
                'sum'     : self.sum,
                'Asum'    : self.Asum,
                'Raverage': self.Raverage,
                'variance': self.variance
            }


def main(infiles):
    for infile in infiles:
        print "\n\nANALYZING", infile
        #$v=0;
        #$c=0;
        #$min=10000000;
        #$max=0;
        #$av=0;
        #$var=0;
        #
        #$a=$v/$c;
        #$dev=sqrt($var/$c);
        #$mx=$a+(2*$dev);
        #
        #print "$c\t$v\t$a\t$min\t$max\t$av\t$var\t$dev\t$mx\n"; }
        #
        #$c+=1;
        #$v+=$_;
        #if ($_ < $min) { $min = $_; };
        #if ($_ > $max) { $max = $_; };
        #if ($c==1) {
        #    $av = $_; $var=0; }
        #
        #else {
        #    $av=(($av*$c)+$_)/($c+1);
        #    $var+=($_-$av)**2;
        #    $dev=sqrt($var/$c);
        #    print "$av\t$var\t$dev\n";}' | \

        values   = {
            'count'   : { },
            'info'    : { },
            'format'  : { },
            'polytype': { },
            'qual'    : { 'all': stats() },
            'dist'    : { 'all': stats() },
        }

        codes = { 'info': {}, 'format': {} }
        count = 0
        with openfile(infile) as fhd:
            for line in fhd:
                line = line.strip()

                if len(line) == 0:
                    continue

                if line[0] == "#":
                    #print line

                    if '##FORMAT' in line:
                        lp   = line[13:]
                        code = lp[:2]
                        nfo  = lp[lp.find('Description="')+13:-2]
                        print 'format\t', code, "\t", nfo
                        codes['format'][code] = nfo

                    elif '##INFO' in line:
                        lp   = line[11:]
                        code = lp[:lp.index(',')]
                        nfo  = lp[lp.find('Description="')+13:-2]
                        print 'info\t', code, "\t", nfo
                        codes['info'][code] = nfo

                    continue

                #sys.exit(0)
                count += 1
                if count % SAMPLE_VALUE != 0:
                    continue


                #print line

                cols   = line.split()
                chrom  =       cols[0]
                pos    = int(  cols[1])
                ref    =       cols[3]
                alt    =       cols[4]
                qual   = float(cols[5])
                info   =       cols[7].split(";")
                fmtLbl =       cols[8].split(":")
                fmtVal =       cols[9].split(":")




                if chrom not in values[ 'dist'  ]:
                    values[ 'dist'     ][ chrom ] = stats()
                    values[ 'qual'     ][ chrom ] = stats()
                    values[ 'count'    ][ chrom ] = 0

                values[ 'count' ][ chrom ] += 1


                polytype = None
                if len(ref) == 1:
                    if len(alt) == 1:
                        polytype = 'SNP'
                    else:
                        polytype = 'INS'
                else:
                    if len(alt) == 1:
                        polytype = 'DEL'
                    else:
                        if len(ref) == len(alt):
                            polytype = 'MNP'
                        else:
                            polytype = 'REP'



                if values[ 'count' ][ chrom ] == 1:
                    print 'first', chrom
                    values[ 'dist'     ][ chrom ].prev = pos
                    #print values[ 'dist'  ][ chrom ].prev

                else:
                    #print 'consecutive', values[ 'dist'  ][ chrom ].prev, pos,
                    dist = pos - values[ 'dist'  ][ chrom ].prev
                    values[ 'dist'     ][ 'all' ].add( dist )
                    values[ 'dist'     ][ chrom ].add( dist )
                    values[ 'dist'     ][ chrom ].prev = pos
                    #print values[ 'dist'  ][ chrom ].prev


                if polytype not in values[ 'polytype' ]:
                    values[ 'polytype' ][ polytype ] = { 'all': stats() }

                if chrom not in values[ 'polytype' ][ polytype ]:
                    values[ 'polytype' ][ polytype ][ chrom ] = stats()
                    values[ 'polytype' ][ polytype ][ chrom ].prev = pos

                else:
                    dist = pos - values[ 'polytype' ][ polytype ][ chrom ].prev
                    values[ 'polytype' ][ polytype ][ 'all' ].add( dist )
                    values[ 'polytype' ][ polytype ][ chrom ].add( dist )
                    values[ 'polytype' ][ polytype ][ chrom ].prev = pos


                values['qual']['all'].add( qual )
                values['qual'][chrom].add( qual )



                for i in info:
                    if "=" in i:
                        k, v = i.split("=")
                        #print "K %s V %s" % (k ,v)

                        if k in codes['info']:
                            k = codes['info'][k]

                        try:
                            v = float(v)
                        except:
                            pass

                        if type(v) is float:
                            #print "float", v

                            if k not in values['info']:
                                values['info'][k]        = { 'all': stats() }

                            if chrom not in values['info'][k]:
                                values['info'][k][chrom] = stats()

                            values['info'][k][chrom].add( v )
                            values['info'][k]['all'].add( v )
                    elif i == "INDEL":
                        if i not in values['info']:
                            values['info'][i]        = { 'all': stats() }

                        if chrom not in values['info'][i]:
                            values['info'][i][chrom] = stats()
                            values['info'][i][chrom].prev = pos
                            continue

                        dist = pos - values['info'][i][chrom].prev
                        values['info'][i][chrom].add( dist )
                        values['info'][i]['all'].add( dist )
                        values['info'][i][chrom].prev = pos




                for fp in range(len(fmtLbl)):
                    f = fmtLbl[fp]
                    v = fmtVal[fp]

                    if f in codes['format']:
                        f = codes['format'][f]

                    #print f

                    if '/' in v:
                        continue

                    if ',' in v:
                        pass

                    else:
                        try:
                            v = float(v)
                        except:
                            continue

                        #print fp, f, v
                        if f not in values['format']:
                            values['format'][f]        = { 'all': stats() }

                        if chrom not in values['format'][f]:
                            values['format'][f][chrom] = stats()

                        values['format'][f][chrom].add( v )
                        values['format'][f]['all'].add( v )



                if count == SAMPLE_END:
                    break








        for k in values:
            #print "k",k
            if   k in [ 'count' ]:
                pass

            elif k in [ 'dist', 'qual' ]:
                for chrom in values[k]:
                    #print "chrom", chrom
                    values[k][chrom] = values[k][chrom].get()

            #elif k in []:
                #values[k] = values[k].get()

            else:
                for chrom in values[k]:
                    #print " chrom", chrom
                    for kk in values[k][chrom]:
                        #print "  kk", kk
                        v = values[k][chrom][kk].get()
                        #pp(v)
                        values[k][chrom][kk] = v

        #pp( values )
        json.dump(values, open(os.path.basename(infile)+'.json', 'w'), sort_keys=True, indent=' ')





if __name__ == '__main__':
    main(sys.argv[1:])
