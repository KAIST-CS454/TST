import sys

from ACOUnit import ACORun, RandomRun

def main(args):
	print("ACO")
	tstSeq, seqFit = ACORun(antSize = 20, generation = 200, seqLength = 5, initP = 10, rho = 0.7, alpha = 0.5, EFGfile = args[0])
	print("Random")
	RandomRun(generation = 200, seqLength = 5, EFGfile = args[0])

	#print(tstSeq, seqFit)
	# Test sequence export

if __name__ == "__main__":
	args = sys.argv[1:]
	main(args)
