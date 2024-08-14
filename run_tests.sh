# Run the tests
python3 -m unittest discover -s tests

# Produce a coverage report
coverage run -m unittest discover -s tests
coverage html
