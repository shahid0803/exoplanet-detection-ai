from lightkurve import search_lightcurve

print("Searching...")

search_result = search_lightcurve(
    "Pi Mensae",
    mission="TESS"
)

print("Downloading first light curve...")

lc = search_result[0].download()

print(lc)

print("Saving file...")

lc.to_fits("pi_mensae.fits")

print("Done!")