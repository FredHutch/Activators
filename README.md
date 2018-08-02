Transcriptional-Activation-Domains
==================================

---
About
-----
<p>ADs were randomly created and screened in yeast using FACS, where GFP fluorescence is correlated with AD's strength</p> 
<p><img style="float: right;" src ="https://raw.githubusercontent.com/FredHutch/Activators/master/figures/FACS_example.jpg" width="300" height="300" /></p>. 
<p></p>

<p>Oligomers of DNA, consisting of 90 nucleotides were designed to randomly contain equal chance of any of the 20 amino-acids at each position. This 90 bp long randomized fragment is encoded in a plasmid (one or two copies of the plasmid per cell) upstream of the DNA Binding Domain of the yeast activator Gcn4. The plasmids were transformed into yeast strains containing GFPe as a reporter gene.</p>
<p><img style="float: right;" src ="https://github.com/FredHutch/Activators/blob/master/figures/figure2.jpg" width="300" height="300" /></p>
<p>Cells were FACS sorted based on their green fluorescence intensity and splitted into 4 bins of increasing fluorescence intensity and sent for sequencing.<p>
<p><img style="float: right;" src ="https://github.com/FredHutch/Activators/blob/master/figures/figure3.jpg" width="300" height="300" /></p>
<p>Sequencing was paired-end (Illumina), 100nt reads with 7nt overlap between read1 and read2.</p>
<p>include figrue</p>
<p>18 mutants from the library were individually expressed and the fluorescence intensity was measured. Scores were validated in this small set.</p> 
<p>include figure</p>
<p>Three experiments were conducted, using different promoters to activate transcription of a GFP reporter gene: ARG3, ARG1 and ILV6.</p> 


---
Data 
------

<img style="float: right;" src ="https://github.com/FredHutch/Activators/blob/master/figures/aws_tree.jpg" width="300" height="300" /><img style="float: right;" src ="https://github.com/FredHutch/Activators/blob/master/figures/github_tree.jpg" width="300" height="300" /></p>

### Fastq files:

* Folder containing the Fastq files for **ARG3** --> `s3://fh-pi-hahn-s/Activators/data/151203/fastq/`
<ul>
    bin1: [Sample_O1-1, Sample_O2-1]<br>
    bin2: [Sample_O1-2, Sample_O2-2]<br>
    bin3: [Sample_O1-3, Sample_O2-3]<br>
    bin4: [Sample_O1-4, Sample_O2-4]<br>
    pre_sorting: Sample_O1-18_8_15, Sample_O2-18_8_15, Sample_O1-7_8_15
</ul>

* Folder containing the Fastq files for **ARG1** and **ILV6** --> `s3://fh-pi-hahn-s/Activators/data/170413/fastq/`
<ul>
    bin1: Sample_GCTACGC<br>
    bin2: Sample_CGAGGCT<br>
    bin3: Sample_AAGAGGC<br>
    bin4: Sample_GTAGAGG<br>
    pre_sorting: Sample_CGTACTA<br><br>
    bin1: Sample_GGACTCC<br>
    bin2: Sample_TAGGCAT<br>
    bin3: Sample_CTCTCTA<br>
    bin4: Sample_CAGAGAG<br>
    pre_sorting: Sample_TAAGGCG<br>
</ul>

### paired reads translated to aminoacids:

**ARG3**:           `s3://fh-pi-hahn-s/Activators/data/151203/protein_fasta`
<ul>
    ARG3_bin1.fasta<br>
    ARG3_bin2.fasta<br>
    ARG3_bin3.fasta<br>
    ARG3_bin4.fasta<br>
    ARG1_presorting.fasta<br>
</ul>
**ARG1** & **ILV6**: `s3://fh-pi-hahn-s/Activators/data/170413/protein_fasta`
<ul>
    ARG1_bin1.fasta<br>
    ARG1_bin2.fasta<br>
    ARG1_bin3.fasta<br>
    ARG1_bin4.fasta<br>
    ARG1_presorting.fasta<br><br>
    ILV6_bin1.fasta<br>
    ILV6_bin2.fasta<br>
    ILV6_bin3.fasta<br>
    ILV6_bin4.fasta<br>
    ILV6_presorting.fasta<br>
</ul>

### centroids after redundancy filtering (usearch)

**ARG3**:                `s3://fh-pi-hahn-s/Activators/data/151203/centroids_usearch` <br>
**ARG1** and **ILV6**:   `s3://fh-pi-hahn-s/Activators/data/170413/centroids_usearch`

### Experimental Fluorescence measurements used to calculate scores to use in regression models and potentially to split data-set into positives and negatives. 
`s3://fh-pi-hahn-s/Activators/data/`

### Additional data to use as predictors
hydrophobicity values for aa --> `s3://fh-pi-hahn-s/Activators/data/hydrophobicities.txt`

---
Codes/Scripts
--------------------
All codes are stored in `s3:/fh-pi-hahn-s/Activators/codes` and if run without arguments will display HELP message.
`FLASH_wrapper.py`      --> Paires R1 and R2 from all experiments.<br>
`translate.py`        --> Translates the paired reads into proteins. This script filters the data for early-stops, lack of 5'/3' primers, frame shifts, low quality and short length<br>
`assign_scores.py`      --> library to use in other scripts. Assigns scores based on experimental values specified within the short script.<br>
`run_usearch.sh`          --> runs programm usearch with predefined parameters. Different bins and pre\_sorting are clustered individualy, since the redundancy should have came to each of them separately.<br>
`clusters.py`          --> Desicion of what sequences to take from usearch clusters.<br>
`external_software.sh` --> Runs external software: IUPred and PSIpred.<br>
`prepare4depp.py`     --> Prepare data for deep learning. Some of the centroids are probably under-represented in the library and we can consider them as noise. Hence, this script tries to make a more robust desicion on what sequence should be taken from each cluster.<br>
<span style="background-color:#33DAFF; color:black">simple\_lerners.py</span>      --> train and test random\_forest and logistic regression as benchmark to compare to models that incorporate sequential ordering.

|   script name        |  input               | output                                                               |
|:--------------------:|:--------------------:|:--------------------------------------------------------------------:|
|FLASH\_wrapper.py     |promoter (e.g. ARG3)  |<path><bin>bin.fasta, where path=promoter, bin={1..4} and pre\_sorting|
|translate.py          |<path><bin>bin.fasta  |promoter\_bin.fasta & promoter\_bin.counter, output=statistics(stdout)|
|run\_usearch.sh       |fasta file            |./clusters/promoter/cluster${i} with i={0..#clusters}                 |
|clusters.py           |promoter (e.g. ARG3)  |<promoter>\_ALLcentroids\_reads.csv file                              |
|external\_software.sh |long, short, glob     |csv file with p(disorder). Indices=seqs                               |
|prepare4deep.py       |   


---
LICENSE
-------------
No lisence yet


Authors
---------------
Ariel Erijman<br>
Linda Warfield<br>
Lukasz Kozlowski<br>
Wout Bittremieux<br>
Jacob Schreiber<br>
Johannes Soding<br>
William Stafford Noble<br>
Steve Hahn
