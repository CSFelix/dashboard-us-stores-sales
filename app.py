# pip install pipreqs
# pipreqs --encoding=utf8

import os
from pathlib import Path

import streamlit as st # pip install streamlit
from streamlit_option_menu import option_menu # pip install streamlit-option-menu
from streamlit_extras.colored_header import colored_header # pip install streamlit-extras
from streamlit_extras.metric_cards import style_metric_cards # pip install streamlit-extras
import plotly.express as px # pip install plotly
import pandas as pd # pip install pandas



# ---- PATH SETTINGS ----
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
css_file = current_dir / 'css' / 'main.css'
data_file = current_dir / 'datas' / 'sales.csv'


# ---- VARIABLES ----
PAGE_TITLE = 'US Stores Sales'
PAGE_ICON = ':bar_chart:'
PAGE_LAYOUT = 'wide'
DATA_SIZE = round(os.path.getsize(data_file) / 1024, 2)

BOX_BAR_PLOT_FEATURES = ('Profit', 'Margin', 'Sales', 'COGS', 'Total_Expenses', 'Marketing', 'Inventory')
BOX_BAR_PLOT_OPTIONS = ('Box Plot', 'Bar Plot')
REGRESSION_PLOT_FEATURES = ('Profit', 'Margin', 'Sales', 'COGS', 'Total_Expenses', 'Inventory')
PIE_PLOT_FEATURES = ('Profit', 'Margin', 'Sales', 'COGS', 'Total_Expenses', 'Marketing', 'Inventory')

SOCIAL_MEDIA = {
	'GitHub': 'https://github.com/csfelix'
	, 'Kaggle': 'https://www.kaggle.com/dsfelix'
	, 'Portfolio': 'https://csfelix.github.io'
	, 'LinkedIn': 'https://linkedin.com/in/csfelix'
	, 'Email': 'csfelix08@gmail.com'
}

# ---- PAGE SETTINGS ----
st.set_page_config(
	page_title=PAGE_TITLE
	, page_icon=PAGE_ICON
	, layout=PAGE_LAYOUT
)


# ---- LOADING CSS AND DATAFRAME ----
with open(css_file) as f:
	st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df = pd.read_csv(data_file)


##########################

# ---- SIDEBAR ----
#
# Just a reminder to myself in the future: Sidebar does not support
# Expanders (at least today: January 11th 2023).
st.sidebar.title('Please Filter Here')
st.sidebar.markdown('----')

# Area Code Filters
min_area_code = min(df['Area_Code'].unique().tolist())
max_area_code = max(df['Area_Code'].unique().tolist())

st.sidebar.info('Area Code')
area_code = st.sidebar.slider(
	'Select the Area Code Range:'
	, min_value=min_area_code
	, max_value=max_area_code
	, value=(min_area_code, max_area_code)
)
st.sidebar.markdown('----')


# Market Filters
st.sidebar.info('Market Filters')
state = st.sidebar.multiselect('Select the State:', options=df['State'].unique(), default=df['State'].unique())
market = st.sidebar.multiselect('Select the Market Region:', options=df['Market'].unique(), default=df['Market'].unique())
market_size = st.sidebar.multiselect('Select the Market Size:', options=df['Market_Size'].unique(), default=df['Market_Size'].unique())
st.sidebar.markdown('----')

# Product Filters
st.sidebar.info('Product Filters')
product_type = st.sidebar.multiselect('Select the Product Type:', options=df['Product_Type'].unique(), default=df['Product_Type'].unique())
product = st.sidebar.multiselect('Select the Product:', options=df['Product'].unique(), default=df['Product'].unique())
flavor_type = st.sidebar.multiselect('Select the Flavor Type:', options=df['Type'].unique(), default=df['Type'].unique())


# Filtering Dataset
df_selection = df.query(
	"State == @state & Market == @market & Market_Size == @market_size &" \
	"Product == @product & Product_Type == @product_type & Type == @flavor_type &" \
	"Area_Code >= @area_code[0] & Area_Code <= @area_code[1]"
)



# ---- TITLE ----
colored_header(
	label='🛍️ US Stores Sales'
	, description='US Stores Sales Between 2010 and 2011'
	, color_name='violet-70'
)
st.markdown('#')



# ---- HORIZONTAL MENU ----
selected = option_menu(
	menu_title=None
	, options=['Dataset', 'Metrics', 'Dashboard', 'Credits']
	, icons=['clipboard-data', 'card-text', 'bar-chart-line', 'person-badge']
	, default_index=0
	, orientation='horizontal'
	, styles={"container": {"padding": "5px"}}
)



