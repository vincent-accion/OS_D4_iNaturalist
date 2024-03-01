import pandas as pd
from pyinaturalist import *
import inspect
import os
# from pyinaturalist_convert import *
import os
import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import plotly.express as px
import math
import plotly.graph_objects as go
import numpy as np
import ast
from matplotlib.colors import LinearSegmentedColormap

os.chdir('C:/Users/vince/Documents/_Université/M1/Open Science/OS_Code')

df_Inat_09_16 = pd.read_csv('09_16_inat_data_filtered.csv', header = 0)
df_inat_17_23 = pd.read_csv('inat_data_filtered_17-23.csv', header = 0)
df_article_03_16 = pd.read_csv('article_data_location_col.csv', header=0)


# CHOOSE THE PARAMETERS FOR THE PLOTTING
km_chosen = 50
transparency = 0.35
# chosen_df = df_article_03_16
# chosen_df = df_inat_17_23
chosen_df = df_Inat_09_16
# name_end_chosen = 'CORRECTED_final_brown_colored_' # choisis le nom du df de fin pour le save en CSV
name_end_chosen = 'CORRECTED_final_inat_09-16_colored_'
# name_end_chosen = 'CORRECTED_final_inat_17-23_colored_'
title_end = f'Distribution of the BROWN&Al (03-16) datatset per {km_chosen} km²'
# title_end = f'Distribution of the INaturalist (09-16) datatset per {km_chosen} km²'


# big grid around UK
# always LONG and LAT
north_west_corner = [-10, 60]
north_est_corner = [5, 60]
south_west_corner = [-10, 49]
south_est_corner = [5, 49]

d_top_north = 832.13
d_side_est_west = 1223.09
d_bottom_south = 1092.42

def center_box(km_decoup):
    
    print('1. center_box() -- centers computation started')
    
    # VERTICAL
    
    degtobox_vertical = (abs(north_west_corner[1] - south_west_corner[1])/(d_side_est_west/km_decoup))/2
    # print(degtobox_vertical)
    
    # VERTICAL centers
    
    nb_box_vetical = math.ceil(d_side_est_west/km_decoup)
    # print(f'{nb_box_vetical = }') 
    
    vertical_degtobox_list = []
    
    vertical_degtobox_list.append(north_west_corner[1])
    vertical_degtobox_list.append(north_west_corner[1] - degtobox_vertical)
    for a in range(1, nb_box_vetical):
        vertical_degtobox_list.append(vertical_degtobox_list[-1] - 2*degtobox_vertical)
    
    # HORIZONTAL
    number_vertical_lines = len(vertical_degtobox_list)
    # print(f'{vertical_degtobox_list = }')
    # print(f'{number_vertical_lines = }')
    # print(f'{nb_box_vetical = }')
    
    temp_rate_h = (d_bottom_south-d_top_north)/nb_box_vetical
    list_distance_deg_horizontal:list = [d_top_north+i*temp_rate_h for i in range(0,nb_box_vetical+1,1)]
    # print(f'{list_distance_deg_horizontal = }')
    # print(f'{len(list_distance_deg_horizontal) = }')
    
    degtobox_horiz_per_long:list = []
    for dist_horiz_long in list_distance_deg_horizontal:
        deg_horiz_temp = (abs(north_west_corner[0] - north_est_corner[0])/(dist_horiz_long/km_decoup))/2
        degtobox_horiz_per_long.append(deg_horiz_temp)  
        
    # print(f'{len(degtobox_horiz_per_long) = }')
    # print(f'{(degtobox_horiz_per_long) = }')
    # HORIZONTAL centers
    
    top_to_bottom_boxnb = []
    
    full_h_dict = {}
    
    for nb in range(1, len(degtobox_horiz_per_long)):
        temp_list_center_h = []
        temp_list_center_h.append(south_west_corner[0])
        temp_list_center_h.append(south_west_corner[0] + degtobox_horiz_per_long[-nb])
        
        box_number_per_dkm = list_distance_deg_horizontal[-nb]/km_decoup
        top_to_bottom_boxnb.append(box_number_per_dkm)
        
        for nb_box in range(0,math.ceil(box_number_per_dkm)):
            temp_list_center_h.append(temp_list_center_h[-1] + 2*degtobox_horiz_per_long[-nb])
            
        
        # print(f'{(box_number_per_dkm) = }')
        # print(f'{len(temp_list_center_h) = }')
        
        full_h_dict.update({box_number_per_dkm : temp_list_center_h})
        # print(full_h_dict)
        
    top_to_bottom_boxnb = top_to_bottom_boxnb[::-1]
    # print(f'{(top_to_bottom_boxnb) = }')
    
    
    # print(f'{len(vertical_degtobox_list) = }')
    # print(f'{len(full_h_dict) = }')
    
    # print(vertical_degtobox_list) 
    # print(f'{full_h_dict = }') 
    
    # vertical_degtobox_list_top_to_bottom = vertical_degtobox_list[::-1]
    # print(f'{vertical_degtobox_list_top_to_bottom = }')  
    
    # centers_horiz_full_list_top_to_bottom is the coord of the center of every box distributed horizonally
    # degtobox_horiz_per_long is the size of the box in degree for each longitude in the same order of the previous list
    
    # vertical_degtobox_list are the centers of the box in the vertical row
    
    return full_h_dict, degtobox_horiz_per_long, vertical_degtobox_list, degtobox_vertical, top_to_bottom_boxnb

