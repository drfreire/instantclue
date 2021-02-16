from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import * #works for pyqt5
from .resortableTable import ResortableTable
from .warnMessage import WarningMessage
from ..delegates.dataTreeViewDelegates import *
from ..utils import createSubMenu, createMenu, createMenus
from ..dialogs.selectionDialog import SelectionDialog
from ..dialogs.ICGrouper import ICGrouper
from ..dialogs.ICCompareGroups import ICCompareGroups
from ..dialogs.ICModel import ICModelBase
import pandas as pd
import numpy as np

dataTypeSubMenu = {
    "Numeric Floats": [
        ("main",["Column operation ..",
                "Sorting",
                "Value Transformation",
                "Data Format Transformation", 
                "Feature Selection", 
                "Filter",
                "Clustering",
                "Model Fitting",
                "Group Comparison",
                ]),
        ("Value Transformation",["Logarithmic","Normalization (row)","Normalization (column)","Smoothing","Density Estimation","Dimensional Reduction","Summarize"]),
        ("Data Format Transformation",[]),
        ("Filter",["NaN Filter","Outlier"]),
        ("Clustering",["k-means"]),
        ("Smoothing",["Aggregate rows ..","Rolling window .."]),
        ("Density Estimation", ["Kernel Density"]),
        ("Column operation ..", ["Change data type to ..","Missing values (NaN)"]),
        ("Feature Selection", ["Model ..","Recursive Elimination .."]),
        ("Model Fitting",["Kinetic"]),
        ("Missing values (NaN)",["Replace NaN by .."]),
        ("Replace NaN by ..",["Iterative Imputer"]),
        ("Group Comparison",["Pairwise Tests","Multiple Groups","Summarize Groups"])
        ],
    "Integers" : [
        ("main",["Column operation ..","Sorting"]),
        ("Column operation ..", ["Change data type to .."])
        ],
    "Categories" : [
        ("main",["Column operation ..","Sorting","Data Format Transformation", "Filter","(Prote-)omics-toolkit"]),
        ("Column operation ..", ["Change data type to ..","String operation"]),
        ("String operation",["Split on .."]),
        ("Filter",["To QuickSelect .."]),
        ("(Prote-)omics-toolkit", ["Match to db.."])
        ]
}


