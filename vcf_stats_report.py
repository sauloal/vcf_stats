#!/usr/bin/python

import os
import sys
import simplejson as json
from datetime import datetime as dt
import zlib
import base64

template_dir = os.path.dirname( os.path.abspath( sys.argv[0] ) )

templates    = {
	'css'    : 'vcf_stats_report.template.css',
	'json'   : 'vcf_stats_report.template.js',
	'html'   : 'vcf_stats_report.template.html',
	'b64'    : 'vcf_stats_report.template.b64.js',
	'b64m'   : 'vcf_stats_report.template.b64.min.js',
	'inflate': 'vcf_stats_report.template.inflate.js',
	'deflate': 'vcf_stats_report.template.deflate.js'
}


def templater( tpl ):
	return open(os.path.join( template_dir, templates[tpl]), 'r').read()

def getjson(data):
    return base64.b64encode( zlib.compress( json.dumps(data, sort_keys=True, indent=''), 9 ) )
    #return json.dumps(data, sort_keys=True, indent='')

def makehtml(gdata):
    #https://google-developers.appspot.com/chart/interactive/docs/gallery/candlestickchart

    html = templater['html'   ]

    html = html % {
        "data"     : getjson( gdata ),
        "now"      : str(dt.now().isoformat()),
        "css"      : templater['css'    ],
        "js"       : templater['json'   ],
        "b64"      : templater['b64m'   ],
        "inflate"  : templater['inflate']
        #css=open( sys.argv[0] + '.css', 'r' ).read()
        #<!-- <link rel="stylesheet" type="text/css" href="%(stylefile)s"> -->
        #"stylefile": sys.argv[0] + '.css'
    }

    #print html
    open('vcf_stats_report.html', 'w').write( html )

def main(infiles):
    gdata = {}
    for infile in infiles:
        print "reading", infile
        if not infile.endswith('.json'):
            print "not a json file"
            sys.exit(0)

        nname = os.path.basename( os.path.abspath( infile ) )
        nname = nname.replace(  'vcf.gz.json', '').replace(  '.vcf.json', '').replace(  '.json', '')
        gdata[ nname ] = json.load( open(infile, 'r') )

    print "generating html"
    makehtml(gdata)
    print "finished"

if __name__ == '__main__':
    main(sys.argv[1:])
