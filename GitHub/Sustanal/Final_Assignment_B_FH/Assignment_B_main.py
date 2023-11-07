
import wbgapi as wb
from stuff.util import *
from stuff.ui import *
import os


if __name__ == "__main__":

    gui_dialog = True
    '''
       True = GUI dialog (Taks 8), False = Analysis (<8)
    '''
    if gui_dialog:
        start_app()
    else:

        data = wb.data.DataFrame(['ER.H2O.FWIN.ZS', 'NV.IND.TOTL.ZS'], time=[2020])


        data.columns = ['Water share industry (%)', 'GDP share industry (%)']


        '''
        TASK 4 c) Check the number of missing values in the primary and secondary indicators and
        print the results.
        '''
        nan_checker(data)

        '''
        TASK 4 d) Determine the number of countries for
        which the data gaps in the primary
        indicator can be filled based on
        information available for the secondary
        indicator and print a statement about it.'''

        imput_countries(data)

        '''
        TASK 5f) Collect the
        results
        from subtask e in a
        common
        data
        frame and print
        the
        results.
        '''
        imp_valid(data, print_output=True)

        '''
        TASK 6f) Export Stuff to Excel
        '''
        imp_data = imput_calc(data)
        valid_data = imp_valid(data)
        # Create an ExcelWriter object and specify the Excel file name
        folder_checker('Data')

        file_name = 'Data\data_imputed.xlsx'

        with pd.ExcelWriter(file_name) as writer:
            imp_data.to_excel(writer, sheet_name='imputed_data')
            valid_data.to_excel(writer, sheet_name='validation_imputation')

        '''
        TASK 7 a) Plot a histogram of the original primary
        indicator.
        '''
        plot_stuff(data)


        '''
        
        TASK 7 c) Make a stacked bar chart of these
        segmentations that shows the proportions
        from 0 to 1.
        '''
        clustering(data, fig_output=True)







