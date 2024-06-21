{ pkgs }: {
  deps = [
    # pkgs.from tradingview_ta import TA_Handler, Interval, Exchange
    # pkgs.import yfinance as yf
    # pkgs.from bs4 import BeautifulSoup
    # pkgs.import Finance-DataReader as fdr
    pkgs.gmp
    pkgs.zlib
    pkgs.openjpeg
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.libyaml
    pkgs.glibcLocales
    pkgs.libxcrypt
    pkgs.tk
    pkgs.tcl
    pkgs.qhull
    pkgs.pkg-config
    pkgs.gtk3
    pkgs.gobject-introspection
    pkgs.ghostscript
    pkgs.freetype
    pkgs.ffmpeg-full
    pkgs.cairo
  ];
}