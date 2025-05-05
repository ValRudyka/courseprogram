from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
import pandas as pd
from datetime import datetime

class CriminalDashboard:
    def __init__(self, data: dict) -> None:
        self.df = pd.DataFrame(data)
        self.charts = {}
    
    def create_dashboard(self) -> None:
        self.charts['crime_types'] = self.create_crime_types_chart()
        self.charts['temporal'] = self.create_temporal_trends_chart()
        self.charts['age'] = self.create_age_distribution_chart()
        self.charts['profession'] = self.create_profession_chart()
        
        dashboard = layout([
            [self.charts['crime_types'], self.charts['age']],
            [self.charts['temporal'], self.charts['profession']]
        ], sizing_mode='stretch_both')
        
        html = file_html(dashboard, CDN, "Дашборд злочинців")
        return html
    
    def create_empty_chart(self, message: str) -> None:
        p = figure(height=350, tools="")
        p.title.text = message
        p.xaxis.visible = False
        p.yaxis.visible = False
        p.grid.visible = False
        p.outline_line_color = None
        
        return p
    
    def create_crime_types_chart(self) -> figure:
        if 'Тип злочину' in self.df.columns and not self.df['Тип злочину'].isna().all():
            crime_counts = self.df['Тип злочину'].value_counts().reset_index()
            crime_counts.columns = ['crime_type', 'count']
            
            crime_counts = crime_counts[crime_counts['crime_type'].notna() & (crime_counts['crime_type'] != '')]
            
            if len(crime_counts) == 0:
                return self.create_empty_chart("Немає даних про типи злочинів")
            
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
            return self.create_empty_chart("Немає даних про типи злочинів")
    
    def create_temporal_trends_chart(self) -> figure:
        if 'Дата останньої справи' in self.df.columns and not self.df['Дата останньої справи'].isna().all():
            self.df['date'] = pd.to_datetime(self.df['Дата останньої справи'], errors='coerce')
            
            df_dates = self.df[self.df['date'].notna()].copy()
            
            if len(df_dates) == 0:
                return self.create_empty_chart("Немає даних про дати злочинів")
                
            df_dates['year'] = df_dates['date'].dt.year
            df_dates['month'] = df_dates['date'].dt.month
            df_dates['year_month'] = df_dates['date'].dt.to_period('M')
            
            yearly_counts = df_dates.groupby('year').size().reset_index()
            yearly_counts.columns = ['year', 'count']
            yearly_counts = yearly_counts.sort_values('year')
            yearly_counts['date'] = pd.to_datetime(yearly_counts['year'].astype(str) + '-01-01')
            
            if len(df_dates) >= 10: 
                monthly_counts = df_dates.groupby('year_month').size().reset_index()
                monthly_counts.columns = ['year_month', 'count']
                monthly_counts = monthly_counts.sort_values('year_month')
                monthly_counts['date'] = monthly_counts['year_month'].dt.to_timestamp()
                monthly_counts['month_year_str'] = monthly_counts['date'].dt.strftime('%b %Y')
                
                monthly_source = ColumnDataSource(monthly_counts)
                p = figure(
                    height=350, 
                    title="Динаміка злочинності за часом",
                    x_axis_type="datetime",
                    toolbar_location="right",
                    tools="pan,box_zoom,wheel_zoom,reset,save"
                )
                
                yearly_source = ColumnDataSource(yearly_counts)
                yearly_line = p.line('date', 'count', source=yearly_source, 
                              line_width=2, line_color="navy", alpha=0.7,
                              legend_label="Річна кількість")
                
                monthly_line = p.line('date', 'count', source=monthly_source, 
                              line_width=3, line_color="#cc3333", alpha=0.8, 
                              legend_label="Помісячна кількість")
                monthly_points = p.scatter('date', 'count', source=monthly_source, 
                                 size=6, color="#cc3333", alpha=0.5)
                
                hover = HoverTool(
                    tooltips=[
                        ("Дата", "@month_year_str"),
                        ("Кількість", "@count злочинів"),
                    ],
                    mode="vline",
                    renderers=[monthly_line]
                )
                p.add_tools(hover)
                
            else:
                source = ColumnDataSource(yearly_counts)
                
                p = figure(
                    height=350, 
                    title="Динаміка злочинності (за роками)",
                    x_axis_type="datetime",
                    toolbar_location="right",
                    tools="pan,box_zoom,wheel_zoom,reset,save"
                )
                
                line = p.line('date', 'count', source=source, line_width=3, 
                             line_color="navy", legend_label="Кількість злочинів")
                points = p.scatter('date', 'count', source=source, size=8, 
                                  color="navy", alpha=0.7)
                
                hover = HoverTool(
                    renderers=[points],
                    tooltips=[
                        ("Рік", "@year"),
                        ("Кількість", "@count злочинів")
                    ]
                )
                p.add_tools(hover)
            
            p.xaxis.axis_label = "Час"
            p.yaxis.axis_label = "Кількість злочинів"
            p.y_range.start = 0 
            
            p.xgrid.grid_line_color = "lightgray"
            p.xgrid.grid_line_alpha = 0.4
            p.ygrid.grid_line_color = "lightgray"
            p.ygrid.grid_line_alpha = 0.4
            
            p.legend.location = "top_left"
            p.legend.click_policy = "hide"
            p.legend.background_fill_alpha = 0.3
            
            return p
        else:
            return self.create_empty_chart("Немає даних про дати злочинів")
    
    def create_age_distribution_chart(self) -> figure:
        if 'Дата народження' in self.df.columns and not self.df['Дата народження'].isna().all():
            df_valid = self.df.copy()
            df_valid['birth_date'] = pd.to_datetime(df_valid['Дата народження'], errors='coerce')
            
            df_valid = df_valid[df_valid['birth_date'].notna()]
            
            if len(df_valid) == 0:
                return self.create_empty_chart("Немає даних про вік злочинців")
            
            today = datetime.now()
            df_valid['age'] = df_valid['birth_date'].apply(lambda x: today.year - x.year - 
                                                       ((today.month, today.day) < (x.month, x.day)))
            
            age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
            age_labels = ["До 18", "18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
            
            df_valid['age_group'] = pd.cut(df_valid['age'], bins=age_bins, labels=age_labels, right=False)
            
            age_counts = df_valid['age_group'].value_counts().reset_index()
            age_counts.columns = ['age_group', 'count']
            age_counts = age_counts.sort_values('age_group')
            
            source = ColumnDataSource(age_counts)
            
            p = figure(
                y_range=age_counts['age_group'].tolist(),
                height=350,
                title="Віковий розподіл злочинців",
                toolbar_location="right",
                tools="pan,box_zoom,reset,save"
            )
            
            bars = p.hbar(
                y='age_group',
                right='count',
                height=0.7,
                source=source,
                line_color='white',
                fill_color="#0099ff"
            )
            
            p.xgrid.grid_line_color = None
            p.x_range.start = 0
            
            p.add_tools(HoverTool(tooltips=[
                ("Віковий діапазон", "@age_group"),
                ("Кількість", "@count")
            ]))
            
            return p
        else:
            return self.create_empty_chart("Немає даних про вік злочинців")
    
    def create_profession_chart(self) -> figure:
        if 'Професії' in self.df.columns and not self.df['Професії'].isna().all():
            all_professions = []
            for prof_str in self.df['Професії'].dropna():
                if prof_str and isinstance(prof_str, str):
                    professions = [p.strip() for p in prof_str.split(',')]
                    all_professions.extend(professions)
            
            if not all_professions:
                return self.create_empty_chart("Немає даних про професії злочинців")
            
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
                height=0.7,
                source=source,
                line_color='white',
                fill_color=color_mapper
            )
            
            p.xgrid.grid_line_color = None
            p.x_range.start = 0
            
            p.add_tools(HoverTool(tooltips=[
                ("Професія", "@profession"),
                ("Кількість", "@count")
            ]))
            
            return p
        else:
            return self.create_empty_chart("Немає даних про професії злочинців")