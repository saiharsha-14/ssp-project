from mrjob.job import MRJob
import logging

class TotalFarePerYear(MRJob):

    def configure_args(self):
        super(TotalFarePerYear, self).configure_args()
        self.add_passthru_arg('--debug', action='store_true', help='Enable debug mode')

    def mapper_init(self):
        self.logger = logging.getLogger(__name__)

    def mapper(self, _, line):
        parts = line.split(',')
        if parts[0] == 'key' or len(parts) < 8:
            return  # Skip header or incorrect lines

        try:
            pickup_datetime = parts[2]
            fare_amount = float(parts[1])
            pickup_year = pickup_datetime[:4]  # Extract year from YYYY-MM-DD hh:mm:ss
            if not pickup_year.isdigit():
                if self.options.debug:
                    self.logger.warning(f"Invalid year from datetime: {pickup_datetime}")
            else:
                yield (pickup_year, fare_amount)
        except ValueError as e:
            if self.options.debug:
                self.logger.warning(f"Skipping line due to error: {e}, Line: {line}")

    def reducer(self, year, fares):
        total_fare = sum(fares)  # Simply sum all the fares for each year

        yield (year, total_fare)

if __name__ == '__main__':
    TotalFarePerYear.run()

