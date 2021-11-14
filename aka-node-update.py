#!/usr/bin/python
import sys
import getopt
import os
import urllib.request
import tarfile
import shutil


def main(argv):
    version = ""
    try:
        opts, args = getopt.getopt(argv, "v:", ["v="])
    except getopt.GetoptError:
        print("error: aka-node-update.py -v 0.4.4")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("help: aka-node-update.py -v 0.4.4")
            sys.exit()
        elif opt in ("-v", "--version"):
            version = arg
    print(f"Version: `{version}`")
    gethfilename = "geth.tar.gz"
    extractedfilename = "geth-linux-amd64"

    if os.path.exists(extractedfilename):
        os.remove(extractedfilename)
    if os.path.exists(gethfilename):
        os.remove(gethfilename)

    downloadpath = f"https://github.com/akroma-project/akroma/releases/download/{version}/geth-linux-amd64-{version}.tar.gz"
    print(downloadpath)
    urllib.request.urlretrieve(downloadpath, "geth.tar.gz")

    if os.path.exists(gethfilename):
        file = tarfile.open(gethfilename)
        file.extractall('.')
        file.close()
        if os.path.exists(gethfilename):
            print('extracted file')
            os.system("service geth stop")
            shutil.move(extractedfilename, 'geth')
            shutil.copy('geth', '/usr/local/bin/')
            os.system("systemctl daemon-reload")
            os.system("service geth restart")
            os.system("service geth status")
        else:
            print("could not extract file")
    else:
        print("could not download file")

if __name__ == "__main__":
    main(sys.argv[1:])
