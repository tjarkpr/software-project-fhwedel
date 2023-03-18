"""
hypertuning.py
Trainiert ein übergebenes Falkon Modell mit verschiedenen Paramterern, die im Vorweg definiert wurden (Hypertuning).
Das Script entscheidet aufgrund der Frobenius Norm der Differenz, welche Parameter den geringsten Fehler produzieren und wendet diese dann final auf das Skript an.
@param [1] - Pfadangabe des zu trainierenden Modells.
@param [2] - Pfadangabe der Inputbilder.
@param [3] - Pfadangabe der Outputvergleichsbilder.
@author Tjark Prokoph, Niclas Zeiss, Fynn Thiem.
Im Rahmen des Softwareprojektes WS2020/2021 an der FH Wedel.
"""
# IMPORTE
import sys
import torch
import os
import falkon
import glob
import pickle
import numpy as np
from sklearn import model_selection, metrics
from PIL import Image

# KONSTANTEN
trainImageX_Path = sys.argv[2]
trainImageY_Path = sys.argv[3]
trainModel_Path = sys.argv[1]
parameter_grid = {
    'kernel': [falkon.kernels.LaplacianKernel(sigma=43000),falkon.kernels.LaplacianKernel(sigma=41000),falkon.kernels.LaplacianKernel(sigma=45000)],
    'penalty': [9e-9,1e-10,8e-9],
    'maxiter': [1],
    'M': [20000,22000],
}
frob_scorer = metrics.make_scorer(frobenius, greater_is_better=False)
TRAINSET_SIZE = 50000
TRAINTESTCUT = 0.8

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
trainImputCounter = 0
X = np.empty((TRAINSET_SIZE,5880))
Y = np.empty((TRAINSET_SIZE,13950))

# ABLAUF
# 1. Modell(.sav) laden - vorher durch create-Script erstellt
if (trainModel_Path is None):
	trainModel_Path = '.'
flk = pickle.load(open(trainModel_Path + '/KRRModel.sav', 'rb'))

# 2. Trainingsdaten laden aus dem Trainingsordnern laden
files = []
files.extend(glob.iglob(trainImageX_Path + '*.jpg'))
files.extend(glob.iglob(trainImageX_Path + '*.png'))
for f in files:
    # Trainingsinput
    tempImg = Image.open(f)
    X[trainImputCounter] = np.array(tempImg.convert('RGB')).flatten()
    # Trainingsoutput
    tempImg = Image.open(trainImageY_Path + os.path.basename(f))
    Y[trainImputCounter] = np.array(tempImg.convert('RGB')).flatten()
    # Maximale Trainingsdatenbegrenzung
    trainImputCounter += 1
    if trainImputCounter == TRAINSET_SIZE:
        break

# 3. Output-Bilderfolge erstellen (100 Bilder, je 3 Vergleichbilder)
new_im = Image.new('RGB', (328, 7500))

# 4. Trainingsdaten vorbereiten
X = np.array(X)
Y = np.array(Y)
num_train = int(X.shape[0] * TRAINTESTCUT)
num_test = X.shape[0] - num_train
shuffle_idx = np.arange(X.shape[0])
np.random.shuffle(shuffle_idx)
train_idx = shuffle_idx[:num_train]
test_idx = shuffle_idx[num_train:]
XtrainI, YtrainI = X[train_idx], Y[train_idx]
XtestI, YtestI = X[test_idx], Y[test_idx]

# 5. Konvertieren numpy -> pytorch
Xtrain = torch.from_numpy(X[train_idx])
Ytrain = torch.from_numpy(Y[train_idx])
Xtest = torch.from_numpy(X[test_idx])
Ytest = torch.from_numpy(Y[test_idx])

# 6. Input und Vergleichsoutput Bilder visualisieren
for i in range(0,100):
    XtestII = XtestI[i].reshape(49,40,3)
    XtestII = XtestII.astype(np.uint8)
    YtestII = YtestI[i].reshape(75,62,3)
    YtestII = YtestII.astype(np.uint8)
    XtrainII = XtrainI[i].reshape(49,40,3)
    XtrainII = XtrainII.astype(np.uint8)
    YtrainII = YtrainI[i].reshape(75,62,3)
    YtrainII = YtrainII.astype(np.uint8)
    new_im.paste(Image.fromarray(XtrainII,'RGB'),(0,i * 75))
    new_im.paste(Image.fromarray(YtrainII,'RGB'),(102,i * 75))
    new_im.paste(Image.fromarray(XtestII,'RGB'),(164,i * 75))
    new_im.paste(Image.fromarray(YtestII,'RGB'),(266,i * 75))

# 7. Normalisierung
train_mean = Xtrain.mean(0, keepdim=True)
train_std = Xtrain.std(0, keepdim=True)
Xtrain -= train_mean
Xtrain /= train_std
Xtest -= train_mean
Xtest /= train_std

# 8. Hyperparametertuning über GridSearchCV
grid_search = model_selection.GridSearchCV(flk, parameter_grid, frob_scorer, cv=5)
print('Hypertraining beginnt!')
grid_search.fit(Xtrain, Ytrain)
print("Die besten Parameter sind: ", grid_search.best_params_)
print('Hypertraining abgeschlossen!')

# 9. Modell mit neunen Parametern trainieren
print('Training beginnt!')
flk = grid_search.best_estimator_
flk.fit(Xtrain, Ytrain)
print('Training abgeschlossen!')

# 10. Ergebnisse überprüfen
test_pred = flk.predict(Xtest)
train_pred = flk.predict(Xtrain)
print("Training Frobenius: %.3f" % (frobenius(Ytrain, train_pred)))
print("Test Frobenius: %.3f" % (frobenius(Ytest, test_pred)))

# 11. Ergebnisse visualisieren und abspeichern
for i in range(0,100):
    test_predI = np.array([cut(x) for x in test_pred[i].numpy()])
    test_predI = test_predI.reshape(75,62,3)
    test_predI = test_predI.astype(np.uint8)
    train_predI = np.array([cut(x) for x in train_pred[i].numpy()])
    train_predI = train_predI.reshape(75,62,3)
    train_predI = train_predI.astype(np.uint8)

    new_im.paste(Image.fromarray(train_predI,'RGB'),(40,i * 75))
    new_im.paste(Image.fromarray(test_predI,'RGB'),(204,i * 75))

new_im.save('./hyperTrainResult.jpg')

# 12. Modell speichern
pickle.dump(flk, open(trainModel_Path + '/KRRModel.sav', 'wb'))