menuBarItems = [
    {
        "subM":"Group Comparison",
        "name":"Annotate Groups",
        "funcKey": "createGroups",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"Pairwise Tests",
        "name":"t-test",
        "funcKey": "compareGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"test":"t-test"}
    },
    {
        "subM":"Pairwise Tests",
        "name":"Welch-test",
        "funcKey": "compareGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"test":"welch-test"}
    },
    {
        "subM":"Multiple Groups",
        "name":"1W-ANOVA",
        "funcKey": "compareGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"test":"1W-ANOVA"}
    },
        {
        "subM":"Multiple Groups",
        "name":"2W-ANOVA",
        "funcKey": "compareGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"test":"2W-ANOVA"}
    },
    {
        "subM":"Pairwise Tests",
        "name":"Euclidean distance",
        "funcKey": "compareGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"test":"euclidean"}
    },
    {
        "subM":"Summarize Groups",
        "name":"min",
        "funcKey": "summarizeGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"metric":"min"}
    },
    {
        "subM":"Summarize Groups",
        "name":"mean",
        "funcKey": "summarizeGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"metric":"mean"}
    },
    {
        "subM":"Summarize Groups",
        "name":"median",
        "funcKey": "summarizeGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"metric":"median"}
    },
    {
        "subM":"Summarize Groups",
        "name":"max",
        "funcKey": "summarizeGroups",
        "dataType": "Numeric Floats",
        "fnKwargs":{"metric":"max"}
    },
    
    {
        "subM":"Logarithmic",
        "name":"ln",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"logarithmic","base":"ln"}
    },
    {
        "subM":"Logarithmic",
        "name":"log2",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"logarithmic","base":"log2"}
    },
    {
        "subM":"Logarithmic",
        "name":"log10",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"logarithmic","base":"log10"}
    },
    {
        "subM":"Logarithmic",
        "name":"-log2",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"logarithmic","base":"-log2"}
    },
    {
        "subM":"Logarithmic",
        "name":"-log10",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"logarithmic","base":"-log10"}
    },
    
    {
        "subM":"Summarize",
        "name":"max",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"summarize","metric":"max"}
    },
    {
        "subM":"Summarize",
        "name":"75% quantile",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"summarize","metric":"quantile","q":0.75}
    },
    {
        "subM":"Summarize",
        "name":"mean",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"summarize","metric":"mean"}
    },
    {
        "subM":"Summarize",
        "name":"50% quantile (median)",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"summarize","metric":"median"}
    },
    {
        "subM":"Summarize",
        "name":"25% quantile",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"summarize","metric":"quantile","q":0.25}
    },
    {
        "subM":"Summarize",
        "name":"min",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transformKey":"summarize","metric":"min"}
    },
    {
        "subM":"Kernel Density",
        "name":"gaussian",
        "funcKey": "data::kernelDensity",
        "dataType": "Numeric Floats",
        "fnKwargs":{"kernel":"gaussian"}
    },
    {
        "subM":"Kernel Density",
        "name":"tophat",
        "funcKey": "data::kernelDensity",
        "dataType": "Numeric Floats",
        "fnKwargs":{"kernel":"tophat"}
    },

    #‘gaussian’|’tophat’|’epanechnikov’|’exponential’|’linear’|’cosine
    {
        "subM":"Sorting",
        "name":"Value",
        "funcKey": "data::sortData",
        "dataType": "All"
    },
    {
        "subM":"Sorting",
        "name":"Custom",
        "funcKey": "customSorting",
        "dataType": ["Integers","Categories"]
    },
    {
        "subM":"Filter",
        "name":"Numeric Filtering",
        "funcKey": "applyFilter",
        "dataType": "Numeric Floats"
    },
    {
        "subM":"Smoothing",
        "name":"IIR Filter",
        "funcKey": "data::transformData",
        "dataType": "Numeric Floats"
    },
    {
        "subM":"Data Format Transformation",
        "name":"To long format (melt)",
        "funcKey": "data::meltData",
        "dataType": "All"
    },
    {
        "subM":"Data Format Transformation",
        "name":"Unstack Column",
        "funcKey": "data::unstackColumn",
        "dataType": "Categories"
    },
    {
        "subM":"Data Format Transformation",
        "name":"Row Correlation Matrix",
        "funcKey": "stats::rowCorrelation",
        "dataType": "Numeric Floats"
    },
    {
        "subM":"Value Transformation",
        "name":"Absolute values",
        "funcKey": "transformer::transformData",
        "dataType": "Numeric Floats",
        "fnKwargs": {"transformKey":"absolute"}
    },
    
    {
        "subM":"Dimensional Reduction",
        "name":"PCA (Loadings)",
        "funcKey": "dimReduction::PCA",
        "dataType": "Numeric Floats"
    },
    {
        "subM":"Dimensional Reduction",
        "name":"PCA (Projection)",
        "funcKey": "dimReduction::PCA",
        "dataType": "Numeric Floats",
        "fnKwargs":{"returnProjections":True}
    },
    # {
    #     "subM":"Dimensional Reduction",
    #     "name":"CVAE",
    #     "funcKey": "dimReduction::CVAE",
    #     "dataType": "Numeric Floats"
    # },
    {
        "subM":"Dimensional Reduction",
        "name":"UMAP",
        "funcKey": "dimReduction::UMAP",
        "dataType": "Numeric Floats"
    },
    {
        "subM":"Dimensional Reduction",
        "name":"UMAP.T",
        "funcKey": "dimReduction::UMAP",
        "dataType": "Numeric Floats",
        "fnKwargs":{"transpose":True}
    },
    {
        "subM":"Dimensional Reduction",
        "name":"t-SNE",
        "funcKey": "dimReduction::TSNE",
        "dataType": "Numeric Floats"
    },
    {
        "subM":"Data Format Transformation",
        "name":"Pivot Table",
        "funcKey": "getUserInput",
        "dataType": "Categories",
        "fnKwargs": {"funcKey":"data::pivotTable",
                    "requiredColumns": ["indexColumn","columnNames"]}
    },
    {
        "subM":"Normalization (row)",
        "name":"Standardize (Z-Score)",
        "funcKey": "normalizer::normalizeData",
        "dataType": "Numeric Floats",
        "fnKwargs": {"normKey": "Standardize (Z-Score)"}
    },
    {
        "subM":"Normalization (row)",
        "name":"Scale (0 - 1)",
        "funcKey": "normalizer::normalizeData",
        "dataType": "Numeric Floats",
        "fnKwargs": {"normKey": "Scale (0 - 1)"}
    },
    {
        "subM":"Normalization (row)",
        "name":"Quantile (25 - 75)",
        "funcKey": "normalizer::normalizeData",
        "dataType": "Numeric Floats",
        "fnKwargs": {"normKey": "Quantile (25 - 75)"}
    },
    {
        "subM":"Normalization (row)",
        "name":"Row Loess Fit Correction",
        "funcKey": "normalizer::normalizeData",
        "dataType": "Numeric Floats",
        "fnKwargs": {"normKey": "loessRowNorm"}
    },
    {
        "subM":"Normalization (column)",
        "name":"Standardize (Z-Score)",
        "funcKey": "normalizer::normalizeData",
        "dataType": "Numeric Floats",
        "fnKwargs": {"normKey": "Standardize (Z-Score)","axis": 0}
    },
    {
        "subM":"Normalization (column)",
        "name":"Scale (0 - 1)",
        "funcKey": "normalizer::normalizeData",
        "dataType": "Numeric Floats",
        "fnKwargs": {"normKey": "Scale (0 - 1)","axis": 0}
    },
    {
        "subM":"Normalization (column)",
        "name":"Quantile (25 - 75)",
        "funcKey": "normalizer::normalizeData",
        "dataType": "Numeric Floats",
        "fnKwargs": {"normKey": "Quantile (25 - 75)","axis": 0}
    },
    {
        "subM":"Change data type to ..",
        "name":"Numeric Floats",
        "funcKey": "data::changeDataType",
        "fnKwargs": {"newDataType":"float64"},
        "dataType": ["Integers","Categories"]
    },
    {
        "subM":"Change data type to ..",
        "name":"Integers",
        "funcKey": "data::changeDataType",
        "fnKwargs": {"newDataType":"int64"},
        "dataType": ["Numeric Floats","Categories"]
    },
    {
        "subM":"Change data type to ..",
        "name":"Categories",
        "funcKey": "data::changeDataType",
        "fnKwargs": {"newDataType":"str"},
        "dataType": ["Numeric Floats","Integers"]
    },
    {
        "subM":"Filter",
        "name":"Categorical Filter",
        "funcKey": "applyFilter",
        "dataType": "Categories"
    },
    {
        "subM":"Filter",
        "name":"Find string(s)",
        "funcKey": "applyFilter",
        "dataType": "Categories",
        "fnKwargs": {"filterType":"string"}
    },
    {
        "subM":"Column operation ..",
        "name":"Combine columns",
        "funcKey": "data::combineColumns",
        "dataType": "All",
    },
    {
        "subM":"Column operation ..",
        "name":"Duplicate column(s)",
        "funcKey": "data::duplicateColumns",
        "dataType": "All",
    },
    {
        "subM":"Column operation ..",
        "name":"Factorize column(s)",
        "funcKey": "data::factorizeColumns",
        "dataType": "Categories",
    },
    {
        "subM":"Missing values (NaN)",
        "name":"Count",
        "funcKey": "data::countNaN",
        "dataType": "Numeric Floats",
    },
    
    {
        "subM":"NaN Filter",
        "name":"Any == NaN",
        "funcKey": "data::removeNaN",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"NaN Filter",
        "name":"All == NaN",
        "funcKey": "data::removeNaN",
        "dataType": "Numeric Floats",
        "fnKwargs": {"how":"all"}
    },
    {
        "subM":"NaN Filter",
        "name":"Threshold",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"data::removeNaN", 
                      "info":"Provide the number of non-NaN values.\nIf value < 1 the fraction of selected columns is considered.",
                      "min": 0.0,
                      "max": "nColumns",
                      "requiredFloat":"thresh"}
    },
    {
        "subM":"NaN Filter",
        "name":"Group positives",
        "funcKey": "grouping::exclusivePositives",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"NaN Filter",
        "name":"Group negatives",
        "funcKey": "grouping::exclusiveNegative",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"Split on ..",
        "name":"Space ( )",
        "funcKey": "data::splitColumnsByString",
        "dataType": "Categories",
        "fnKwargs": {"splitString":" "}
    },
    {
        "subM":"Split on ..",
        "name":"Semicolon (;)",
        "funcKey": "data::splitColumnsByString",
        "dataType": "Categories",
        "fnKwargs": {"splitString":";"}
    },
    {
        "subM":"Split on ..",
        "name":"Underscore (_)",
        "funcKey": "data::splitColumnsByString",
        "dataType": "Categories",
        "fnKwargs": {"splitString":"_"}
    },
    {
        "subM":"Split on ..",
        "name":"Comma (,)",
        "funcKey": "data::splitColumnsByString",
        "dataType": "Categories",
        "fnKwargs": {"splitString":","}
    },
    {
        "subM":"Split on ..",
        "name":"Custom string",
        "funcKey": "getUserInput",
        "dataType": "Categories",
        "fnKwargs" : {"funcKey":"data::splitColumnsByString", 
                      "info":"Provide split string to separate strings in a column.",
                      "requiredStr":"splitString",
                      }
    },
    {
        "subM":"To QuickSelect ..",
        "name":"Raw values",
        "funcKey": "sendSelectionToQuickSelect",
        "dataType": "Categories",
        "fnKwargs" : {"mode" : "raw"}
    },
    {
        "subM":"To QuickSelect ..",
        "name":"Unique Categories",
        "funcKey": "sendSelectionToQuickSelect",
        "dataType": "Categories",
    },
    {
        "subM":"Recursive Elimination ..",
        "name":"Random Forest",
        "funcKey": "featureSelection",
        "dataType": "Numeric Floats",
        "fnKwargs": {"RFEVC":True}
    },
    {
        "subM":"Recursive Elimination ..",
        "name":"SVM (linear)",
        "funcKey": "featureSelection",
        "dataType": "Numeric Floats",
        "fnKwargs": {"RFEVC":True}
    },
    # {
    #     "subM":"Recursive Elimination ..",
    #     "name":"SVM (rbf)",
    #     "funcKey": "featureSelection",
    #     "dataType": "Numeric Floats",
    #     "fnKwargs": {"RFEVC":True}
    # },
    # {
    #     "subM":"Recursive Elimination ..",
    #     "name":"SVM (poly)",
    #     "funcKey": "featureSelection",
    #     "dataType": "Numeric Floats",
    #     "fnKwargs": {"RFEVC":True}
    # },
    {
        "subM":"Model ..",
        "name":"Random Forest",
        "funcKey": "featureSelection",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"Model ..",
        "name":"SVM (linear)",
        "funcKey": "featureSelection",
        "dataType": "Numeric Floats",
    },
