"""
testKRRModel.py
Das Script liest ein KRR-Modell und testet es mit einem übergebene Input.
@param [1] - Pfadangabe des zu trainierenden Modells.
@param [2] - Pfadangabe des Inputbildes.
@param [3] - Pfadangabe des Outputvergleichsbildes.
@param [4] - Pfadangabe des Resultats.
@author Tjark Prokoph, Niclas Zeiss, Fynn Thiem.
Im Rahmen des Softwareprojektes WS2020/2021 an der FH Wedel.
"""
# IMPORTE
from PIL import Image
import numpy as np
import sys
import torch
import pickle
import falkon

# FUNKTIONEN
def cutOverhead(n):
    if (n > 255):
        return 255
    if (n < 0):
        return 0
    return round(n)

def frobeniusError(true, pred):
    return torch.linalg.norm(true.reshape(-1, 1) - pred.reshape(-1, 1), 'fro')

# VARIABLEN
test_ModelPath = sys.argv[1]
testX_ImagePath = sys.argv[2]
testY_ImagePath = sys.argv[3]
savePath = sys.argv[4]

# ABLAUF
# 1. Modell(.sav) laden - vorher durch create-Script erstellt und trainiert
if (test_ModelPath is None):
	test_ModelPath = '.'
flk = pickle.load(open(test_ModelPath + '/KRRModel.sav', 'rb'))

# 2. Testdaten laden aus dem Testordner
X_Input = np.array(Image.open(testX_ImagePath).convert('RGB'))
Y_Input = np.array(Image.open(testY_ImagePath).convert('RGB'))
X = X_Input.reshape(1, -1)
Y = Y_Input.reshape(1, -1)

# 3. Konvertieren numpy -> pytorch
Ytest = torch.from_numpy(Y)
Xtest = torch.from_numpy(X)

# 4. Testen
test_pred = flk.predict(Xtest)
print("Test Frobenius: %.3f" % (frobeniusError(Ytest, test_pred)))

# 5. Datenumwandlung
test_pred = np.array([cutOverhead(x) for x in test_pred[0].numpy()])
test_pred = test_pred.reshape(75,62, 3)
test_pred = test_pred.astype(np.uint8)

# 6. Bild speichern
new_im = Image.new('RGB', (164, 75))
new_im.paste(Image.fromarray(X_Input,'RGB'),(0,0))
new_im.paste(Image.fromarray(test_pred,'RGB'),(40,0))
new_im.paste(Image.fromarray(Y_Input,'RGB'),(102,0))
new_im.save(savePath + '/result.jpg')
