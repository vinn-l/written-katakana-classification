import struct
import numpy as np
from matplotlib import pyplot as plt
import math
from sklearn.svm import LinearSVC

size_record = 2952

def read_record(f):
    pixels = []
    s = f.read(size_record)
    str_data = struct.unpack_from('>2736s',s,216)[0]

    offset = 0
    while offset < len(str_data):

        byte = bin(int(str_data[offset]))[2:].zfill(8)
        pixels.append(byte[0:4])
        pixels.append(byte[4:8])
        offset = offset + 1
    pixels = [float(x) for x in pixels]
    return pixels


def read_hiragana():
    # 51: number of katakana characters
    # 208: number of images for each katakana
    # 50*50: image size
    arr = np.zeros([51,208, 50,50], dtype=np.float32)
    filename = 'ETL5C'
    with open(filename, 'rb') as f:
        for i in range(10608):
        # for i in range(500):
            pixels_arr = np.array(read_record(f))
            pic = np.reshape(pixels_arr,(76,72)).astype(np.float32)
            pic = pic[10:60,10:60]
            # plt.imshow(pic, cmap='gray', interpolation='nearest')
            # plt.savefig("pic{:04d}.png".format(i))
            # print("{:04d} finished.".format(i))
            #

                # plt.show()
            # if i%208==0:
            #     plt.imshow(pic, cmap='gray', interpolation='nearest')
            #     plt.savefig("pic{:04d}.png".format(math.floor(i/208)))
            arr[math.floor(i/208),i%208]= pic
    return arr

def training(arr):
    # prepare X and y
    train_sz = 100
    test_sz = 10
    X = np.zeros([train_sz*51, 50*50], dtype=np.float32)
    Xte = np.zeros([test_sz*51, 50*50], dtype=np.float32)

    # get training matrix X, training label y, testing matrix Xte, testing label yte
    for i in range(51):
         train_pics = arr[i,0:train_sz,:,:]
         train_tuples = np.reshape(train_pics,(train_sz,50*50))
         X[i*train_sz:(i+1)*train_sz,:] = train_tuples

         test_pics = arr[i,train_sz:train_sz+test_sz,:,:]
         test_tuples = np.reshape(test_pics,(test_sz,50*50))
         Xte[i*test_sz:(i+1)*test_sz,:] = test_tuples

    y = np.zeros([train_sz*51])
    yte = np.zeros([test_sz*51])

    for i in range(train_sz*51):
        y[i] = math.floor(i/train_sz)

    for i in range(test_sz*51):
        yte[i] = math.floor(i/test_sz)
    print(Xte)
    clf = LinearSVC()
    clf.fit(X, y)

    Xte_res = clf.predict(Xte)

    #print out predict results and compare
    for i in range(len(yte)):
        print("{} ------ {}".format(Xte_res[i],yte[i]))



         # plt.imshow(samples[100], cmap='gray', interpolation='nearest')
         # plt.show()
#             plt.savefig("pic{:04d}.png".format(i)) #save image as file
#             print("{:04d} finished.".format(i))

def main():
    arr = read_hiragana()
    training(arr)

if __name__ == "__main__":
    main()
