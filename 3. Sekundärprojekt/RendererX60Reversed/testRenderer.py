"""
testRenderer.py
Das Script liest ein KRR-Modell und testet es mit einem übergebene Input.
@param [1] - Pfadangabe des zu trainierenden Modells.
@param [2] - Pfadangabe der Inputdaten - DIREKT.
@param [3] - Pfadangabe der Inputdaten - INDIREKT.
@param [4] - Pfadangabe des Resultats.
@author Tjark Prokoph, Niclas Zeiss, Fynn Thiem.
Im Rahmen des Softwareprojektes WS2020/2021 an der FH Wedel.
"""
#IMPORTE
from PIL import Image
import sys
import numpy as np
import torch
import falkon
import pickle
import time
#KONSTANTEN
CROP_BOX = [(0,0,15,60),(45,0,60,60),(15,0,45,15),(15,45,45,60)]
CROP_BOX_INDIRECT_SIZE = 2700
CROP_PIX_SIZE = 60
CROP_H_SIZE = 32
CROP_V_SIZE = 18
COLOR_CHANS = 3
IMG_START = 1920
#FUNKTIONEN
def cutOverhead(n):
    if (n > 255):
        return 255
    if (n < 0):
        return 0
    return round(n)
def frobeniusError(true, pred):
    return torch.linalg.norm(true.reshape(-1, 1) - pred.reshape(-1, 1), 'fro')/255
#VARIABLEN
modelPath = sys.argv[1]
inputPathDirect = sys.argv[2]
inputPathIndirect = sys.argv[3]
resultPath = sys.argv[4]
testSetSize = CROP_H_SIZE * CROP_V_SIZE
testImgSize = CROP_PIX_SIZE * CROP_PIX_SIZE * COLOR_CHANS
testImgIndirectSize = CROP_BOX_INDIRECT_SIZE * COLOR_CHANS
X = np.empty((testSetSize,testImgSize + testImgIndirectSize))
Y = np.empty((testSetSize,testImgSize))
testSetCounter = 0
#MAIN
print('---- START TESTPROZESS ----')
# 1. Modell laden.
print('Modell laden ...')
flk = pickle.load(open(modelPath, 'rb'))
# 2. Bild erstellen.
new_im = Image.new('RGB', (5760, 1080))
# 3. Daten laden und zuschneiden.
print('Daten laden ...')
directImg = Image.open(inputPathDirect).convert('RGB')
new_im.paste(directImg,(0,0))
indirectImg = Image.open(inputPathIndirect).convert('RGB')
new_im.paste(indirectImg,(3840,0))
for v in range(0, CROP_V_SIZE):
    for h in range(0, CROP_H_SIZE):
        print(' Quadrant (' + str(v) + ';' + str(h) + ') wird geladen ...')
        cropBox = (h * CROP_PIX_SIZE, v * CROP_PIX_SIZE, (h + 1) * CROP_PIX_SIZE, (v + 1) * CROP_PIX_SIZE)
        croppedDirectImg = directImg.crop(cropBox)
        croppedIndirectImg = indirectImg.crop(cropBox)
        Y[testSetCounter] = (np.array(croppedIndirectImg).astype(np.int32) - np.array(croppedDirectImg).astype(np.int32)).flatten()
        hint = []
        for t in range(0, len(CROP_BOX)):
            print('  Crop ' + str(t) + ' ...')
            croppedIndirectImgHint = croppedIndirectImg.crop(CROP_BOX[t])
            croppedDirectImgHint = croppedDirectImg.crop(CROP_BOX[t])
            hint.append((np.array(croppedIndirectImgHint).astype(np.int32) - np.array(croppedDirectImgHint).astype(np.int32)).flatten())
        X[testSetCounter] = np.concatenate((np.array(croppedDirectImg).flatten(), hint[0], hint[1], hint[2], hint[3]))
        testSetCounter = testSetCounter + 1
# 4. Testen der Chunks
print('Daten normalisieren und testen ...')
testSetCounter = 0
# 4.1. Normalisieren der Daten
XI = np.copy(X)
X = torch.from_numpy(X)
Y = torch.from_numpy(Y)
train_mean = X.mean(0, keepdim=True)
train_std = X.std(0, keepdim=True)
X -= train_mean
X /= train_std
X[torch.isnan(X)] = 0
for img in X:
    # 4.2. Ergebnisse berechnen.
    start = time.time()
    test_pred = flk.predict(img.reshape(1, -1))
    end = time.time()
    print("Quadrant " + str(testSetCounter) + ": %.3f Error " % (frobeniusError(Y[testSetCounter], test_pred)) + "%.3f sec." % (end - start))
    # 4.3. Ergebnisse einfügen.
    test_pred = test_pred[0].numpy().astype(np.int32) + XI[testSetCounter][:testImgSize].astype(np.int32)
    test_pred = np.array([cutOverhead(x) for x in test_pred])
    test_pred = test_pred.reshape(CROP_PIX_SIZE,CROP_PIX_SIZE,COLOR_CHANS).astype(np.uint8)
    xPos = IMG_START + (testSetCounter % CROP_H_SIZE) * CROP_PIX_SIZE
    yPos = (testSetCounter // CROP_H_SIZE) * CROP_PIX_SIZE
    new_im.paste(Image.fromarray(test_pred,'RGB'),(xPos,yPos))
    testSetCounter = testSetCounter + 1
# 7. Bild speichern.
print('Bild speichert ...')
new_im.save(resultPath)
print('---- ENDE TESTPROZESS ----')
