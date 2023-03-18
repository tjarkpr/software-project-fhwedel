"""
createKRRModel.py
Das Script erstellt ein KRR-Modell mit dem Falkon Framework.
Das KRR-Modell soll erstellt und in einer Datei gespeichert werden, um es später trainieren und testen zu können.
@param [1] - Pfadangabe des zu trainierenden Modells.
@author Tjark Prokoph, Niclas Zeiss, Fynn Thiem.
Im Rahmen des Softwareprojektes WS2020/2021 an der FH Wedel.
"""
# IMPORTE
import sys
import numpy as np
import torch
import falkon
import pickle

# KONSTANTEN
model_Path = sys.argv[1]
input_Sigma = 43000.0
input_Penalty = 9e-9
input_M = 22000
options = falkon.options.FalkonOptions(debug=True)

# ABLAUF
# 1. Erstellen eines Modells mit FalkonML
kernel = falkon.kernels.LaplacianKernel(sigma=input_Sigma)
flk = falkon.Falkon(options=options, maxiter=2, kernel=kernel, penalty=input_Penalty, M=input_M)

# 2. Speichern des Modells in einer lokalen Datei
if (model_Path is None):
	model_Path = '.'
pickle.dump(flk, open(model_Path + '/KRRModel.sav', 'wb'))
