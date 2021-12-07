from setuptools import setup, find_namespace_packages

setup(
    name='clean_folders',
    version='1',
    description='Сортировка файлов по типам (extensions).',
    url='',
    author='Inna K',
    author_email='kostenko.inna.victorovna@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folders = clean_folders.clean_folders:clean_folders']}
)