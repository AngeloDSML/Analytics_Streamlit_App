#Importing Libraries
import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


#Titles
st.write("## **Home Sales Data Analytics**")
image_1 = Image.open('Image_1.jpg')
st.image(image_1)

#Description of the tool
st.write('''This tool can be use to analyze residential real estate sales during the development of appraisals, BPOs, and CMAs. 
            It provides stats, histograms, correlation heatmap, and the suggested adjustment for gross living area.''')

st.markdown('---')

st.sidebar.header('File uploader')


#File uploader
uploaded_file = st.sidebar.file_uploader("Choose a subject file")


#Data preview
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
 
  st.markdown('#### **Data uploaded**')
 
  st.write(df.head())
  
  st.markdown('''---
  
 
  #### **Stats**''')
 
  st.write(df.describe())
 
  
   
  st.markdown('''--- 
 
 
  #### **Visualizations**
   
  ''')
   
 
  #Price Trends
  time_df = df[['Sales Date','Sales Price']]
  time_df['Sales Date'] = pd.to_datetime(time_df['Sales Date'])
  time_df = time_df.set_index('Sales Date')  
  time_df = time_df.resample(rule = 'M').mean().round()
  time_df = time_df.sort_index()
  time_df['Month/Year'] = time_df.index.strftime('%m/%Y')
  time_df = time_df.set_index('Month/Year')
  time_df = time_df[-13:-1]
  
  
  fig1, ax = plt.subplots()
  ax.bar(time_df.index,time_df['Sales Price'], color='cadetblue', edgecolor='black', linewidth=0.25)
  ax.plot(time_df.index,time_df['Sales Price'], color='black', linewidth=0.5)
  ax.set_axisbelow(True)
  ax.yaxis.grid(True, color='grey', linewidth=0.2)
  plt.title('Median Price Trend',fontsize=9)
  plt.xlabel('Sales Date',fontsize=8)
  plt.ylabel('Sales Price',fontsize=8)
  plt.xticks(fontsize=5)
  plt.yticks(fontsize=6)
  st.pyplot(fig1)

  percentage_trend_12 = round((((time_df['Sales Price'][-1] - time_df['Sales Price'][0]) / time_df['Sales Price'][0]) * 100),1)
  percentage_trend_3 = round((((time_df['Sales Price'][-1] - time_df['Sales Price'][-3]) / time_df['Sales Price'][-3]) * 100),1)

  st.markdown(f'**3-Month Price change**: {percentage_trend_3}%')
  st.markdown(f'**12-Month Price change**: {percentage_trend_12}%')
  
  st.markdown('''---

  ''')


  #Sales Price Histogram
  fig2, ax = plt.subplots()
  ax.hist(df['Sales Price'], bins=8, color='steelblue',edgecolor='black', linewidth=0.6)
  plt.title('Histogram - Sales Price',fontsize=9)
  plt.xlabel('Sales Price',fontsize=8)
  plt.ylabel('Frequency (# of Properties)',fontsize=8)
  plt.xticks(fontsize=7)
  plt.yticks(fontsize=7)
  st.pyplot(fig2)
 
  st.markdown('''---

  ''')


  #GLA Histogram
  fig3, ax = plt.subplots()
  ax.hist(df['Gross Living Area Sqft'], bins=8, color='steelblue',edgecolor='black', linewidth=0.6)
  plt.title('Histogram - GLA (Gross Living Area)',fontsize=9)
  plt.xlabel('GLA (Gross Living Area)',fontsize=8)
  plt.ylabel('Frequency (# of Properties)',fontsize=8)
  plt.xticks(fontsize=7)
  plt.yticks(fontsize=7)
  st.pyplot(fig3)

  st.markdown('''---

  ''')


  #Site Histogram
  fig4, ax = plt.subplots()
  ax.hist(df['Site Area Sqft'], bins=8, color='steelblue',edgecolor='black', linewidth=0.6)
  plt.title('Histogram - Site',fontsize=9)
  plt.xlabel('Site',fontsize=8)
  plt.ylabel('Frequency (# of Properties)',fontsize=8)
  plt.xticks(fontsize=7)
  plt.yticks(fontsize=7)
  st.pyplot(fig4)

  st.markdown('''---

  ''')


  #Bedrooms Histogram   
  bins = range(1,9)
  fig5, ax = plt.subplots()
  ax.hist(df['Bedrooms'], bins=bins, color='steelblue',edgecolor='black', linewidth=0.6)
  plt.title('Histogram - Bedrooms',fontsize=9)
  plt.xlabel('Bedrooms',fontsize=8)
  plt.ylabel('Frequency (# of Properties)',fontsize=8)
  ax.xaxis.set_ticks(bins)
  plt.xticks(fontsize=7)
  plt.yticks(fontsize=7)
  st.pyplot(fig5)

  st.markdown('''---

  ''')
  

  #Bathrooms Histogram   
  fig6, ax = plt.subplots()
  ax.hist(df['Bathrooms'], bins=bins, color='steelblue',edgecolor='black', linewidth=0.6)
  plt.title('Histogram - Bathrooms',fontsize=9)
  plt.xlabel('Bathrooms',fontsize=8)
  plt.ylabel('Frequency (# of Properties)',fontsize=8)
  ax.xaxis.set_ticks(bins)
  plt.xticks(fontsize=7)
  plt.yticks(fontsize=7)
  st.pyplot(fig6)

  st.markdown('''---

  ''')


  #Correlation Matrix
  corrdf = df[['Sales Price','Gross Living Area Sqft','Site Area Sqft','Bedrooms','Bathrooms','Garage Spaces']]
  fig7, ax = plt.subplots()
  sns.heatmap(corrdf.corr(),
              linewidths = 0.25,
              square = True,
              cmap = 'RdBu_r',
              linecolor = 'black',
              annot= True,
              annot_kws={'size': 7});

  plt.title("Correlation Matrix",fontsize=9)
  plt.xticks(fontsize=7)
  plt.yticks(fontsize=7)
  st.pyplot(fig7)
  
  st.markdown('''---

  ''')


  #GLA / Sales Price Visualization
  fig8, ax = plt.subplots()
  sns.regplot(x='Gross Living Area Sqft', y='Sales Price', data=df)
  plt.title("Scatter Plot - GLA & Sales Price",fontsize=9)
  plt.xlabel('GLA',fontsize=8)
  plt.ylabel('Sales Price',fontsize=8)
  plt.xticks(fontsize=7)
  plt.yticks(fontsize=7)
  st.pyplot(fig8)
    
  st.markdown('''---

  ''')


  #GLA Adjustment
  gla_fit = np.polyfit(df['Gross Living Area Sqft'], df['Sales Price'],1)
  gla_fit_fn = np.poly1d(gla_fit)
  st.write(f'##### GLA Adjustment (Based on Linear Regression)= $ {round(gla_fit[0],2)} / sf')
  st.write(f'###### Slope = {round(gla_fit[0],2)} , Intercept = {round(gla_fit[1],2)}')
    
  st.markdown('''---


  ##### 😁 🍻
  
   
  ''')