#    {
#        "subM":"Model ..",
#        "name":"SVM (rbf)",
#        "funcKey": "featureSelection",
#        "dataType": "Numeric Floats",
#    },
#    {
#        "subM":"Model ..",
#        "name":"SVM (poly)",
#        "funcKey": "featureSelection",
#        "dataType": "Numeric Floats",
#    },
    {
        "subM":"Model ..",
        "name":"False Positive Rate",
        "funcKey": "featureSelection",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"Model ..",
        "name":"False Discovery Rate",
        "funcKey": "featureSelection",
        "dataType": "Numeric Floats",
    },  
    {
        "subM":"Aggregate rows ..",
        "name":"Mean",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"data::aggregateNRows", 
                      "info":"Provide window size (n) for aggregation.\nA window of 50 rows will be aggregated using selected metric.",
                      "min": 2,
                      "max": "nDataRows",
                      "requiredInt":"n",
                      "otherKwargs":{"metric":"mean"}}
    },
    {
        "subM":"Rolling window ..",
        "name":"mean",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"transformer::transformData", 
                      "info":"Provide rolling window size.\nA rolling window of 50 rows will be used.",
                      "min": 2,
                      "max": "nDataRows",
                      "requiredInt":"windowSize",
                      "otherKwargs":{"transformKey":"rolling","metric":"mean"}}
    },
    {
        "subM":"Rolling window ..",
        "name":"median",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"transformer::transformData", 
                      "info":"Provide rolling window size.\nA rolling window of 50 rows will be used.",
                      "min": 2,
                      "max": "nDataRows",
                      "requiredInt":"windowSize",
                      "otherKwargs":{"transformKey":"rolling","metric":"median"}}
    },
    {
        "subM":"Rolling window ..",
        "name":"sum",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"transformer::transformData", 
                      "info":"Provide rolling window size.\nA rolling window of 50 rows will be used.",
                      "min": 2,
                      "max": "nDataRows",
                      "requiredInt":"windowSize",
                      "otherKwargs":{"transformKey":"rolling","metric":"sum"}}
    },
    {
        "subM":"Rolling window ..",
        "name":"standard deviation",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"transformer::transformData", 
                      "info":"Provide rolling window size.\nA rolling window of 50 rows will be used.",
                      "min": 2,
                      "max": "nDataRows",
                      "requiredInt":"windowSize",
                      "otherKwargs":{"transformKey":"rolling","metric":"std"}}
    },
    {
        "subM":"Rolling window ..",
        "name":"max",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"transformer::transformData", 
                      "info":"Provide rolling window size.\nA rolling window of 50 rows will be used.",
                      "min": 2,
                      "max": "nDataRows",
                      "requiredInt":"windowSize",
                      "otherKwargs":{"transformKey":"rolling","metric":"max"}}
    },
    {
        "subM":"Rolling window ..",
        "name":"min",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"transformer::transformData", 
                      "info":"Provide rolling window size.\nA rolling window of 50 rows will be used.",
                      "min": 2,
                      "max": "nDataRows",
                      "requiredInt":"windowSize",
                      "otherKwargs":{"transformKey":"rolling","metric":"min"}}
    },
    {   
        "subM":"Replace NaN by ..",
        "name":"Row mean",
        "funcKey": "data::fillNa",
        "dataType": "Numeric Floats",
        "fnKwargs": {"fillBy":"Row mean"}
    },
    {
        "subM":"Replace NaN by ..",
        "name":"Row median",
        "funcKey": "data::fillNa",
        "dataType": "Numeric Floats",
        "fnKwargs": {"fillBy":"Row median"}
    },
    {
        "subM":"Replace NaN by ..",
        "name":"Column mean",
        "funcKey": "data::fillNa",
        "dataType": "Numeric Floats",
        "fnKwargs": {"fillBy":"Column mean"}
    },
    {
        "subM":"Replace NaN by ..",
        "name":"Column median",
        "funcKey": "data::fillNa",
        "dataType": "Numeric Floats",
        "fnKwargs": {"fillBy":"Column median"}
    },
    {
        "subM":"Replace NaN by ..",
        "name":"Gaussian distribution",
        "funcKey": "featureSelection",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"Replace NaN by ..",
        "name":"Smart Group Replace",
        "funcKey": "smartReplace",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"Kinetic",
        "name":"First Order",
        "funcKey": "fitModel",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"Outlier",
        "name":"Remove outliers (Group)",
        "funcKey": "removeOutliersFromGroup",
        "dataType": "Numeric Floats",
    },
    {
        "subM":"Outlier",
        "name":"Remove outliers (Selection)",
        "funcKey": "data::replaceOutlierWithNaN",
        "dataType": "Numeric Floats"
    },
     {
        "subM":"Clustering",
        "name":"HDBSCAN",
        "funcKey": "stats::runHDBSCAN",
        "dataType": "Numeric Floats"
    },
    {
        "subM":"k-means",
        "name":"Elbow method",
        "funcKey": "stats::kmeansElbow",
        "dataType": "Numeric Floats"
    },
    {
        "subM":"k-means",
        "name":"K-Means",
        "funcKey": "getUserInput",
        "dataType": "Numeric Floats",
        "fnKwargs" : {"funcKey":"stats::runKMeans", 
                      "info":"Provide number of clusters (k).",
                      "min": 2,
                      "max": "nDataRows",
                      "requiredInt":"k"}
    },
    {
        "subM":"Iterative Imputer",
        "name":"BayesianRidge",
        "funcKey": "data::imputeByModel",
        "dataType": "Numeric Floats",
        "fnKwargs": {"estimator":"BayesianRidge"}
    },
    {
        "subM":"Iterative Imputer",
        "name":"DecisionTreeRegressor",
        "funcKey": "data::imputeByModel",
        "dataType": "Numeric Floats",
        "fnKwargs": {"estimator":"DecisionTreeRegressor"}
    },
    {
        "subM":"Iterative Imputer",
        "name":"ExtraTreesRegressor",
        "funcKey": "data::imputeByModel",
        "dataType": "Numeric Floats",
        "fnKwargs": {"estimator":"ExtraTreesRegressor"}
    },
    {
        "subM":"Iterative Imputer",
        "name":"KNeighborsRegressor",
        "funcKey": "data::imputeByModel",
        "dataType": "Numeric Floats",
        "fnKwargs": {"estimator":"KNeighborsRegressor"}
    },
]

