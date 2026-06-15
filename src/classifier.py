class TransitClassifier:

    def classify(self, depth, duration, snr):

        if snr < 5:
            return "Noise"

        if depth < 0.001:
            return "Exoplanet Candidate"

        if depth < 0.05:
            return "Possible Transit"

        return "Eclipsing Binary"