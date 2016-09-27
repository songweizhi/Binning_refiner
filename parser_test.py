import argparse
parser = argparse.ArgumentParser()


parser.add_argument('-i', help='path to input folder')
parser.add_argument('-o', help='path to output folder')
parser.add_argument('-cc', help='contamination cutoff', type=int)
parser.add_argument('-sc', help='bin size cutoff', type=int)

args = parser.parse_args()


print('input folder: %s, type: %s' % (args.i, type(args.i)))
print('output folder: %s, type: %s' % (args.o, type(args.o)))
print('contamination cutoff: %s, type: %s' % (args.cc, type(args.cc)))
print('bin size cutoff: %s, type: %s' % (args.sc, type(args.sc)))




# python3 parser_test.py -cc 50 -sc 500 -o Destop/test/output -i Destop/test/input
# python3 parser_test.py Destop/test/input Destop/test/output -cc 50 -sc 500


