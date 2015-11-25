from BioinformaticsFile import BioinformaticsFile

DEFAULT_INPUT_PATH = '../../BIO_DATA/raw23andme_SNPs_teyden.txt'

BFile = BioinformaticsFile('23andme', DEFAULT_INPUT_PATH)
BFile.convertTo(format='rsid')
BFile.convertTo(format='SS')