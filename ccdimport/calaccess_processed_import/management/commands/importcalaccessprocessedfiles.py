#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import data from previously archived calaccess .csv files into a database after matching each file to the corresponding calaccess model by file name
"""
import os
from django.apps import apps
from django.core.files import File
from calaccess_raw import get_data_directory
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models.tracking import ProcessedDataVersion, ProcessedDataFile


class Command(CalAccessCommand):
    """
    Import data from previously archieved calaccess .csv files into a database
    """
    help = 'Import data from previously archieved calaccess .csv files into a database'

    def get_model(self, processed_file):
        """
        Get the model linked to this processed file record.
        """
        #TODO: implement model resolution
        elections_model_dict = apps.get_app_config("calaccess_processed_elections").get_ocd_proxy_lookup()
        #Filings lookup
        model_list = apps.get_app_config("calaccess_processed_filings").get_filing_models()
        filings_model_dict = dict((m.__name__, m) for m in model_list)

        #Flatfiles lookup
        flatfiles_model_dict = apps.get_app_config("calaccess_processed_flatfiles").get_flat_proxy_lookup()

        resolved_model = None
        if processed_file in elections_model_dict.keys():
            resolved_model = elections_model_dict[processed_file]
        elif processed_file in filings_model_dict.keys():
            resolved_model = filings_model_dict[processed_file]
        elif processed_file in flatfiles_model_dict.keys():
            resolved_model = flatfiles_model_dict[processed_file]

        return resolved_model

    def list_models(self):
        """
        List the known models ( for debug purposes )
        """
        elections_model_dict = apps.get_app_config("calaccess_processed_elections").get_ocd_proxy_lookup()
        self.log("ELECTIONS LOOKUP:")
        for key in elections_model_dict.keys():
            self.log("'{0}': '{1}'".format(key, elections_model_dict[key]))
        #Filings lookup
        model_list = apps.get_app_config("calaccess_processed_filings").get_filing_models()
        filings_model_dict = dict((m.__name__, m) for m in model_list)
        self.log("FILINGS LOOKUP:")
        for key in filings_model_dict.keys():
            self.log("'{0}': '{1}'".format(key, filings_model_dict[key]))

        #Flatfiles lookup
        flatfiles_model_dict = apps.get_app_config("calaccess_processed_flatfiles").get_flat_proxy_lookup()
        for key in flatfiles_model_dict.keys():
            self.log("'{0}': '{1}'".format(key, flatfiles_model_dict[key]))

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        #establish "import" directory location
        csv_dir = os.path.join(
            get_data_directory(),
            'processed'
        )
        
        file_list = os.listdir(csv_dir)
        for fname in file_list:
            filename, file_extension = os.path.splitext(fname)
            model = self.get_model(filename)
            if model is None:
                self.warn("FAILED to resolve model for the file '{}'".format(filename))
            else:
                self.log("IMPORTING file: '{}'; model: '{}'".format(filename, model))
                model.objects.from_csv(
                    os.path.join(csv_dir, fname),
                    dict((f.name, f.db_column) for f in model._meta.fields)
                )
