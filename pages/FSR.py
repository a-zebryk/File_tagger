# import streamlit as st
#
# st.header("This is placeholder for further work, where FSRs will be implemented. ")

import pandas as pd
import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def query_df(df, phrase):
    phrase = phrase.lower()
    return df.query(f'Text.str.contains("{phrase}", na=False)', engine='python')

# def filter_df

@st.cache(allow_output_mutation=True)
def load_data(file_name):
    df = pd.read_csv(file_name, index_col=0)
    # df = df.fillna(False)
    return df

st.set_page_config(layout='wide')
pd.set_option('display.precision', 0)

# Loading data

df = load_data('C:/Users/ebryaga/Desktop/Github/File_tagger/Tagged_July_25_22.csv')
df.columns = ['File name', 'Source', 'Text', 'SN', 'Job', 'Report Type', 'Year', 'Month', 'Day']
df['SN'] = df['SN'].apply(lambda x: str(x).upper().replace("{'", '').replace("'}", '').replace('SET()',''))

print(df.isna().sum())
print(df.isnull().sum())


st.title('Test, test, test')

# input = st.text_input("Please enter the text you want to search within document","Search..")
keyword = st_tags(
    label='# Please enter the text you want to search within document:',
    text='Press enter to add more',
    value=['atlantic'],
    suggestions=['liner', 'houston'],
    maxtags=6,
    key='1')
# st.write(len(keyword))
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
# for filter in filters:
#     if len(filters[1]) > 0:
#         df_result = df_result[df_result[filter[0]].isin(filter[1])]

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


#
# # Aggrid:
df_temp = df.iloc[:2000,:]
df_temp = df_temp[['File name', 'Source', 'SN', 'Job', 'Report Type', 'Year', 'Month', 'Day']]
#
# st.header('This is AG Grid')
# gd = GridOptionsBuilder.from_dataframe(df_temp)
# gd.configure_pagination(enabled=True)
# gd.configure_default_column(editable=True, groupable=True)
#
# # #selection
# # sel_mode = st.radio('Selection Type', options=['single', 'multiple'])
# # gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
# # gridoptions = gd.build()
# # grid_table = AgGrid(df_temp, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED,
# #                     height=500, allow_unsafe_jscode=True, theme= 'fresh')
# # sel_row = grid_table['selected_rows']
# # st.write(sel_row)
#
# gridoptions = gd.build()
# data = AgGrid(df_temp, gridOptions=gridoptions, update_mode=GridUpdateMode.MODEL_CHANGED, data_return_mode=DataReturnMode.AS_INPUT)
# st.info(len(df_temp))
# df_updated = pd.DataFrame(data['selected_rows'])
# st.info(df_updated.info())
#
# st.write(df_temp['Source'].value_counts())



#Aggrid 2
st.header('Found error?')
st.subheader("If you found error and would like to update data please:")
st.write('1. Select checkbox in the row you would like to update\n'
         '2. Pass corrected value in the cell\n'
         '3. Insert your e-mail address and justification\n'
         '4. Double check in "Output" below if the changes are OK and click "Sumbitt Change')

gd = GridOptionsBuilder.from_dataframe(df_temp)
# gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True, groupable=True)
# sel_mode = st.radio('Selection Type', options=['single', 'multiple'])
gd.configure_selection(selection_mode='single', use_checkbox=True)
gridoptions = gd.build()
grid_table = AgGrid(df_temp, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                    height=500,
                    allow_unsafe_jscode=True,
                    enable_enterprise_modules = True,
                    theme='fresh')

sel_row = grid_table["selected_rows"]

user_email = st.text_input('Please enter your e-mail')
usex_expl = st.text_input('Please justify the change')


st.subheader("Verify your change")
st.write(sel_row)
cor_button = st.button("Submitt Change")

# df_selected = pd.DataFrame(sel_row)
# create_grid_table(df_selected)
# st.write(df_selected)