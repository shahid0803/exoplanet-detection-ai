from lightkurve import search_lightcurve

print("Searching TESS data...")

search = search_lightcurve("TOI 700", mission="TESS")

print(search)

lc = search.download()

lc.to_fits("toi700.fits")

print("Downloaded successfully!")