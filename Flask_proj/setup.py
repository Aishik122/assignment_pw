from setuptools import find_packages,setup


def get_requirements(file_path:str)->list[str]:
    requirements = []
    with open(file_path, 'r') as file_obj:
        requirements=file_obj.readlines()
        requirements=[x.replace("\n", "") for x in requirements]
        
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements

setup(
    name='Mushrooms',
    version='1.0.0',
    author='Aishik',
    author_email='aishikchatterjee12@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
    
)