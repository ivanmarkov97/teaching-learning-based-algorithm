import setuptools

with open('README.md', 'r') as f:
	long_description = f.read()
	print(long_description)

setuptools.setup(
	name='tlbo-imarkov',
	version='0.0.1',
	author='Ivan Markov',
	author_email='thiendio@yandex.ru',
	description='tearching learning based algorithm',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/ivanmarkov97/teaching-learning-based-algorithm',
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	]
)
