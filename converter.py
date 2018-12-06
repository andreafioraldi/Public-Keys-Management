#!/usr/bin/env python2

import sys
import os

formats = {
    ".pem": "pem",
    ".p12": "pkcs12",
    ".pfx": "pkcs12",
    ".p7b": "pkcs7",
    ".der": "der",
}

def usage():
    print "usage: ./pubconv.py <output format> <input file> [additional input file]\n"
    print " avaiable formats:"
    print "   - pem"
    print "   - der"
    print "   - pkcs7"
    print "   - pkcs12\n"
    exit()

def main():
    if len(sys.argv) < 3:
        usage()
    oformat = sys.argv[1]
    filename = sys.argv[2]
    base, ext = os.path.splitext(filename)
    extra = "" if len(sys.argv) < 4 else sys.argv[3]
    
    if ext != ".pem":
        convert_to_pem = {
            "der": "openssl rsa -pubin -inform der -in %s -out %s.pem" % (filename, base),
            "pkcs7": "openssl pkcs7 -print_certs -in %s -out %s.pem" % (filename, base),
            "pkcs12": "openssl pkcs12 -in %s -out %s.priv.pem -nodes && openssl rsa -in %s.priv.pem -outform PEM -pubout -out %s.pem" % (filename, base, base, base),
        }
        os.system(convert_to_pem[formats[ext]])
    
        
    if oformat != "pem":
        convert_from_pem = {
            "der": "openssl rsa -pubin -inform PEM -outform der -in %s -out %s.der" % (base + ".pem", base),
            "pkcs7": "openssl crl2pkcs7 -nocrl -certfile %s -out %s.p7b" % (base + ".pem", base),
            "pkcs12": "openssl pkcs12 -export -nocerts -in %s -out %s.p12 -inkey %s" % (base + ".pem", base, extra),
        }
        os.system(convert_from_pem[oformat])
    

if __name__ == "__main__":
    main()
