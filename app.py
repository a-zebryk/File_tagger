import pandas as pd
import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def query_df(df, phrase):
    phrase = phrase.lower()
    return df.query(f'Text.str.contains("{phrase}", na=False)', engine='python')

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


st.header('Data search app')
st.write("All of the files can be found at: **\\Bhifdnbj4j\Shared\ROP**")
# input = st.text_input("Please enter the text you want to search within document","Search..")
keyword = st_tags(
    label='# Please enter the text you want to search within document:',
    text='Press enter to add more',
    value=['atlantic'],
    suggestions=['liner', 'houston'],
    maxtags=6,
    key='1')
st.write(len(keyword))

df_filter = df.copy()
if len(keyword) > 0:
    for x in range(len(keyword)):
        df_result = query_df(df_filter, keyword[x])
        df_filter = df_result

    st.write(f"**Found {df_result.shape[0]} results**")
    st.dataframe(df_result.style.set_precision(0))
else:
    st.write(f"**Found {df.shape[0]} results**")
    st.dataframe(df)


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

gd = GridOptionsBuilder.from_dataframe(df_temp)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True, groupable=True)
sel_mode = st.radio('Selection Type', options=['single', 'multiple'])
gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
gridoptions = gd.build()
grid_table = AgGrid(df_temp, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
                    height=500,
                    allow_unsafe_jscode=True,
                    # enable_enterprise_modules = True,
                    theme='fresh')

sel_row = grid_table["selected_rows"]
st.subheader("Output")
st.write(sel_row)

df_selected = pd.DataFrame(sel_row)
st.write(df_selected)