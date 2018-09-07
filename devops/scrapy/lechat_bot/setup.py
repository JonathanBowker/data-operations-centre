from setuptools import setup, find_packages

setup(
    name='lechat_bot',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = lechat_bot.settings']},
)
