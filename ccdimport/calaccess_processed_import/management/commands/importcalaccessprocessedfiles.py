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
        self.get_model("")
        for fname in file_list:
            filename, file_extension = os.path.splitext(fname)
            model = self.get_model(filename)
            if model is None:
                self.log("FAILED to resolve model for '{}'".format(filename))
            else:
                self.log("RESOLVED file: '{}'; model: '{}'".format(filename, model))

        #get files in the directory
        '''os.path.exists(csv_dir) or os.mkdir(csv_dir)
        csv_name = '{}.csv'.format(processed_file.file_name)
        csv_path = os.path.join(csv_dir, csv_name)

        # Open up the .CSV file for reading so we can wrap it in the Django File obj
        with open(csv_path, 'rb') as csv_file:
            # Save the .CSV on the processed data file
            processed_file.file_archive.save(csv_name, File(csv_file))

        #go through the files
        #map each file to a model & execute model from_csv
            # Get the data obj that is paired with the processed_file obj
        data_model = self.get_model(processed_file)'''