center_h, dtb_h, center_v, dtb_v, t2b_box = center_box(km_chosen)
# display(center_h)
# display(dtb_h)
    
    
 # center_h, dtb_h, center_v, dtb_v, t2b_box = center_box(10)

def order_coords(results_center_box_tuple):
    
    print('2. order_coords() -- coords center matrix started')
    
    center_h, dtb_h, center_v, dtb_v, t2b_box = results_center_box_tuple

    dict_end_right_order = {}
    max_length_center_h = math.ceil(max(t2b_box)) + 5
    # print(f'{max_length_center_h = }'

    # for index_c_l in range(0, 1):
    for index_c_l in range(0, len(center_h)):
        
        # housekeeping
        final_list_ro = []
        temp_list_right_order = []
        id = 0
        temp_list = []
        per_line_list = []
        
        id = t2b_box[index_c_l]
        temp_list = center_h[id]
        for horiz_lat in temp_list:
            per_line_list.append([center_v[index_c_l], horiz_lat])
        
        # print(f'{per_line_list = }')
        
        
        frozen = len(per_line_list)
        # print(f'{frozen = }')
        final_list_ro = per_line_list
        
        for q in range(frozen, max_length_center_h, 1):
            final_list_ro.append([0, 0])
        
        dict_end_right_order.update({index_c_l: final_list_ro})
        

    df_end_right_order = (pd.DataFrame(dict_end_right_order)).transpose()
    # display(df_end_right_order)
    
    return df_end_right_order

centers_ordered = order_coords(center_box(km_chosen))

# faire other df avec le nombre de signtings par box pour la couleur

# centers_10_ordered
# df_Inat_09_16
# center_h, dtb_h, center_v, dtb_v, t2b_box = center_box(10)

# 1. read each line et extract location
# 2. check in which box it is (en fonction du bon degtobox)
#     - first check x car c'est plus fast (et le degtobox change pas)
#     - then dans la ligne check le bon y (et le degtobox change par ligne)
# 3. noter la bonne box, donc la bonne coord
# 4. add 1 to the color_coord_df

# faire other df avec le nombre de signtings par box pour la couleur

# centers_10_ordered
# df_Inat_09_16
# center_h, dtb_h, center_v, dtb_v, t2b_box = center_box(10)

