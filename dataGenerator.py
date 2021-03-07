"""
Author: Philippe Sanio
Simple data generation with Survivor, minimap2, samtools and mosdepth
"""

import sys, getopt, os
import dataSimulation

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
       opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print ('Input file is "', inputfile)
   print ('Output file is "', outputfile)

def help():
    print("""
            Options:
            -r --refFile <path/to/refFile.fa>       locations of reference file
            -o --outDir <path/to/outdir>            output location for sim data
            -n --number <amount>                    amount of simulations
            """)
def options(argv):
    reffile = ""
    outdir = os.getcwd()
    amount = 1
    try:
         opts, args = getopt.getopt(argv, "hr:n:o:",["help","refFile=","number=","outDir="])
    except getopt.GetoptError:
        help()
        sys.exit(2)



    for opt, arg in opts:
        if opt in ("-r", "--refFile"):
            reffile = arg
        elif opt in ("-o","--outDir"):
            outdir = arg
        elif opt in ("-n", "--number"):
            amount = arg
        else:
            help()

    result = dict()
    result["reffile"] = reffile
    result["outdir"] = outdir
    result["amount"] = int(amount)
    return result


if __name__ == "__main__":

   result = options(sys.argv[1:])
   result["survivor"] ="../SURVIVOR-master/Debug/SURVIVOR"
   result["survivorparamfile"] ="../survivor/parameter_file"
   result["errorprofile"] = "../SURVIVOR-master/Debug/HG002_Pac_error_profile_bwa.txt"
   result["minimap2"] ="../minimap2-2.17_x64-linux/minimap2"
   result["samtools"] ="../samtools"
   result["mosdepth"] ="../mosdepth"
   print(result)
   ds = dataSimulation.dataSimulation(result)
