from mrjob.job import MRJob

class TaxiFareAnalysis(MRJob):

    def mapper(self, _, line):
        # Split the line into columns
        parts = line.split(',')

        # Skip lines that don't have the expected number of columns
        if len(parts) < 8:
            return

        # Skip the header line
        if parts[0] == 'key':
            return

        # Extract the relevant fields
        try:
            passenger_count = int(parts[7])
            fare_amount = float(parts[1])
            yield passenger_count, fare_amount
        except ValueError:
            pass

    def reducer(self, passenger_count, fares):
        total_fare = 0
        total_rides = 0

        # Sum up fares and count the number of rides
        for fare in fares:
            total_fare += fare
            total_rides += 1

        # Calculate the average fare
        avg_fare = total_fare / total_rides if total_rides > 0 else 0

        yield passenger_count, avg_fare

if __name__ == '__main__':
    TaxiFareAnalysis.run()


