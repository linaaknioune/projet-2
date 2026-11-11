import json
import os
from typing import Dict

import sklearn
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from donnees import COLONNES_CATEGORIELLES, COLONNES_NUMERIQUES, GRAINE
from exceptions import DonneeInvalideError, ModeleIndisponibleError
from outils import chronometre


