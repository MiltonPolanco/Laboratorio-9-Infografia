"""Laboratorio 9: infografia estatica reproducible desde la base original.
Ejecutar desde cualquier carpeta: python scripts/generar_entrega.py
"""
from pathlib import Path
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'data' / 'raw' / 'Base_Migracion_2009-2026jun.xlsx'
PROCESSED = ROOT / 'data' / 'processed'
REPORT = ROOT / 'reporte'
NAVY, TEAL, ORANGE = '#17354c', '#087e8b', '#e48a36'
BG, WHITE, MUTED = '#f5f8fa', '#ffffff', '#516678'


def load_data():
    if not RAW.is_file():
        raise FileNotFoundError(f'No se encontro el Excel: {RAW}')
    df = pd.read_excel(RAW, sheet_name='Datos')
    df = df[df['Tipo de Viajero'].isin(['Turista', 'Excursionista'])].copy()
    df['fecha'] = pd.to_datetime(dict(year=df['Año'], month=df['Mes cod'], day=1))
    monthly = df.groupby('fecha')['Viajero'].sum().sort_index().asfreq('MS')
    if monthly.isna().any():
        raise ValueError('Faltan meses en la serie: revisar la base.')
    return df, monthly.astype(float)


def forecast(series):
    train, test = series.loc[:'2023-12-01'], series.loc['2024-01-01':]
    fit = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
                  enforce_stationarity=False, enforce_invertibility=False).fit(
                      disp=False, maxiter=120)
    result = fit.get_forecast(steps=len(test))
    pred, interval = result.predicted_mean, result.conf_int(alpha=0.20)
    out = pd.DataFrame({'observado': test, 'estimacion': pred,
                        'limite_inferior_80': interval.iloc[:, 0],
                        'limite_superior_80': interval.iloc[:, 1]})
    return out, mean_absolute_error(test, pred), np.sqrt(mean_squared_error(test, pred))


def panel(fig, rect, title, subtitle=None):
    x, y, w, h = rect
    fig.add_artist(FancyBboxPatch((x, y), w, h, transform=fig.transFigure,
                   boxstyle='round,pad=0.004,rounding_size=0.009',
                   linewidth=0, facecolor=WHITE, zorder=0))
    fig.text(x + .018, y + h - .028, title, color=NAVY,
             fontsize=13, weight='bold', va='center')
    if subtitle:
        fig.text(x + .018, y + h - .051, subtitle, color=MUTED, fontsize=9.5)
    return fig.add_axes([x + .045, y + .045, w - .075, h - .125], zorder=2)


def note(fig, x, y, text, width=65, size=10, spacing=.021, color=NAVY):
    for i, line in enumerate(textwrap.wrap(text, width=width, break_long_words=False)):
        fig.text(x, y - i * spacing, line, fontsize=size, color=color, va='top')


