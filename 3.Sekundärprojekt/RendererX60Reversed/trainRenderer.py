"""
trainRenderer.py
Das Script trainiert ein zugrunde liegender KRR Modell, welches durch Falkon erstellt wurde. Das Modell wird mit Quadranten eines Bilder trainiert.
@param [1] - Pfadangabe des zu trainierenden Modells.
@param [2] - Pfadangabe des Datensatzes. [RAW, DIREKT, INDIREKT]
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
#KONSTANTEN
CROP_BOX = [(0,0,15,60),(45,0,60,60),(15,0,45,15),(15,45,45,60)]
CROP_BOX_INDIRECT_SIZE = 2700
CROP_PIX_SIZE = 60
CROP_H_SIZE = 32
CROP_V_SIZE = 18
TRAIN_SCENES = 65
COLOR_CHANS = 3
EXTENSION = '.png'
#FUNKTIONEN
def frobeniusError(true, pred):
    return torch.linalg.norm(true.reshape(-1, 1) - pred.reshape(-1, 1), 'fro')/255
#VARIABLEN
modelPath = sys.argv[1]
inputPath = sys.argv[2]
trainSetCounter = 0
trainSetSize = CROP_H_SIZE * CROP_V_SIZE * (TRAIN_SCENES + 1)
trainImgSize = CROP_PIX_SIZE * CROP_PIX_SIZE * COLOR_CHANS
trainImgIndirectSize = CROP_BOX_INDIRECT_SIZE * COLOR_CHANS
X = np.empty((trainSetSize,trainImgSize + trainImgIndirectSize))
Y = np.empty((trainSetSize,trainImgSize))
#MAIN
print('---- START TRAININGSPROZESS ----')
# 1. KRR Modell laden.
print('Modell laden ...')
flk = pickle.load(open(modelPath, 'rb'))
# 2. Trainingsdaten laden und zuschneiden.
print('Trainingsdaten laden ...')
for i in range(0, TRAIN_SCENES + 1):
    print(' Datensatz ' + str(i) + ' wird geladen ...')
    directImg = Image.open(inputPath + '/direct/' + str(i).zfill(4) + EXTENSION).convert('RGB')
    indirectImg = Image.open(inputPath + '/indirect/' + str(i).zfill(4) + EXTENSION).convert('RGB')
    for v in range(0, CROP_V_SIZE):
        for h in range(0, CROP_H_SIZE):
            print('  Quadrant (' + str(v) + ';' + str(h) + ') wird geladen ...')
            cropBox = (h * CROP_PIX_SIZE, v * CROP_PIX_SIZE, (h + 1) * CROP_PIX_SIZE, (v + 1) * CROP_PIX_SIZE)
            croppedDirectImg = directImg.crop(cropBox)
            croppedIndirectImg = indirectImg.crop(cropBox)
            Y[trainSetCounter] = (np.array(croppedIndirectImg).astype(np.int32) - np.array(croppedDirectImg).astype(np.int32)).flatten()
            hint = []
            for t in range(0, len(CROP_BOX)):
                print('  Crop ' + str(t) + ' ...')
                croppedIndirectImgHint = croppedIndirectImg.crop(CROP_BOX[t])
                croppedDirectImgHint = croppedDirectImg.crop(CROP_BOX[t])
                hint.append((np.array(croppedIndirectImgHint).astype(np.int32) - np.array(croppedDirectImgHint).astype(np.int32)).flatten())
            X[trainSetCounter] = np.concatenate((np.array(croppedDirectImg).flatten(), hint[0], hint[1], hint[2], hint[3]))
            trainSetCounter = trainSetCounter + 1

# 3. Konvertieren der Daten.
print('Daten werden vorbereitet ...')
X = torch.from_numpy(X)
Y = torch.from_numpy(Y)
# 4. Normalisieren der Daten.
train_mean = X.mean(0, keepdim=True)
train_std = X.std(0, keepdim=True)
X -= train_mean
X /= train_std
X[torch.isnan(X)] = 0
# 5. Trainieren des Modells.
print('Modell trainiert ...')
print('----------------')
flk.fit(X, Y)
train_pred = flk.predict(X)
print('----------------')
print("Training Frobenius: %.3f" % (frobeniusError(Y, train_pred)))
# 6. KRR Modell speichern.
print('Modell speichert ...')
pickle.dump(flk, open(modelPath, 'wb'))
print('---- ENDE TRAININGSPROZESS ----')
