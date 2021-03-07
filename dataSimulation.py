import subprocess
import os

class dataSimulation:
    def __init__(self, args):
        os.mkdir(args["outdir"])
        self.__bpSimulationPipeLine(args)

    def __bpSimulationPipeLine(self, args):
        self.__Survivor(args)
        self.__Minimap2(args)
        self.__Samtools(args)
        self.__Mosdepth(args)

    def __Survivor(self, args):
        self.__SurvivorDataSimulation(args)
        self.__SurvivorSimRead(args)

    def __SurvivorDataSimulation(self, args):
        parameterFile = args["survivorparamfile"]
        progPath = args["survivor"]
        refFile = args["reffile"]
        simCount = 999
        command = progPath + " simSV " + refFile + " " + parameterFile + " 0.01 0 " + args["outdir"]+"/simulation"
        print(command)
        self.__runCommand(command)
        print("DONE SDS")

    def __SurvivorSimRead(self, args):
        progPath = args["survivor"]
        simulatedFasta = args["outdir"] + "/simulation.fasta"
        errorProfile = args["errorprofile"]
        avg = 10
        destination = args["outdir"] + "/bacreads"
        command = progPath + " simreads " + simulatedFasta + " " + errorProfile + " " + str(avg) + " " + destination
        print(command)
        self.__runCommand(command)
        print("DONE SSR")


    def __Minimap2(self, args):
        #prog = "./minimap2_helper.sh"
        prog = args["minimap2"]
        params = "-a --MD -x map-pb"
        refFile = args["reffile"]
        destination = args["outdir"]
        command = prog +" "+ params+" "+ refFile + " " + destination + "/bacreads > "+destination+"/bacreads_map.sam"
        print(command)
        self.__runCommand(command)
        print("Done MM2")

    def __Samtools(self, args):
        print("Starting Samtools")
        self.__SamtoolsView(args)
        self.__SamtoolsSort(args)
        self.__SamtoolsIndex(args)
        print("Done with Samtools")

    def __SamtoolsView(self, args):
        prog = args["samtools"]
        params = "view -bh"
        destination = args["outdir"]
        command = prog + " " + params + " " + destination + "/bacreads_map.sam > " + destination + "/bacreads_map.bam "
        self.__runCommand(command)

    def __SamtoolsSort(self, args):
        prog = args["samtools"]
        params = "sort"
        destination = args["outdir"]
        command = prog + " " + params + " " + destination + "/bacreads_map.bam >" + destination + "/bacreads_map_sorted.bam "
        self.__runCommand(command)

    def __SamtoolsIndex(self, args):
        prog = args["samtools"]
        params = "index"
        destination = args["outdir"]
        command = prog + " " + params + " " + destination + "/bacreads_map_sorted.bam"
        self.__runCommand(command)

    def __Mosdepth(self, args):
        destination = args["outdir"]
        prog = args["mosdepth"]
        command = prog + " " + destination + "/mosdepth_out" + " " + destination + "/bacreads_map_sorted.bam"
        print(command)
        self.__runCommand(command)

    @staticmethod
    def __runCommand(command):
        subprocess.call(command, shell=True)
