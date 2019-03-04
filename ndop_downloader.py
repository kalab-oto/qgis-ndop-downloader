# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NDOPDownloader
                                 A QGIS plugin
 downlaoder
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-12-14
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Oto Kaláb
        email                : oto.kalab@opengeolabs.cz
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .ndop_downloader_dialog import NDOPDownloaderDialog
import os.path
from pathlib import Path
from qgis.utils import iface
from . import ndop

class NDOPDownloader:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'NDOPDownloader_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = NDOPDownloaderDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&NDOP Downloader')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'NDOPDownloader')
        self.toolbar.setObjectName(u'NDOPDownloader')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('NDOPDownloader', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ndop_downloader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'NDOP Downloader'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&NDOP Downloader'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        
        if result:
            
            if self.dlg.line_user.text() == '':
                try:
                    username, password = ndop.read_config(Path(Path.home(), ".ndop.cfg"))
                except:
                    print("Kongigurační soubor nenalezen") 
            else:
                username = self.dlg.line_user.text()
                password = self.dlg.line_pass.text()

            taxon = self.dlg.line_taxon.text()
            # region = self.dlg.line_region.text()
            # if region == '':
                # region = None

#           polygon=self.dlg.mMapLayerComboBox.currentLayer()

            search_payload = ndop.get_search_pars(taxon=taxon
                                                # ,region=region
                                                )

            data_path = Path(
                os.path.dirname(os.path.realpath(__file__)),
                "downloaded_data"
            )

            
            ndop.get_ndop_data(
                username,
                password,
                search_payload,
                str(Path(data_path,"data"))
            )

            for filename in os.listdir(data_path):
                if filename.endswith("zip"):
                    layer = iface.addVectorLayer(str(Path(data_path,filename)), "", "ogr")
                    if not layer:
                        print("Layer failed to load!")
                
                if filename.endswith(".csv"):
                    uri = (
                        'file://{}?type=csv&detectTypes=yes&crs={}&'
                        'delimiter={}&xField={}&yField={}&decimalPoint={}'
                    ).format(
                        str(Path(data_path,filename)),
                        "EPSG:5514", ",", "X", "Y", ","
                    )
                    layer = iface.addVectorLayer(
                        uri, "centroids_"+filename, "delimitedtext"
                    )