class DataTreeView(QWidget):
    def __init__(self,parent=None, mainController = None, sendToThreadFn = None, dataID = None, tableID = None):
        super(DataTreeView, self).__init__(parent)
        self.tableID = tableID
        self.mC = mainController
        self.__controls()
        self.__layout()
        self.__connectEvents()
        self.sendToThreadFn = sendToThreadFn
        self.showShortcuts = True
        self.dataID = dataID
        self.groupingName = ""
        

    def __controls(self):

        self.__setupTable()

    def __connectEvents(self):
        ""

    def __setupTable(self):
        ""
        self.table = DataTreeViewTable(parent = self, 
                                    sendToThread = self.sendToThread, 
                                    tableID= self.tableID, 
                                    mainController=self.mC)
        self.table.setFocusPolicy(Qt.ClickFocus)
        self.model = DataTreeModel(parent=self.table)
        self.table.setItemDelegateForColumn(0,ItemDelegate(self.table))
        self.table.setItemDelegateForColumn(1,AddDelegate(self.table,highLightColumn=1))
        self.table.setItemDelegateForColumn(3,GroupDelegate(self.table,highLightColumn=3))#CopyDelegateCopyDelegate
        self.table.setItemDelegateForColumn(2,FilterDelegate(self.table,highLightColumn=2))
        self.table.setItemDelegateForColumn(4,DeleteDelegate(self.table,highLightColumn=4))

        self.table.setModel(self.model)
        

        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3,QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4,QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.resizeColumns()
        
    def __layout(self):
        ""
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().addWidget(self.table)
        
    def getData(self):
        ""
        return self.table.model().getLabels()

    def getDataID(self):
        ""
        return self.dataID

    def getSelectedData(self):
        "Returns Selected Data."
        return self.table.getSelectedData()

    def sendToThread(self, funcProps = {}, addSelectionOfAllDataTypes = False, addDataID = False):
        ""
        if hasattr(self,"sendToThreadFn"):

            self.sendToThreadFn(funcProps,
                                addSelectionOfAllDataTypes  = addSelectionOfAllDataTypes,
                                addDataID = addDataID)

    def setDataID(self,dataID):
        ""
        self.dataID = dataID 

    def sortLabels(self):
        "Sorts label, first ascending, then descending, then raw order"
        how = "ascending"
        if hasattr(self.table.model(),"lastSearchType"):
            lastSerachType = getattr(self.table.model(),"lastSearchType")
            if lastSerachType is None:
                how = "ascending"
            elif lastSerachType == "ascending":
                how = "descending"
            elif lastSerachType == "descending":
                #reset view
                setattr(self.table.model(),"lastSearchType",None)
            
        self.table.model().sort(how=how)

    def customSortLabels(self):
        ""
        resortLabels = ResortableTable(self.table.model()._labels)
        if resortLabels.exec_():
            sortedLabels = resortLabels.savedData
            self.addData(sortedLabels)

    def hideShowShortCuts(self):
        "Show / Hide Shortcuts"
        for i in range(1,5):
            if self.showShortcuts:
                self.table.hideColumn(i)
            else:
                self.table.showColumn(i)

        self.showShortcuts = not self.showShortcuts

    def addData(self,X, dataID = None):
        ""
        self.table.model().layoutAboutToBeChanged.emit()
        self.table.model().setNewData(X)
        self.table.selectionModel().clear()
        self.table.model().layoutChanged.emit()
        
        if dataID is not None:
            self.setDataID(dataID)

    def setColumnState(self,columnNames,newState):
        ""
        self.table.model().setColumnStateByData(columnNames,newState)

    def setGrouping(self,grouping,groupingName):
        ""        
       
        if isinstance(grouping,dict):
            self.groupingName = groupingName
            groupColors = self.mC.grouping.getGroupColors()
            self.model.resetGrouping()
            for n,(groupName, columnNames) in enumerate(grouping.items()):
                #for idx in columnNames.index:

                self.model.setColumnStateByDataIndex(columnNames.index,True)
                
                self.model.setGroupingColorByDataIndex(columnNames.index,groupColors[groupName])
                
                self.model.setGroupNameByDataIndex(columnNames.index,groupName)
                
            self.table.model().completeDataChanged()
    
    def setCurrentGrouping(self):
        ""
        if self.mC.grouping.groupingExists():
            self.setGrouping(self.mC.grouping.getCurrentGrouping(), self.mC.grouping.getCurrentGroupingName())
        

