from parseNstream import stream2SSfile, _23andmeObject, _referenceObject

DEFAULT_REF_FILE = '/Volumes/teyden/BIOINFORMATICS/23andme2vcf/23andme_v4_hg19_ref.txt'
DEFAULT_INPUT_PATH = '../../BIO_DATA/raw23andme_SNPs_teyden.txt'

# UserChromosomeDict = _23andmeObject('../../BIO_DATA/raw23andme_SNPs_teyden.txt', 'CHROMOSOME')
RefChromosomeDict = _referenceObject('/Volumes/teyden/BIOINFORMATICS/23andme2vcf/23andme_v4_hg19_ref.txt', 'CHROMOSOME')
# stream2SSfile(RefChromosomeDict, UserChromosomeDict, 'myOUTPUT')