# 1. read each line et extract location
# 2. check in which box it is (en fonction du bon degtobox)
#     - first check x car c'est plus fast (et le degtobox change pas)
#     - then dans la ligne check le bon y (et le degtobox change par ligne)
# 3. noter la bonne box, donc la bonne coord
# 4. add 1 to the color_coord_df

def color_coded_box(df_to_search, df_box_ref):

    color_coord_df = pd.DataFrame(np.zeros_like(df_box_ref), columns=df_box_ref.columns)
    dtb_h_df = pd.DataFrame(np.zeros_like(df_box_ref), columns=df_box_ref.columns)
    
    dtb_height_per_point = []

    # 1
    for lign in df_to_search.index:
    # for lign in range(0,1):
        
        series_per_line = df_to_search.iloc[lign,]
        loc_box_quon_cherche_inat = ast.literal_eval(series_per_line['location'])
        # print(loc_box_quon_cherche_inat)
        # print(f'{loc_box_quon_cherche_inat = }')
        
        # 2.a find the x, ie the ligne on which this dot is
        for coord_tmp in df_box_ref.index:
            # print(coord_tmp)
            coord_n1_x = (df_box_ref.iloc[coord_tmp, 1])[0]
            
            # print(f'{type(coord_n1_x) = }')
            if (coord_n1_x - dtb_v) < loc_box_quon_cherche_inat[0] <= (coord_n1_x + dtb_v):
                
                index_coord_n1_x_FOUND = coord_tmp
                coord_n1_x_FOUND = coord_n1_x
                # 2.b now on try to find y, soit la colone
                lign_of_right_x = df_box_ref.iloc[index_coord_n1_x_FOUND]
                
                for y_search_list_index in range(0, len(lign_of_right_x)):
                    # need find right dtb_h
                    right_d2bx_line = dtb_h[index_coord_n1_x_FOUND]
                    list_y_search = lign_of_right_x[y_search_list_index]
                    
                    if (list_y_search[1] - right_d2bx_line) <  loc_box_quon_cherche_inat[1] <= (list_y_search[1] + right_d2bx_line):
                        index_coord_n2_y_FOUND = y_search_list_index
                        coord_n2_y_FOUND = list_y_search[1]
                        
                        
                        # now on add 1 au df des couleurs
                        temp_color_basis = float(color_coord_df.at[index_coord_n1_x_FOUND, index_coord_n2_y_FOUND]) + 1
                        
                        color_coord_df.at[index_coord_n1_x_FOUND, index_coord_n2_y_FOUND] = temp_color_basis
                        
                        dtb_h_df.at[index_coord_n1_x_FOUND, index_coord_n2_y_FOUND] = right_d2bx_line
                        
                        
                        break

    # cleaning up the df pour plotting
    lat_x = []
    lat_y = []
    location_temp = []
    color_not_null = []
    
    for coord_row in color_coord_df.index:
        row_colors = color_coord_df.loc[0]
        for coords_col in range(0, len(row_colors)):
            if color_coord_df.iloc[coord_row, coords_col] != 0:
                color_not_null.append(color_coord_df.iloc[coord_row, coords_col])
                location_temp.append(df_box_ref.iloc[coord_row, coords_col])
                dtb_height_per_point.append(dtb_h_df.iloc[coord_row, coords_col])
    
    
    for loc in location_temp:
        lat_x.append(loc[0])
        lat_y.append(loc[1])
        
    ploting_colored_box = pd.DataFrame({'lat_x': lat_x, 'lat_y': lat_y, 
                                        'color_value': color_not_null,
                                       'dtb_height': dtb_height_per_point,
                                       'dtb_width': [dtb_v]*len(dtb_height_per_point)})

    return color_coord_df, ploting_colored_box

# colors_10_inat_219, plotting_colors_10_inat_219 = color_coded_box(df_Inat_09_16, centers_10_ordered)
colors_chosen_df, plotting_colors_chosen_df = color_coded_box(chosen_df, centers_ordered)

