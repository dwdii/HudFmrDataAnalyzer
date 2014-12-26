# HudFmrDataAnalyzer

[![Codacy](https://img.shields.io/codacy/39298c168a044a5eb0a297a0169f71af.svg)](https://www.codacy.com/public/daniel_2/HudFmrDataAnalyzer/dashboard)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](http://opensource.org/licenses/MIT)

The Housing and Urban Development (HUD) Fair Market Rent Data Analyzer application is written in Python. It was written as
part of my work in the CUNY Master of Science, Data Analytics program to exercise various programming techniques in
Python and analyze the Fair Market Rent data sets offered by the Department of Housing and Urban Development.

The app is a simple form using the TkInter user interface layer. Development of the app was performed on Windows 8.1
using the PyCharm IDE and Python 2.7. No testing has been performed on other platforms, though no known Windows dependencies exist.

## Getting Started

As a result of the app being written in Python, a scripting language, to get started using the app all that is
required is to download this repository using the [Download Zip](https://github.com/dwdii/HudFmrDataAnalyzer/archive/master.zip)
link on the right side of the [HudFmrDataAnalyzer repository GitHub root page](https://github.com/dwdii/HudFmrDataAnalyzer).

After downloading and extracting the ZIP, simply run the `project_hudfmr.py` script, found in the
[Project subfolder](https://github.com/dwdii/HudFmrDataAnalyzer/tree/master/Project), in your Python runtime.

The initial dataset, years 2005-2015, is included in the
[Data subfolder](https://github.com/dwdii/HudFmrDataAnalyzer/tree/master/Project/Data) and will be loaded automatically
when the app is started. 

The following screenshots provide a brief overview of the current functionality:

![Hud Fair Market Rent Data Analyzer App](https://github.com/dwdii/HudFmrDataAnalyzer/raw/master/Docs/img/HudFmrDataAnalyzerApp.png)

![Fair Market Rent Geographic Heatmap](https://github.com/dwdii/HudFmrDataAnalyzer/raw/master/Docs/img/Heatmap-US-fmr-3bd-2015.png)

![Linear Regression of Fair Market Rents in Santa Clara County, CA, 2005-2015](https://github.com/dwdii/HudFmrDataAnalyzer/raw/master/Docs/img/LinReg-SantaClaraCA-3bd.png)