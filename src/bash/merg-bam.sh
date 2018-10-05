#!/bin/bash

: '
cm1=$(samtools merge -n Col_MB_G1_L2_merged.bam 132652-3_S1_L001_R1_001_bismark_bt2.bam 132652-3_S1_L002_R1_001_bismark_bt2.bam 132652-3_S1_L003_R1_001_bismark_bt2.bam 132652-3_S1_L004_R1_001_bismark_bt2.bam
)


cm2=$(samtools merge -n Col_MB_G1_L8_merged.bam 132652-4_S10_L001_R1_001_bismark_bt2.bam 132652-4_S10_L002_R1_001_bismark_bt2.bam 132652-4_S10_L003_R1_001_bismark_bt2.bam 132652-4_S10_L004_R1_001_bismark_bt2.bam
)


cm3=$(samtools merge -n Col_MB_G2_L2_merged.bam 132652-5_S8_L001_R1_001_bismark_bt2.bam 132652-5_S8_L002_R1_001_bismark_bt2.bam 132652-5_S8_L003_R1_001_bismark_bt2.bam 132652-5_S8_L004_R1_001_bismark_bt2.bam)


cm4=$(samtools merge -n Col_MB_G2_L8_merged.bam 132652-6_S4_L001_R1_001_bismark_bt2.bam 132652-6_S4_L002_R1_001_bismark_bt2.bam 132652-6_S4_L003_R1_001_bismark_bt2.bam 132652-6_S4_L004_R1_001_bismark_bt2.bam)

cm5=$(samtools merge -n Col_MB_G4_L2_merged.bam 132652-7_S5_L001_R1_001_bismark_bt2.bam 132652-7_S5_L002_R1_001_bismark_bt2.bam 132652-7_S5_L003_R1_001_bismark_bt2.bam 132652-7_S5_L004_R1_001_bismark_bt2.bam)

cm6=$(samtools merge -n Col_MB_G4_L8_merged.bam 132652-8_S6_L001_R1_001_bismark_bt2.bam 132652-8_S6_L002_R1_001_bismark_bt2.bam 132652-8_S6_L003_R1_001_bismark_bt2.bam 132652-8_S6_L004_R1_001_bismark_bt2.bam)

cm7=$(samtools merge -n Col_MB_G5_L2_merged.bam 132652-9_S2_L001_R1_001_bismark_bt2.bam 132652-9_S2_L002_R1_001_bismark_bt2.bam 132652-9_S2_L003_R1_001_bismark_bt2.bam 132652-9_S2_L004_R1_001_bismark_bt2.bam)

cm8=$(samtools merge -n Col_MB_G5_L8_merged.bam 132652-10_S9_L001_R1_001_bismark_bt2.bam 132652-10_S9_L002_R1_001_bismark_bt2.bam 132652-10_S9_L003_R1_001_bismark_bt2.bam 132652-10_S9_L004_R1_001_bismark_bt2.bam
)

cm9=$(samtools merge -n Col_MB_G8_L2_merged.bam 132652-11_S7_L001_R1_001_bismark_bt2.bam 132652-11_S7_L002_R1_001_bismark_bt2.bam 132652-11_S7_L003_R1_001_bismark_bt2.bam 132652-11_S7_L004_R1_001_bismark_bt2.bam
)

cm10=$(samtools merge -n Col_MB_G8_L8_merged.bam 132652-12_S11_L001_R1_001_bismark_bt2.bam 132652-12_S11_L002_R1_001_bismark_bt2.bam 132652-12_S11_L003_R1_001_bismark_bt2.bam  132652-12_S11_L004_R1_001_bismark_b
t2.bam)

cm11=$(samtools merge -n Col_MB_G11_L2_merged.bam 1209-8_S11_L001_R1_001_bismark_bt2.bam 1209-8_S11_L002_R1_001_bismark_bt2.bam 1209-8_S11_L003_R1_001_bismark_bt2.bam 1209-8_S11_L004_R1_001_bismark_bt2.bam)

cm12=$(samtools merge -n Col_MB_G11_L8_merged.bam 1208-1_S2_L001_R1_001_bismark_bt2.bam 1208-1_S2_L002_R1_001_bismark_bt2.bam 1208-1_S2_L003_R1_001_bismark_bt2.bam 1208-1_S2_L004_R1_001_bismark_bt2.bam 1209-10_S
9_L001_R1_001_bismark_bt2.bam 1209-10_S9_L002_R1_001_bismark_bt2.bam 1209-10_S9_L003_R1_001_bismark_bt2.bam 1209-10_S9_L004_R1_001_bismark_bt2.bam 1209-9_S10_L001_R1_001_bismark_bt2.bam 1209-9_S10_L002_R1_001_bi
smark_bt2.bam 1209-9_S10_L003_R1_001_bismark_bt2.bam 1209-9_S10_L004_R1_001_bismark_bt2.bam)
'

cm9=$(samtools merge -n Col_MB_G0_merged.bam 125607-1_S6_L001_R1_001_bismark_bt2.bam 125607-1_S6_L002_R1_001_bismark_bt2.bam 125607-1_S6_L003_R1_001_bismark_bt2.bam 125607-1_S6_L004_R1_001_bismark_bt2.bam)


