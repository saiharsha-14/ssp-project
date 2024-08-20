from mrjob.job import MRJob
import math

class AverageFareByLocation(MRJob):

    def configure_args(self):
        super(AverageFareByLocation, self).configure_args()
        self.add_passthru_arg('--precision', type=int, default=2, help='Decimal precision for rounding coordinates')

    def mapper(self, _, line):
        parts = line.split(',')
        if parts[0] == 'key' or len(parts) < 8:
            return  # Skip header or incorrect lines

        try:
            pickup_longitude = float(parts[3])
            pickup_latitude = float(parts[4])
            fare_amount = float(parts[1])

            # Round coordinates to the specified precision to cluster nearby pickup locations
            rounded_longitude = round(pickup_longitude, self.options.precision)
            rounded_latitude = round(pickup_latitude, self.options.precision)

            yield ((rounded_longitude, rounded_latitude), fare_amount)
        except ValueError:
            pass  # Skip lines with invalid data

    def reducer(self, location, fares):
        total_fare = 0
        total_rides = 0

        # Sum up fares and count the number of rides
        for fare in fares:
            total_fare += fare
            total_rides += 1

        # Calculate the average fare
        avg_fare = total_fare / total_rides if total_rides > 0 else 0

        yield (location, avg_fare)

if __name__ == '__main__':
    AverageFareByLocation.run()

