import pandas as pd


def water_coeff():
	df_water_coeff = pd.read_excel('TuoiNuoc-Autosaved.xlsx',sheet_name='Sheet5')

	return df_water_coeff.dropna()

def plant_progress():
	df_plant_progress = pd.read_excel('TuoiNuoc-Autosaved.xlsx',sheet_name='Sheet4',index_col=0)

	return df_plant_progress.dropna()

def climate():
	df = pd.read_excel('TuoiNuoc-Autosaved.xlsx',sheet_name='Sheet8')
	#print(df['Nhiệt độ trung bình hằng ngày'])

	return df

climate()