def make_infographic(df, series, result, mae, rmse):
    fig = plt.figure(figsize=(12, 18.55), facecolor=BG)
    fig.text(.06, .969, 'GUATEMALA: 17 ANOS DE TURISMO EN TRANSFORMACION',
             fontsize=22, weight='bold', color=NAVY)
    fig.text(.06, .948, 'Turistas y excursionistas | Enero 2009 - junio 2026',
             fontsize=12, color=TEAL)
    regions = df.groupby('Región dos')['Viajero'].sum().sort_values(ascending=False)
    routes = df.groupby('Vía')['Viajero'].sum().sort_values(ascending=False)
    kpis = [('VIAJEROS ACUMULADOS', f'{series.sum()/1e6:.1f} millones'),
            ('MESES ANALIZADOS', str(len(series))),
            ('VIA PRINCIPAL', str(routes.index[0])),
            ('REGION LIDER', str(regions.index[0]))]
    for i, (label, value) in enumerate(kpis):
        x, w = .06 + i * .225, .205
        fig.add_artist(FancyBboxPatch((x, .867), w, .063, transform=fig.transFigure,
                       boxstyle='round,pad=0.003,rounding_size=.009',
                       linewidth=0, facecolor=WHITE))
        fig.text(x + .013, .913, label, color=MUTED, fontsize=8.5, weight='bold')
        fig.text(x + .013, .883, value, color=TEAL, fontsize=15.5, weight='bold')

    ax = panel(fig, (.06, .649, .88, .199), '01  PANORAMA HISTORICO',
               'Crecimiento, ruptura por COVID-19 y recuperacion')
    ax.plot(series.index, series.values / 1000, color=TEAL, linewidth=1.7)
    ax.axvspan(pd.Timestamp('2020-03-01'), pd.Timestamp('2021-04-01'),
               color=ORANGE, alpha=.20)
    ax.annotate('COVID-19 / cierres', (pd.Timestamp('2020-07-01'),
                series.max()/1000*.73), color=NAVY, fontsize=9,
                ha='center', bbox={'facecolor': WHITE, 'edgecolor': 'none', 'alpha': .85})
    ax.set_ylabel('Miles de viajeros', fontsize=9)
    ax.xaxis.set_major_locator(mdates.YearLocator(3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.grid(alpha=.15)

    months = series.groupby(series.index.month).mean()
    peak = int(months.idxmax())
    ax = panel(fig, (.06, .441, .427, .189), '02  ESTACIONALIDAD',
               'Promedio mensual de viajeros')
    ax.bar(range(1, 13), months.values / 1000,
           color=[ORANGE if m == peak else TEAL for m in range(1, 13)])
    ax.set_xticks(range(1, 13), ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
    ax.set_ylabel('Miles', fontsize=9)
    ax.grid(axis='y', alpha=.15)
    ax.set_axisbelow(True)

    ax = panel(fig, (.513, .441, .427, .189), '03  MERCADOS REGIONALES',
               'Principales regiones de residencia')
    r = regions.head(4).sort_values()
    ax.barh([textwrap.fill(str(v), 16) for v in r.index], r.values/1e6, color=TEAL)
    ax.tick_params(axis='y', labelsize=7, pad=2)
    ax.set_position([.685, .486, .22, .064])
    ax.set_xlabel('Millones de viajeros', fontsize=9)
    ax.grid(axis='x', alpha=.15)
    ax.set_axisbelow(True)

    x, y, w, h = .06, .316, .88, .106
    fig.add_artist(FancyBboxPatch((x, y), w, h, transform=fig.transFigure,
                   boxstyle='round,pad=0.004,rounding_size=.009',
                   linewidth=0, facecolor=WHITE))
    fig.text(x + .018, y + h - .025, '04  CUADRANTE COMPARATIVO | Hallazgos reportados en Lab 1',
             fontsize=12.5, weight='bold', color=NAVY)
    cells = [
        ('ESTACIONALIDAD', 'Total y El Salvador: picos en abril y agosto.'),
        ('CRECIMIENTO', 'America del Norte: +5.8 % anual prepandemia.'),
        ('VOLATILIDAD', 'Guatemala: CV residual de 0.38.'),
        ('PANDEMIA', 'Europa: descenso reportado de 89.2 % en 2020.')]
    for i, (heading, body) in enumerate(cells):
        cx = x + .018 + (i % 2) * .44
        cy = y + .068 - (i // 2) * .039
        fig.text(cx, cy, heading, fontsize=9.4, color=TEAL, weight='bold')
        note(fig, cx, cy - .012, body, width=54, size=8.5, spacing=.012)

    ax = panel(fig, (.06, .123, .88, .174), '05  PRONOSTICO | ESTIMACION SARIMA',
               'Prueba: enero 2024 - junio 2026 | Banda predictiva nominal del 80 %')
    ax.plot(result.index, result['observado']/1000, color=NAVY, lw=1.8, label='Observado')
    ax.plot(result.index, result['estimacion']/1000, color=ORANGE, lw=1.8, label='Estimacion')
    ax.fill_between(result.index, result['limite_inferior_80'].to_numpy()/1000,
                    result['limite_superior_80'].to_numpy()/1000,
                    color=ORANGE, alpha=.22, label='Intervalo 80 %')
    ax.set_ylabel('Miles de viajeros', fontsize=9)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', labelsize=8)
    ax.legend(fontsize=8, loc='upper left', ncol=3, frameon=False)
    ax.grid(alpha=.15)

    fig.text(.06, .104, '06  RECOMENDACIONES PARA INGUAT',
             color=NAVY, fontsize=12, weight='bold')
    recommendations = [
        'Reforzar capacidad fronteriza en Semana Santa y agosto.',
        'Segmentar promocion para Centroamerica y Norteamerica.',
        'Preparar protocolos ante interrupciones del turismo.',
        'Actualizar estimaciones antes de planificar capacidad.']
    for i, line in enumerate(recommendations):
        col, row = i % 2, i // 2
        fig.text(.06 + col * .45, .083 - row * .018, f'{i+1:02d}  {line}',
                 fontsize=8.7, color=NAVY)
    fig.text(.06, .042, f'Validacion SARIMA: MAE {mae:,.0f} | RMSE {rmse:,.0f} viajeros. '
             'El periodo de prueba difiere del Lab 1.', fontsize=8.6, color=NAVY)
    fig.text(.06, .029, 'Fuente: Base Migracion 2009-2026, uso academico; cifras no oficiales. '
             'Autores: Osman de Leon y Milton Polanco.', fontsize=8.1, color=MUTED)
    fig.text(.06, .018, 'Nota: resultados del cuadrante tomados del informe Lab 1; '
             'no revalidados en este script.', fontsize=8.1, color=MUTED)
    path = REPORT / 'infografia_corregida.png'
    fig.savefig(path, dpi=180, facecolor=BG)
    plt.close(fig)
    pdf = canvas.Canvas(str(REPORT / 'infografia_corregida.pdf'), pagesize=(792, 1224))
    pdf.drawImage(ImageReader(str(path)), 0, 0, width=792, height=1224)
    pdf.showPage()
    pdf.save()


def main():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    REPORT.mkdir(parents=True, exist_ok=True)
    df, series = load_data()
    series.rename('viajeros').to_csv(PROCESSED / 'serie_mensual_verificada.csv')
    result, mae, rmse = forecast(series)
    result.to_csv(PROCESSED / 'pronostico_prueba_intervalo80.csv', index_label='fecha')
    make_infographic(df, series, result, mae, rmse)
    (REPORT / 'NOTAS_VALIDACION.txt').write_text(
        f'Filas filtradas: {len(df):,}\nMeses: {len(series)}\n'
        f'Total turistas + excursionistas: {series.sum():,.0f}\n'
        'SARIMA(1,1,1)(1,1,1,12) | Entrenamiento hasta 2023-12 | '
        'Prueba 2024-01 a 2026-06\n'
        f'MAE: {mae:,.2f}\nRMSE: {rmse:,.2f}\n'
        'Intervalo predictivo nominal: 80 %\n'
        'Las cifras del cuadrante provienen del informe Lab 1 y no se '
        'revalidaron aqui. No se ha demostrado que SARIMA sea el mejor '
        'modelo frente a todos los algoritmos con este corte.\n', encoding='utf-8')
    print(f'Listo. PNG y PDF: {REPORT}')
    print(f'CSV: {PROCESSED}')
    print(f'MAE: {mae:,.2f} | RMSE: {rmse:,.2f}')


if __name__ == '__main__':
    main()
