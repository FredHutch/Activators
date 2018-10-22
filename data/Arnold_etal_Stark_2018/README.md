# How to use this dataset

fastq and bigwig files from [Stark\'s lab website](http://www.starklab.org/data/arnold_nemcko_woodfin_2018/).  
These files correspond to GFP+ and GFP-. __BE AWARE__: There are - and + that correspond to frame, not to GFP.

* [Table EV1](Table_EV1.txt): Candidate library composition --> List of 180 TF coding sequences flanked by 510bp of the upstream and downstream plasmid backbone sequence, that are contained in the short- and long-fragment library

* [Table EV2](Table_EV2.xlsx): Short-fragment library native (+1) reading-frame tADs --> List of 53 called tADs: relative position within TF CDS, length [aa], amino acid sequence of tAD, tAD-seq enrichment (GFP+/GFP-), hypergeometric P-value, FDR, and protein sequence analysis. We also provide tADs called with a more lenient cutoff (66 tADs total), see Methods.

* [Table EV6](Table_EV6.xlsx): Long-fragment library non-native frame tADs --> List of 13 tADs detected with the long library in the frames +2, +3, -1, -2, -3 including: relative position within TF CDS, length [aa], amino acid sequence of tAD, tAD-seq enrichment (GFP+/GFP-), hypergeometric P-value, FDR, and protein sequence analysis.

* [Table EV5](Table_EV5.xlsx): Long-fragment library native (+1) reading-frame tADs --> List of 18 tADs detected with the long library in the +1 frame including: relative position within TF CDS, length [aa], amino acid sequence of tAD, tAD-seq enrichment (GFP+/GFP-), hypergeometric P-value, FDR, and protein sequence analysis.

* [Table EV4](Table_EV4.xlsx): Short-fragment library non-native frame tADs --> List of 103 tADs detected with the short-library in the frames +2, +3, -1, -2, -3 including: relative position within TF CDS, length [aa], amino acid sequence of tAD, tAD-seq enrichment (GFP+/GFP-), hypergeometric P-value, FDR, and protein sequence analysis. We also provide tADs in non-native frames called with a more lenient cutoff (143 tADs total), see Methods.

* [Table EV3](Table_EV3.xlsx): Luciferase validations --> List of native (+1) and out-of-frame short-library and native (+1) long-library candidate fragments individually tested by luciferase assays. This table includes: candidate fragment coordinates (within TF CDS), normalized luciferase activity (normalized to GFP control), standard deviation, P-value (two-sided Student’s t-test vs. GFP control).


