from typing import List, Union
import os

SectionPathOrStr = Union[str, 'SectionPath']

class SectionPath:

    def __init__(self, section_path: str):
        self.path_str = section_path
        self.sections = _section_path_str_to_section_strs(section_path)

    def __iter__(self):
        for section in self.sections:
            yield section

    def __getitem__(self, item):
        return self.sections[item]

    @classmethod
    def from_filepath(cls, basepath: str, filepath: str):
        relative_path = os.path.relpath(filepath, start=basepath)
        section_path = _relative_filepath_to_section_path(relative_path)
        return cls(section_path)

    @classmethod
    def from_section_str_list(cls, section_strs: List[str]):
        section_path = _section_strs_to_section_path_str(section_strs)
        return cls(section_path)

    @classmethod
    def join(cls, section_path_1: SectionPathOrStr, section_path_2: SectionPathOrStr):
        section_path_1 = _convert_to_section_path_if_necessary(section_path_1)
        section_path_2 = _convert_to_section_path_if_necessary(section_path_2)

        output_path_sections = section_path_1.sections + section_path_2.sections
        return cls.from_section_str_list(output_path_sections)


def _section_path_str_to_section_strs(section_path_str: str) -> List[str]:
    return section_path_str.split('.')

def _section_strs_to_section_path_str(section_strs: List[str]) -> str:
    return '.'.join(section_strs)

def _relative_filepath_to_section_path(filepath: str) -> str:
    sections = filepath.split(os.path.sep)
    sections[-1] = _strip_py(sections[-1]) # remove .py if exists at end of filepath
    return _section_strs_to_section_path_str(sections)


def _strip_py(filename_str: str) -> str:
    if not filename_str.endswith('.py'):
        return filename_str

    return filename_str[:-3]

def _convert_to_section_path_if_necessary(section_path: SectionPathOrStr) -> SectionPath:
    if isinstance(section_path, SectionPath):
        return section_path
    elif isinstance(section_path, str):
        return SectionPath(section_path)
    else:
        raise ValueError(f'expected SectionPath or str. got {section_path} of type {type(section_path)}')