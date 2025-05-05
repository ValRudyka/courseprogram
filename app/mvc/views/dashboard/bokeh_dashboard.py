from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.palettes import Category10, Viridis256
from bokeh.transform import factor_cmap
import pandas as pd

def create_bokeh_dashboard(data):
    df = pd.DataFrame(data)
    crime_types_chart = create_crime_types_chart(df)
    temporal_chart = create_temporal_trends_chart(df)
    location_chart = create_location_chart(df)
    profession_chart = create_profession_chart(df)
    
    dashboard = layout([
        [crime_types_chart, location_chart],
        [temporal_chart, profession_chart]
    ], sizing_mode='stretch_both')
    
    html = file_html(dashboard, CDN, "Дашборд злочинців")
    return html

def create_crime_types_chart(df):
    if 'Тип злочину' in df.columns and not df['Тип злочину'].isna().all():
        crime_counts = df['Тип злочину'].value_counts().reset_index()
        crime_counts.columns = ['crime_type', 'count']
        
        crime_counts = crime_counts[crime_counts['crime_type'].notna() & (crime_counts['crime_type'] != '')]
        
        if len(crime_counts) == 0:
            return create_empty_chart("Немає даних про типи злочинів")
        
        source = ColumnDataSource(crime_counts)
        
        p = figure(
            x_range=crime_counts['crime_type'].tolist(),
            height=350,
            title="Розподіл за типами злочинів",
            toolbar_location="right",
            tools="pan,box_zoom,reset,save"
        )
        
        color_palette = Category10[len(crime_counts) if len(crime_counts) < 10 else 10]
        color_mapper = factor_cmap('crime_type', palette=color_palette, factors=crime_counts['crime_type'].tolist())
        
        bars = p.vbar(
            x='crime_type',
            top='count',
            width=0.9,
            source=source,
            line_color='white',
            fill_color=color_mapper
        )
        
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_orientation = 1.0
        
        p.add_tools(HoverTool(tooltips=[
            ("Тип злочину", "@crime_type"),
            ("Кількість", "@count")
        ]))
        
        return p
    else:
        return create_empty_chart("Немає даних про типи злочинів")

def create_temporal_trends_chart(df):
    if 'Дата останньої справи' in df.columns and not df['Дата останньої справи'].isna().all():
        df['date'] = pd.to_datetime(df['Дата останньої справи'], errors='coerce')
        
        df_dates = df[df['date'].notna()].copy()
        
        if len(df_dates) == 0:
            return create_empty_chart("Немає даних про дати злочинів")
        
        df_dates['year'] = df_dates['date'].dt.year
        yearly_counts = df_dates.groupby('year').size().reset_index()
        yearly_counts.columns = ['year', 'count']
        yearly_counts = yearly_counts.sort_values('year')
        
        yearly_counts['date'] = pd.to_datetime(yearly_counts['year'].astype(str) + '-01-01')
        
        source = ColumnDataSource(yearly_counts)
        
        p = figure(
            height=350, 
            title="Динаміка злочинності (за роками)",
            x_axis_type="datetime",
            toolbar_location="right",
            tools="pan,box_zoom,reset,save"
        )
        
        line = p.line('date', 'count', source=source, line_width=3, line_color="navy", legend_label="Кількість злочинів")
        circles = p.circle('date', 'count', source=source, size=10, color="navy", alpha=0.7)
        
        p.add_tools(HoverTool(
            renderers=[circles],
            tooltips=[
                ("Рік", "@year"),
                ("Кількість", "@count")
            ]
        ))
        
        p.xaxis.axis_label = "Рік"
        p.yaxis.axis_label = "Кількість злочинів"
        
        p.legend.location = "top_left"
        p.legend.click_policy = "hide"
        
        return p
    else:
        return create_empty_chart("Немає даних про дати злочинів")

def create_location_chart(df):
    if 'Місце останньої справи' in df.columns and not df['Місце останньої справи'].isna().all():
        location_counts = df['Місце останньої справи'].value_counts().reset_index()
        location_counts.columns = ['location', 'count']
        
        location_counts = location_counts[location_counts['location'].notna() & (location_counts['location'] != '')]
        location_counts = location_counts.head(10)
        
        if len(location_counts) == 0:
            return create_empty_chart("Немає даних про місця злочинів")
        
        source = ColumnDataSource(location_counts)
        
        p = figure(
            y_range=location_counts['location'].tolist(),
            height=350,
            title="Географічний розподіл злочинів (топ 10)",
            toolbar_location="right",
            tools="pan,box_zoom,reset,save"
        )
        
        color_palette = Viridis256[:len(location_counts)]
        color_mapper = factor_cmap('location', palette=color_palette, factors=location_counts['location'].tolist())
        
        bars = p.hbar(
            y='location',
            right='count',
            height=0.9,
            source=source,
            line_color='white',
            fill_color=color_mapper,
            legend_field="location"
        )
        
        p.xgrid.grid_line_color = None
        p.x_range.start = 0
        
        p.add_tools(HoverTool(tooltips=[
            ("Місце", "@location"),
            ("Кількість", "@count")
        ]))
        
        return p
    else:
        return create_empty_chart("Немає даних про місця злочинів")

def create_profession_chart(df):
    if 'Професії' in df.columns and not df['Професії'].isna().all():
        all_professions = []
        for prof_str in df['Професії'].dropna():
            if prof_str and isinstance(prof_str, str):
                professions = [p.strip() for p in prof_str.split(',')]
                all_professions.extend(professions)
        
        if not all_professions:
            return create_empty_chart("Немає даних про професії злочинців")
        
        profession_counts = pd.Series(all_professions).value_counts().reset_index()
        profession_counts.columns = ['profession', 'count']
        
        profession_counts = profession_counts.head(10)
        source = ColumnDataSource(profession_counts)
        
        p = figure(
            y_range=profession_counts['profession'].tolist(),
            height=350,
            title="Розподіл злочинців за професіями (топ 10)",
            toolbar_location="right",
            tools="pan,box_zoom,reset,save"
        )
        
        color_palette = Category10[len(profession_counts) if len(profession_counts) < 10 else 10]
        color_mapper = factor_cmap('profession', palette=color_palette, factors=profession_counts['profession'].tolist())
        
        bars = p.hbar(
            y='profession',
            right='count',
            height=0.9,
            source=source,
            line_color='white',
            fill_color=color_mapper,
            legend_field="profession"
        )
        
        p.xgrid.grid_line_color = None
        p.x_range.start = 0
        
        p.add_tools(HoverTool(tooltips=[
            ("Професія", "@profession"),
            ("Кількість", "@count")
        ]))
        return p
    else:
        return create_empty_chart("Немає даних про професії злочинців")

def create_empty_chart(message):
    p = figure(height=350, tools="")
    p.title.text = message
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.grid.visible = False
    p.outline_line_color = None
    
    return p