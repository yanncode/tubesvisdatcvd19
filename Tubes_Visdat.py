import numpy as np
import pandas as pd

from bokeh.io import curdoc, show
from bokeh.models.widgets import Tabs
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.models import Panel, Spinner, ColorPicker, ColumnDataSource, Slider
from bokeh.layouts import column, row

data = pd.read_csv('Data Set 2.csv')
curdoc().theme = 'night_sky'

del data['longitude']
del data['latitude']
del data['iso_code']
del data['population']
del data['population_kmsquare']
del data['capital_city']

def barplot(data):
    source = ColumnDataSource(data)

    daftar_provinsi = source.data['province_name'].tolist()
    daftar_provinsi.reverse()

    bar_plot = figure(
        y_range=daftar_provinsi,
        plot_width=1000,
        plot_height=800,
        title='Jumlah Kasus Meninggal Karena COVID-19',
        x_axis_label='Jumlah Meninggal',
        y_axis_label='Provinsi',
        tools="zoom_in,zoom_out,save,reset",
        toolbar_location='above'
    )

    bar =  bar_plot.hbar(
        y='province_name',
        right='deceased',
        left=0,
        height=0.5,
        fill_color='red',
        color = 'white',
        fill_alpha=0.5,
        source=source,
    )

    hover = HoverTool()
    hover.tooltips = """
      <div>
        <h3>@province_name</h3>
        <div><strong>Id Provinsi: </strong>@province_id</div>
        <div><strong>Pulau: </strong>@island</div>
        <div><strong>Terkonfirmasi Positif: </strong>@confirmed</div>
        <div><strong>Meninggal: </strong>@deceased</div>
        <div><strong>Sembuh: </strong>@released</div>
      </div>
    """
    bar_plot.add_tools(hover)

    spinner1 = Spinner(title="Bar Height", low=0.1, high=1, step=0.1, value=0.5, width=200)
    spinner1.js_link('value', bar.glyph, 'height')

    spinner2 = Spinner(title="Bar Fill Alpha", low=0.1, high=1, step=0.1, value=0.5, width=200)
    spinner2.js_link('value', bar.glyph, 'fill_alpha')

    picker = ColorPicker(title="Bar Color", width = 200)
    picker.js_link('color', bar.glyph, 'fill_color')

    widgets = column(spinner1, spinner2, picker)

    layout = row(widgets, bar_plot)

    tab_bar = Panel(child=layout, title="BAR PLOT")

    return tab_bar

def lineplot(data):
    source = ColumnDataSource(data)

    line_plot = figure(
        plot_width=1000,
        plot_height=800,
        title='Jumlah Kasus Terkonfirmasi Positif COVID-19',
        x_axis_label='Id Provinsi',
        y_axis_label='Jumlah Positif',
    )

    hover = HoverTool()
    hover.tooltips = """
      <div>
        <h3>@province_name</h3>
        <div><strong>Id Provinsi: </strong>@province_id</div>
        <div><strong>Pulau: </strong>@island</div>
        <div><strong>Terkonfirmasi Positif: </strong>@confirmed</div>
        <div><strong>Meninggal: </strong>@deceased</div>
        <div><strong>Sembuh: </strong>@released</div>
      </div>
    """
    line_plot.add_tools(hover)

    line =  line_plot.line(x='province_id', y='confirmed', line_width=3, source=source)

    slider = Slider(start=1, end=10, step=1, value=3, title='Line Width', width=200)
    slider.js_link('value', line.glyph, 'line_width')

    picker = ColorPicker(title="Line Color", width = 200)
    picker.js_link('color', line.glyph, 'line_color')

    widgets = column(slider, picker)

    layout = row(widgets, line_plot)

    tab_line = Panel(child=layout, title="LINE PLOT")

    return tab_line


#main
tab_bar = barplot(data)
tab_line = lineplot(data)

tabs = Tabs(tabs=[tab_bar, tab_line])

curdoc().add_root(tabs)
#show(tabs)