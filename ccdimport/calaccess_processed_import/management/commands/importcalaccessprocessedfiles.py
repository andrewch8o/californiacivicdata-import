#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import data from previously archived calaccess .csv files into a database after matching each file to the corresponding calaccess model by file name
"""
import os
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
        raise NotImplementedError

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
            self.get_model(filename)

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
