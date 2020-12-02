import os
import pickle
from timeit import default_timer as timer
import requests


class AOCLib:
    """Advent of Code helper library.

    Attributes:
        aoc_year (int): The year of Advent of Code to work with.
    """

    _aoc_input_url = 'http://adventofcode.com/{year}/day/{day}/input'

    def __init__(self, aoc_year):
        """Initialise helper library.

        Args:
            aoc_year (int): The year of Advent of Code to work with.
        """

        self._timer_start = timer()
        self._timer_last = self._timer_start

        self.aoc_year = aoc_year
        user_profile = os.environ['USERPROFILE']
        self._aoc_path = '{}\\aoc'.format(user_profile)

        with open('{}\\aoc.cookie'.format(self._aoc_path),
                  'r') as aoc_cookie_file:
            aoc_cookie_value = aoc_cookie_file.read()

        self._aoc_cookie = dict(session=aoc_cookie_value)

    def print_solution(self, part, *args, **kwargs):
        """Print the puzzle solution with timer.

        Args:
            part (int or string): The part of the puzzle.
        """

        timer_now = timer()
        print('\n{banner}'.format(banner='-' * 80))
        print(' LAP -> {:<15.6f} | {:>15.6f} <- ELAPSED'
              .format(timer_now - self._timer_last,
                      timer_now - self._timer_start))

        print('{banner}\n Part {:<3} : '
              .format(
                  part,
                  banner='-' * 80),
              end='')
        print(*args, **kwargs)
        print('{}\n'.format('-' * 80), flush=True)

        self._timer_last = timer_now

    def get_puzzle_input(self, day, transform_function=lambda x: x):
        """Get puzzle input from the AOC website.

        Apply an optional transform function to it before returning.

        Cache the puzzle input locally for next time.

        Args:
            day (int): The day of the puzzle.
            transform_function: A transformation function to apply to
                the puzzle input.
        Returns:
            The puzzle input, transformed by transform_function.
        """

        cache_filename = '{}\\{}_{:02d}.txt'.format(self._aoc_path,
                                                    self.aoc_year, day)

        try:
            with open(cache_filename, 'r') as cache_file:
                puzzle_input = cache_file.read()
        except FileNotFoundError:
            puzzle_input = None

        if puzzle_input is None:
            response = requests.get(
                self._aoc_input_url.format(year=self.aoc_year, day=day),
                cookies=self._aoc_cookie)

            if response.status_code != 200:
                raise AssertionError('Unable to obtain puzzle input!')

            puzzle_input = response.text.rstrip('\n')

            with open(cache_filename, 'w') as cache_file:
                cache_file.write(puzzle_input)

        return transform_function(puzzle_input)

    def cache_some_data(self, day, key, obj):
        """Store some data in a cache file for later"""
        cache_filename = '{}\\cache_{}_{:02d}_{}.txt'.format(
            self._aoc_path, self.aoc_year, day, key)
        with open(cache_filename, 'wb') as cache_file:
            pickle.dump(obj, file=cache_file)

    def retrieve_some_data(self, day, key):
        """Retrieve some data from a cache file"""
        cache_filename = '{}\\cache_{}_{:02d}_{}.txt'.format(
            self._aoc_path, self.aoc_year, day, key)
        try:
            with open(cache_filename, 'rb') as cache_file:
                pickled_input = pickle.load(cache_file)
        except FileNotFoundError:
            pickled_input = None

        return pickled_input

    # Various static methods for manipulating the puzzle input:

    @staticmethod
    def to_list(puzzle_input):
        """Transform a comma-separated string to a list."""
        return [element.strip() for element in puzzle_input.split(',')]

    @staticmethod
    def to_list_int(puzzle_input):
        """Transform a string of comma-separated integers to a list."""
        return [int(element) for element in puzzle_input.split(',')]

    @staticmethod
    def lines_to_list(puzzle_input):
        """Transform multi-line input to a list."""
        return puzzle_input.split('\n')

    @staticmethod
    def lines_to_list_int(puzzle_input):
        """Transform multi-line integer input to a list."""
        return [int(x) for x in puzzle_input.split('\n')]

    @staticmethod
    def sequence_to_int(puzzle_input):
        """Transform a sequence of digits to a list of integers."""
        return [int(digit) for digit in puzzle_input]
