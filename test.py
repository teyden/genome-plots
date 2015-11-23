from parser import stream2SSfile, rsidDict

ChromosomeDict = rsidDict('../BIO_DATA/raw23andme_SNPs_teyden.txt', 'CHROMOSOME')
stream2SSfile(ChromosomeDict, 'myOUTPUT')