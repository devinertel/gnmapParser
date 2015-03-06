import re,sys
from optparse import OptionParser,OptionGroup

#Protocols if no options passed
DEFAULT_PROTOCOLS = ['http','ssh','telnet','ftp']

#Parse gnmap file
def pGnmap(line, protocols):
    
    #No protocols passed
    if len(protocols) == 0:
        protocols = DEFAULT_PROTOCOLS

    for protocol in protocols:

        # Check if protocol blank string
        if protocol == "":
            continue

        # Remove spaces from protocol name
        protocol = protocol.strip()

        #debug
        #print "PROTOCOL: %s" % protocol
        
        if protocol in line:
            pLines = str(re.findall('Ports:(\s.*)', line))
            pLines = pLines.split(",")

            for i in xrange(1,len(pLines)):
                if protocol in pLines[i]:
                    host = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line)
                    host = ''.join(host)

                    port = ''.join(pLines[i].split('/')[0]).replace(' ','')

                    target = '{}{}{}'.format(host,':',port)
                    print target                

def main (filename, protocols):
    for fname in filename:
        
        #debug
        #print "Parsing File %s" % filename
        
        tLine = False
        try:        
            with open(fname) as infile:
                for line in infile:                
                    if tLine == False:
                        if 'Status: Up' in line:
                            tLine = True
                            continue
                    if tLine == True:
                        pGnmap(line, protocols)
                        tLine = False                

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

if __name__ == '__main__':

    header = "Gnmap Parser \n"
    usage  = "gnmapParser.py [--OPTIONS] *.gnmap"
    parser = OptionParser(usage = usage, description="Protocol parser for gnmap files. Default protocols: http,ssh,telnet,ftp")

    parser.add_option('--protocols', help='Parse Protocols: "http","ssh","telnet","ftp","pop3","domain","smtp"')

    (options,args) = parser.parse_args() 

    protocols = []

    # Print program header
    if options.protocols:
        protocols = options.protocols.split(",")
        print "PROTOCOLS:%s" % protocols

    if len(args) == 0:
        print parser.print_help()

    main(args, protocols)   