# colors_10_inat_219.to_csv('colors_10_inat2019.csv', header=None, index=None)

# TO CHECK IF NEEDED
# total_sum = color_coord_df.sum().sum()
# print(total_sum)


def get_color(value):
    
    color1 = 'green'
    color2 = 'red'
    
    # Define the custom color range
    colors = [color1, color2]

    # Create a custom colormap
    cmap = LinearSegmentedColormap.from_list('custom_colormap', colors)

    # Get RGB color for the specified value
    rgb_color = cmap(value)[:3]  # Extract RGB values and ignore alpha channel
    
    custom_str_tuple = 'rgba('
    
    for c in rgb_color:
        
        custom_str_tuple = custom_str_tuple + str(int(c * 255)) + ', '
        
    custom_str_tuple = custom_str_tuple + str(transparency) + ')'
    
    return custom_str_tuple


def add_boxes_plot(df_start, title_end):
    
    print('add_boxes_plot() -- adding boxes to the plot')
    percentage = 0
    
    custom_min_value = df_start['color_value'].min()
    custom_max_value = df_start['color_value'].max()
    color_for_min = 'green'
    color_for_max = 'red'
    
    df_start['elsewhere_1'] = [0]*len(df_start)
    
    
    rgb_color_value = []
    for cv in df_start['color_value']:
        rgb_color_value.append(get_color(cv/custom_max_value))
        
    df_start['RBG_custom'] = rgb_color_value
    
    # REGULAR PLOT
    
    fig_select_colored = px.scatter_mapbox(df_start,
                    lat='lat_x',
                    lon='lat_y',
                    color = 'color_value',
                    title=title_end,
                    color_continuous_scale=[(0, color_for_min), (1, color_for_max)],
                    range_color=[custom_min_value, custom_max_value],
                    zoom=5, 
                    height=700,
                    )

    # fig_select_colored.update_layout(mapbox_style="carto-positron", showlegend=False)
    fig_select_colored.update_traces(marker=dict(opacity=0))
    fig_select_colored.update_layout(
                margin={"r":0,"t":80,"l":0,"b":0},
                  mapbox_style="carto-positron",
                  showlegend=True,
                #   legend=dict(
                #     yanchor="top",
                #     y=0.99,
                #     xanchor="left",
                #     x=0.01),
                  )
    
    # custom BOXES    
    
    for index, row in df_start.iterrows():
        lat_y0 = row['lat_x']
        lon_x0 = row['lat_y']
        color_RBG = row['RBG_custom']
        
        # Specify box dimensions (you can adjust width and height as needed)
        deg_y = row['dtb_width']
        deg_x = row['dtb_height']
        # print(height)
        
        # Calculate rectangle coordinates
        lat_y_box = [lat_y0 - deg_y, lat_y0 + deg_y, lat_y0 + deg_y, lat_y0 - deg_y, lat_y0 - deg_y]
        # print(lat_box)
        lon_x_box = [lon_x0 - deg_x, lon_x0 - deg_x, lon_x0 + deg_x, lon_x0 + deg_x, lon_x0 - deg_x]
        
        # Add rectangle trace to the map
        fig_select_colored.add_trace(go.Scattermapbox(
            lat=lat_y_box,
            lon=lon_x_box,
            mode='lines',
            line=dict(color=color_RBG),  # You can set the color of the rectangle border
            fill='toself',
            fillcolor = color_RBG,  # Set the fill color to transparent
            showlegend=False
        ))
        
        percentage = percentage + 1
        print(f'add_boxes_plot() -- progress: {round((percentage/len(df_start))*100, 1)}')

    fig_select_colored.update_layout(mapbox_style="carto-positron")

    # Show the plot
    fig_select_colored.show()
    
    return df_start

plotting_colors_chosen_df = add_boxes_plot(plotting_colors_chosen_df, title_end)
plotting_colors_chosen_df.to_csv(name_end_chosen + str(km_chosen) + 'km.csv', index=None)