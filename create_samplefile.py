import random
def createSample(numOfSamples,filename,filetype):
    for i in range(numOfSamples):
        file_type=random.choice(filetype)
        file= open(filename+str(i)+'.'+file_type,'w')
        file.write(''.join(random.choices('ATCG', k=10)))
        file.close()
        
createSample(numOfSamples=50,filename='RawData/',filetype=['fastq','fasta'])
createSample(numOfSamples=50,filename='ProcessedData/',filetype=['sam','bam','cram'])
createSample(numOfSamples=50,filename='SummaryData/',filetype=['vcf','tiff'])