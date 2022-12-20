# Import libraries
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from datetime import datetime
import os

# Setting options
st.set_page_config(layout='wide')
pd.set_option('display.precision', 0)

# Functions
def query_df(df, phrase):
    phrase = phrase.lower()
    return df.query(f'Text.str.contains("{phrase}", na=False)', engine='python')

@st.cache(allow_output_mutation=True)
def load_data(file_name):
    df = pd.read_csv(file_name, index_col=0)
    # df = df.fillna(False)
    return df

def get_temp_df_number():
    org_dir = r'C:\Users\ebryaga\Desktop\Github\File_tagger'
    search_dir = r'C:\Users\ebryaga\Desktop\Github\File_tagger\temp_df'
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files]  # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    last_nr = files[0].split('\\')[-1].split('_')[0]
    os.chdir(org_dir)
    return int(last_nr)




# Loading data, changing column names & 'SN' column type/style
df = load_data('C:/Users/ebryaga/Desktop/Github/File_tagger/Tagged_July_25_22.csv')
df.columns = ['File name', 'Source', 'Text', 'SN', 'Job', 'Report Type', 'Year', 'Month', 'Day']
df['SN'] = df['SN'].apply(lambda x: str(x).upper().replace("{'", '').replace("'}", '').replace('SET()',''))


st.title('Test, test, test')

# Multiple keyword search using st_tags
keyword = st_tags(
    label='# Please enter the text you want to search within document:',
    text='Press enter to add more',
    value=['atlantic'],
    suggestions=['liner', 'houston'],
    maxtags=6,
    key='1')

# Tag filters
tag_filters = st.expander('Tag filters:')

with tag_filters:
    col1, col2, col3, col4 = st.columns(4)

    sns = df['SN'].unique()
    sel_sns = col1.multiselect("Serial Number:", sns)

    jobs = df['Job'].unique()
    sel_jobs = col2.multiselect("Job Number:", jobs)

    reports = df['Report Type'].unique()
    sel_reports = col3.multiselect("Report Type:", reports)

    years = df['Year'].unique()
    sel_years = col4.multiselect("Year:", years)

    tag_button = st.button('Apply Tag Filters')

filters = [('SN', sel_sns), ('Job', sel_jobs), ('Report Type', sel_reports), ('Year', sel_years)]
tag_columns = ['SN', 'Job', 'Report Type', 'Year']
tags_sel = [sel_sns, sel_jobs, sel_reports, sel_years]

# Filtering df based on keywords and filters
df_filter = df.copy()
if len(keyword) > 0:
    for x in range(len(keyword)):
        df_result = query_df(df_filter, keyword[x])
        df_filter = df_result
    if tag_button:
        for i in range(4):
            if len(tags_sel[i]) > 0:
                df_result = df_result[df_result[tag_columns[i]].isin(tags_sel[i])]
    st.write(f"**Found {df_result.shape[0]} results**")
    st.dataframe(df_result.style.set_precision(0))
else:
    if tag_button:
        for i in range(4):
            if len(tags_sel[i]) > 0:
                df_filter = df_filter[df_filter[tag_columns[i]].isin(tags_sel[i])]
    st.write(f"**Found {df_filter.shape[0]} results**")
    # st.dataframe(df_filter.style.set_precision(0))
    st.write(df_filter)

# Wrong tag correction by user
st.header('Found error?')
st.subheader("If you found error and would like to update data please:")
st.write('1. Select checkbox in the row you would like to update\n'
         '2. Pass corrected value in the cell\n'
         '3. Insert your e-mail address and justification\n'
         '4. Double check in "Output" below if the changes are OK and click "Sumbitt Change')

df_temp = df[['File name', 'Source', 'SN', 'Job', 'Report Type', 'Year', 'Month', 'Day']]
gd = GridOptionsBuilder.from_dataframe(df_temp)
gd.configure_default_column(editable=True, groupable=True)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gridoptions = gd.build()
grid_table = AgGrid(df_temp, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                    height=500,
                    allow_unsafe_jscode=True,
                    enable_enterprise_modules = True,
                    theme='fresh')

sel_row = grid_table["selected_rows"]

# User input data
user_email = st.text_input('Please enter your e-mail', '..@bakerhughes.com')
usex_expl = st.text_input('Please justify the change', "I've noticed error in..")

# Change verification
st.subheader("Verify your change")
col1, col2 = st.columns(2)
col1.subheader('IS')
col1.write(sel_row)
# st.write(sel_row[0]["File name"])

col2.subheader('WAS')
old_row = df_temp[df_temp['File name'] == sel_row[0]["File name"]]   # get original value from df, based on file name/md5
col2.write(old_row.to_dict(orient='records'))
cor_button = st.button("Submitt Change")


df_change = pd.DataFrame(sel_row)
file_text = df[df['File name'] == df_change.loc[0,'File name']]['Text'].values
df_change['Text'] = file_text
df_change = df_change[df.columns]

df_old = df[df['File name'] == df_change.loc[0,'File name']]


# Get Temporary DF number
# st.write(os.getcwd())
# os.chdir(os.getcwd(f'{os.getcwd()}//temp_df'))
# org_dir = r'C:\Users\ebryaga\Desktop\Github\File_tagger'
# search_dir = r'C:\Users\ebryaga\Desktop\Github\File_tagger\temp_df'
# os.chdir(search_dir)
# files = filter(os.path.isfile, os.listdir(search_dir))
# files = [os.path.join(search_dir, f) for f in files] # add path to each file
# files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
# last_nr = files[0].split('\\')[-1].split('_')[0]
# st.write(last_nr)
# my_files = sorted(filter(os.path.isfile, os.listdir(r'C:\Users\ebryaga\Desktop\Github\File_tagger\temp_df')), key=os.path.getmtime, reverse=True)
# st.write(my_files)
# os.chdir(org_dir)
if cor_button:
    i = get_temp_df_number() + 1
    st.write(df_change)
    st.write(datetime.now())
    df_change.to_csv(f'temp_df/{i}_Temporary_change.csv')
    df_old.to_csv(f'org_df/{i}_Before_change.csv')

    #log file
    # log = pd.read_csv('Changes.csv', sep=';')  # First
    log = pd.read_csv('Changes.csv', sep=';', index_col=0, parse_dates=['date'])
    new_row = {'date': datetime.now(), 'name new':  f'{i}_Temporary_change.csv',
               'name old': f'{i}_Before_change.csv', 'mail': user_email, 'justification': usex_expl}
    log = log.append(new_row, ignore_index=True)
    st.write(log)
    log.to_csv('Changes.csv', sep=';')
    st.write(log)


update_but = st.button('Update Df')
if update_but:
    st.writ(df.loc[df_change['File name'].isin(df['File name']), :] == df_change.iloc[0,:])

# df_selected = pd.DataFrame(sel_row)
# create_grid_table(df_selected)
# st.write(df_selected)