import sys

from ACOUnit import ACORun

def main(args):

	tstSeq, seqFit = ACORun(antSize = 200, generation = 40, seqLength = 100, initP = 200, rho = 0.7, alpha = 0.5, EFGfile = args[0])
	# generation number = 100
	# ant population size = 20
	# seqence length = 20

	print(tstSeq, seqFit)
	# Test sequence export

if __name__ == "__main__":
	args = sys.argv[1:]
	main(args)
