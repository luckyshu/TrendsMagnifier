import sys

ifile = open('test_dataset.csv', 'r')
ofile = open('median_train_dataset.csv', 'w')
#ofile2 = open('small_test_dataset.csv', 'w')

i = 0

for line in ifile:
    if i <= 100000:
        ofile.write(line)
    else:
        break
    i += 1
    '''
    elif i <= 11000:
        ofile2.write(line)
        '''

ifile.close()
ofile.close()
#ofile2.close()
