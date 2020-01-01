
.. _versions:

Version History
===============

Version 0.2.4
-------------

- Adds :code:`exoplanet` function for providing access to
  `NASA's Exoplanet Archive <https://exoplanetarchive.ipac.caltech.edu/index.html>`_.

Version 0.2.3
-------------

- Fixes bug in :code:`nhats` function when :code:`return_df` parameter is set to :code:`True`.

Version 0.2.2
-------------

- An optional :code:`return_df` parameter has been implemented in the listed functions below. When set as :code:`True`,
  the resulting JSON data will be coerced into a pandas DataFrame to allow easier and more straightforward data
  analysis for those interested. Please see the individual function documentation for more information and
  examples.

  * :code:`fireballs`
  * :code:`close_approach`
  * :code:`nhats`
  * :code:`sentry`
  * :code:`scout`

- General bug fixes
  * The :code:`sentry` function should now operate correctly when passing a :code:`des` or :code:`spk` parameter.

Version 0.2.1
-------------

- Added `sentry` function that wraps the `CNEOS Sentry System API <https://cneos.jpl.nasa.gov/sentry/>`_ for providing
  Near-Earth Object impact risk assessment data.

Version 0.2.0
-------------

Initial release.