# Hotel Data Aggregation Project

This project aggregates hotel data from multiple supplier URLs and filters the data based on provided hotel IDs and destination IDs. The main components of the project include fetching data from suppliers, merging the responses, and filtering the aggregated data.

## Features

- **Data Fetching**: Fetches data from multiple supplier URLs using the `Supplier` class.
- **Data Merging**: Merges the fetched data into a unified list of hotels using the `merge_responses` function.
- **Data Filtering**: Filters the aggregated data based on provided hotel IDs and destination IDs using the `filter_aggregated_data` function.
- **Command-Line Interface**: Provides a CLI to input hotel IDs and destination IDs for data filtering.

## Code Cleanliness Approach

- **Consistent Naming Conventions**: Used consistent naming conventions for variables and functions.
- **Docstrings and Comments**: Added appropriate docstrings and comments to all functions and classes.
- **Modular Functions**: Ensured that functions are modular and manageable.
- **Error Handling**: Ensured proper error handling in the fetch method.
- **Code Formatting**: Ensured proper code formatting and indentation.

## Usage

To run the project, use the following command in a bash shell:

./runner $1 $2

where:
- **$1** is the list of string that contains a list of value, each of which is separated by a comma , for hotel_ids
- **$2** is the list of string that contains a list of value, each of which is separated by a comma , for destination_ids
- In the case that the list is empty, the value of the argument is none.

For example:
    ./runner iJhz,SjyX 5432