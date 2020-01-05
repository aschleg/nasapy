# Version History

## Version 0.2.5

- `sentry` function now returns results as expected when not returning a pandas DataFrame.

## Version 0.2.4

- Adds `exoplanet` function for providing access to [NASA's Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/index.html>).

## Version 0.2.3

- Fixes bug in `nhats` function when `return_df` parameter is set to `True`.

## Version 0.2.2

- An optional `return_df` parameter has been implemented in the listed functions below. When set 
  as `True`, the resulting JSON data will be coerced into a pandas DataFrame to allow easier and more straightforward 
  data analysis for those interested. Please see the individual function documentation for more information and 
  examples.
  
  * `fireballs`
  * `close_approach`
  * `nhats`
  * `sentry`
  * `scout`
  
- General bug fixes
  * The `sentry` function should now operate correctly when passing a `des` or `spk` parameter.

## Version 0.2.1

- Added `sentry` function that wraps the [CNEOS Sentry System API](https://cneos.jpl.nasa.gov/sentry/) for providing 
  Near-Earth Object impact risk assessment data.

## Version 0.2.0

Initial release.