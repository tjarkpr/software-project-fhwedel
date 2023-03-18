"""
predictKRR.py
Script zur Vorhersage eines erweitertes Bild anhand des aufgerufenen Modells.
Kann die Frobenius Norm der Differenz bei vorhandenem Referenzbild als Fehler ausgeben.
@param [1] - Bildname im UserIO Ordner.
@param [2] - Referenzbild.
@param [3] - Modellvariante.
"""
# IMPORTE
from PIL import Image
import numpy as np
import sys
import torch
import pickle
import falkon
import timeit

# KONSTANTEN
USERIOPATH = "/var/www/public/uploads/"
MODELPATH = "/data/models/krr/"
IMAGENAME = sys.argv[1]
REFERENCENAME = sys.argv[2]
MODELDATASET = sys.argv[3]

# FUNKTIONEN
def cutOverhead(n):
    if (n > 255):
        return 255
    if (n < 0):
        return 0
    return round(n)

def frobeniusError(true, pred):
    return torch.linalg.norm((true.reshape(-1, 1) - pred.reshape(-1, 1))/255, 'fro')

# ABLAUF
# 1. Bild laden von "/data/images/input/[imageName]"
userImage = Image.open(USERIOPATH +  IMAGENAME).convert('RGB')

# 2. Modell laden von "/data/models/[modellOption]"
model = pickle.load(open(MODELPATH + "model_" + MODELDATASET + ".sav", "rb"))

# 3. Bild umwandeln
userInput = np.array(userImage).reshape(1, -1)
userInput = userInput.astype(float)
userInput = torch.from_numpy(userInput)
mean = userInput.mean()
stddev = userInput.std()
userInput -= mean
userInput /= stddev

# 4. Modell vorhersagen lassen und Zeit messen
std_ref = sys.stderr
sys.stderr = open('/dev/null', 'w')
startTime = timeit.default_timer()
prediction = model.predict(userInput)
stopTime = timeit.default_timer()
sys.stderr = std_ref

# 5. Fehler berechnen und über stdout ausgeben, sowie die Laufzeit
if REFERENCENAME != "False":
    referenceImage = Image.open(USERIOPATH + REFERENCENAME).convert('RGB')
    # Image umwandlung
    referenceInput = np.array(referenceImage).reshape(1, -1)
    referenceInput = torch.from_numpy(referenceInput)
    # Fehlerberechnung
    print("%.3f" % (stopTime - startTime), "%.3f" % frobeniusError(referenceInput, prediction))
else:
    print("%.3f" % (stopTime - startTime))

# 6. Datenumwandlung
prediction = np.array([cutOverhead(x) for x in prediction[0].numpy()])
prediction = prediction.reshape(75,62,3)
prediction = prediction.astype(np.uint8)

# Bild speichern in "/data/images/output/[imageName]"
resultImage = Image.new('RGB', (63,75))
resultImage.paste(Image.fromarray(prediction,'RGB'), (0,0))
resultImage.save(USERIOPATH + IMAGENAME + "_krr_" + MODELDATASET, format='jpeg')
