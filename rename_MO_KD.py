import os
import re
import sys
import subprocess

# This script copies and renames all files in a folder to preferred format
# into a specified new directory.

## Files we want to rename are in the format:
## UniqueID_AmplificationType_Genus_species_SampleID_Plate_Barcode_Genus_Sequencer_Lane_Read.fastq.gz
## e.g.
## IZYN_NanoAmplified_Saccharina_angustissima_SA-CB-5-MG-3_1_GCAATGCA_Saccharina_I997_L1_R1.fastq.gz
## IZYN_NanoAmplified_Saccharina_angustissima_SA-CB-5-MG-3_1_GCAATGCA_Saccharina_I997_L1_R2.fastq.gz

## Some files (sequenced by machine I1018 or I1019) have a '_Number_' before SampleID
## Two sets of files are unique (the ones that contain 'LIS') and are handled as an exception
## e.g.
## JCGT_NanoAmplified_Saccharina__LIS-F1-3_3_TCTGTTGG_Saccharina_I1018_L1_R1.fastq.gz

## Renamed format:
## UniqueID_SampleID_Sequencer_Plate_Lane_Read.fastq.gz

# Specify new directory for writing files
newdir = sys.argv[1]

print('Creating list of all FASTQs in folder...')
cmd = 'ls *fastq.gz >' + newdir + '/' + 'original_filenames.txt'
os.system(cmd)

print('Renaming...')

with open(newdir + '/' + 'original_filenames.txt','r') as files:
    with open(newdir + '/' + 'rename_MO_KD.log', 'w') as changed_files:
        for file in files:
            file_stripped = file.strip()
            file_list = file_stripped.rsplit('_')
            alts = ['I1018','I1019']
            if 'LIS' in file_stripped:
                uniqueid = file_list[0]
                sampleid = file_list[4]
                sequencer = file_list[8]
                plate = file_list[5]
                lane = file_list[9]
                read_fq = file_list[10]
            elif any(item in file_stripped for item in alts):
                uniqueid = file_list[0]
                sampleid = file_list[5]
                sequencer = file_list[9]
                plate = file_list[6]
                lane = file_list[10]
                read_fq = file_list[11]
            else:
                uniqueid = file_list[0]
                sampleid = file_list[4]
                sequencer = file_list[8]
                plate = file_list[5]
                lane = file_list[9]
                read_fq = file_list[10]
            newname = uniqueid + '_' + sampleid + '_' + sequencer + '_' + plate + '_' + lane + '_' + read_fq
            print('Copying', file_stripped, 'to', newdir + '/' + newname, sep=' ')
            changed_files.write(file_stripped + '\t' + newdir + '/' + newname + '\n')
            cmd = 'cp ' + file_stripped + ' ' + newdir + '/' + newname
            os.system(cmd)
        changed_files.close()
    files.close()

os.system('rm ' + newdir + '/' + 'original_filenames.txt')


