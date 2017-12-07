# -*- coding: utf-8 -*-
from .. import header
from ..tables import ExchangeTableWidget
from ..widgets import ActivityDataGrid
import brightway2 as bw
from PyQt5 import QtCore, QtWidgets
import functools


class ActivityDetailsTab(QtWidgets.QWidget):
    def __init__(self, parent=None, activity=None):
        super(ActivityDetailsTab, self).__init__(parent)
        self.parent = parent

        self.details_widget = self.get_details_widget()

        container = QtWidgets.QVBoxLayout()
        container.setAlignment(QtCore.Qt.AlignTop)
        container.addWidget(self.details_widget)

        self.setLayout(container)

        if activity:
            self.populate(activity)

    def toggle_visible(self, table):
        if table.state == "shown":
            table.state = "hidden"
            table.toggle_button.setText("Show")
            table.hide()
        else:
            table.state = "shown"
            table.show()
            table.toggle_button.setText("Hide")

    def get_details_widget(self):
        self.production = ExchangeTableWidget(self, production=True)
        self.inputs = ExchangeTableWidget(self)
        self.flows = ExchangeTableWidget(self, biosphere=True)
        self.upstream = ExchangeTableWidget(self)

        layout = QtWidgets.QVBoxLayout()
        self.metadata = ActivityDataGrid()
        layout.addWidget(self.metadata)

        tables = [
            (self.production, "Products:"),
            (self.inputs, "Technosphere Inputs:"),
            (self.flows, "Biosphere flows:"),
            (self.upstream, "Upstream consumers:"),
        ]

        for table, label in tables:
            table.state = "shown"
            table.toggle_button = QtWidgets.QPushButton("Hide")
            table.toggle_button.clicked.connect(functools.partial(self.toggle_visible, table=table))

            inside_widget = QtWidgets.QWidget()
            inside_layout = QtWidgets.QHBoxLayout()
            inside_layout.addWidget(header(label))
            inside_layout.addWidget(table.toggle_button)
            inside_layout.addStretch(1)
            inside_widget.setLayout(inside_layout)

            layout.addWidget(inside_widget)
            layout.addWidget(table)

        widget = QtWidgets.QWidget(self)
        widget.setLayout(layout)
        return widget

    def populate(self, key):
        self.activity = bw.get_activity(key)

        self.production.set_queryset(key[0], self.activity.production())
        self.inputs.set_queryset(key[0], self.activity.technosphere())
        self.flows.set_queryset(key[0], self.activity.biosphere())
        self.upstream.set_queryset(key[0], self.activity.upstream(), upstream=True)
        self.metadata.populate(self.activity)
