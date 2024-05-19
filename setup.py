from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(files_path:str)->List[str]:
    '''
    This function will return the list or requirements
    '''
    requirements=[]
    with open(files_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
setup(
   name="mlproject",
   version="0.1",
   author="prakash",
   author_email="naiduprakash@gmail.com",
   packages=find_packages(),
   install_requires=get_requirements('requirements.txt')
)