class DataTreeModel(QAbstractTableModel):
    

    def __init__(self, labels = pd.Series(), parent=None):
        super(DataTreeModel, self).__init__(parent)
        self.initData(labels)

    def initData(self,labels):

        self._labels = labels
        self._inputLabels = labels.copy()
        self.columnInGraph = pd.Series(np.zeros(shape=labels.index.size), index=labels.index)
        self.resetGrouping()
        self.setDefaultSize()
        self.lastSearchType = None

    def rowCount(self, parent=QModelIndex()):
        
        return self._labels.size

    def columnCount(self, parent=QModelIndex()):
        
        return 5

    def setDefaultSize(self,size=50):
        ""
        self.defaultSize = size

    def getDataIndex(self,row):
        ""
        if self.validDataIndex(row):
            return self._labels.index[row]
        
    def getColumnStateByDataIndex(self,dataIndex):
        ""
        return self.columnInGraph.loc[dataIndex] == 1

    def getColumnStateByTableIndex(self,tableIndex):
        ""
        dataIndex = self.getDataIndex(tableIndex.row())
        if dataIndex is not None:
            return self.getColumnStateByDataIndex(dataIndex)

    def setColumnState(self,tableIndex, newState = None):
        ""
        dataIndex = self.getDataIndex(tableIndex.row())
        if dataIndex is not None:
            if newState is None:
                newState = not self.columnInGraph.loc[dataIndex]
            self.columnInGraph.loc[dataIndex] = newState
            return newState
    
    def setColumnStateByData(self,columnNames,newState):
        ""
        idx = self._labels[self._labels.isin(columnNames)].index
        if not idx.empty:
            self.columnInGraph[idx] = newState

    def getGroupingStateByTableIndex(self,tableIndex):
        ""
        dataIndex = self.getDataIndex(tableIndex.row())
        if dataIndex is not None:
            return self.getGroupingStateByDataIndex(dataIndex)

    def getGroupingStateByDataIndex(self,dataIndex):
        ""
        return self.columnInGrouping.loc[dataIndex] == 1
    
    def setColumnStateByDataIndex(self,columnNameIndex,newState):
        ""
        idx = self._labels.index.intersection(columnNameIndex)
        if not idx.empty:
             self.columnInGrouping[idx] = newState

    def setGroupingState(self,tableIndex, newState = None):
        ""
        dataIndex = self.getDataIndex(tableIndex.row())
        if dataIndex is not None:
            if newState is None:
                newState = not self.columnInGrouping.loc[dataIndex]
            self.columnInGrouping.loc[dataIndex] = newState
            return newState

    def setGroupingColorByDataIndex(self,columnNameIndex,hexColor):
        ""
        idx = self._labels.index.intersection(columnNameIndex)
        if not idx.empty:
             self.colorsInGrouping[idx] = hexColor
    
    def setGroupNameByDataIndex(self,columnNameIndex,hexColor):
        ""
        idx = self._labels.index.intersection(columnNameIndex)
        if not idx.empty:
             self.nameGrouping[idx] = hexColor

    def getGroupNameByTableIndex(self,tableIndex):
        ""
        dataIndex = self.getDataIndex(tableIndex.row())
        if dataIndex is not None:
            return self.nameGrouping.loc[dataIndex]

    def getGroupColorByTableIndex(self,tableIndex):
        ""
        dataIndex = self.getDataIndex(tableIndex.row())
        if dataIndex is not None:
            return self.getGroupColorByDataIndex(dataIndex)

    def getGroupColorByDataIndex(self,dataIndex):
        ""
        return self.colorsInGrouping.loc[dataIndex]
    
    def resetGrouping(self):
        ""
        self.columnInGrouping = pd.Series(np.zeros(shape=self._labels.index.size), index=self._labels.index)
        self.colorsInGrouping = pd.Series(np.zeros(shape=self._labels.index.size), index=self._labels.index)
        self.nameGrouping = pd.Series(np.zeros(shape=self._labels.index.size), index=self._labels.index)

    def updateData(self,value,index):
        ""
        dataIndex = self.getDataIndex(index.row())
        if dataIndex is not None:
            self._labels[dataIndex] = str(value)
            self._inputLabels = self._labels.copy()

    def validDataIndex(self,row):
        ""
        return row <= self._labels.index.size - 1

    def deleteEntriesByIndexList(self,indexList):
        ""
        dataIndices = [self.getDataIndex(tableIndex.row()) for tableIndex in indexList]
        self._labels = self._labels.drop(dataIndices)
        self._inputLabels = self._labels.copy()
        self.completeDataChanged()

    def deleteEntry(self,tableIndex):
        ""
        dataIndex = self.getDataIndex(tableIndex.row())
        if dataIndex in self._inputLabels.index:
            self._labels = self._labels.drop(dataIndex)
            self._inputLabels = self._labels
            self.completeDataChanged()

    def getLabels(self):
        ""
        return self._labels

    def getSelectedData(self,indexList):
        ""
        dataIndices = [self.getDataIndex(tableIndex.row()) for tableIndex in indexList]
        return self._labels.loc[dataIndices]

    def setData(self,index,value,role):
        ""
        row =index.row()
        indexBottomRight = self.index(row,self.columnCount())
        if role == Qt.UserRole:
            self.dataChanged.emit(index,indexBottomRight)
            return True
        if role == Qt.CheckStateRole:
            self.setCheckState(index)
            self.dataChanged.emit(index,indexBottomRight)
            return True

        elif role == Qt.EditRole:
            if index.column() != 0:
                return False
            newValue = str(value)
            oldValue = str(self._labels.iloc[index.row()])
            columnNameMapper = {oldValue:newValue}
            if oldValue != newValue:
                self.parent().renameColumn(columnNameMapper)
                self.updateData(value,index)
                self.dataChanged.emit(index,index)
            return True

    def data(self, index, role=Qt.DisplayRole): 
        ""
        if not index.isValid(): 
            return QVariant()
        elif role == Qt.DisplayRole and index.column() == 0: 
            rowIndex = index.row() 
            if rowIndex >= 0 and rowIndex < self._labels.index.size:
                return str(self._labels.iloc[index.row()])
        elif role == Qt.FontRole and index.column() == 0:
            font = QFont()
            font.setFamily("Arial")
            font.setPointSize(10)
            return font
        elif role == Qt.ToolTipRole:
            if index.column() == 3:
                groupName = self.getGroupNameByTableIndex(index)
                if groupName:
                    groupingName = self.parent().mC.grouping.getCurrentGroupingName()
                    return "Grouping: {}\nGroupName: {}".format(groupingName,groupName)
                else:
                    return "Group Indicator"
            elif index.column() == 2:
                return "Filter Data"
            elif index.column() == 4:
                return "Delete Column"
            elif index.column() == 1:
                if self.getColumnStateByTableIndex(index):
                    return "Remove Column from Graph"
                else:
                    return "Add column to Graph"
            else:
                return ""

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.MoveAction | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    def setNewData(self,labels):
        ""
        self.initData(labels)
        self.completeDataChanged()

    def search(self,searchString):
        ""
        if self._inputLabels.size == 0:
            return
        if len(searchString) > 0:
      
            boolMask = self._labels.str.contains(searchString,case=False,regex=False)
            self._labels = self._labels.loc[boolMask]
        else:
            self._labels = self._inputLabels
        self.completeDataChanged()

    def sort(self, e = None, how = "ascending"):
        ""
        if self._inputLabels.size == 0:
            return
        if self.lastSearchType is None or self.lastSearchType != how:

            self._labels.sort_values(
                                    inplace = True,
                                    ascending = how == "ascending")
            self.lastSearchType = how

        else:
            self._labels.sort_index(
                                    inplace =  True,
                                    ascending=True)
            self.lastSearchType = None
        self.completeDataChanged()
    
    def completeDataChanged(self):
        ""
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount()-1, self.columnCount()-1))

    def rowRangeChange(self,row1, row2):
        ""
        self.dataChanged.emit(self.index(row1,0),self.index(row2,self.columnCount()-1))

    def rowDataChanged(self, row):
        ""
        self.dataChanged.emit(self.index(row, 0), self.index(row, self.columnCount()-1))

    def resetView(self):
        ""
        self._labels = pd.Series()
        self._inputLabels = self._labels.copy()
        self.completeDataChanged()


