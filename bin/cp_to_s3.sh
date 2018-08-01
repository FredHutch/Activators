a=/shared/ngs/illumina/aerijman/170413_SN367_0904_AHKNKTBCXY/Unaligned/Project_aerijman/Sample_*
b=/shared/ngs/illumina/aerijman/151203_D00300_0225_AHGJM3BCXX/Unaligned/Project_aerijman/Sample_*

for ii in $a $b	
do
	for i in `ls -d ${ii}`
	do 
		g=$(echo $i | grep -ob "Sample" | grep -oE '^[0-9]+')
		f=${i:30:6}
		for j in `ls $i/*fastq.gz`
		do 
			aws s3 cp $j s3://fh-pi-hahn-s/Activators/data/${f}/fastq/${j:$g:-1}z
		done
	done
done
