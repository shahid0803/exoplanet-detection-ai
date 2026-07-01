from lightkurve import search_lightcurve

search_result = search_lightcurve("WASP-18", mission="TESS")

print(search_result)

lc = search_result[0].download()

lc.to_fits(path="wasp18.fits", overwrite=True)

print("Saved as wasp18.fits")