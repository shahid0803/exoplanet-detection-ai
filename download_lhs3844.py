from lightkurve import search_lightcurve

print("Searching TESS data...")

search = search_lightcurve("LHS 3844", mission="TESS")

print(search)

lc = search.download()

lc.to_fits("lhs3844.fits")

print("Downloaded successfully!")