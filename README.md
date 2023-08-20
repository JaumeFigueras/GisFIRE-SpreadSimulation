# GisFIRE-SpreadSimulation
GisFire module to simulate wildfire spread. It is mainly a FARSITE implementation into QGIS.

# GisFIRE

GisFIRE SpreadSimulation is a plugin for QGIS that implements a wildfire spread simulator and other tools related to 
wildfire management. It is part of a PhD and implements a [FARSITE software](https://www.firelab.org/project/farsite) 
port to python integrated into [QGIS](https://qgis.org/en/site/). It is also an intent to be a framework to develop and 
test other spread simulation algorithms different from the ones implemented in FARSITE or other management tools.

## Getting Started

To get familiar with the project follow all the information in the wiki and then clone the project to continue 
developing or testing it.

### Prerequisites

To use GisFIRE you need QGIS and all of its requirements. Visit the QGIS website and follow install instructions.
[https://qgis.org/en/site/forusers/download.html](https://qgis.org/en/site/forusers/download.html)

### Installing

The plugin is not published in the QGIS repository. The easiest way to install the plugin is to download de the latest 
distribution zip file and install it with QGIS. In the "Plugins" menu entry of QGIS select the "Manage and Install 
Plugins..." and in the plugins interface select the "Install from ZIP" option.

## Development

Fork the repo and enjoy

### Compiling the resources

```console
pyrcc5 ../GisFIRE-SpreadSimulation/src/gisfire_spread_simulation/resources.qrc -o ../GisFIRE-SpreadSimulation/src/gisfire_spread_simulation/resources.py
```

### Translations

First generate the `.ts` file from the `.py` and `.ui` files.
```console
pylupdate5 ../GisFIRE-SpreadSimulation/src/gisfire_spread_simulation/gisfire_spread_simulation.py -ts ../GisFIRE-SpreadSimulation/src/gisfire_spread_simulation/i18n/gisfire_lightnings_ca.ts
pylupdate5 ../GisFIRE-SpreadSimulation/src/gisfire_spread_simulation/ui/dialogs/settings.ui -ts ../GisFIRE-SpreadSimulation/src/gisfire_spread_simulation/i18n/gisfire_lightnings_ca.ts
```

Then use QLinguist to translate to different languages

Finally, compile the `.ts` translation files to binary `.qm` files.
```console
lrelease ../GisFIRE-SpreadSimulation/src/gisfire_spread_simulation/i18n/gisfire_lightnings_ca.ts
```
### Running the tests

Testing was inspired by lots of tutorials and also with lots of problems. This is the best I get running.
```console
 python3 -m pytest -x -v --cov-report=html:html_gisfire_spread_simulation_test_results --cov=../GisFIRE-SpreadSimulation/ ../GisFIRE-SpreadSimulation/test/
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull 
requests to us.

## Authors

* **Jaume Figueras** - *GisFIRE SpreadSimulation* - [JaumeFigueras](https://github.com/JaumeFigueras)

See also the list of [contributors](https://github.com/JaumeFigueras/GisFIRE/contributors) who participated in this 
project.

## License

This project is licensed under the GNU GPLv3 License - see the [COPYING](COPYING) file for details

## Acknowledgments

* [FireLab](https://www.firelab.org)