class DataTreeViewTable(QTableView):

    def __init__(self, parent=None, rowHeight = 22, mainController = None, sendToThread = None, tableID = None):

        super(DataTreeViewTable, self).__init__(parent)
       
        self.setMouseTracking(True)
        self.setShowGrid(False)
        self.verticalHeader().setDefaultSectionSize(rowHeight)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.rightClick = False
        self.rightClickMove = False
        self.focusRow = None
        self.focusColumn = None
        self.mC = mainController
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)# sssetSelectionBehavior(QAbstractItemView::SelectRows
       # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.rowHeight = rowHeight
        self.sendToThread = sendToThread
        self.tableID = tableID
        self.addMenu()
        self.setStyleSheet("""QTableView {background-color: white;border:None};""")
        
    def checkMenuItem(self,item):
        ""
        if isinstance(item["dataType"],str):
            return  item["dataType"] in ["All",self.tableID]
        elif isinstance(item["dataType"], list):
            return any(item in ["All",self.tableID] for item in item["dataType"])
        
    def addMenu(self):
        "Define Menu"
        try:
            if self.tableID in dataTypeSubMenu:
                mainMenu = createMenu()
                menuCollection = dict()
                menuCollection["main"] = mainMenu
                for menuName,subMenus in dataTypeSubMenu[self.tableID]:
                    
                    if menuName == "main":
                        menus = createSubMenu(main = mainMenu, subMenus = subMenus)
                        self.menu = mainMenu
                    else:
                        menus = createSubMenu(main=menuCollection[menuName],subMenus=subMenus)
                   
                    for menuName, menuObj in menus.items():
                        menuCollection[menuName] = menuObj
                filteredMenuBarItems = [item for item in menuBarItems if self.checkMenuItem(item)]
                for menuAction in filteredMenuBarItems:
                    if menuAction["subM"] in menuCollection:
                        if menuAction["subM"] == "main":
                            action = self.menu.addAction(menuAction["name"])
                        else:
                            action = menuCollection[menuAction["subM"]].addAction(menuAction["name"])
                            if "fnKwargs" in menuAction:
                                action.triggered.connect(lambda _,funcKey = menuAction["funcKey"], kwargs = menuAction["fnKwargs"]: self.prepareMenuAction(funcKey=funcKey,kwargs = kwargs))
                            else:
                                action.triggered.connect(lambda _,funcKey = menuAction["funcKey"]:self.prepareMenuAction(funcKey=funcKey))
        except Exception as e:
            print(e)
    
    def resizeColumns(self):
        columnWidths = [(0,400)] + [(n+1,self.rowHeight) for n in range(self.model().columnCount())]
        for columnId,width in columnWidths:
            self.setColumnWidth(columnId,width)

    def mouseReleaseEvent(self,e):
        #reset move signal
        self.rightClickMove = False
        #find table index by event
        tableIndex = self.mouseEventToIndex(e)
        #tableColumn
        tableColumn = tableIndex.column()
        #get key modifiers
        keyMod = QApplication.keyboardModifiers()
        #is shift key pressed?
        shiftPressed = keyMod == Qt.ShiftModifier
        #check if cmd(mac) or ctrl(windows) is clicked
        ctrlPressed = keyMod == Qt.ControlModifier
        #cast menu if right click
        
        if self.rightClick and not self.rightClickMove and tableColumn == 0:
           
            self.menu.exec_(self.mapToGlobal(e.pos()))
        
        elif tableColumn == 0 and not self.rightClick:
            if not shiftPressed and not ctrlPressed:
                self.selectionModel().clear() 
                self.selectionModel().select(tableIndex,QItemSelectionModel.Select)
                #update data (e.g remove selction grey area)
                self.model().completeDataChanged()
            else:
                self.removeSelection(e)  

        elif tableColumn == 1:

            self.addRemoveItems(tableIndex)

        elif tableColumn == 2:
            
            self.applyFilter(tableIndex)
        elif tableColumn == 3:
        
            self.copyDataToClipboard(tableIndex)
             
        
        elif tableColumn == 4:

            self.dropColumn(tableIndex)
        
    

    def keyPressEvent(self,e):
        ""
        if e.key() in [Qt.Key_Delete, Qt.Key_Backspace]:

            #delete selected rows
            self.model().layoutAboutToBeChanged.emit()
            selectedRows = self.selectionModel().selectedRows()
            self.model().deleteEntriesByIndexList(selectedRows)
            self.selectionModel().clear()
            self.model().layoutChanged.emit()

        elif e.key() == Qt.Key_Escape:
            #clear selection
            self.selectionModel().clear()

        elif e.key() == Qt.Key_Tab:

            if self.focusColumn is not None and self.focusRow is not None:
                self.focusColumn += 1
                if self.focusColumn == self.model().columnCount():
                    self.focusColumn = 0
                self.model().rowDataChanged(self.focusRow)

        elif e.key() in [Qt.Key_Enter, Qt.Key_Return]:
            #get focused index
            tableIndex = self.model().index(self.focusRow,self.focusColumn)

            if self.focusColumn == 1:
                #handles hitting enter while focu is on add delegate (column 1)
                self.addRemoveItems(tableIndex)

            elif self.focusColumn == 2:

                self.mC.mainFrames["sliceMarks"].applyFilter(columnNames = self.getSelectedData([tableIndex]))

            elif self.focusColumn == 3:

                self.copyDataToClipboard(tableIndex)

            elif self.focusColumn == 4:
                #delete items
                self.dropColumn(tableIndex)
        else:
            if self.focusColumn is not None and self.focusRow is not None:
                currentFocusRow = int(self.focusRow)
                if e.key() == Qt.Key_Down:
                        
                        if self.focusRow < self.model().rowCount() - 1:
                            self.focusRow += 1
                        self.model().rowRangeChange(currentFocusRow,self.focusRow)
 
                if e.key() == Qt.Key_Up:
                        
                        if self.focusRow > 0 and self.focusRow < self.model().rowCount():
                            self.focusRow -= 1
                        self.model().rowRangeChange(self.focusRow,currentFocusRow)
    
    def applyFilter(self,tableIndex = None,*args,**kwargs):
        "Apply filtering (numeric or categorical)"
        if tableIndex is None:
            
            tableIndex = self.model().index(self.focusRow,0)
        self.mC.mainFrames["sliceMarks"].applyFilter(columnNames = self.getSelectedData([tableIndex]), dragType = self.tableID, *args,**kwargs)
        
    def leaveEvent(self, event):
   
        if self.rightClick:
            return
        if self.focusRow is not None:
            dataRow = int(self.focusRow)
            self.focusColumn = None
            self.focusRow = None
            self.model().rowDataChanged(dataRow)

    def mousePressEvent(self,e):
        ""
        tableIndex = self.mouseEventToIndex(e)
        if e.buttons() == Qt.RightButton:
            self.startIndex = tableIndex
            self.rightClick = True
        elif e.buttons() == Qt.LeftButton:
            if tableIndex.column() == 0:
                self.removeSelection(e)
                super(QTableView,self).mousePressEvent(e)
                self.saveDragStart()
            self.rightClick = False
        else:
            self.rightClick = False

    def addRemoveItems(self,tableIndex):
        ""
        if self.model().getColumnStateByTableIndex(tableIndex):
            self.removeItemFromRecieverbox(tableIndex)
        else:
            self.sendItemToRecieverbox(tableIndex)
        #update state (clicked) and refresh table
        self.model().setColumnState(tableIndex)
        self.model().rowDataChanged(tableIndex.row())

    def isGroupigActive(self):
        ""
        return np.any(self.model().columnInGrouping)

    def sendItemToRecieverbox(self, tableIndex):
        ""
        items = self.getSelectedData(indices=[tableIndex])
        funcProps = {"key":"receiverBox:addItems","kwargs":{"columnNames":items,"dataType":self.tableID}}
        self.sendToThread(funcProps,addDataID=True)

    def removeItemFromRecieverbox(self, tableIndex):
        ""
        items = self.getSelectedData(indices=[tableIndex])
        funcProps = {"key":"receiverBox:removeItems","kwargs":{"columnNames":items}}
        self.sendToThread(funcProps)

    def saveDragStart(self):
        ""
        self.currentDragIndx = self.selectionModel().selectedRows()
        selectedData = self.getSelectedData(self.currentDragIndx)
         
        self.parent().parent().parent().parent().updateDragData(selectedData,self.tableID)
       
    def setColumnStateOfDraggedColumns(self):
        
        if hasattr(self,"currentDragIndx"):
            for indx in self.currentDragIndx:
                self.model().setColumnState(indx,newState=True)


    def mouseMoveEvent(self,event):
        
        if event.buttons() == Qt.LeftButton:
            
            super(QTableView,self).mouseMoveEvent(event)

        elif event.buttons() == Qt.RightButton:

            endIndex = self.mouseEventToIndex(event)
            for tableIndex in self.getIndicesForRow(endIndex.row()):
                self.selectionModel().select(tableIndex,QItemSelectionModel.Select)
            self.rightClickMove = True
    
        else:
            self.focusRow = self.rowAt(event.pos().y())
            index = self.model().index(self.focusRow,0)
            self.focusColumn = self.columnAt(event.pos().x())
            self.model().setData(index,self.focusRow,Qt.UserRole)

    def removeSelection(self,e):
        ""
        tableIndex = self.mouseEventToIndex(e)
        self.model().rowDataChanged(tableIndex.row())

    def isSelected(self,tableIndex):
        return tableIndex in self.selectionModel().selectedRows()

    def getIndicesForRow(self,row):
        ""
        numColumns = self.model().columnCount()
        indexList = [self.model().index(row,column) for column in range(numColumns)]
        return indexList

    def getSelectedData(self, indices = None):
        ""
        if indices is None:
            indices = self.selectionModel().selectedRows()
        return self.model().getSelectedData(indices)


    def compareGroups(self, event=None, test = None, *args, **kwargs):
        ""
        try:
            #print(test)
            #print(self.mC.grouping.groupingExists())
            if False and not self.mC.grouping.groupingExists():
                w = WarningMessage(infoText="No Grouping found. Please annotate Groups first.",iconDir = self.mC.mainPath)
                w.exec_()
                return
            else: 
                dlg = ICCompareGroups(mainController = self.mC, test = test)
                dlg.exec_()
        except Exception as e:
            print(e)

    def summarizeGroups(self,event=None, metric = "min"):
        ""
        if not self.mC.grouping.groupingExists():
            w = WarningMessage(infoText="No Grouping found. Please annotate Groups first.")
            w.exec_()
            return
        print("summarize groups")
        
        funcProps = {"key":"data::summarizeGroups",
                    "kwargs":{
                        "metric":metric,
                        "grouping":self.mC.grouping.getCurrentGrouping()}}
        self.sendToThread(funcProps,addDataID = True)



    def createGroups(self, event=None,**kwargs):
        ""

        if self.mC.data.hasData():
            groupDialog = ICGrouper(self.mC)
            groupDialog.exec()
        

    def mouseEventToIndex(self,event):
        "Converts mouse event on table to tableIndex"
        row = self.rowAt(event.pos().y())
        column = self.columnAt(event.pos().x())
        return self.model().index(row,column)

    def renameColumn(self,columnNameMapper):
        ""
        funcProps = {"key":"data::renameColumns","kwargs":{"columnNameMapper":columnNameMapper}}
        self.sendToThread(funcProps,addDataID=True)
    
    def dropColumn(self, tableIndex):
        "Drops column by table Index"
        selectedRows = [tableIndex]
        #get selected data by index
        deletedColumns = self.model().getSelectedData(selectedRows)
        self.model().deleteEntriesByIndexList(selectedRows)
        funcProps = {"key":"data::dropColumns","kwargs":{"columnNames":deletedColumns}}
        self.sendToThread(funcProps,addDataID = True)

    def copyDataToClipboard(self,tableIndex):
      
        funcProps = {"key":"data::copyDataFrameSelection",
                    "kwargs":{"columnNames":self.model().getSelectedData([tableIndex])}}   

        self.sendToThread(funcProps=funcProps,addSelectionOfAllDataTypes=True,addDataID=True)


    def customSorting(self,*args,**kwargs):
        ""
        columnName = self.getSelectedData().values[0]
        dataID = self.mC.mainFrames["data"].getDataID()
        uniqueValues = self.mC.data.getUniqueValues(dataID,columnName)
        customSort = ResortableTable(inputLabels = uniqueValues)
        if customSort.exec_():
            sortedValues = customSort.savedData.values
            funcProps = {"key":"data::sortDataByValues",
                         "kwargs":{"columnName":columnName,
                                    "dataID":dataID,
                                    "values":sortedValues}}
            #print(funcProps)
            self.sendToThread(funcProps=funcProps)
    
    def featureSelection(self,*args,**kwargs):
        ""
        ""
        #check if recursive feature elimination should be performed
        if 'RFEVC' in kwargs and kwargs['RFEVC']:
            runRFEVC = True
        else:
            runRFEVC = False

        if self.mC.grouping.groupingExists():
            try:
                columnNames = self.mC.grouping.getColumnNames()
                grouping = self.mC.grouping.getCurrentGrouping() 
                groupFactors = self.mC.grouping.getFactorizedColumns() 
                model = self.sender().text()
                createSubset = self.mC.config.getParam("feature.create.subset")
                fnKwargs = {"columnNames":columnNames,"grouping":grouping,"model":model,"groupFactors":groupFactors,"RFECV":runRFEVC,"createSubset":createSubset}
                self.prepareMenuAction("stats::featureSelection",fnKwargs,addColumnSelection=False)
            except Exception as e:
                print(e)

        else:

            self.mC.sendMessageRequest({"title":"Error..","message":"No Grouping found."})
       
    def fitModel(self,*args,**kwargs):
        if not self.mC.grouping.groupingExists():
            try:
                #columnNames = self.mC.grouping.getColumnNames()
                #grouping = self.mC.grouping.getCurrentGrouping()
                w = ICModelBase(self.mC)
                w.exec_()
               # fnKwargs = {"columnNames":columnNames,"grouping":grouping}
                #self.prepareMenuAction("data::smartReplace",fnKwargs,addColumnSelection=False)
            except Exception as e:
                print("??")
                print(e)

        else:

            self.mC.sendMessageRequest({"title":"Error..","message":"No Grouping found."})

    def smartReplace(self,*args,**kwargs):
        ""
        if self.mC.grouping.groupingExists():
            try:
                columnNames = self.mC.grouping.getColumnNames()
                grouping = self.mC.grouping.getCurrentGrouping()
                fnKwargs = {"columnNames":columnNames,"grouping":grouping}
                self.prepareMenuAction("data::smartReplace",fnKwargs,addColumnSelection=False)
            except Exception as e:
                print(e)

        else:

            self.mC.sendMessageRequest({"title":"Error..","message":"No Grouping found."})



    def removeOutliersFromGroup(self,**kwargs):
        ""
        if self.mC.grouping.groupingExists():
            try:
               # columnNames = self.mC.grouping.getColumnNames()
                grouping = self.mC.grouping.getCurrentGrouping()
                fnKwargs = {"grouping":grouping}
                self.prepareMenuAction("data::replaceGroupOutlierWithNaN",fnKwargs,addColumnSelection=False)
            except Exception as e:
                print(e)

        else:

            self.mC.sendMessageRequest({"title":"Error..","message":"No Grouping found."})


    def sendSelectionToQuickSelect(self,mode="unique"):
        "Sends filter props to quick select widget"
        columnName = self.getSelectedData().values[0]
        quickSelect = self.mC.mainFrames["data"].qS
        sep = self.mC.config.getParam("quick.select.separator")
        
        filterProps = {'mode': mode, 'sep': sep, 'columnName': columnName}
        quickSelect.updateQuickSelectData(columnName,filterProps)

    def getUserInput(self,**kwargs):

        if "requiredColumns" in kwargs:
         
            askUserForColumns = kwargs["requiredColumns"]
            dataID = self.mC.mainFrames["data"].getDataID()
            dragColumns = self.mC.mainFrames["data"].getDragColumns()
            categoricalColumns = self.mC.data.getCategoricalColumns(dataID).values.tolist()
            
            sel = SelectionDialog(selectionNames = askUserForColumns, 
                    selectionOptions = dict([(selectionName, categoricalColumns) for selectionName in askUserForColumns]),
                    
                    selectionDefaultIndex = dict([(askUserForColumns[n],dragColumn) for \
                        n,dragColumn in enumerate(dragColumns) if n < len(askUserForColumns)]))

            if sel.exec_():
                self.prepareMenuAction(funcKey=kwargs["funcKey"],kwargs=sel.savedSelection, addColumnSelection=False)

        elif "requiredStr" in  kwargs:
            
            labelText = kwargs["info"]
            splitString, ok = QInputDialog().getText(self,"Provide String",labelText)
            if ok: 
                self.prepareMenuAction(funcKey = kwargs["funcKey"],kwargs = {kwargs["requiredStr"]:splitString})
        
        elif "requiredFloat" in kwargs:
            
            labelText, minValue, maxValue = kwargs["info"], kwargs["min"], kwargs["max"]
            if maxValue == "nColumns":
                maxValue = self.getSelectedData().size
        
            number, ok = QInputDialog().getDouble(self,"Provide float",labelText, maxValue-minValue/2 ,minValue, maxValue, 2 )
            if ok:
                self.prepareMenuAction(funcKey = kwargs["funcKey"],kwargs = {kwargs["requiredFloat"]:number})
        
        elif "requiredInt" in kwargs:
            
            labelText, minValue, maxValue = kwargs["info"], kwargs["min"], kwargs["max"]
            if maxValue == "nColumns":
                maxValue = self.getSelectedData().size
            elif maxValue == "nDataRows":
                dataID = self.mC.mainFrames["data"].getDataID()
                maxValue = self.mC.data.getRowNumber(dataID)

            number, ok = QInputDialog().getInt(self,"Provide integer",labelText, maxValue-minValue/2 ,minValue, maxValue)
        
            if ok:
                fnKwargs = {kwargs["requiredInt"]:number}
                if "otherKwargs" in kwargs:
                    fnKwargs = {**fnKwargs,**kwargs["otherKwargs"]}
                self.prepareMenuAction(funcKey = kwargs["funcKey"],kwargs = fnKwargs) 
           

    
    def prepareMenuAction(self,funcKey,kwargs = {},addDataID=True,addColumnSelection=True):

        ""
        try:
            if hasattr(self,funcKey):
                getattr(self,funcKey)(**kwargs)
            else:
                
                funcProps = {"key":funcKey,"kwargs":kwargs}
                if addColumnSelection:
                    funcProps["kwargs"]["columnNames"] = self.getSelectedData()
                    #funcProps["kwargs"]["transformGraph"] = True
            
                self.sendToThread(funcProps=funcProps,addDataID=addDataID)
        except Exception as e:
            print(e)
        