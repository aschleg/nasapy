# Version 0.2.2

- An optional `return_df` parameter has been implemented in the listed functions below. When set 
  as `True`, the resulting JSON data will be coerced into a pandas DataFrame to allow easier and more straightforward 
  data analysis for those interested.
  
  * `fireballs`
  * `close_approach`
  * `nhats`
  * `sentry`
  
- General bug fixes
  * The `sentry` function should now operate correctly when passing a `des` or `spk` parameter.

# Version 0.2.1

- Added `sentry` function that wraps the [CNEOS Sentry System API](https://cneos.jpl.nasa.gov/sentry/) for providing 
  Near-Earth Object impact risk assessment data.

# Version 0.2.0

Initial release.