# ---- DATASET VISUALIZATION ----
if selected == 'Dataset':
	# Metric Cards
	col1, col2, col3 = st.columns(3)
	col1.metric(label='Nº Registers', value=df_selection.shape[0])
	col2.metric(label='Nº Features', value=df_selection.shape[1])
	col3.metric(label='File Size', value=f'{DATA_SIZE} kB')
	style_metric_cards(
		background_color='#0a394d'
		, border_left_color='#7159c1'
		, border_color='#f6f6ff'
		, border_size_px=5
		, border_radius_px=100
		, box_shadow=True
	)

	# Dataframe
	st.dataframe(df_selection)

	# Target Description
	with st.expander('🎯 Target Feature', expanded=True):
		st.info('Sales')
		st.write('Value Acquired in Sales (U$)')

	# Features Descriptions
	with st.expander('📝 Features', expanded=False):
		# Area Code
		st.info('Area Code')
		st.write("Store's Code")
		st.markdown('#')

		# State
		st.info('State')
		st.write("Store's State")
		st.markdown('#')

		# Market
		st.info('Market')
		st.write("Store's Region")
		st.markdown('#')

		# Market Size
		st.info('Market Size')
		st.write("Store's Size")
		st.markdown('#')

		# Profit
		st.info('Profit')
		st.write("Profit in Dollars (U$)")
		st.markdown('#')

		# Margin
		st.info('Margin')
		st.write("Profit + Total Expenses (U$)")
		st.markdown('#')

		# OR Sales
		st.info('ORSales')
		st.write("COGS (U$)")
		st.markdown('#')

		# COGS
		st.info('COGS')
		st.write("Cost of Goods Sold (U$)")
		st.markdown('#')

		# Total Expenses
		st.info('Total Expenses')
		st.write("Total Expenses to get the Product to Selling (U$)")
		st.markdown('#')

		# Marketing
		st.info('Markting')
		st.write("Expenses in Marketing (U$)")
		st.markdown('#')

		# Inventory
		st.info('Inventory')
		st.write("Inventory Value of the Product in the Sale Moment (U$)")
		st.markdown('#')

		# Budget Profit
		st.info('Budget Profit')
		st.write("Expected Profit (U$)")
		st.markdown('#')

		# Budget COGS
		st.info('Budget COGS')
		st.write("Expected COGS (U$)")
		st.markdown('#')

		# Budget Margin
		st.info('Budget Margin')
		st.write("Expected Profit + Expected Total Expenses OR Expected Sales - Expected COGS")
		st.markdown('#')

		# Budget Sales
		st.info('Budget Sales')
		st.write("Expected Value Acquired in Sales (U$)")
		st.markdown('#')

		# Product ID
		st.info('ProductID')
		st.write("Product ID")
		st.markdown('#')

		# Date
		st.info('Date')
		st.write("Sale Date")
		st.markdown('#')

		# Product Type
		st.info('Product Type')
		st.write("Product Category")
		st.markdown('#')

		# Product
		st.info('Product')
		st.write("Product Description")
		st.markdown('#')

		# Type
		st.info('Type')
		st.write("Flavor Type")



