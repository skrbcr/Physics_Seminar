import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from astropy.io import fits
import os
import sys
import yaml

plt.style.use('default')

def monochro(arre: np.ndarray, arrx: np.ndarray, arry: np.ndarray, enerange: list[float], cmin: float, cmax: float, outname: str, ranges: list[list[float]], bins: int, log: bool, cp: str) -> None:
    binx: int = int((ranges[0][1] - ranges[0][0]) / bins)
    biny: int = int((ranges[1][1] - ranges[1][0]) / bins)
    if log:
        normlog = mpl.colors.LogNorm()
    else:
        normlog = None
    xs = []
    ys = []
    n = arre.size
    for i in range(n):
        if arre[i] >= enerange[0] and arre[i] <= enerange[1]:
            xs.append(arrx[i])
            ys.append(arry[i])
    # グラフ作成
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    hi, xe, ye, img = ax.hist2d(xs, ys, bins=[binx,biny], range=ranges, norm=normlog, cmap=cp, cmin=cmin, cmax=cmax)
    plt.colorbar(img)
    strFile = outname + 'ene_' + str(enerange[0]) + '_' + str(enerange[1]) + '.png'
    fig.savefig(strFile, dpi=200)
    print('Save: ' + strFile)
    # plt.show()

def makeImage(data, cfg) -> None:
    # data の展開
    arrx = np.array(data.x, float)
    arry = np.array(data.y, float)
    arre = np.array(data.energy, float)
    # cfg の展開
    try:
        outname: str = cfg['outname']
    except:
        outname: str = ''
    try:
        rg: list[list[float]] = cfg['range']
    except:
        rg: list[list[float]] = None
    try:
        bins: float = cfg['bin']
    except:
        bins: float = 10
    try:
        if cfg['log'] == 1:
            normlog = True
        else:
            normlog = False
    except:
        normlog = None
    try:
        cp: str = cfg['cmap']
    except:
        cp: str = 'gray'
    try:
        cmin = cfg['cmin']
    except:
        cmin = None
    try:
        cmax = cfg['cmax']
    except:
        cmax = None
    n = len(cfg['band'])
    for i in range(n):
        try:
            enerange = cfg['band'][i]['energy']
        except:
            enerange = None
        try:
            cmin = cfg['band'][i]['cmin']
        except:
            cmin = None
        try:
            cmax = cfg['band'][i]['cmax']
        except:
            cmax = None
        monochro(arre, arrx, arry, enerange, cmin, cmax, outname, rg, bins, normlog, cp)

def main() -> None:
    args = sys.argv
    if len(args) == 2:
        strYml = args[1]
    else:
        print('Error: please specify recipe file', file=sys.stderr)
        sys.exit(1)
    try:
        with open(strYml) as file:
            cfg = yaml.safe_load(file)
    except Exception as e:
        print('Error: cannot open ' + 'recipe.yaml')
        print(e, file=sys.stderr)
        sys.exit(1)
    try:
        hdul = fits.open(cfg['data'])
    except Exception as e:
        print('Error: cannot open fits file')
        print(e, file=sys.stderr)
        sys.exit(1)
    try:
        data = hdul['EVENTS'].data
        hdul.close()
    except:
        print('Error: cannot find events data. please notify the author of this script about this error.')
        print(e, file=sys.stderr)
        sys.exit(1)
    try:
        makeImage(data, cfg)
    except Exception as e:
        print('Error: cannot make image')
        print(e, file=sys.stderr)
        sys.exit(1)
    print('done.')
    
main()
