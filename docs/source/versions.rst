
.. _versions:

Version History
===============

Version 0.2.2
-------------

- An optional :code:`return_df` parameter has been implemented in the listed functions below. When set as :code:`True`,
  the resulting JSON data will be coerced into a pandas DataFrame to allow easier and more straightforward data
  analysis for those interested.

  * :code:`fireballs`
  * :code:`close_approach`
  * :code:`nhats`

Version 0.2.1
-------------

- Added `sentry` function that wraps the `CNEOS Sentry System API <https://cneos.jpl.nasa.gov/sentry/>`_ for providing
  Near-Earth Object impact risk assessment data.

Version 0.2.0
-------------

Initial release.