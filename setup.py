from setuptools import setup

setup(
    name="filtered_search_pack",
    version="0.0.1",
    description="""A package for exploring research topics that takes a keyword 
      as an input and returns a list of ten papers arranged by citations/year.""",
    maintainer="Eli Barbour",
    maintainer_email="ebarbour@andrew.cmu.edu",
    license="MIT",
    packages=["filtered_search_pack"],
    entry_points={"console_scripts": ["oa = s26pack.main:main"]},
    long_description="""A software package that takes a topic or a keyword as an input
      and then uses the OpenAlex api to fetch research papers associated with the topic
      or keyword. Ten papers are retrieved which are arranged according to the amount of 
      citations they have per year. The citations/year metric is used instead of 
      citations to remove some of the bias given to papers that have been published 
      for a long period of time. Additionally, the user can specify filtered_search to
      only return publications after a particular year.""",
)