# ---- METRICS VISUALIZATION ----
elif selected == 'Metrics':
	# Metric Values
	avg_sales = round(df_selection['Sales'].mean(), 2)
	avg_cogs = round(df_selection['COGS'].mean(), 2)
	avg_margin = round(df_selection['Margin'].mean(), 2)
	avg_total_expenses = round(df_selection['Total_Expenses'].mean(), 2)
	avg_marketing = round(df_selection['Marketing'].mean(), 2)
	avg_profit = round(df_selection['Profit'].mean(), 2)
	avg_inventory = round(df_selection['Inventory'].mean(), 2)
	perc_small_markets = round(len(df_selection['Market_Size'].loc[df_selection['Market_Size'] == 'Small Market']) * 100 / len(df_selection['Market_Size']), 2)
	perc_large_markets = round(len(df_selection['Market_Size'].loc[df_selection['Market_Size'] == 'Major Market']) * 100 / len(df_selection['Market_Size']), 2)

	# Metric Cards
	col1, col2, col3 = st.columns(3)
	col1.metric(label='AVG Sales', value=f'U$ {avg_sales}', delta=avg_sales)
	col2.metric(label='AVG COGS', value=f'U$ {avg_cogs}', delta=avg_cogs * -1)
	col3.metric(label='AVG Margin', value=f'U$ {avg_margin}', delta=avg_margin)

	col4, col5, col6 = st.columns(3)
	col4.metric(label='AVG Total Expenses', value=f'U$ {avg_total_expenses}', delta=avg_total_expenses * -1)
	col5.metric(label='AVG Marketing', value=f'U$ {avg_marketing}', delta=avg_marketing * -1)
	col6.metric(label='AVG Profit', value=f'U$ {avg_profit}', delta=avg_profit)

	col7, col8, col9 = st.columns(3)
	col7.metric(label='AVG Inventory', value=f'U$ {avg_inventory}', delta=avg_inventory)
	col8.metric(label='% Small Markets', value=f'{perc_small_markets} %', delta=0)
	col9.metric(label='% Large Markets', value=f'{perc_large_markets} %', delta=0)	

	style_metric_cards(
		background_color='#0a394d'
		, border_left_color='#7159c1'
		, border_color='#f6f6ff'
		, border_size_px=5
		, border_radius_px=100
		, box_shadow=True
	)


# ---- DASHBBOARD VISUALIZATION ----
elif selected == 'Dashboard':
	# Box and Bar Plots Title
	st.markdown('#')
	st.info('Market Size, Region and State Analysis')

	# Box and Bar Plots Selections
	box_bar_plot_feature = st.selectbox('What would you like to analyse?', BOX_BAR_PLOT_FEATURES)
	box_bar_plot_style = st.selectbox('What style do you like to see?', BOX_BAR_PLOT_OPTIONS)

	# Box and Bar Plots
	if box_bar_plot_style == 'Box Plot':
		small_large_markets_plot = px.box(df_selection, x='Market_Size', y=box_bar_plot_feature, notched=True, color='Market_Size')
		region_markets_plot = px.box(df_selection, x='Market', y=box_bar_plot_feature, notched=True, color='Market')
		states_markets_plot = px.box(df_selection, x='State', y=box_bar_plot_feature, notched=True)

	elif box_bar_plot_style == 'Bar Plot':
		small_large_markets_plot = px.bar(df_selection, x='Market_Size', y=box_bar_plot_feature, color='Market_Size')
		region_markets_plot = px.bar(df_selection, x='Market', y=box_bar_plot_feature, color='Market')
		states_markets_plot = px.bar(df_selection, x='State', y=box_bar_plot_feature)

	small_large_markets_plot.update_layout(legend=dict(orientation="h", itemwidth=70, yanchor="bottom", y=1.02, xanchor="right", x=1))
	region_markets_plot.update_layout(legend=dict(orientation="h", itemwidth=70, yanchor="bottom", y=1.02, xanchor="right", x=1))

	st.plotly_chart(small_large_markets_plot, use_container_width=True)
	st.plotly_chart(region_markets_plot, use_container_width=True)
	st.plotly_chart(states_markets_plot, use_container_width=True)
	st.markdown('----')



	# Regression Plot Title
	st.info('Marketing Correlations')

	# Regression Plot Selection
	regression_plot_feature = st.selectbox('What correlation would you like to analyse?', REGRESSION_PLOT_FEATURES)

	# Regression Plot
	regression_marketing_plot = px.scatter(df_selection, x='Marketing', y=regression_plot_feature, trendline='ols', trendline_color_override='red')
	
	st.plotly_chart(regression_marketing_plot, use_container_width=True)
	st.markdown('----')



	# Pie Plots
	st.info('Market Size and Regions Percentages')

	# Pie Plot Selection
	pie_plot_feature = st.selectbox('What percentage would you like to see?', PIE_PLOT_FEATURES)

	# Pie Plots
	market_size_pie_plot = px.pie(df_selection, values=pie_plot_feature, names='Market_Size')
	market_region_pie_plot = px.pie(df_selection, values=pie_plot_feature, names='Market')

	st.plotly_chart(market_size_pie_plot, use_container_width=True)
	st.plotly_chart(market_region_pie_plot, use_container_width=True)



# ---- CREDITS VISUALIZATION ----
elif selected == 'Credits':
	st.title('📬 Reach Me')
	st.write('#')

	cols = st.columns(len(SOCIAL_MEDIA))
	for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
		cols[index].write(f'[{platform}]({link})')