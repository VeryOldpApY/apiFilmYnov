from setuptools import setup, find_packages

setup(
	name="apiFilmYnov",
	version="0.1",
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'run-app=run:main',
		],
	},
)
